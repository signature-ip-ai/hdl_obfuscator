/**
 * SipcNcNocMacroLexer.g4
 * 
 * This grammar defines protected identifiers that should NOT be obfuscated
 * during code processing. These are typically:
 * - Special macro identifiers
 * - Protocol interface names
 * - Other identifiers that must remain unchanged
 * 
 * Add new protected identifiers by extending the PROTECTED_IDENTIFIER rule below.
 * Format: One identifier per line, separated by pipes (|)
 * 
 * Note: These are treated separately from regular SystemVerilog keywords
 * to maintain readability in obfuscated output where needed.
 */
lexer grammar SipcNcNocMacroLexer;

PROTECTED_MACRO: 
    'CL'
  | 'CL_NUM'
  | 'E_NUM'
  | 'I_NUM'
  | 'CL_NUM_E'
  | 'CL_NUM_I'
  | 'CL_NUM_FROM'
  | 'CL_NUM_TO'
  | 'NUM'
  | 'IDX'
  | 'PREFIX'
  | 'NAME'
  | [a-zA-Z0-9_$]+ '_if'
  | 'E'
  | 'e'
  | 'I'
  | 'i'
  | 'ifdef'
  | 'ifndef'
  | 'elsif'
  | 'endif'
  | 'define'
  | 'SUBTOP'
  | 'SUB_NUM'
  | MACRO_TITLE
  // Add new protected identifiers below this line, follow the same pipe-separated format
  ;
  
MACRO_TITLE:
    'CONNECT_'[a-zA-Z0-9_$]*
  | 'DEFINE_'[a-zA-Z0-9_$]*
  | 'GEN_'[a-zA-Z0-9_$]*
  | 'GENERATE_'[a-zA-Z0-9_$]*
  | 'INST_'[a-zA-Z0-9_$]*
  | 'SET_'[a-zA-Z0-9_$]*
  | 'MODULE_'[a-zA-Z0-9_$]*
  ;

NON_PROTECTED_MACRO: [a-zA-Z_][a-zA-Z0-9_$]* ;

// Catch-all for any other input (prevents token recognition errors)
ANY_OTHER : . -> skip ;