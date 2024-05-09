import os
import sys
import pytest

# Añade la carpeta raíz (un nivel arriba) al `sys.path`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa el lexer correctamente ahora
from little_duck_lex import lexer

# Función para procesar un texto con el lexer
def tokenize(input_text):
    lexer.input(input_text)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    return tokens

# Función para comparar un token con los valores esperados
def assert_token(token, expected_type, expected_value):
    assert token.type == expected_type
    assert token.value == expected_value

# Prueba 1: Comprobación de palabras reservadas y delimitadores
def test_reserved_keywords_and_delimiters():
    data = 'program main; var x : int;'
    tokens = tokenize(data)
    assert_token(tokens[0], 'PROGRAM', 'program')
    assert_token(tokens[1], 'MAIN', 'main')
    assert_token(tokens[2], 'SEMICOLON', ';')
    assert_token(tokens[3], 'VAR', 'var')
    assert_token(tokens[4], 'ID', 'x')
    assert_token(tokens[5], 'COLON', ':')
    assert_token(tokens[6], 'INT', 'int')
    assert_token(tokens[7], 'SEMICOLON', ';')

# Prueba 2: Expresiones aritméticas
def test_arithmetic_expressions():
    data = 'x = 3 + 5 * (10 - 2);'
    tokens = tokenize(data)
    assert_token(tokens[0], 'ID', 'x')
    assert_token(tokens[1], 'ASSIGN', '=')
    assert_token(tokens[2], 'CTE_INT', 3)
    assert_token(tokens[3], 'PLUS', '+')
    assert_token(tokens[4], 'CTE_INT', 5)
    assert_token(tokens[5], 'TIMES', '*')
    assert_token(tokens[6], 'LPAREN', '(')
    assert_token(tokens[7], 'CTE_INT', 10)
    assert_token(tokens[8], 'MINUS', '-')
    assert_token(tokens[9], 'CTE_INT', 2)
    assert_token(tokens[10], 'RPAREN', ')')
    assert_token(tokens[11], 'SEMICOLON', ';')

# Prueba 3: Literales de tipo flotante y cadenas
def test_floats_and_strings():
    data = 'var y : float; y = 4.56; print("Hello!");'
    tokens = tokenize(data)
    assert_token(tokens[0], 'VAR', 'var')
    assert_token(tokens[1], 'ID', 'y')
    assert_token(tokens[2], 'COLON', ':')
    assert_token(tokens[3], 'FLOAT', 'float')
    assert_token(tokens[4], 'SEMICOLON', ';')
    assert_token(tokens[5], 'ID', 'y')
    assert_token(tokens[6], 'ASSIGN', '=')
    assert_token(tokens[7], 'CTE_FLOAT', 4.56)
    assert_token(tokens[8], 'SEMICOLON', ';')
    assert_token(tokens[9], 'PRINT', 'print')
    assert_token(tokens[10], 'LPAREN', '(')
    assert_token(tokens[11], 'CTE_STRING', 'Hello!')
    assert_token(tokens[12], 'RPAREN', ')')
    assert_token(tokens[13], 'SEMICOLON', ';')

# Prueba 4: Estructuras condicionales
def test_conditionals():
    data = 'if (x != 5) { print("Not five"); } else { print("Is five"); }'
    tokens = tokenize(data)
    assert_token(tokens[0], 'IF', 'if')
    assert_token(tokens[1], 'LPAREN', '(')
    assert_token(tokens[2], 'ID', 'x')
    assert_token(tokens[3], 'NOTEQUALS', '!=')
    assert_token(tokens[4], 'CTE_INT', 5)
    assert_token(tokens[5], 'RPAREN', ')')
    assert_token(tokens[6], 'LBRACE', '{')
    assert_token(tokens[7], 'PRINT', 'print')
    assert_token(tokens[8], 'LPAREN', '(')
    assert_token(tokens[9], 'CTE_STRING', 'Not five')
    assert_token(tokens[10], 'RPAREN', ')')
    assert_token(tokens[11], 'SEMICOLON', ';')
    assert_token(tokens[12], 'RBRACE', '}')
    assert_token(tokens[13], 'ELSE', 'else')
    assert_token(tokens[14], 'LBRACE', '{')
    assert_token(tokens[15], 'PRINT', 'print')
    assert_token(tokens[16], 'LPAREN', '(')
    assert_token(tokens[17], 'CTE_STRING', 'Is five')
    assert_token(tokens[18], 'RPAREN', ')')
    assert_token(tokens[19], 'SEMICOLON', ';')
    assert_token(tokens[20], 'RBRACE', '}')

if __name__ == '__main__':
    pytest.main([__file__])
