import os
import sys
import pytest

# Añade la carpeta raíz (un nivel arriba) al `sys.path`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa el lexer correctamente ahora
from little_duck_lex import lexer

# Función auxiliar para tokenizar una cadena
def get_tokens(data):
    lexer.input(data)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    return tokens

# Pruebas para diferentes palabras clave y tokens
def test_keywords_and_tokens():
    data = '''
    program ejemplo;
    var x : int;
    main {
        print("Hola Mundo");
    }
    '''
    tokens = get_tokens(data)
    expected_types = [
        'PROGRAM', 'ID', 'SEMI',
        'VAR', 'ID', 'COLON', 'INT', 'SEMI',
        'MAIN', 'LBRACE',
        'PRINT', 'LPAREN', 'CTE_STRING', 'RPAREN', 'SEMI',
        'RBRACE'
    ]
    assert [tok.type for tok in tokens] == expected_types

# Prueba para operadores aritméticos
def test_arithmetic_operators():
    data = '3 + 4 * (5 - 6) / 7'
    tokens = get_tokens(data)
    expected_types = [
        'CTE_INT', 'PLUS', 'CTE_INT', 'MUL', 'LPAREN', 'CTE_INT',
        'MINUS', 'CTE_INT', 'RPAREN', 'DIV', 'CTE_INT'
    ]
    assert [tok.type for tok in tokens] == expected_types

# Prueba para operadores relacionales
def test_relational_operators():
    data = 'x < 10 == y != 20'
    tokens = get_tokens(data)
    expected_types = ['ID', 'LT', 'CTE_INT', 'EQ', 'ID', 'NE', 'CTE_INT']
    assert [tok.type for tok in tokens] == expected_types

# Prueba para comentarios
def test_comments():
    data = '''
    # Esto es un comentario
    var x : int;
    '''
    tokens = get_tokens(data)
    expected_types = ['VAR', 'ID', 'COLON', 'INT', 'SEMI']
    assert [tok.type for tok in tokens] == expected_types

if __name__ == '__main__':
    pytest.main([__file__])
