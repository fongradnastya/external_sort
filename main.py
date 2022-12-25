import csv

from file import File
from sort import *


def generate_csv_input(file_name="input.csv", delimiter=","):
    """
    Генерация случайного входного csv файла
    :param file_name: имя файла
    :param delimiter: разделитель между столбцами
    """
    from random import randint
    rows = list("abcd")
    with open(file_name, "w", newline="") as file:
        writer = csv.DictWriter(file, rows, delimiter=delimiter)
        writer.writeheader()
        for _ in range(200):
            writer.writerow({row: randint(-100, 1000) for row in rows})


if __name__ == "__main__":
    my_sort("inp.txt", 2, bsize=2, output="out.txt")
