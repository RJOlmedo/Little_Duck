import sys
import os
import pytest
from io import StringIO
from contextlib import redirect_stdout

# Añadir el directorio raíz del proyecto al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from virtual_machine import VirtualMachine

def test_addition():
    const_table = {500: 10, 501: 20}
    quadruples = [
        ('+', 500, 501, 200),  # t0 = 10 + 20
        ('print', 200, None, None)  # print(t0)
    ]
    
    vm = VirtualMachine(const_table)
    vm.initialize_memory()
    
    for address, value in const_table.items():
        vm.set_memory(address, value)
    
    vm.load_quadruples(quadruples)
    
    f = StringIO()
    with redirect_stdout(f):
        vm.execute()
    
    output = f.getvalue().strip()
    assert output == '30'

def test_subtraction():
    const_table = {500: 30, 501: 10}
    quadruples = [
        ('-', 500, 501, 200),  # t0 = 30 - 10
        ('print', 200, None, None)  # print(t0)
    ]
    
    vm = VirtualMachine(const_table)
    vm.initialize_memory()
    
    for address, value in const_table.items():
        vm.set_memory(address, value)
    
    vm.load_quadruples(quadruples)
    
    f = StringIO()
    with redirect_stdout(f):
        vm.execute()
    
    output = f.getvalue().strip()
    assert output == '20'

def test_multiplication():
    const_table = {500: 5, 501: 4}
    quadruples = [
        ('*', 500, 501, 200),  # t0 = 5 * 4
        ('print', 200, None, None)  # print(t0)
    ]
    
    vm = VirtualMachine(const_table)
    vm.initialize_memory()
    
    for address, value in const_table.items():
        vm.set_memory(address, value)
    
    vm.load_quadruples(quadruples)
    
    f = StringIO()
    with redirect_stdout(f):
        vm.execute()
    
    output = f.getvalue().strip()
    assert output == '20'

def test_division():
    const_table = {500: 20, 501: 5}
    quadruples = [
        ('/', 500, 501, 200),  # t0 = 20 / 5
        ('print', 200, None, None)  # print(t0)
    ]
    
    vm = VirtualMachine(const_table)
    vm.initialize_memory()
    
    for address, value in const_table.items():
        vm.set_memory(address, value)
    
    vm.load_quadruples(quadruples)
    
    f = StringIO()
    with redirect_stdout(f):
        vm.execute()
    
    output = f.getvalue().strip()
    assert output == '4.0'

def test_comparison():
    const_table = {500: 10, 501: 20}
    quadruples = [
        ('>', 500, 501, 400),  # t0 = 10 > 20
        ('print', 400, None, None)  # print(t0)
    ]
    
    vm = VirtualMachine(const_table)
    vm.initialize_memory()
    
    for address, value in const_table.items():
        vm.set_memory(address, value)
    
    vm.load_quadruples(quadruples)
    
    f = StringIO()
    with redirect_stdout(f):
        vm.execute()
    
    output = f.getvalue().strip()
    assert output == 'False'
