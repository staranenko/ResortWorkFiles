import os
import shutil
import sys
import clear_string
from ProgressBar import printProgressBar
import InputOutputParams

NAME_PATTERN = 'НСО'
RESULT_DIR_NAME = 'Результат'
NO_NUMBER = 'не число'

CMD_RW = 'rewrite'  # Включает перезапись всех файлов в папке назначения
CMD_ALL = 'all'  # Включает копирование файлов в том числе с "нет числа"
CMD_SOURCE = 'source'  # Включает создание выходной структуры каталогов как у исходных файлов
CMD_NO_COPY = 'nocopy'  # Не копировать и не создавать каталоги. Только просмотр и анализ.

cmd_rw = False
cmd_all = False
cmd_source = False
cmd_no_copy = False

INPUT = InputOutputParams.INPUT
OUTPUT = InputOutputParams.OUTPUT

LOG_FILE = InputOutputParams.LOG_FILE


def get_file_name(name, name_pattern):
    if name_pattern:
        name_short = name.split(name_pattern)[0][:-1]
        zone = name_pattern + name.split(name_pattern)[1].split('.')[0]
    else:
        name_short = name.split('.')[0]
        zone = '_none'

    file_names = [name,
                  name_short + '.tif',
                  name_short + '.' + name.rsplit('.')[-1],
                  name_short + '.tif'
                  ]

    return file_names, zone


def sort_dirs_work(dirs):
    if len(dirs) > 3:
        dirs = [dirs[2], dirs[-1], dirs[0], dirs[1]]
    return dirs


def sort_dirs_source(dirs):
    dirs = [dirs[0], dirs[1], dirs[2], '']
    return dirs


def get_file(input, name_pattern):
    print('Сканирование и предобработка...')
    list_files = []
    for subdir, dirs, files in os.walk(os.path.normpath(input), topdown=False):
        # print(os.listdir(input))
        for name in files:
            l = []
            if (name_pattern in name) and (('.TAB' in name) or ('.tab' in name)):
                # print(os.path.join(subdir, name))
                path_tree = subdir.replace(os.path.normpath(input), '').split(os.sep)[1:]
                # print(path_tree)
                # for path in path_tree:
                #     print(clear_string.clear_dir_name(path, clear_string.SUBSTR))
                clean_dirs = clear_string.clear_dirs_name(path_tree, clear_string.SUBSTR)
                files = get_file_name(name, name_pattern)
                # print(clean_dirs)
                # print(os.path.join(name))
                # print(files[0])
                clean_dirs.append(files[-1])
                # print(clean_dirs)
                sorted_dirs = sort_dirs_source(clean_dirs) if cmd_source else sort_dirs_work(clean_dirs)
                # print(sorted_dirs)
                l.append(sorted_dirs)
                l.append(subdir)
                l.append(files)
                list_files.append(l)
    print(f'Сканирование и предобработка завершена. Найдено {len(list_files)} пар.')
    return list_files


def create_directory(output, new_dir) -> str:
    full_path = os.path.join(os.path.normpath(output), new_dir)
    try:
        os.makedirs(full_path, exist_ok=True)
    except OSError as e:
        print(f'Создать директорию не удалось: {e.strerror}')

    return full_path


def copy_file(input_file_name, output_file_name):
    if os.path.exists(output_file_name):
        # print('input\t', os.path.getsize(input_file_name), os.path.getmtime(input_file_name))
        # print('output\t', os.path.getsize(output_file_name), os.path.getmtime(output_file_name))
        if not cmd_rw:
            if (os.path.getsize(input_file_name) != os.path.getsize(output_file_name)) and (
                    os.path.getmtime(output_file_name) != os.path.getmtime(input_file_name)):
                copy_file_now(input_file_name, output_file_name)
        else:
            copy_file_now(input_file_name, output_file_name)
    else:
        copy_file_now(input_file_name, output_file_name)


def copy_file_now(input_file_name, output_file_name):
    try:
        shutil.copyfile(input_file_name,
                        output_file_name)
    except OSError as e:
        print(f'Ошибка копирования файла {input_file_name}: {e.args}')


