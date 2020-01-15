import sys
import shutil
import os
import re
import fileinput
import locale

import ClearString
import InputOutputParams
from ProgressBar import printProgressBar
import Eversion

# INPUT = InputOutputParams.INPUT
INPUT = 'C:\\Temp\\TEST2'
# INPUT = 'v:\\Контракт Геофонд НСО\\ГОТОВО 2020\\ГОТОВО для загрузки в Панораму'


def replace_line_in_file(file, search_pubstring, replace_pubstring):
    # print(f'Замена в файле ({file}) строки ({search_pubstring}) на строку ({replace_pubstring})')

    # print(replace_pubstring)
    # print(locale.getpreferredencoding())
    s = replace_pubstring  # .encode('cp1251').decode('koi8-r')
    # print(s)

    try:
        for line in fileinput.FileInput(file, inplace=1):  # inplace=1 - печать в файл. 0 - в консоль.
            # if line.find(search_pubstring) >= 0:
            #     line = new_coord_system
            #     line = new_coord_system
            #     print(line.rstrip('\n'))
            # else:
            #     print(line.rstrip('\n'))

            line = re.sub(search_pubstring, s, line.encode().decode('cp1251'))
            print(line.rstrip('\n'))
    except FileNotFoundError as e:
        print(f'Ошибка замены строки имени файла: {e.args}')


def main():
    files = Eversion.get_file(INPUT, '')
    number_of_pairs = len(files)

    answer = str(input('Продолжить обработку? (y/n или любой символ):'))
    if answer != 'y':
        return

    printProgressBar(0, number_of_pairs, prefix='Progress:', suffix='Complete', length=50)
    for i, f in enumerate(files):
        file_tab = os.path.join(f[1], f[2][0][0])
        file_rastr = os.path.join(f[1], f[2][0][1])
        replace_line_in_file(file_tab, 'File \"(.*)\"', 'File \"' + os.path.basename(file_rastr) + '\"')

        printProgressBar(i + 1, number_of_pairs, prefix='Выполнение:', suffix='Завершено', length=50)


if __name__ == '__main__':
    main()
