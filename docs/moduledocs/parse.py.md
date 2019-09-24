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

`from pathlib import Path`

`from copy import copy`

`from typing import List, Iterator, Union, Any`

`import parso`

`from parso.python.tree import PythonBaseNode, PythonNode, Module, Class, Function, Keyword, Name, Operator, ExprStmt, Literal`

`from .parsed_objects import ParsedClass, ParsedDecorator, ParsedDocstring, ParsedFunction, ParsedImport, ParsedModule, ParsedParameter, ParsedStatement, ParsedKeyword, ParsedOperator, ParsedName, ParsedLiteral`

