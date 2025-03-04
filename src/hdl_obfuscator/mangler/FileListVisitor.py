#!/bin/env python3
import os
import re
from . import config

class FileListVisitor:
    def __init__(self, file_list_path: str):
        self._file_list_path = file_list_path
        self._source_files = []

    def parse(self) -> None:
        self._source_files = self._read_file_list(self._file_list_path)

    def get_source_files(self) -> list[str]:
        return self._source_files

    def _read_file_list(self, file_list_path) -> list[str]:
        source_files = set()
        with open(file_list_path, "r", encoding="utf-8") as obfuscation_list:
            for line in obfuscation_list.readlines():
                line = line.rstrip('\n')
                line = line.strip()
                line = os.path.expandvars(line)
                print(f"Reading path: {line}")

                if self._is_line_commented(line):
                    continue

                if self._is_verilog_file_path(line):
                    print(f"Using Verilog file: {line}")
                    line = os.path.normpath(line)
                    if line:
                        source_files.add((line))

                elif self._is_incdir_path(line):
                    incdir_line = self._get_file_list_from_incdir_path(line)
                    incdir_files_path = os.path.normpath(incdir_line)

                    if not os.path.exists(incdir_files_path):
                        print(f"Directory not found: {incdir_files_path}")
                        continue

                    for root, _, files in os.walk(incdir_files_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            print(f"Adding file: {file_path}")
                            source_files.add((file_path))

                elif self._is_file_list_file_path(line):
                    inner_file_list_path = os.path.normpath(self._get_file_list_from_file_path(line))

                    if not os.path.exists(inner_file_list_path):
                        print(f"File list not found: {inner_file_list_path}")
                        continue

                    inner_source_files = self._read_file_list(inner_file_list_path)
                    source_files.update(inner_source_files)

        return source_files

    def _is_line_commented(self, line) -> bool:
        expression = re.compile(r'^\s*(//|#)')
        return expression.search(line)

    def _is_incdir_path(self, path: str) -> bool:
        return path.startswith("+incdir+")

    def _get_file_list_from_incdir_path(self, path: str) -> str:
        if path.startswith("+incdir+"):
            return path[len("+incdir+"):]

    def _is_file_list_file_path(self, path) -> bool:
        if 2 != len(path.split()):
            return False

        return '-f' == path.split()[0]

    def _get_file_list_from_file_path(self, line):
        return line.split()[1]

    def _is_verilog_file_path(self, path) -> bool:
        if 1 != len(path.split()):
            return False

        extension = os.path.splitext(path)[1]
        return extension in config.verilog_extensions
