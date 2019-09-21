"""Parser based on parso. Returns objects compatible with BaseBuilder class."""

from pathlib import Path
from typing import List, Iterator, Dict, Union, Any
import parso
from parso.python.tree import PythonBaseNode, PythonNode, Module, Class,\
    Function, Keyword, Name, Operator, ExprStmt, Literal
from .parsed_objects import ParsedArgument, ParsedClass, ParsedDecorator,\
    ParsedDocstring, ParsedFunction, ParsedImport, ParsedModule,\
    ParsedParameter, ParsedStatement, ParsedKeyword, ParsedOperator, ParsedName


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


def filter_nodes(node: PythonBaseNode,
                 targets: List[Any]) -> Iterator[PythonBaseNode]:
    """Recursive find every node with target type."""
    targets_hit = [isinstance(node, t) for t in targets]
    if any(targets_hit):
        yield node
    elif hasattr(node, 'children'):
        for child in node.children:
            for nodes in filter_nodes(child, targets):
                yield nodes


def shallow_filter_nodes(node: PythonBaseNode,
                         targets: List[Any],
                         depth: int = 2,
                         examine: bool = True) -> Iterator[PythonBaseNode]:
    """Recursive find every node with target type with depth limit."""
    if depth:
        targets_hit = [isinstance(node, t) for t in targets]
        if any(targets_hit):
            yield node
        elif isinstance(node, (Module, PythonNode)) or (
             examine and hasattr(node, 'children')):
            for child in node.children:
                for nodes in shallow_filter_nodes(child, targets, depth - 1):
                    yield nodes


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
                import_data.append(ParsedName(value))
            elif isinstance(n, Keyword):
                import_data.append(ParsedKeyword(value))
            elif isinstance(n, Operator):
                import_data.append(ParsedOperator(value))
            else:
                raise ValueError('Unexpected "import" python code: ' +
                                 node_import.get_code())
        node_imports.append(ParsedImport(from_module, import_data))
    return node_imports


def extract_statements(node: PythonBaseNode) -> List[ParsedStatement]:
    """
    Extract parsed statements from module.

    Examples:
    RED = (255, 0, 0)
    app = web.Application(port='69')
    nice = True

    """
    statements = []
    for statement_node in shallow_filter_nodes(node, [ExprStmt], 3,
                                               examine=False):
        statement_data: Dict[str, List[str]] = {}
        statement_data_order: List[str] = []
        state = True
        order = 0
        for n in filter_nodes(statement_node,
                              [Name, Keyword, Operator, Literal]):
            v = n.value
            if isinstance(n, Operator):
                if v == '=':
                    state = False
                elif v == ',':
                    if not state:
                        order += 1
                else:
                    write = statement_data[statement_data_order[order]]
                    write.append(v)
            elif isinstance(n, (Name, Literal)):
                if state:
                    statement_data_order.append(v)
                    statement_data[v] = []
                else:
                    write = statement_data[statement_data_order[order]]
                    write.append(v)
        for n, v in statement_data.items():
            statements.append(ParsedStatement(n, None, ' '.join(v)))
    return statements


def extract_params(node: Union[Class, Function]) -> List[ParsedParameter]:
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


def extract_decorators(node: Union[Class, Function]) -> List[ParsedDecorator]:
    """Extract parsed decorators for function, method or class."""
    ParsedArgument('60', 'x')
    return []


def extract_functions(node: Union[Module, Class]) -> List[ParsedFunction]:
    """Extract parsed functions from node."""
    return []


def extract_classes(node: Module) -> List[ParsedClass]:
    """Extract parsed classes from node."""
    return []


def extract(file_name: Path) -> ParsedModule:
    """Extract parsed module from file by path."""
    with open(file_name.absolute()) as file:
        root_node = parso.parse(file.read())
    return ParsedModule(name=ParsedName(file_name.name[:-3]),
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


# TESTS


def test_find():
    """Test for recursive python files search."""
    module_dir = Path('testset/mypy')
    paths = list(find_python(module_dir))
    assert paths


def test_extract():
    """Test for recursive files parsing."""
    return
    from random import shuffle
    module_dir = Path('testset/mypy')
    python_files = list(find_python(module_dir))
    shuffle(python_files)
    parsed_modules = []
    for python_file in python_files[:10]:
        parsed_modules.append(extract(python_file))
    assert parsed_modules


def test_import():
    """Test imports extraction."""
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
    """Test statements extraction."""
    code = ['x = 200',
            'y = pow(3)',
            'a, b = 130, x + y',
            'print("Henlo")',
            'HTTP = os.environ["HTTP"]',
            'x: int = 1']
    module = parso.parse('\n'.join(code))
    statements = extract_statements(module)
    assert len(statements) == 7
