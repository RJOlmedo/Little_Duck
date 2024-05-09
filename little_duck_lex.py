import ply.lex as lex

# Lista de palabras reservadas (reserved words)
reserved = {
    'program': 'PROGRAM',
    'main': 'MAIN',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
    'void': 'VOID',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'print': 'PRINT',
    'end': 'END',
    'do': 'DO'
}

# Lista de tokens (agregar los reservados)
tokens = [
    'ID', 'CTE_INT', 'CTE_FLOAT', 'CTE_STRING',
    'PLUS', 'MINUS', 'MUL', 'DIV', 'ASSIGN',
    'LT', 'GT', 'EQ', 'NE', 'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE', 'SEMI', 'COLON', 'COMMA'
] + list(reserved.values())

# Literales
literals = ['+', '-', '*', '/', '=', '(', ')', '{', '}', ';', ':', ',']

# Reglas de expresión regular para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_ASSIGN = r'='
t_LT = r'<'
t_GT = r'>'
t_EQ = r'=='
t_NE = r'!='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r';'
t_COLON = r':'
t_COMMA = r','

# Identificadores (ID) y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Verificar si es una palabra reservada
    return t

# Constantes enteras (CTE_INT)
def t_CTE_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Constantes flotantes (CTE_FLOAT)
def t_CTE_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Constantes de cadena (CTE_STRING)
def t_CTE_STRING(t):
    r'"[^"]*"'
    return t

# Seguir el número de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espacios, tabulaciones y comentarios
t_ignore = ' \t'

def t_COMMENT(t):
    r'\#.*'
    pass  # No se devuelve valor; el token se descarta

# Manejo de errores
def t_error(t):
    print(f"Carácter ilegal: '{t.value[0]}' en línea {t.lineno}, posición {t.lexpos}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Prueba del lexer
if __name__ == '__main__':
    data = '''
    program ejemplo;
    var x : int;
    var y : string;
    main {
        if (x < 10) {
            print("Hola Mundo");
        }
    }
    '''
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
