import os
import sys
import pytest

# Añade la carpeta raíz (un nivel arriba) al `sys.path`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from symbol_table import VariableTable, FunctionDirectory

def test_variable_table():
    vt = VariableTable()
    vt.add_variable('x', 'int')
    vt.add_variable('y', 'float')
    assert vt.get_variable('x') == 'int'
    assert vt.get_variable('y') == 'float'
    assert vt.get_variable('z') == None

    with pytest.raises(Exception) as excinfo:
        vt.add_variable('x', 'string')
    assert "Variable 'x' ya declarada." in str(excinfo.value)

def test_function_directory():
    fd = FunctionDirectory()
    fd.add_function('main', 'void', [])
    fd.add_function('add', 'int', [('a', 'int'), ('b', 'int')])
    
    assert fd.get_function('main')['return_type'] == 'void'
    assert fd.get_function('add')['return_type'] == 'int'
    assert fd.get_function('add')['params'] == [('a', 'int'), ('b', 'int')]
    assert fd.get_function('nonexistent') == None

    with pytest.raises(Exception) as excinfo:
        fd.add_function('main', 'void', [])
    assert "Function 'main' ya declarada." in str(excinfo.value)

    fd.add_variable_to_function('main', 'x', 'int')
    fd.add_variable_to_function('add', 'a', 'int')
    fd.add_variable_to_function('add', 'b', 'int')

    assert fd.get_function('main')['variables'].get_variable('x') == 'int'
    assert fd.get_function('add')['variables'].get_variable('a') == 'int'
    assert fd.get_function('add')['variables'].get_variable('b') == 'int'

    with pytest.raises(Exception) as excinfo:
        fd.add_variable_to_function('main', 'x', 'float')
    assert "Variable 'x' ya declarada" in str(excinfo.value)

if __name__ == '__main__':
    pytest.main([__file__])
