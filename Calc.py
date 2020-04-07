"""

"""


from ProgressBar import printProgressBar
import InputOutputParams
import Eversion


INPUT = '/mnt/storage/GIS-DATA/СГУГиТ/СЕРВЕР/ГОТОВО 2020/Проекты Окончательные/'
# INPUT = 'v:\\Контракт Геофонд НСО\\ГОТОВО для записи на диски СТРУКТУРА ЗАКАЗЧИКА'
OUTPUT = InputOutputParams.OUTPUT

CALC_FILE_FULL = InputOutputParams.CALC_FILE_FULL
CALC_FILE_SHORT = InputOutputParams.CALC_FILE_SHORT


def get_string_from_full_info(rec):
    separator = ','
    output = rec[0][2] + separator\
             + rec[0][3] + separator\
             + rec[0][0] + separator\
             + str(rec[2][0][0:2]) + separator\
             + rec[1]
    return output


def main():
    files = Eversion.get_file(INPUT, '')
    number_of_pairs = len(files)

    answer = str(input('Продолжить обработку? (y/n или любой символ):'))
    if answer != 'y':
        return

    printProgressBar(0, number_of_pairs, prefix='Progress:', suffix='Complete', length=50)
    for i, f in enumerate(files):
        with open(CALC_FILE_FULL, mode='a') as log_file:
            log_file.write(f'{f}\n')

        info = get_string_from_full_info(f)

        with open(CALC_FILE_SHORT, mode='a') as log_file:
            log_file.write(f'{info}\n')

        printProgressBar(i + 1, number_of_pairs, prefix='Выполнение:', suffix='Завершено', length=50)

        # if i > 100:
        #     break


if __name__ == '__main__':
    main()
