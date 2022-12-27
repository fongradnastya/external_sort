import argparse
import sort


def main():
    """
    Точка входа CLI
    """
    parser = argparse.ArgumentParser(
        description="Внешняя сортировка методом n-путевого слияния")
    parser.add_argument("-src", dest="src", type=str, nargs="+",
                        help="Список исходных файлов")
    parser.add_argument("--output", "-out", dest="output", type=str,
                        default=None, help="Выходной файл")
    parser.add_argument("--type_data", "-td", dest="type_data", type=str,
                        default="s",
                        help="Тип данных считываемых из файла")
    parser.add_argument("--reverse", "-r", dest="reverse", action="store_true",
                        help="Если указано - сортирует по не возрастанию")
    parser.add_argument("--key", "-k", dest="key", default=None, type=str,
                        help="Ключ столбца для csv файла")
    parser.add_argument("--buff_size", "-sz", dest="bsize", default=10,
                        type=int, help="Размер буфера памяти")
    parser.add_argument("--n_paths", "-n", dest="n_paths", default=3, type=int,
                        help="Количество путей сортировки")
    args = parser.parse_args()
    res = {"file_names": args.src,
           "output": args.output,
           "type_data": args.type_data,
           "reverse": args.reverse,
           "key": args.key,
           "bsize": args.bsize,
           "n_paths": args.n_paths,
           }
    if not args.src:
        print("no files to sort")
    else:
        if args.bsize < 2:
            print("buffer size is to small")
        elif args.n_paths < 2:
            print("number of paths is too small")
        elif args.type_data not in ("i", "s", "f"):
            print("wrong data type")
        else:
            sort.my_sort(**res)
            print("successfully sorted")


if __name__ == '__main__':
    main()
