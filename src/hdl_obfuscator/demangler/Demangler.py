import argparse
import sys
from FileDemangler import FileDemangler

def print_info():
    print(__file__)

def main():
    parser = argparse.ArgumentParser("HDL File Demangler")
    parser.add_argument("mapFile", help="Map file")
    parser.add_argument("inputFile", help="Path of file to be demangled")
    parser.add_argument("outputFile", help="Target output path")
    args = parser.parse_args()

    map_file = args.mapFile
    input_file = args.inputFile
    output_file = args.outputFile
    try:
        demangler = FileDemangler(map_file)
        demangler.demangle_file(input_file, output_file)
    except Exception as ex:
        sys.exit(str(ex))


if __name__ == "__main__":
    main()
