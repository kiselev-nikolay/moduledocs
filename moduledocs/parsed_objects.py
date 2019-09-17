"""Objects that can be handled by documentation builder class."""

from dataclasses import dataclass
from typing import List
from pathlib import Path


@dataclass
class ParsedDocstring:
    """
    Parsed docstring from module, class or function.

    If uses style as rst or markdown will be also
    prepaired.
    """

    raw: str

    def __post_init__(self):
        """Render markdown or ReST  docstring."""
        # TODO process markdown or rst in docstring
        self.doc = self.raw


@dataclass
class ParsedImport:
    """Parsed import from module."""

    import_from: str
    import_import: List[str]
    import_as: List[str]


@dataclass
class ParsedStatement:
    """Parsed statement from class or module."""

    name: str
    value: str
    annotation: str


@dataclass
class ParsedParameter:
    """Parsed parameter from class, method or funcion definition."""

    name: str
    annotation: str
    default: str


@dataclass
class ParsedArgument:
    """Parsed argument from call callable."""

    value: str
    name: str


@dataclass
class ParsedDecorator:
    """Parsed decorator from class, method of function."""

    name: str
    factory_parameters: List[ParsedArgument]


@dataclass
class ParsedFunction:
    """Parsed function or method."""

    name: str
    docstring: ParsedDocstring
    paramenters: List[ParsedParameter]
    decorators: List[ParsedDecorator]
    returns: str


@dataclass
class ParsedClass:
    """Parsed class."""

    name: str
    docstring: ParsedDocstring
    parent_class: List[ParsedArgument]
    decorators: List[ParsedDecorator]
    variables: List[ParsedStatement]
    methods: List[ParsedFunction]


@dataclass
class ParsedModule:
    """Parsed module."""

    name: str
    path: Path
    docstring: ParsedDocstring
    imports: List[ParsedImport]
    statements: List[ParsedStatement]
    classes: List[ParsedClass]
    functions: List[ParsedFunction]