def get_args():
    global cmd_rw, cmd_all, cmd_source, cmd_no_copy
    for a in sys.argv:
        if a == CMD_RW:
            cmd_rw = True
        elif a == CMD_ALL:
            cmd_all = True
        elif a == CMD_SOURCE:
            cmd_source = True
        elif a == CMD_NO_COPY:
            cmd_no_copy = True
    print('Режимы работы:',
          '\n->', 'Перезапись.' if cmd_rw else 'Без перезаписи.',
          '\n->', 'Коипировать всё без разбора.' if cmd_all else 'Копировать только не совпадающие.',
          '\n->', 'Только анализ (без копирования).' if cmd_no_copy else 'Анализ и копирование.',
          '\n->', 'Создание исходной структуры каталогов.' if cmd_source else 'Создание рабочей структуры каталогов '
                                                                              'удобной для нарезки.'
          )


def main():
    get_args()

    files = get_file(INPUT, NAME_PATTERN)
    number_of_pairs = len(files)

    answer = str(input('Продолжить обработку? (y/n или любой символ):'))
    if answer != 'y':
        return

    copy = False
    printProgressBar(0, number_of_pairs, prefix='Progress:', suffix='Complete', length=50)
    for i, f in enumerate(files):
        # print(f)
        input_file_name = f[2][0][0]
        input_file_full_name = os.path.join(f[1], input_file_name)

        if cmd_all:
            copy = True
        else:
            no_number = False

            with open(input_file_full_name) as file_handler:
                try:
                    for line in file_handler:
                        if NO_NUMBER in line:
                            no_number = True
                            print(f'Finding \"{NO_NUMBER}\" in file {input_file_full_name}')

                            with open(LOG_FILE, mode='a') as log_file:
                                log_file.write(f'{input_file_full_name}\n')

                            break
                except UnicodeDecodeError as e:
                    print(f'Ошибка поиска в файле {input_file_full_name}: {e.args}')

            if no_number:
                copy = False
                # print('Don''t copy file')
            else:
                copy = True
                # print('Copy file')

        if cmd_no_copy:
            copy = False  # Никогда не копировать файлы

        if copy:
            current_dir_lever = OUTPUT
            current_dir_name = f[0][0]
            current_dir_lever = create_directory(current_dir_lever, current_dir_name)

            # print(current_dir_lever)
            # print(current_dir_name)
            current_dir_name = f[0][1]
            current_dir_lever = create_directory(current_dir_lever, current_dir_name)

            current_dir_name = f[0][2]
            current_dir_lever = create_directory(current_dir_lever, current_dir_name)

            current_dir_name = f[0][3]
            current_dir_lever = create_directory(current_dir_lever, current_dir_name)

            #  Copy TAB
            input_file_name = f[2][0][0]
            input_file_full_name = os.path.join(f[1], input_file_name)

            output_file_name = f[2][0][2]
            output_file_full_name = os.path.join(current_dir_lever, output_file_name)

            copy_file(input_file_full_name, output_file_full_name)

            #  Copy TIF
            input_file_name = f[2][0][1]
            input_file_full_name = os.path.join(f[1], input_file_name)

            output_file_name = f[2][0][3]
            output_file_full_name = os.path.join(current_dir_lever, output_file_name)

            if input_file_full_name.split(os.path.sep)[-2] == RESULT_DIR_NAME:
                input_file_full_name = input_file_full_name.replace(os.path.join(RESULT_DIR_NAME,
                                                                                 os.path.basename(input_file_full_name)),
                                                                    '')
                input_file_full_name = os.path.join(input_file_full_name, input_file_name)
                # print(os.path.exists(input_file_full_name))
                copy_file(input_file_full_name, output_file_full_name)
            else:
                copy_file(input_file_full_name, output_file_full_name)

        printProgressBar(i + 1, number_of_pairs, prefix='Выполнение:', suffix='Завершено', length=50)


if __name__ == '__main__':
    main()
