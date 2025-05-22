# Generated from SystemVerilogMacroLexer.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,3,55,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,1,0,1,0,1,0,1,0,1,0,1,0,1,
        0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,
        0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,3,0,43,8,0,1,1,
        1,1,5,1,47,8,1,10,1,12,1,50,9,1,1,2,1,2,1,2,1,2,0,0,3,1,1,3,2,5,
        3,1,0,2,3,0,65,90,95,95,97,122,5,0,36,36,48,57,65,90,95,95,97,122,
        62,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,1,42,1,0,0,0,3,44,1,0,0,0,
        5,51,1,0,0,0,7,43,5,69,0,0,8,9,5,67,0,0,9,43,5,76,0,0,10,11,5,67,
        0,0,11,12,5,76,0,0,12,13,5,95,0,0,13,14,5,78,0,0,14,15,5,85,0,0,
        15,43,5,77,0,0,16,17,5,69,0,0,17,18,5,95,0,0,18,19,5,78,0,0,19,20,
        5,85,0,0,20,43,5,77,0,0,21,22,5,73,0,0,22,23,5,95,0,0,23,24,5,78,
        0,0,24,25,5,85,0,0,25,43,5,77,0,0,26,27,5,78,0,0,27,28,5,65,0,0,
        28,29,5,77,0,0,29,43,5,69,0,0,30,31,5,112,0,0,31,32,5,114,0,0,32,
        33,5,111,0,0,33,34,5,116,0,0,34,35,5,111,0,0,35,36,5,99,0,0,36,37,
        5,111,0,0,37,38,5,108,0,0,38,39,5,95,0,0,39,40,5,105,0,0,40,43,5,
        102,0,0,41,43,5,101,0,0,42,7,1,0,0,0,42,8,1,0,0,0,42,10,1,0,0,0,
        42,16,1,0,0,0,42,21,1,0,0,0,42,26,1,0,0,0,42,30,1,0,0,0,42,41,1,
        0,0,0,43,2,1,0,0,0,44,48,7,0,0,0,45,47,7,1,0,0,46,45,1,0,0,0,47,
        50,1,0,0,0,48,46,1,0,0,0,48,49,1,0,0,0,49,4,1,0,0,0,50,48,1,0,0,
        0,51,52,9,0,0,0,52,53,1,0,0,0,53,54,6,2,0,0,54,6,1,0,0,0,3,0,42,
        48,1,6,0,0
    ]

class SystemVerilogMacroLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    PROTECTED_MACRO = 1
    NON_PROTECTED_MACRO = 2
    ANY_OTHER = 3

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
 ]

    symbolicNames = [ "<INVALID>",
            "PROTECTED_MACRO", "NON_PROTECTED_MACRO", "ANY_OTHER" ]

    ruleNames = [ "PROTECTED_MACRO", "NON_PROTECTED_MACRO", "ANY_OTHER" ]

    grammarFileName = "SystemVerilogMacroLexer.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


