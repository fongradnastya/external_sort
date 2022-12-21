from file import File
from sort import split_file


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
    new_file = File("inp.txt")
    new_file.open_file("r")
    line = new_file.read_n_lines(5)
    out_1 = File("out1.txt")
    out_2 = File("out2.txt")
    split_file(new_file, 3, [out_1, out_2])
    print(line)
