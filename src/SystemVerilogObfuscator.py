#!/bin/env python3

import sys
import HashFunctions
from antlr4 import CommonTokenStream
from antlr4 import FileStream
from antlr4 import InputStream
from antlr4 import Token
from ObfuscatorException import ObfuscatorException
from systemverilog.SystemVerilogLexer import SystemVerilogLexer

class SystemVerilogObfuscator:
    def __init__(self,mapFile):
        self.mapFile = mapFile
        self.mapFileOutputStream = {}
        self._populateMapDict()

    def _populateMapDict(self) -> None:
        with open(self.mapFile, "r", encoding="utf-8") as mapFileDict:
            for line in mapFileDict:
                key, value = line.strip().split("=")
                self.mapFileOutputStream[key] = value

    def mangle(self,inFile,outFile) -> None:
        try:
            print(f"Obfuscating: {inFile}")
            lexer = self._getLexerFromStream(inFile)
            token = lexer.nextToken()

            with open(outFile, "w", encoding="utf-8") as targetOutFile:
                while token.type != Token.EOF:
                    if token.type == SystemVerilogLexer.SIMPLE_IDENTIFIER:
                        outputString = self._processSimpleIdentifier(token.text)
                        targetOutFile.write(outputString)
                    elif token.type == SystemVerilogLexer.SOURCE_TEXT:
                        subLexer = self._getLexerFromString(token.text)
                        tokenStream = CommonTokenStream(subLexer)
                        tokenStream.fill()
                        for subToken in tokenStream.tokens:
                            if subToken.text != "<EOF>":
                                outputString = subToken.text
                                if subToken.type == SystemVerilogLexer.SIMPLE_IDENTIFIER:
                                    outputString = self._processSimpleIdentifier(outputString)
                                targetOutFile.write(outputString)
                    elif token.type in [SystemVerilogLexer.BLOCK_COMMENT,SystemVerilogLexer.LINE_COMMENT,]:
                        outputString = ""
                        targetOutFile.write(outputString)
                    elif token.type == SystemVerilogLexer.PRAGMA_DIRECTIVE:
                        outputString = "\n" + token.text + "\n"
                        targetOutFile.write(outputString)
                    else:
                        targetOutFile.write(token.text)

                    token = lexer.nextToken()
        except Exception as ex:
            raise ObfuscatorException(str(ex)) from ex

    def unMangle(self,inFile,outFile) -> None:
        pass

    def _getLexerFromStream(self, inStream: str) -> SystemVerilogLexer:
        charStream = FileStream(inStream, encoding="utf-8")
        lexer = SystemVerilogLexer(charStream)
        return lexer

    def _getLexerFromString(self, inString: str) -> SystemVerilogLexer:
        charStream = InputStream(inString)
        lexer = SystemVerilogLexer(charStream)
        return lexer

    def _processSimpleIdentifier(self, tokenText: str) -> str:
        if tokenText in self.mapFileOutputStream:
            newOutputString = self.mapFileOutputStream[tokenText]
            return newOutputString
        else:
            hashString = ("ID_S_" + HashFunctions.hash1(tokenText) + "_" + HashFunctions.hash2(tokenText) + "_E")
            self.mapFileOutputStream[tokenText] = hashString
            with open(self.mapFile, "a", encoding="utf-8") as mapFileOutput:
                mapFileOutput.write(tokenText + "=" + hashString + "\n")
            return hashString
