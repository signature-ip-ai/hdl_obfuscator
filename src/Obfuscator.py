#!/bin/env python3
import argparse
import os
import sys
from ObfuscatorException import ObfuscatorException
from SystemVerilogObfuscator import SystemVerilogObfuscator

def main():
    parser = argparse.ArgumentParser(description="HDL Obfuscator")
    parser.add_argument("mapFile", help="Map file to be used")
    parser.add_argument("inputFile",nargs = '?', help="Source file")
    parser.add_argument("outputFile",nargs = '?', help="Output file")
    parser.add_argument("-f", "--fileList", help="List of files to be obfuscated")
    modeGroup = parser.add_mutually_exclusive_group(required=True)
    modeGroup.add_argument("--mangle", help ="Obfuscate file",action ='store_true',dest="mangle",default=False)
    modeGroup.add_argument("--unmangle",help ="Decode obfuscated file",action ='store_true',dest="unmangle",default=False)
    args = parser.parse_args()

    mangle = args.mangle
    unmangle = args.unmangle

    if args.fileList and (args.inputFile or args.outputFile):
        parser.error("Please remove input and output arguments when using filelist command for Obfuscator")

    try:
        if mangle:
            if args.fileList:
                for source, target in _walkFileTree(args.fileList):
                    SystemVerilogObfuscator(args.mapFile).mangle(source,target)
            else:
                SystemVerilogObfuscator(args.mapFile).mangle(args.inputFile, args.outputFile)
        elif unmangle:
            if args.fileList:
                for source, target in _walkFileTree(args.fileList):
                    SystemVerilogObfuscator(args.mapFile).unMangle(source,target)
            else:
                SystemVerilogObfuscator(args.mapFile).unMangle(args.inputFile, args.outputFile)
    except Exception as ex:
        sys.exit(str(ex))

def _walkFileTree(fileList:str) -> set:
    filePairs = set()
    with open(fileList, 'r', encoding='utf-8') as obfuscationList:
        for line in obfuscationList:
            file = os.path.expandvars(line.strip())
            filePairs.add((file, file))

    return filePairs


if __name__ == "__main__":
    main()
