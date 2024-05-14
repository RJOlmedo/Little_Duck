from ply import lex

reserved = {
    'program': 'PROGRAM',
    'main': 'MAIN',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'end': 'END',
    'print': 'PRINT',
    'var': "VAR",
    'void': 'VOID',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
}

tokens = [
    'ID', 'CTE_INT', 'CTE_FLOAT', 'CTE_STRING',
    'COLON', 'SEMICOLON', 'COMMA',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'ASSIGN', 'NOTEQUALS', 'LESS', 'GREATER'
] + list(reserved.values())

t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ASSIGN = r'='
t_NOTEQUALS = r'!='
t_LESS = r'<'
t_GREATER = r'>'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_CTE_FLOAT(t):
    r'[-]?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTE_INT(t):
    r'[-]?\d+'
    t.value = int(t.value)
    return t

def t_CTE_STRING(t):
    r'"(\\.|[^"\\])*"'
    t.value = t.value.strip('"')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    raise SyntaxError(f"Illegal character {t.value[0]} on line {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

