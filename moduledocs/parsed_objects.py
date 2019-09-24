"""Objects that can be handled by documentation builder class."""

from dataclasses import dataclass
from typing import List, Union, Any
from pathlib import Path


@dataclass
class ParsedName:
    """
    Parsed name.

    Any "variable" is name. For call `spider(9, surname='oleg')` names is
    [spider, surname]. Used for store code lines as it is it code. Solves the
    problem of post-processing imports or expressions.
    """

    value: str
    annotation: str = ''


@dataclass
class ParsedOperator:
    """
    Parsed operator.

    Used for store code lines as it is it code. Solves the problem of
    post-processing imports or expressions.
    """

    value: str


@dataclass
class ParsedKeyword:
    """
    Parsed keyword.

    Used for store code lines as it is it code. Solves the problem of
    post-processing imports or expressions.
    """

    value: str


@dataclass
class ParsedLiteral:
    """
    Parsed Literal.

    Used for difine "strings", numbers as 1 or 2.4.
    """

    value: str


@dataclass
class ParsedDocstring:
    """
    Parsed docstring from module, class or function.

    If uses style as rst or markdown will be also
    prepaired.
    """

    raw: str
    doc: str = ''

    def __post_init__(self):
        """
        Magic post processing on module data.

        Render markdown or ReST docstring.
        """
        # TODO process markdown or rst in docstring
        self.doc = self.raw


@dataclass
class ParsedImport:
    """Parsed import from module."""

    from_module: str
    import_data: List[Union[ParsedName, ParsedKeyword, ParsedOperator]]

    def code(self) -> str:
        """Return code recreation for parsed import."""
        import_code = []
        stick = False
        for parsed_data in self.import_data:
            parsed_value = parsed_data.value
            if isinstance(parsed_data, ParsedKeyword):
                import_code.append(parsed_value)
            elif isinstance(parsed_data, ParsedOperator):
                stick = True
                if parsed_value == ',':
                    parsed_value += ' '
                import_code[-1] += parsed_value
            elif isinstance(parsed_data, ParsedName):
                if stick:
                    stick = False
                    import_code[-1] += parsed_value
                else:
                    import_code.append(parsed_value)
        if 'from.' in import_code[0]:
            import_code[0] = import_code[0].replace('from.', 'from .', 1)
        return ' '.join(import_code)


@dataclass
class ParsedStatement:
    """Parsed statement from class or module."""

    name: List[ParsedName]
    value: List[Any]

    def code(self):
        """Return code recreation for parsed statement."""
        full_name = ''.join([n.value for n in self.name])
        full_value = ''.join([n.value for n in self.value])
        return '{} = {}'.format(full_name, full_value)


@dataclass
class ParsedParameter:
    """Parsed parameter from class, method or funcion definition."""

    name: ParsedName
    default: List[Any]


@dataclass
class ParsedDecorator:
    """Parsed decorator from class, method of function."""

    name: ParsedName
    factory_parameters: List[Any]  # TODO parsed arguments


@dataclass
class ParsedFunction:
    """Parsed function or method."""

    name: ParsedName
    docstring: ParsedDocstring
    paramenters: List[Any]
    decorators: List[ParsedDecorator]
    return_annotation: ParsedName
    returns: List[Any]
    yields: List[Any]
    raises: List[Any]

    def code_param(self) -> str:
        """Return code recreation for parsed function parameters."""
        code = ''.join([p.value for p in self.paramenters])
        code = code.replace(',', ', ')
        code = code.replace(':', ': ')
        code = '({})'.format(code)
        return code
    # TODO Parse or not nested class or func


@dataclass
class ParsedClass:
    """Parsed class."""

    name: ParsedName
    docstring: ParsedDocstring
    parent_class: List[Any]  # TODO parsed arguments
    decorators: List[ParsedDecorator]
    variables: List[ParsedStatement]
    methods: List[ParsedFunction]
    # TODO Parse or not nested class


@dataclass
class ParsedModule:
    """Parsed module."""

    name: ParsedName
    path: Path
    docstring: ParsedDocstring
    imports: List[ParsedImport]
    statements: List[ParsedStatement]
    classes: List[ParsedClass]
    functions: List[ParsedFunction]
