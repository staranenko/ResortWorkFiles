SUBSTR = [
    '+',
    ',',
    '_',
    'СК42',
    'НСО1',
    'НСО2',
    'НСО3',
    'НСО4',
    'весь_переименовать',
    'разложить',
    'переименовать',
    'весь'
]


def clear_dir_name(dir, substr):
    for str in substr:
        dir = dir.replace(str, '')
    return dir


def clear_dirs_name(dirs, substr):
    """ Получение списка каталогов очищенных от всякого мусора перечисленного в substr """
    clear_dirs = []
    for d in dirs:
        for s in substr:
            d = d.replace(s, '')
        clear_dirs.append(d.strip())
    return clear_dirs
