import re

class FileDemangler:
    def __init__(self, map_file_path):
        self.map_file_path = map_file_path
        self.map_file_dict = {}
        self._populate_map_dict()

    def _populate_map_dict(self) -> None:
        try:
            with open(self.map_file_path, "r", encoding="utf-8", errors="surrogateescape") as map_file:
                for line in map_file:
                    key, value = line.strip().split("=")
                    self.map_file_dict[value] = key
        except FileNotFoundError as ex:
            print(f"Error processing map file: {ex}")

    def demangle_file(self, input_file_path: str, output_file_path: str) -> None:
        try:
            with open(input_file_path, "r", encoding="utf-8", errors="surrogateescape") as input_file:
                with open(output_file_path, "w", encoding="utf-8", errors="surrogateescape") as output_file:
                    input_contents = input_file.read()
                    demangled_contents = self._demangle_string(input_contents)
                    if demangled_contents is not None:
                        output_file.write(demangled_contents)
        except FileNotFoundError as ex1:
            print(f"Error processing file: {ex1}")
        except Exception as ex2:
            print(f"Error processing file: {ex2}")

    def _demangle_string(self, input_string: str) -> str | None:
        try:
            compiled_patterns = {re.compile(re.escape(value)): key for value, key in self.map_file_dict.items()}
            for pattern, replacement in compiled_patterns.items():
                if pattern.search(input_string):
                    print(f"Demangling from '{pattern.pattern}' to '{replacement}'")
                    input_string = pattern.sub(replacement, input_string)
            return input_string
        except Exception as ex:
            print(f"Error during string demangling: {ex}")
            return None
