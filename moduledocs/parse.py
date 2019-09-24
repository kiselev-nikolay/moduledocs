"""Parser based on parso. Returns objects compatible with BaseBuilder class."""

from pathlib import Path
from copy import copy
from typing import List, Iterator, Union, Any
import parso
from parso.python.tree import PythonBaseNode, PythonNode, Module, Class,\
    Function, Keyword, Name, Operator, ExprStmt, Literal
from .parsed_objects import ParsedClass, ParsedDecorator,\
    ParsedDocstring, ParsedFunction, ParsedImport, ParsedModule,\
    ParsedParameter, ParsedStatement, ParsedKeyword, ParsedOperator,\
    ParsedName, ParsedLiteral


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


def same_parsed(
    node: Union[Name, Keyword, Operator, Literal],
    *values: List[str]
) -> Union[ParsedName, ParsedKeyword, ParsedOperator, ParsedLiteral]:
    """Get same object from parsed object."""
    if isinstance(node, Name):
        return ParsedName(*values)
    elif isinstance(node, Keyword):
        return ParsedKeyword(*values)
    elif isinstance(node, Operator):
        return ParsedOperator(*values)
    elif isinstance(node, Literal):
        return ParsedLiteral(*values)
    else:
        raise Exception('Same not found!')


def norm_stmt(node: PythonBaseNode, equation: bool = True) -> List[Any]:
    """Statement normalization function."""
    statement_data: List[ParsedName] = []
    statement_value: List[Any] = []
    state = copy(equation)
    for part in filter_nodes(node, [Name, Keyword, Operator, Literal]):
        value = part.value
        if isinstance(part, Operator):
            if state and value == '=':
                state = False
            elif state and value != ',':
                statement_data.append(value)
            elif not state:
                statement_value.append(ParsedOperator(value))
        elif isinstance(part, Name):
            if state:
                statement_data.append(ParsedName(value))
            else:
                statement_value.append(ParsedName(value))
        elif not state:
            statement_value.append(ParsedLiteral(value))
    return ParsedStatement(statement_data, statement_value)


def extract_imports(node: Module) -> List[ParsedImport]:
    """Extract parsed imports from module."""
    node_imports = []
    for node_import in node.iter_imports():
        from_module = ''
        import_data = []
        for part in filter_nodes(node_import, [Name, Keyword, Operator]):
            value = part.value
            if not from_module and isinstance(part, Name):
                from_module = value
            if isinstance(part, (Name, Keyword, Operator)):
                import_data.append(same_parsed(part, value))
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
        statements.append(norm_stmt(statement_node))
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
    params = []
    for param in node.get_params():
        for part in filter_nodes(param, [Name,
                                         Operator,
                                         Literal]):
            params.append(same_parsed(part, part.value))
            # TODO Parsed parameter!!
    return params


def extract_decorators(node: Union[Class, Function]) -> List[ParsedDecorator]:
    """Extract parsed decorators for function, method or class."""
    decorators = []
    for decorator in node.get_decorators():
        name = []
        args = []
        brackets = False
        for part in filter_nodes(decorator, [Name,
                                             Operator,
                                             Literal]):
            if part.value in '()' and isinstance(part, Operator):
                brackets = True
            elif brackets:
                args.append(same_parsed(part, part.value))
            elif not brackets:
                name.append(part.value)
        decorators.append(ParsedDecorator(''.join(name), args))
    return decorators


def extract_functions(node: Union[Module, Class]) -> List[ParsedFunction]:
    """Extract parsed functions from node."""
    functions = []
    for function_node in node.iter_funcdefs():
        f_annotation = function_node.annotation
        if f_annotation:
            f_annotation = f_annotation.get_code()
        else:
            f_annotation = ''
        f_return = [norm_stmt(i, False)
                    for i in function_node.iter_return_stmts()]
        f_yield = [norm_stmt(i, False)
                   for i in function_node.iter_yield_exprs()]
        f_raise = [norm_stmt(i, False)
                   for i in function_node.iter_raise_stmts()]
        functions.append(ParsedFunction(
            name=ParsedName(function_node.name.value),
            docstring=extract_doc(function_node),
            paramenters=extract_params(function_node),
            decorators=extract_decorators(function_node),
            return_annotation=ParsedName('', annotation=f_annotation),
            returns=f_return,
            yields=f_yield,
            raises=f_raise))
    return functions


def extract_classes(node: Module) -> List[ParsedClass]:
    """Extract parsed classes from node."""
    classes = []
    for class_node in node.iter_classdefs():
        class_arg = class_node.get_super_arglist()
        if class_arg:
            if isinstance(class_arg, Name):
                class_arg = class_arg.value
            else:
                class_arg = '.'.join([n.value for n in filter_nodes(class_arg,
                                                                    [Name])])
        classes.append(ParsedClass(name=ParsedName(class_node.name.value),
                                   docstring=extract_doc(class_node),
                                   parent_class=class_arg,
                                   decorators=extract_decorators(class_node),
                                   variables=extract_statements(class_node),
                                   methods=extract_functions(class_node)))
    return classes


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
