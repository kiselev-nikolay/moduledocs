"""Parser based on parso. Returns objects compatible with BaseBuilder class."""

from pathlib import Path
from typing import List, Tuple, Iterator
import parso
from parso.python.tree import Node
from .parsed_objects import ParsedArgument, ParsedClass, ParsedDecorator,\
    ParsedDocstring, ParsedFunction, ParsedImport, ParsedModule,\
    ParsedParameter, ParsedStatement


def extract_params(d: Node) -> List[ParsedParameter]:
    return []


def extract_functions(d: Node) -> List[ParsedFunction]:
    return []


def extract_classes(d: Node) -> List[ParsedClass]:
    return []


def extract_imports(d: Node) -> List[ParsedImport]:
    return []


def extract_statements(d: Node) -> List[ParsedStatement]:
    return []


def extract(file_name: Path) -> ParsedModule:
    with open(file_name.absolute()) as file:
        root_node = parso.parse(file.read())
    return ParsedModule(name=file_name.name[:-3],
                        path=file_name,
                        docstring=ParsedDocstring(''),
                        imports=extract_imports(root_node),
                        statements=extract_statements(root_node),
                        classes=extract_classes(root_node),
                        functions=extract_functions(root_node))


def find_python(base: Path) -> Iterator[Path]:
    if base.is_dir():
        for child in base.iterdir():
            for python_file in find_python(child):
                yield python_file
    elif base.match('*.py'):
        yield base


def find_and_extract(base: Path) -> Iterator[ParsedModule]:
    for python_file in find_python(base):
        yield extract(python_file)


def test_find():
    """Test for recursive python files search."""
    module_dir = Path('testset/mypy')
    paths = list(find_python(module_dir))
    assert paths


def test_find_and_extract():
    """Test for recursive files parsing."""
    module_dir = Path('testset/mypy')
    parsed_modules = list(find_and_extract(module_dir))
    assert parsed_modules
    breakpoint()
