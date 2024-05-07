#!/bin/env python3
import argparse
import os
import sys
from SystemVerilogObfuscator import SystemVerilogObfuscator

def main():
    parser = argparse.ArgumentParser(description="HDL Obfuscator")
    parser.add_argument("mapfile", help="Map file to be used")
    parser.add_argument("inputFile",nargs = '?', help="Source file")
    parser.add_argument("outputFile",nargs = '?', help="Output file")
    parser.add_argument("-f", "--fileList", help="List of files to be obfuscated")
    args = parser.parse_args()

    if args.fileList:
        if args.inputFile or args.outputFile:
            parser.error("Please remove input and output arguments when using filelist command for Obfuscator")
        else:
            for source, target in _walkFileTree(args.fileList):
                print(f"Obfuscated: {source}")
                _systemVerilogObfuscate(args.mapfile, source, target)
    else:
        _systemVerilogObfuscate(args.mapfile, args.inputFile, args.outputFile)

def _systemVerilogObfuscate(mapFile: str, inputFile, outputFile: str):
    try:
        systemVerilogObfuscator = SystemVerilogObfuscator(mapFile, inputFile, outputFile)
        systemVerilogObfuscator.generateObfuscatedFile()
    except Exception as ex:
        sys.exit("Unable to initialize Obfuscator")

def _walkFileTree(fileList:str) -> set:
    filePairs = set()
    with open(fileList, 'r', encoding='utf-8') as obfuscationList:
        for line in obfuscationList:
            file = os.path.expandvars(line.strip())
            filePairs.add((file, file))

    return filePairs


if __name__ == "__main__":
    main()
