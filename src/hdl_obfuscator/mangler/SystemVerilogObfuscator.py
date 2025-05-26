#!/bin/env python3

import sys
import re
from antlr4 import CommonTokenStream
from antlr4 import FileStream
from antlr4 import InputStream
from antlr4 import Token

from .ObfuscatorException import ObfuscatorException
from . import HashFunctions

from .systemverilog.SystemVerilogLexer import SystemVerilogLexer
from .systemverilog.SipcNcNocMacroLexer import SipcNcNocMacroLexer

class SystemVerilogObfuscator:
    def __init__(self,map_file):
        self._map_file = map_file
        self._map_file_output_stream = {}
        self._populateMapDict()

    def _populateMapDict(self) -> None:
        with open(self._map_file, "r", encoding="utf-8") as map_file_dict:
                for line in map_file_dict.readlines():
                    line = line.rstrip('\n')
                    line = line.strip()
                    if not line or "=" not in line:
                        continue
                    key, value = line.split("=")
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
                    elif token.type == SystemVerilogLexer.MACRO_TEXT:
                        sub_lexer = self._get_lexer_from_string(token.text)
                        token_stream = CommonTokenStream(sub_lexer)
                        token_stream.fill()
                        for sub_token in token_stream.tokens:
                            if sub_token.text != "<EOF>":
                                output_string = sub_token.text
                                match = re.match(r'^(_)?(.*?)(_[a-z])?$', output_string)
                                if match:
                                    leading_underscore = match.group(1) or ""
                                    output_string = match.group(2)
                                    trailing = match.group(3) or ""
                                macro_token = (self._get_lexer_from_macro(output_string)).nextToken()
                                if (sub_token.type == SystemVerilogLexer.SIMPLE_IDENTIFIER and
                                    macro_token.type != SipcNcNocMacroLexer.PROTECTED_MACRO):
                                    output_string = self.__process_simple_identifier(output_string)
                                output_string = f"{leading_underscore}{output_string}{trailing}"
                                target_out_file.write(output_string)
                    elif token.type in [SystemVerilogLexer.BLOCK_COMMENT, SystemVerilogLexer.LINE_COMMENT]:
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

    def _get_lexer_from_stream(self, input_stream: str) -> SystemVerilogLexer:
        char_stream = FileStream(input_stream, encoding="utf-8")
        lexer = SystemVerilogLexer(char_stream)
        return lexer

    def _get_lexer_from_string(self, input_string: str) -> SystemVerilogLexer:
        char_stream = InputStream(input_string)
        lexer = SystemVerilogLexer(char_stream)
        return lexer
    
    def _get_lexer_from_macro(self, input_string: str) -> SipcNcNocMacroLexer:
        char_stream = InputStream(input_string)
        lexer = SipcNcNocMacroLexer(char_stream)
        return lexer

    def __process_simple_identifier(self, token_text: str) -> str:
        if token_text in self._map_file_output_stream:
            new_output_string = self._map_file_output_stream[token_text]
            return new_output_string
        else:
            hash_string = ("ID_S_" + HashFunctions.hash1(token_text) + "_" + HashFunctions.hash2(token_text) + "_E")
            self._map_file_output_stream[token_text] = hash_string
            with open(self._map_file, "a", encoding="utf-8") as map_file_output:
                map_file_output.write(token_text + "=" + hash_string + "\n")
            return hash_string
