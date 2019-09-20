"""Parser based on parso. Returns objects compatible with BaseBuilder class."""

from pathlib import Path
from typing import List, Iterator, Union, Any
import parso
from parso.python.tree import Node, Module, Class, Function, Keyword,\
    PythonNode, Name, Operator, Import, ImportFrom, ImportName
from .parsed_objects import ParsedArgument, ParsedClass, ParsedDecorator,\
    ParsedDocstring, ParsedFunction, ParsedImport, ParsedModule,\
    ParsedParameter, ParsedStatement, ParsedKeyword, ParsedOperator


def extract_doc(node: Union[Module, Class, Function]) -> ParsedDocstring:
    doc_node = node.get_doc_node()
    if doc_node:
        doc = eval(doc_node.value)
        # eval function is way to extract docstring exacly as anyone want to
        # injections cannot be here, because parso search only for docstring
    else:
        doc = ''
    return ParsedDocstring(doc.strip())


def find_nodes(node: Node, target_type: Any) -> Iterator[Node]:
    has_type_match = isinstance(node, target_type)
    if not has_type_match and hasattr(node, 'children'):
        for child in node.children:
            for target in find_nodes(child, target_type):
                yield target
    elif has_type_match:
        yield node


def filter_nodes(node: Node, targets: List[Any]) -> Iterator[Node]:
    targets_hit = [isinstance(node, t) for t in targets]
    if hasattr(node, 'children'):
        for child in node.children:
            for nodes in filter_nodes(child, targets):
                yield nodes
    elif any(targets_hit):
        yield node


def extract_imports(node: Module) -> List[ParsedImport]:
    node_imports = []
    for node_import in node.iter_imports():
        from_module = ''
        import_data = []
        for n in filter_nodes(node_import, [Name, Keyword, Operator]):
            value = n.value
            if not from_module and isinstance(n, Name):
                from_module = value
            if isinstance(n, Name):
                import_data.append(value)
            elif isinstance(n, Keyword):
                import_data.append(ParsedKeyword(value))
            elif isinstance(n, Operator):
                import_data.append(ParsedOperator(value))
            else:
                raise ValueError('Unexpected python code: ' +
                                 node_import.get_code())
        node_imports.append(ParsedImport(from_module, import_data))
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
