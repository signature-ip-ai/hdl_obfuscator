#!/bin/env python3

import HashFunctions
from antlr4 import *
from systemverilog.SystemVerilogLexer import SystemVerilogLexer

class SystemVerilogObfuscator:
    def __init__(self, mapFile, inFileOutputStream, outfileOutputStream):
        self.mapFile = mapFile
        self.mapFileOutputStream = {}
        self.inFileOutputStream = inFileOutputStream
        self.outFileOutputStream = outfileOutputStream
        self._populateMapDict()

    def _populateMapDict(self) -> None:
        with open(self.mapFile, "r", encoding="utf-8") as mapFileDict:
            for line in mapFileDict:
                key, value = line.strip().split("=")
                self.mapFileOutputStream[key] = value

    def generateObfuscatedFile(self) -> None:
        try:
            lexer = self._getLexerFromStream(self.inFileOutputStream)
            token = lexer.nextToken()

            with open(self.outFileOutputStream, "w", encoding="utf-8") as outFile:
                while token.type != Token.EOF:
                    if token.type == SystemVerilogLexer.SIMPLE_IDENTIFIER:
                        outputString = self._processSimpleIdentifier(token.text)
                        outFile.write(outputString)
                    elif token.type == SystemVerilogLexer.SOURCE_TEXT:
                        subLexer = self._getLexerFromString(token.text)
                        tokenStream = CommonTokenStream(subLexer)
                        tokenStream.fill()
                        for subToken in tokenStream.tokens:
                            if subToken.text != "<EOF>":
                                outputString = subToken.text
                                if subToken.type == SystemVerilogLexer.SIMPLE_IDENTIFIER:
                                    outputString = self._processSimpleIdentifier(outputString)
                                outFile.write(outputString)
                    elif token.type in [SystemVerilogLexer.BLOCK_COMMENT,SystemVerilogLexer.LINE_COMMENT,]:
                        outputString = ""
                        outFile.write(outputString)
                    elif token.type == SystemVerilogLexer.PRAGMA_DIRECTIVE:
                        outputString = "\n" + token.text + "\n"
                        outFile.write(outputString)
                    else:
                        outFile.write(token.text)

                    token = lexer.nextToken()

        except Exception as ex:
            return None

    def _getLexerFromStream(self, inStream: str) -> SystemVerilogLexer:
        try:
            charStream = FileStream(inStream, encoding="utf-8")
            lexer = SystemVerilogLexer(charStream)
        except Exception as ex:
            return None
        return lexer

    def _getLexerFromString(self, inString: str) -> SystemVerilogLexer:
        try:
            charStream = InputStream(inString)
            lexer = SystemVerilogLexer(charStream)
        except Exception as ex:
            return None
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
