import ply.lex as lex


# PALABRAS RESERVADAS

reserved = {
    'int': 'INT',
    'char': 'CHAR',
    'void': 'VOID',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'return': 'RETURN',
    'printf': 'PRINTF',
    'scanf': 'SCANF'
}


# TOKENS

tokens = [
    'ID',
    'INTEGER_CONSTANT',
    'CHAR_CONSTANT',
    'STRING_CONSTANT',

    # operadores aritméticos
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',

    # operadores relacionales y de igualdad
    'EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE',

    # asignación
    'ASSIGN',

    # símbolos
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'COMMA', 'SEMICOLON', 'PUNTOS', "COMILLAS"
] + list(reserved.values())


# REGLAS LEXICAS SIMPLES

t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_EQ       = r'=='
t_NEQ      = r'!='
t_LT       = r'<'
t_LE       = r'<='
t_GT       = r'>'
t_GE       = r'>='
t_ASSIGN   = r'='
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_LBRACE   = r'\{'
t_RBRACE   = r'\}'
t_COMMA    = r','
t_SEMICOLON= r';'
t_PUNTOS = r'\.\.\.'  # puntos suspensivos
t_COMILLAS = r'\"'  # comillas dobles

# REGLAS CON CÓDIGO

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  
    return t

def t_INTEGER_CONSTANT(t):
    r'0|([1-9][0-9]*)'
    t.value = int(t.value)
    return t

def t_CHAR_CONSTANT(t):
    r"\'([^\\\n]|(\\.))\'"
    return t

def t_STRING_CONSTANT(t):
    r'\"([^\\\n]|(\\[n"\\]))*\"'
    return t


# COMENTARIOS Y ESPACIOS

def t_COMMENT(t):
    r'/\*([^*]|\*+[^*/])*\*+/'
    pass  # ignorar comentario

t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# ERRORES

def t_error(t):
    print(f"error lexico en linea {t.lineno}: caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)


# CONSTRUIR EL LEXER
lexer = lex.lex()
