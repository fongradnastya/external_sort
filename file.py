import os
import csv
from io import UnsupportedOperation


class File:

    def __init__(self, path, d_type="s", key=None):
        self._path = path
        self.create_file()
        self._is_txt = self._path.endswith(".txt")
        self._reader = None
        self._writer = None
        self._key = key
        self._file = None
        self._data_type = d_type

    @property
    def is_txt(self):
        return self._is_txt

    @property
    def key(self):
        return self._key

    @property
    def data_type(self):
        return self._data_type

    def create_file(self):
        if not os.path.exists(self._path):
            with open(self._path, "x", encoding="utf-8") as _:
                pass

    def open_file(self, mode):
        if self._file:
            self.close_file()
        self._file = open(self._path, mode, encoding='utf-8', newline="")
        if not self._is_txt:
            if mode in ("w", "a"):
                self._writer = csv.DictWriter(self._file,
                                              fieldnames=[self._key])
            elif mode == "r":
                self._reader = csv.DictReader(self._file)

    def _read_csv_line(self):
        if not self._reader:
            raise UnsupportedOperation("This file is not readable")
        try:
            return next(self._reader)[self._key]
        except StopIteration:
            return ''

    def _read_txt_file(self):
        try:
            return self._file.readline()
        except StopIteration:
            return ''

    def read_line(self):
        if not self._file:
            self.open_file("r")
        if self._is_txt:
            line = self._read_txt_file()
        else:
            line = self._read_csv_line()
        return line

    def read_n_lines(self, n_lines):
        lines = []
        for i in range(n_lines):
            line = self.read_line()
            if not line:
                break
            lines.append(line)
        return lines

    def write_line(self, line):
        if not self._file:
            self.open_file("r")
        if self._is_txt:
            self._file.write(str(line))
        else:
            if self._data_type == "s":
                value = str(line)
            elif self._data_type == "i":
                value = int(line)
            elif self._data_type == "f":
                value = float(line)
            elif self._data_type == "c":
                value = chr(line)
            else:
                raise ValueError("Wrong file data type")
            self._writer.writerow({self._key: value})

    def write_n_lines(self, lines):
        if not self._file:
            self.open_file("a")
        for line in lines:
            self.write_line(line)

    def close_file(self):
        if self._file:
            self._file.close()
            self._file = None
            self._reader = None
            self._writer = None

    def clean(self):
        self.open_file("w")
        self.write_line("")
        self.close_file()

    def delete(self):
        self.close_file()
        os.remove(self._path)
        self._path = None

    def is_valid(self, line):
        line = line.replace(" ", "").replace("\t", "").replace("\n", "")
        if not line:
            return False
        if self._data_type == "i":
            pass
