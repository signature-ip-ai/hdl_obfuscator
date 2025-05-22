/**
 * SystemVerilogProtectedIdentifiers.g4
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
lexer grammar SystemVerilogMacroLexer;

PROTECTED_MACRO: 
    'E'
  | 'CL'
  | 'CL_NUM'
  | 'E_NUM'
  | 'I_NUM'
  | 'NAME'
  | 'protocol_if'
  | 'e'
  // Add new protected identifiers below this line, follow the same pipe-separated format
  ;

NON_PROTECTED_MACRO: [a-zA-Z_][a-zA-Z0-9_$]* ;

// Catch-all for any other input (prevents token recognition errors)
ANY_OTHER : . -> skip ;