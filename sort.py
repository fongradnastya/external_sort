from typing import Optional
from file import File
from sys import getrecursionlimit


def my_sort(file_names, n_paths: int = 3, output: Optional[str] = None,
            type_data="s", reverse: bool = False,
            key=None,bsize: Optional[int] = 2) -> None:
    """

    :param file_names:
    :param n_paths:
    :param output:
    :param type_data:
    :param reverse:
    :param key:
    :param bsize:
    :return:
    """
    if isinstance(file_names, str):
        inp_file = File(file_names, key=key, d_type=type_data)

        def cmp(val1, val2):
            if inp_file.is_txt:
                return val1 > val2 if reverse else val1 < val2
            return val1[key] > val2[key] if reverse else val1[key] < val2[key]

        new_file = sort_one_file(inp_file, n_paths, cmp, bsize)
        print(new_file)
        if output:
            out_file = File(output, key=key, d_type=type_data)
            new_file.copy_to(out_file)
        else:
            new_file.copy_to(inp_file)
        new_file.delete()
    else:
        files = []
        for file_name in file_names:
            file = File(file_name, key=key, d_type=type_data)
            sorted_file = sort_one_file(file, n_paths, reverse, bsize)
            files.append(sorted_file)
        if output:
            out_file = File(output, key=key, d_type=type_data)
            merge_to_one(files, out_file, reverse)
        else:
            if files[0].is_txt:
                new_file = File("merged.txt", d_type=type_data)
            else:
                new_file = File("merged.csv", d_type=type_data, key=key)
            merge_to_one(files, new_file, reverse)
        for file in files:
            file.delete()


def sort_one_file(file, n_paths: int, cmp,
                  bsize: Optional[int] = None):
    tapes = create_tapes(file, n_paths)
    split_file(file, bsize, tapes[:n_paths], cmp)
    number = 0
    file = None
    while file is None:
        file = merge_tapes(tapes, number, bsize, cmp)
        number += 1
    for tape in tapes:
        if tape is not file:
            tape.delete()
    return file


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
            new_file = File(f"temp{i}.txt", d_type=input_file.data_type)
        else:
            new_file = File(f"temp{i}.csv", key=input_file.key,
                            d_type=input_file.data_type)
        files.append(new_file)
    return files


def split_file(file, buff_size, tapes, cmp):
    """
    Разделяет входной файл на n различных файлов
    :param file:
    :param buff_size:
    :param tapes:
    :param cmp
    :return:
    """
    curr_id = 0
    file.open_file("r")
    for tape in tapes:
        tape.clean()
        tape.open_file("a")
    while curr_id < len(tapes):
        data = file.read_n_lines(buff_size)
        data = sort_buffer(data, cmp)
        print(data)
        tape = tapes[curr_id]
        tape.write_n_lines(data)
        curr_id = curr_id + 1 if curr_id + 1 < len(tapes) else 0
        if len(data) < buff_size:
            break
    file.close_file()
    for tape in tapes:
        tape.close_file()


def sort_buffer(buffer, cmp):

    def insertion_sort(arr):
        for i in range(1, len(arr)):
            temp = arr[i]
            j = i - 1
            while j >= 0 and cmp(temp, arr[j]):
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = temp

    def merge_sort(arr: list, depth: int = 1) -> list:
        if (n_len := len(arr)) > 1:
            mid = n_len // 2
            left = arr[:mid]
            right = arr[mid:]
            if depth + 1 > getrecursionlimit():
                insertion_sort(left)
                insertion_sort(right)
            else:
                merge_sort(left, depth + 1)
                merge_sort(right, depth + 1)

            i = j = k = 0

            while i < len(left) and j < len(right):
                if cmp(left[i], right[j]):
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                k += 1

            while j < len(right):
                arr[k] = right[j]
                j += 1
                k += 1

            while i < len(left):
                arr[k] = left[i]
                i += 1
                k += 1
        return arr

    return merge_sort(buffer)


def merge_tapes(files, number, buff_size, cmp):
    """
    Сливает первые n лент в другие n лент
    :param files:
    :param number:
    :param buff_size:
    :param cmp:
    :return:
    """
    n = len(files) // 2
    if number % 2 == 0:
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
    while curr_id < n:
        is_read = list([False for _ in range(n)])
        values = list(["" for _ in range(n)])
        curr_len = n ** number * buff_size
        counters = list([0 for _ in range(n)])
        while True:
            end = False
            for cnt in counters:
                if cnt > curr_len:
                    end = True
            if end:
                break
            for i in range(n):
                if not is_read[i] and counters[i] < curr_len:
                    values[i] = to_read[i].read_line()
                    is_read[i] = True
                    counters[i] += 1
            written_id = find_value_id(values, cmp)
            if written_id is not None:
                to_write[curr_id].write_line(str(values[written_id]))
                is_read[written_id] = False
                print(f"file {curr_id} value {str(values[written_id])}")
                print(values)
                values[written_id] = None
            else:
                break
        curr_id = curr_id + 1 if curr_id + 1 < n else 0
        quantity = sum(counters)
        if quantity < curr_len * n:
            break

    for file in to_read:
        file.close_file()
    written = []
    for file in to_write:
        file.close_file()
        if not file.is_empty():
            written.append(file)
    if len(written) == 1:
        return written[0]
    return None


def find_value_id(values, cmp):
    """
    Ищет индекс следующего элемента для записи
    :param values:
    :param cmp:
    :return:
    """
    v_id = 0
    value = None
    for i in range(len(values)):
        if values[i] is not None:
            value = values[i]
            v_id = i
            break
    if value is None:
        return None
    for i in range(len(values)):
        if values[i] is not None:
            if cmp(values[i], value):
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
    out_file.open_file("a")
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
