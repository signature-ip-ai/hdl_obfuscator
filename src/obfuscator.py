#!/bin/env python3
import argparse
import sys
from SystemVerilogObfuscator import SystemVerilogObfuscator

def main():
    parser = argparse.ArgumentParser(description="HDL Obfuscator")
    parser.add_argument("mapfile", help="Map file to be used")
    parser.add_argument("inputfile", help="Source file")
    parser.add_argument("outputfile", help="Output file")
    args = parser.parse_args()

    _systemVerilogObfuscate(args.mapfile, args.inputfile, args.outputfile)

def _systemVerilogObfuscate(mapFile: str, inputFile: str, outputFile: str):
    try:
        systemVerilogObfuscator = SystemVerilogObfuscator(mapFile, inputFile, outputFile)
        systemVerilogObfuscator.generateObfuscatedFile()
    except Exception as ex:
        sys.exit("Unable to initialize Obfuscator")

if __name__ == "__main__":
    main()
