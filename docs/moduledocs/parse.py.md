# Parse

## Require

1. pathlib

1. copy

1. typing

1. parso

1. parsed\_objects

## Docstring

Parser based on parso. Returns objects compatible with BaseBuilder class.

## Configuration

### Imports

`from pathlib import Path`

`from copy import copy`

`from typing import List, Iterator, Union, Any`

`import parso`

`from parso.python.tree import PythonBaseNode, PythonNode, Module, Class, Function, Keyword, Name, Operator, ExprStmt, Literal`

`from .parsed_objects import ParsedClass, ParsedDecorator, ParsedDocstring, ParsedFunction, ParsedImport, ParsedModule, ParsedParameter, ParsedStatement, ParsedKeyword, ParsedOperator, ParsedName, ParsedLiteral`

## Functions

### extract\_doc __(node: Union[Module, Class, Function])__

_return_ ParsedDocstring

Extract parsed docstring from module, class or function.

------

### filter\_nodes __(node: PythonBaseNode, targets: List[Any])__

_return_ Iterator[PythonBaseNode]

Recursive find every node with target type.

------

### shallow\_filter\_nodes __(node: PythonBaseNode, targets: List[Any], depth: int=2, examine: bool=)__

_return_ Iterator[PythonBaseNode]

Recursive find every node with target type with depth limit.

------

### same\_parsed __(node: Union[Name, Keyword, Operator, Literal], *values: List[str])__

_return_ Union[ParsedName, ParsedKeyword, ParsedOperator, ParsedLiteral]

Get same object from parsed object.

------

### norm\_stmt __(node: PythonBaseNode, equation: bool=)__

_return_ List[Any]

Statement normalization function.

------

### extract\_imports __(node: Module)__

_return_ List[ParsedImport]

Extract parsed imports from module.

------

### extract\_statements __(node: PythonBaseNode)__

_return_ List[ParsedStatement]

Extract parsed statements from module.

    Examples:
    RED = (255, 0, 0)
    app = web.Application(port='69')
    nice = True

------

### extract\_params __(node: Union[Class, Function])__

_return_ List[ParsedParameter]

Extract parsed parameters from node.

    If this is class method
    For:
        def g(a: int, b: int = 2):
            ...
    Extracted parameters:
        a: int, b: int = 2

------

### extract\_decorators __(node: Union[Class, Function])__

_return_ List[ParsedDecorator]

Extract parsed decorators for function, method or class.

------

### extract\_functions __(node: Union[Module, Class])__

_return_ List[ParsedFunction]

Extract parsed functions from node.

------

### extract\_classes __(node: Module)__

_return_ List[ParsedClass]

Extract parsed classes from node.

------

### extract __(file\_name: Path)__

_return_ ParsedModule

Extract parsed module from file by path.

------

### find\_python __(base: Path)__

_return_ Iterator[Path]

Find python files in directory and subdirectories.

------

### find\_and\_extract __(base: Path)__

_return_ Iterator[ParsedModule]

Recursive extract parsed module in directory.

    Extract parsed module for every python files in directory and
    subdirectories.

------

