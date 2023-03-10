import os
import csv
from io import UnsupportedOperation


class File:
    """
    Класс для работы с txt и csv файлами
    """
    def __init__(self, path, d_type="s", key=None, header=None):
        """
        Создаёт новый экземпляр файла
        :param path:
        :param d_type:
        :param key:
        """
        self._path = path
        self.create_file()
        self._is_txt = self._path.endswith(".txt")
        self._reader = None
        self._writer = None
        self._key = key
        self._file = None
        self._data_type = d_type
        self._lines_cnt = 0
        self.count_lines()
        self._header = header

    @property
    def is_txt(self):
        """
        Геттер для поля _is_txt
        :return: является ли файл текстовым
        """
        return self._is_txt

    @property
    def key(self):
        """
        Геттер для поля _key
        :return: ключ, по которому будет происходить сортировка
        """
        return self._key

    @property
    def data_type(self):
        """
        Геттер для поля _data_type
        :return: тип сортируемых значений
        """
        return self._data_type

    @property
    def header(self):
        """
        Геттер для заголовка csv файла
        :return: заголовок файла
        """
        return self._header

    def is_empty(self):
        """
        Проверяет файл на пустоту
        :return: является ли файл пустым
        """
        return self._lines_cnt == 0

    def create_file(self):
        """
        Создаёт новый файл
        """
        if not os.path.exists(self._path):
            with open(self._path, "x", encoding="utf-8") as _:
                pass

    def open_file(self, mode):
        """
        Открывает файл в заданном режиме
        :param mode: режим открытия файла
        """
        if self._file:
            self.close_file()
        self._file = open(self._path, mode, encoding='utf-8', newline="")
        if not self._is_txt:
            if mode in ("w", "a"):
                self._writer = csv.DictWriter(self._file,
                                              fieldnames=self._header)
                if mode == "w":
                    self._writer.writeheader()
            elif mode == "r":
                self._reader = csv.DictReader(self._file)
                self._header = self._reader.fieldnames
                if not self._key:
                    self._key = self._header[0]

    def _read_csv_line(self):
        """
        Считывание строки из txt файла
        :return: считанная строка
        """
        if not self._reader:
            raise UnsupportedOperation("This file is not readable")
        try:
            res = next(self._reader)
            res[self._key] = self.validate(res[self._key])
            return res
        except StopIteration:
            return None

    def _read_txt_file(self):
        """
        Считывание строки из текстового файла
        :return: считанная строка
        """
        try:
            return self._file.readline()
        except StopIteration:
            return None

    def read_line(self):
        """
        Считывание строки из файла
        :return: считанная строка
        """
        if not self._file:
            self.open_file("r")
        if self._is_txt:
            line = self._read_txt_file()
            line = self.validate(line)
        else:
            line = self._read_csv_line()
        return line

    def read_n_lines(self, n_lines):
        """
        Считывание заданного количества строк из файла
        :param n_lines: число строк для считывания
        :return: список считанных строк
        """
        lines = []
        for i in range(n_lines):
            line = ""
            while line == "":
                line = self.read_line()
                if line is None:
                    return lines
            lines.append(line)
        return lines

    def write_line(self, line, new_line=True):
        """
        Запись строки в файл
        :param line: значение для записи
        :param new_line
        """
        if not self._file:
            self.open_file("r")
        if self._is_txt:
            string = str(line) + "\n" if new_line else str(line)
            self._file.write(string)
            self._lines_cnt += 1
        else:
            self._writer.writerow(line)
            self._lines_cnt += 1

    def write_n_lines(self, lines):
        """
        Запись списка строк в файл
        :param lines: список строк
        """
        if not self._file:
            self.open_file("a")
        for line in lines:
            self.write_line(line)

    def count_lines(self):
        """Метод для вычисления количества строк"""
        if self._file is None:
            self.open_file('r')
        if self._is_txt:
            for _ in self._file:
                self._lines_cnt += 1
        else:
            for _ in self._reader:
                self._lines_cnt += 1
        self.close_file()

    def copy_to(self, other: "File"):
        """
        Копирует содержимое файла в новый файл
        :param other: файл, в который будет производиться копирование
        :return:
        """
        other.clean()
        other.open_file("w")
        self.open_file("r")
        while (line := self.read_line()) is not None:
            other.write_line(line)
        other.close_file()

    def close_file(self):
        """
        Закрывает файл
        """
        if self._file:
            self._file.close()
            self._file = None
            self._reader = None
            self._writer = None

    def clean(self):
        """
        Очищает содержимое файла
        """
        self.open_file("w")
        if self._is_txt:
            self.write_line("", new_line=False)
        self.close_file()
        self._lines_cnt = 0

    def delete(self):
        """
        Удаляет файл из файловой системы
        """
        self.close_file()
        os.remove(self._path)
        self._path = None

    def validate(self, line):
        """
        Проверяет, является ли считанная строка корректной
        :param line: строка для проверки
        :return:
        """
        line = line.replace(" ", "").replace("\t", "").replace("\n", "").\
            replace("\r", "")
        if not line:
            return None
        if self._data_type == "s":
            return line
        if self._data_type == "i":
            try:
                val = int(line)
            except ValueError as ex:
                print(ex, "wrong data type")
                val = ""
            return val
        if self._data_type == "f":
            try:
                val = float(line)
            except ValueError as ex:
                print(ex, "wrong data type")
                val = ""
            return val

    def __str__(self):
        """Получение строкового представления файла"""
        return self._path

    def __repr__(self):
        """Получение строкового представления файла"""
        return self._path
