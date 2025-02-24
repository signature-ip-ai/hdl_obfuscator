#!/bin/env python3

import argparse
import os
import sys
from .SystemVerilogObfuscator import SystemVerilogObfuscator
from .ModuleWalker import ModuleWalker
from .FileListVisitor import FileListVisitor


def main():
    parser = argparse.ArgumentParser(description="HDL Obfuscator")
    parser.add_argument("mapFile", nargs="?", help="Map file", default="mapfile.dat")
    parser.add_argument("inputFile", nargs="?", help="Source file")
    parser.add_argument("outputFile", nargs="?", help="Output file")
    parser.add_argument("-f", "--fileList", help="List of files to be obfuscated")
    parser.add_argument("-tm", "--topModule", help="Path containing top module used")
    modeGroup = parser.add_mutually_exclusive_group(required=True)
    modeGroup.add_argument(
        "--mangle",
        help="Obfuscate file",
        action="store_true",
        dest="mangle",
        default=False,
    )
    modeGroup.add_argument(
        "--unmangle",
        help="Decode obfuscated file",
        action="store_true",
        dest="unmangle",
        default=False,
    )
    args = parser.parse_args()

    mangle = args.mangle
    unmangle = args.unmangle
    mapFile = args.mapFile

    if args.topModule is not None:
        walker = ModuleWalker(args.topModule)
        mapFile = walker.generateMapFile(args.mapFile)
    else:
        if not os.path.exists(mapFile):
            print(f"Map file '{mapFile}' not found. Creating default map file.")
        try:
            open(mapFile, "w").close()
        except Exception as e:
            sys.exit(f"Error creating map file: {e}")

    if args.fileList and (args.inputFile or args.outputFile):
        parser.error(
            "Please remove input and output arguments when using filelist command for Obfuscator"
        )

    try:
        if mangle:
            if args.fileList:
                visitor = FileListVisitor(args.fileList)
                visitor.parse()
                for source, target in visitor.get_source_files():
                    SystemVerilogObfuscator(mapFile).mangle(source, target)
            else:
                SystemVerilogObfuscator(mapFile).mangle(args.inputFile, args.outputFile)
        elif unmangle:
            if args.fileList:
                visitor = FileListVisitor(args.fileList)
                visitor.parse()
                for source, target in visitor.get_source_files():
                    SystemVerilogObfuscator(mapFile).unMangle(source, target)
            else:
                SystemVerilogObfuscator(mapFile).unMangle(
                    args.inputFile, args.outputFile
                )
    except Exception as ex:
        sys.exit(str(ex))


if __name__ == "__main__":
    main()
