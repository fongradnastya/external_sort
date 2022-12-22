from typing import Optional, Callable
from file import File


def my_sort(file_names, n_paths: int, output: Optional[str] = None, type_data="s",
            reverse: bool = False, key: Optional[Callable] = None,
            bsize: Optional[int] = None) -> None:
    if isinstance(file_names, str):
        file = File(file_names, key=key, d_type=type_data)
        sort_one_file(file, n_paths, reverse, bsize)
    else:
        files = []
        for file_name in file_names:
            file = File(file_name, key=key, d_type=type_data)
            sort_one_file(file, n_paths, reverse, bsize)
            files.append(file)
        if output:
            out_file = File(output, key=key, d_type=type_data)
            merge_to_one(files, out_file)


def sort_one_file(file, n_paths: int, reverse: bool = False,
                  bsize: Optional[int] = None):
    tapes = create_tapes(file, n_paths)
    split_file(file, bsize, tapes[:n_paths])
    is_first = True
    merge_tapes(tapes, is_first, reverse)
    is_first = not is_first


def create_tapes(input_file: File, n_path):
    """
    Создаёт вспомогательные сортировочные файлы
    :param input_file:
    :param n_path:
    :return:
    """
    files = []
    for i in range(1, n_path * 2 + 1):
        if input_file.is_txt:
            new_file = File(f"temp{i}.txt")
        else:
            new_file = File(f"temp{i}.csv", key=input_file.key,
                            d_type=input_file.data_type)
        files.append(new_file)
    return files


def split_file(file, buff_size, tapes):
    """
    Разделяет входной файл на n различных файлов
    :param file:
    :param buff_size:
    :param tapes:
    :return:
    """
    curr_id = 0
    file.open_file("r")
    for tape in tapes:
        tape.clean()
        tape.open_file("a")
    while curr_id < len(tapes):
        data = file.read_n_lines(buff_size)
        tape = tapes[curr_id]
        tape.write_n_lines(data)
        curr_id = curr_id + 1
        if curr_id >= len(tapes):
            curr_id = 0
        if len(data) < buff_size:
            break
    file.close_file()
    for tape in tapes:
        tape.close_file()


def merge_tapes(files, is_first, is_reversed=False):
    """
    Сливает первые n лент в другие n лент
    :param files:
    :param is_first:
    :param is_reversed:
    :return:
    """
    n = len(files) // 2
    if is_first:
        to_read = files[:n]
        to_write = files[n:]
    else:
        to_read = files[n:]
        to_write = files[:n]
    for file in to_read:
        file.open_file("r")
    for file in to_write:
        file.clean()
        file.open_file("a")
    curr_id = 0
    is_read = list([False for _ in range(n)])
    values = list(["" for _ in range(n)])
    while curr_id < n:
        for i in range(n):
            if not is_read[i]:
                values[i] = to_read[i].read_line()
                if values[i]:
                    is_read[i] = True
                else:
                    values[i] = None
        written_id = find_value_id(values, is_reversed)
        if written_id is not None:
            to_write[curr_id].write_line(str(values[written_id]) + "\n")
            is_read[written_id] = False
            curr_id = curr_id + 1 if curr_id < n - 1 else 0
        else:
            break
    for file in to_read:
        file.close_file()
    for file in to_write:
        file.close_file()


def find_value_id(values, is_max):
    """
    Ищет индекс следующего элемента для записи
    :param values:
    :param is_max:
    :return:
    """
    v_id = 0
    value = None
    for i in range(len(values)):
        if values[i]:
            value = values[i]
            v_id = i
            break
    if not value:
        return None
    for i in range(len(values)):
        if values[i] and (values[i] > value == is_max):
            value = values[i]
            v_id = i
    return v_id


def merge_to_one(files, out_file, is_reversed):
    """
    Сливает несколько отсортированных файлов в один общий файл
    :param files:
    :param out_file:
    :param is_reversed:
    :return:
    """
    is_read = list([False for _ in range(len(files))])
    values = list(["" for _ in range(len(files))])
    for file in files:
        file.open_file("r")
    out_file.clean()
    out_file.open_file("w")
    while True:
        for i in range(len(files)):
            if not files[i]:
                values[i] = files[i].read_line()
                if values[i]:
                    is_read[i] = True
                else:
                    values[i] = None
        written_id = find_value_id(values, is_reversed)
        if written_id is not None:
            out_file.write_line(str(values[written_id]) + "\n")
            is_read[written_id] = False
        else:
            break
