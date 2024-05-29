import sys
import os
import pytest

# Añadir el directorio raíz del proyecto al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from little_duck_lex import lexer, tokens

def test_reserved_words():
    data = 'program main end var int float print if else void while do'
    lexer.input(data)
    expected_tokens = ['PROGRAM', 'MAIN', 'END', 'VAR', 'INT', 'FLOAT', 'PRINT', 'IF', 'ELSE', 'VOID', 'WHILE', 'DO']
    
    for expected_token in expected_tokens:
        tok = lexer.token()
        assert tok.type == expected_token

def test_operators():
    data = '+ - * / = != < >'
    lexer.input(data)
    expected_tokens = ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'NE', 'LT', 'GT']
    
    for expected_token in expected_tokens:
        tok = lexer.token()
        assert tok.type == expected_token

def test_delimiters():
    data = '( ) ; : , { }'
    lexer.input(data)
    expected_tokens = ['LPAREN', 'RPAREN', 'SEMICOLON', 'COLON', 'COMMA', 'LBRACE', 'RBRACE']
    
    for expected_token in expected_tokens:
        tok = lexer.token()
        assert tok.type == expected_token

def test_identifiers():
    data = 'var1 var_2 _var3'
    lexer.input(data)
    expected_tokens = ['ID', 'ID', 'ID']
    
    for expected_token in expected_tokens:
        tok = lexer.token()
        assert tok.type == expected_token
        assert tok.value in ['var1', 'var_2', '_var3']

def test_constants():
    data = '123 45.67 "hello world" \'test string\''
    lexer.input(data)
    expected_tokens = [('CTE_INT', 123), ('CTE_FLOAT', 45.67), ('CTE_STRING', 'hello world'), ('CTE_STRING', 'test string')]
    
    for expected_token in expected_tokens:
        tok = lexer.token()
        assert tok.type == expected_token[0]
        assert tok.value == expected_token[1]

def test_illegal_character():
    data = '@'
    lexer.input(data)
    tok = lexer.token()
    assert tok is None  # Illegal character should be skipped
