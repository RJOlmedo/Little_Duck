import ply.lex as lex

# List of token names
tokens = [
    'ID', 'CTE_STRING', 'CTE_INT', 'CTE_FLOAT', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'LPAREN', 'RPAREN', 'SEMICOLON', 'COLON', 'COMMA', 'LBRACE', 'RBRACE', 'LT', 'GT', 'NE'
]

# Reserved words
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

# Regular expressions for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LT = r'<'
t_GT = r'>'
t_NE = r'!='

# Regular expression rules with some action code
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
    t.value = t.value[1:-1]  # Remove the quotes
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Define a rule for new lines to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
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
