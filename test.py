from pathlib import Path
from random import shuffle
from moduledocs.parsed_objects import ParsedKeyword
from moduledocs.parse import find_python, extract, extract_statements,\
    extract_imports
import parso


def test_find():
    module_dir = Path('testset/mypy')
    paths = list(find_python(module_dir))
    assert paths


def test_extract():
    module_dir = Path('testset/mypy')
    python_files = list(find_python(module_dir))
    shuffle(python_files)
    parsed_modules = []
    for python_file in python_files[:10]:
        parsed_modules.append(extract(python_file))
    assert parsed_modules


def test_import():
    code = ['import numpy as np',
            'from city.zoo import dog, cat as spider, chupacabra',
            'from os.path import\\',
            '    exist']
    module = parso.parse('\n'.join(code))
    imports = extract_imports(module)
    assert imports[0].from_module == 'numpy'
    assert imports[0].import_data[2] == ParsedKeyword('as')
    assert len(imports[1].import_data) == 12
    assert len(imports[2].import_data) == 6
    replica = imports[0].code()
    assert replica == code[0]
    replica = imports[1].code()
    assert replica == code[1]


def test_statement():
    code = ['x = 200',
            'y = pow(3)',
            'a, b = 130, x + y',
            'print("Henlo")',
            'HTTP = os.environ["HTTP"]',
            'x: int = 1']
    module = parso.parse('\n'.join(code))
    statements = extract_statements(module)
    assert len(statements) == 5
