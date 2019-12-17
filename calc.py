from ProgressBar import printProgressBar
import InputOutputParams
import resort


INPUT = 'v:\\Контракт Геофонд НСО\\ГОТОВО для записи на диски СТРУКТУРА ЗАКАЗЧИКА'
OUTPUT = InputOutputParams.OUTPUT


def get_string_from_full_info(rec):
    output = rec[0][2] + '\t'\
             + rec[0][3] + '\t'\
             + rec[0][0] + '\t'\
             + str(rec[2][0][0:2]) + '\t'\
             + rec[1]
    return output


def main():
    files = resort.get_file(INPUT, '')
    number_of_pairs = len(files)

    answer = str(input('Продолжить обработку? (y/n или любой символ):'))
    if answer != 'y':
        return

    printProgressBar(0, number_of_pairs, prefix='Progress:', suffix='Complete', length=50)
    for i, f in enumerate(files):
        with open('calc.txt', mode='a') as log_file:
            log_file.write(f'{f}\n')

        info = get_string_from_full_info(f)

        with open('calc2.txt', mode='a') as log_file:
            log_file.write(f'{info}\n')

        printProgressBar(i + 1, number_of_pairs, prefix='Выполнение:', suffix='Завершено', length=50)

        # if i > 100:
        #     break


if __name__ == '__main__':
    main()
