import ply.lex as lex

# Lista de nombres de tokens
tokens = [
    'ID', 'CTE_STRING', 'CTE_INT', 'CTE_FLOAT', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'LPAREN', 'RPAREN', 'SEMICOLON', 'COLON', 'COMMA', 'LBRACE', 'RBRACE', 'LT', 'GT', 'NE'
]

# Palabras reservadas
reserved = {
    'program': 'PROGRAM',
    'main': 'MAIN',
    'end': 'END',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'void': 'VOID',
    'while': 'WHILE',
    'do': 'DO'
}

tokens = tokens + list(reserved.values())

# Expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LT = r'<'
t_GT = r'>'
t_EQUALS = r'='
t_NE = r'!='
t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Reglas de expresiones regulares con código de acción
def t_CTE_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTE_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CTE_STRING(t):
    r'("[^\n"]*")|(\'[^\n\']*\')'
    t.value = t.value[1:-1]  # Eliminar las comillas
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Verificar palabras reservadas
    return t

# Una cadena que contiene caracteres ignorados (espacios y tabulaciones)
t_ignore = ' \t'

# Definir una regla para nuevas líneas para rastrear los números de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regla de manejo de errores
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Probarlo
if __name__ == "__main__":
    data = '''
    program test;

    var a : float;
        b : float;
        c : float;
        d : float;
        e : float;
        f : float;
        g : float;
        h : float;
        j : float;
        k : float;

    main {
        a = b + c * (d - e / f) * h;
        b = e - f;
        do {
            h = j * k + b;
            if (b < h) {
                b = h + j;
                do {
                    print (a + b * c, d - e);
                    b = b - j;
                } while (b > a + c);
            } else {
                do {
                    a = a + b;
                    print (b - d);
                } while (a - d < c + b);
            };
        } while (a * b - c > d * e / (g + h));
        f = a + b;
    }
    end
    '''
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
