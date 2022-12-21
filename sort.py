from typing import Optional, Callable
from file import File
import csv


def my_sort(file_names: list, output: Optional[str] = None, type_data="s",
            reverse: bool = False, key: Optional[Callable] = None,
            bsize: Optional[int] = None) -> None:
    files = []
    for file_name in file_names:
        file = File(file_name, key=key, d_type=type_data)
        files.append(file)

    if output:
        out_file = File(output, key=key, d_type=type_data)


def create_tapes(input_file: File, n_path):
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


def merge_tapes(files, is_first, is_reversed):
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
                is_read[i] = True
        written_id = find_value_id(values, is_reversed)
        to_write[curr_id].write_line(str(values[written_id]))
        is_read[written_id] = False


def find_value_id(values, is_max):
    v_id = 0
    value = values[0]
    for i in range(len(value)):
        if values[i] > value == is_max:
            value = values[i]
            id = i
    return v_id

