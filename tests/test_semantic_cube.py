import os
import sys
import pytest

# Añade la carpeta raíz (un nivel arriba) al `sys.path`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from semantic_cube import get_result_type, INT, FLOAT, STRING, BOOL, ADD, SUB, MUL, DIV, LT, GT, EQ, NE

def test_int_operations():
    assert get_result_type(INT, ADD, INT) == INT
    assert get_result_type(INT, SUB, INT) == INT
    assert get_result_type(INT, MUL, INT) == INT
    assert get_result_type(INT, DIV, INT) == FLOAT
    assert get_result_type(INT, LT, INT) == BOOL
    assert get_result_type(INT, GT, INT) == BOOL
    assert get_result_type(INT, EQ, INT) == BOOL
    assert get_result_type(INT, NE, INT) == BOOL

def test_float_operations():
    assert get_result_type(FLOAT, ADD, FLOAT) == FLOAT
    assert get_result_type(FLOAT, SUB, FLOAT) == FLOAT
    assert get_result_type(FLOAT, MUL, FLOAT) == FLOAT
    assert get_result_type(FLOAT, DIV, FLOAT) == FLOAT
    assert get_result_type(FLOAT, LT, FLOAT) == BOOL
    assert get_result_type(FLOAT, GT, FLOAT) == BOOL
    assert get_result_type(FLOAT, EQ, FLOAT) == BOOL
    assert get_result_type(FLOAT, NE, FLOAT) == BOOL

def test_mixed_operations():
    assert get_result_type(INT, ADD, FLOAT) == FLOAT
    assert get_result_type(FLOAT, ADD, INT) == FLOAT
    assert get_result_type(INT, SUB, FLOAT) == FLOAT
    assert get_result_type(FLOAT, SUB, INT) == FLOAT

def test_string_operations():
    assert get_result_type(STRING, ADD, STRING) == STRING
    assert get_result_type(STRING, LT, STRING) == BOOL
    assert get_result_type(STRING, GT, STRING) == BOOL
    assert get_result_type(STRING, EQ, STRING) == BOOL
    assert get_result_type(STRING, NE, STRING) == BOOL

def test_invalid_operations():
    assert get_result_type(INT, ADD, STRING) == None
    assert get_result_type(STRING, SUB, STRING) == None
    assert get_result_type(FLOAT, MUL, STRING) == None
    assert get_result_type(STRING, DIV, FLOAT) == None

if __name__ == '__main__':
    pytest.main([__file__])
