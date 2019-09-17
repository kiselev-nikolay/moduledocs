"""Parser based on parso. Returns objects compatible with BaseBuilder class."""

from pathlib import Path
from typing import List, Iterator, Union
import parso
from parso.python.tree import Node, Module, Class, Function, Keyword,\
    PythonNode, Name, Operator
from .parsed_objects import ParsedArgument, ParsedClass, ParsedDecorator,\
    ParsedDocstring, ParsedFunction, ParsedImport, ParsedModule,\
    ParsedParameter, ParsedStatement


def extract_doc(node: Union[Module, Class, Function]) -> ParsedDocstring:
    doc_node = node.get_doc_node()
    if doc_node:
        doc = eval(doc_node.value)
        # eval function is way to extract docstring exacly as anyone want to
        # injections cannot be here, because parso search only for docstring
    else:
        doc = ''
    return ParsedDocstring(doc.strip())


def extract_imports(node: Module) -> List[ParsedImport]:
    node_imports = []
    for node_import in node.iter_imports():
        import_data = dict(import_from=[],
                           import_import=[],
                           import_as=[])
        scan = 'from'
        for part_node in node_import.children:
            if isinstance(part_node, Operator):
                continue
            if isinstance(part_node, Keyword):
                keyword = part_node.value
                if keyword in ['from', 'import', 'as']:
                    scan = keyword
            else:
                if isinstance(part_node, Name):
                    import_data['import_' + scan].append(part_node.value)
                elif isinstance(part_node, PythonNode):
                    value = ['']
                    for child in part_node.children:
                        if isinstance(child, Operator):
                            if child.value.strip() == '.':
                                value[-1] += '.'
                            elif child.value.strip() == ',':
                                value.append('')
                            else:
                                import_data['import_' + scan].append(
                                    part_node.get_code())
                                continue
                        else:
                            value[-1] += child.value
                    import_data['import_' + scan].extend(value)
                else:
                    import_data['import_' + scan].append(part_node.get_code())
        node_imports.append(ParsedImport(**import_data))
    return node_imports


def extract_statements(node: Node) -> List[ParsedStatement]:
    return []


def extract_params(node: Node) -> List[ParsedParameter]:
    return []


def extract_functions(node: Node) -> List[ParsedFunction]:
    return []


def extract_classes(node: Node) -> List[ParsedClass]:
    return []


def extract(file_name: Path) -> ParsedModule:
    with open(file_name.absolute()) as file:
        root_node = parso.parse(file.read())
    return ParsedModule(name=file_name.name[:-3],
                        path=file_name,
                        docstring=extract_doc(root_node),
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
    import itertools
    module_dir = Path('testset/mypy')
    parsed_modules = list(itertools.islice(find_and_extract(module_dir), 19))
    assert parsed_modules
    breakpoint()
