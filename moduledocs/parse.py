"""Parser based on parso. Returns objects compatible with BaseBuilder class."""

from pathlib import Path
from typing import List, Iterator, Union, Any
import parso
from parso.python.tree import Node, Module, Class, Function,\
    Keyword, Name, Operator, ExprStmt
from .parsed_objects import ParsedArgument, ParsedClass, ParsedDecorator,\
    ParsedDocstring, ParsedFunction, ParsedImport, ParsedModule,\
    ParsedParameter, ParsedStatement, ParsedKeyword, ParsedOperator


def extract_doc(node: Union[Module, Class, Function]) -> ParsedDocstring:
    """Extract parsed docstring from module, class or function."""
    doc_node = node.get_doc_node()
    if doc_node:
        doc = eval(doc_node.value)
        # eval function is way to extract docstring exacly as anyone want to
        # injections cannot be here, because parso search only for docstring
    else:
        doc = ''
    return ParsedDocstring(doc.strip())


def filter_nodes(node: Node, targets: List[Any]) -> Iterator[Node]:
    """Recursive find every node with target type."""
    targets_hit = [isinstance(node, t) for t in targets]
    if hasattr(node, 'children'):
        for child in node.children:
            for nodes in filter_nodes(child, targets):
                yield nodes
    elif any(targets_hit):
        yield node


def shallow_filter_nodes(node: Node, targets: List[Any],
                         depth: int = 0) -> Iterator[Node]:
    """Recursive find every node with target type with depth limit."""
    if depth:
        targets_hit = [isinstance(node, t) for t in targets]
        if hasattr(node, 'children'):
            for child in node.children:
                for nodes in shallow_filter_nodes(child, targets, depth - 1):
                    yield nodes
        elif any(targets_hit):
            yield node


def extract_imports(node: Module) -> List[ParsedImport]:
    """Extract parsed imports from module."""
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
                raise ValueError('Unexpected "import" python code: ' +
                                 node_import.get_code())
        node_imports.append(ParsedImport(from_module, import_data))
    return node_imports


def extract_statements(node: Node) -> List[ParsedStatement]:
    """
    Extract parsed statements from module.

    Examples:
    RED = (255, 0, 0)
    app = web.Application(port='69')
    nice = True

    """
    for expr_node in shallow_filter_nodes(node, [ExprStmt], 3):
        pass
    return []


def extract_params(node: Node) -> List[ParsedParameter]:
    """
    Extract parsed parameters from node.

    If this is class method
    For:
        def g(a: int, b: int = 2):
            ...
    Extracted parameters:
        a: int, b: int = 2

    """
    return []


def extract_decorators(node: Node) -> List[ParsedDecorator]:
    """Extract parsed decorators for function, method or class."""
    ParsedArgument('60', 'x')
    return []


def extract_functions(node: Node) -> List[ParsedFunction]:
    """Extract parsed functions from node."""
    return []


def extract_classes(node: Node) -> List[ParsedClass]:
    """Extract parsed classes from node."""
    return []


def extract(file_name: Path) -> ParsedModule:
    """Extract parsed module from file by path."""
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
    """Find python files in directory and subdirectories."""
    if base.is_dir():
        for child in base.iterdir():
            for python_file in find_python(child):
                yield python_file
    elif base.match('*.py'):
        yield base


def find_and_extract(base: Path) -> Iterator[ParsedModule]:
    """
    Recursive extract parsed module in directory.

    Extract parsed module for every python files in directory and
    subdirectories.
    """
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
    parsed_modules = list(itertools.islice(find_and_extract(module_dir), 8))
    assert parsed_modules


def test_import():
    """Test imports extraction."""
    node = parso.parse(
        'import numpy as np\n'
        'from city.zoo import dog, cat as spider, chupacabra\n'
        'from os.path import\\\n'
        '    exist')
    imports = extract_imports(node)
    assert imports[0].from_module == 'numpy'
    assert imports[0].import_data[2] == ParsedKeyword('as')
    assert len(imports[1].import_data) == 12
    assert len(imports[2].import_data) == 6


def test_statment():
    """Test statements extraction."""
    pass
