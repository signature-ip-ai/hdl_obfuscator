#!/bin/env python3

from antlr4 import CommonTokenStream
from antlr4 import FileStream
from antlr4 import InputStream
from antlr4 import Token

from .ObfuscatorException import ObfuscatorException
from . import HashFunctions

from .systemverilog.SystemVerilogLexer import SystemVerilogLexer

class SystemVerilogObfuscator:
    def __init__(self,map_file):
        self._map_file = map_file
        self._map_file_output_stream = {}
        self._populateMapDict()

    def _populateMapDict(self) -> None:
        with open(self._map_file, "r", encoding="utf-8") as map_file_dict:
            for line in map_file_dict:
                key, value = line.strip().split("=")
                self._map_file_output_stream[key] = value

    def mangle(self,in_file,out_file) -> None:
        try:
            print(f"Obfuscating: {in_file}")
            lexer = self._get_lexer_from_stream(in_file)
            token = lexer.nextToken()

            with open(out_file, "w", encoding="utf-8") as target_out_file:
                while token.type != Token.EOF:
                    if token.type == SystemVerilogLexer.SIMPLE_IDENTIFIER:
                        output_string = self.__process_simple_identifier(token.text)
                        target_out_file.write(output_string)
                    elif token.type == SystemVerilogLexer.SOURCE_TEXT:
                        sub_lexer = self._get_lexer_from_string(token.text)
                        token_stream = CommonTokenStream(sub_lexer)
                        token_stream.fill()
                        for sub_token in token_stream.tokens:
                            if sub_token.text != "<EOF>":
                                output_string = sub_token.text
                                if sub_token.type == SystemVerilogLexer.SIMPLE_IDENTIFIER:
                                    output_string = self.__process_simple_identifier(output_string)
                                target_out_file.write(output_string)
                    elif token.type in [SystemVerilogLexer.BLOCK_COMMENT,SystemVerilogLexer.LINE_COMMENT,]:
                        output_string = ""
                        target_out_file.write(output_string)
                    elif token.type == SystemVerilogLexer.PRAGMA_DIRECTIVE:
                        output_string = "\n" + token.text + "\n"
                        target_out_file.write(output_string)
                    else:
                        target_out_file.write(token.text)

                    token = lexer.nextToken()
        except Exception as ex:
            raise ObfuscatorException(str(ex)) from ex

    def unMangle(self,in_file,out_file) -> None:
        pass

    def _get_lexer_from_stream(self, inStream: str) -> SystemVerilogLexer:
        charStream = FileStream(inStream, encoding="utf-8")
        lexer = SystemVerilogLexer(charStream)
        return lexer

    def _get_lexer_from_string(self, inString: str) -> SystemVerilogLexer:
        charStream = InputStream(inString)
        lexer = SystemVerilogLexer(charStream)
        return lexer

    def __process_simple_identifier(self, tokenText: str) -> str:
        if tokenText in self._map_file_output_stream:
            newOutputString = self._map_file_output_stream[tokenText]
            return newOutputString
        else:
            hashString = ("ID_S_" + HashFunctions.hash1(tokenText) + "_" + HashFunctions.hash2(tokenText) + "_E")
            self._map_file_output_stream[tokenText] = hashString
            with open(self._map_file, "a", encoding="utf-8") as mapFileOutput:
                mapFileOutput.write(tokenText + "=" + hashString + "\n")
            return hashString
