# Parse



  + [Parse](#parse)

    + [Require](#require)

    + [Docstring](#docstring)

    + [Configuration](#configuration)

      + [Imports](#imports)

    + [Functions](#functions)

      + [extract\_doc](#extract_doc)

      + [filter\_nodes](#filter_nodes)

      + [shallow\_filter\_nodes](#shallow_filter_nodes)

      + [same\_parsed](#same_parsed)

      + [norm\_stmt](#norm_stmt)

      + [extract\_imports](#extract_imports)

      + [extract\_statements](#extract_statements)

      + [extract\_params](#extract_params)

      + [extract\_decorators](#extract_decorators)

      + [extract\_functions](#extract_functions)

      + [extract\_classes](#extract_classes)

      + [extract](#extract)

      + [find\_python](#find_python)

      + [find\_and\_extract](#find_and_extract)



## Require

_pathlib, copy, typing, textwrap, parso, parsed\_objects_ 

## Docstring

Parser based on parso. Returns objects compatible with BaseBuilder class.

## Configuration

### Imports

`from pathlib import Path`

`from copy import copy`

`from typing import List, Iterator, Union, Any`

`from textwrap import dedent`

`import parso`

`from parso.python.tree import PythonBaseNode, PythonNode, Module, Class, Function, Keyword, Name, Operator, ExprStmt, Literal`

`from .parsed_objects import ParsedClass, ParsedDecorator, ParsedDocstring, ParsedFunction, ParsedImport, ParsedModule, ParsedParameter, ParsedStatement, ParsedKeyword, ParsedOperator, ParsedName, ParsedLiteral`

## Functions



### extract_doc

__(node: Union[Module, Class, Function])__ -> __ParsedDocstring__ 

Extract parsed docstring from module, class or function.

### filter_nodes

__(node: PythonBaseNode, targets: List[Any])__ -> __Iterator[PythonBaseNode]__ 

Recursive find every node with target type.

### shallow_filter_nodes

__(node: PythonBaseNode, targets: List[Any], depth: int = 2, examine: bool = True)__ -> __Iterator[PythonBaseNode]__ 

Recursive find every node with target type with depth limit.

### same_parsed

__(node: Union[Name, Keyword, Operator, Literal], *values: List[str])__ -> __Union[ParsedName, ParsedKeyword, ParsedOperator, ParsedLiteral]__ 

Get same object from parsed object.

### norm_stmt

__(node: PythonBaseNode, equation: bool = True)__ -> __List[Any]__ 

Statement normalization function.

### extract_imports

__(node: Module)__ -> __List[ParsedImport]__ 

Extract parsed imports from module.

### extract_statements

__(node: PythonBaseNode)__ -> __List[ParsedStatement]__ 

Extract parsed statements from module.

    Examples:
    RED = (255, 0, 0)
    app = web.Application(port='69')
    nice = True

### extract_params

__(node: Union[Class, Function])__ -> __List[ParsedParameter]__ 

Extract parsed parameters from node.

    If this is class method
    For:
        def g(a: int, b: int = 2):
            ...
    Extracted parameters:
        a: int, b: int = 2

### extract_decorators

__(node: Union[Class, Function])__ -> __List[ParsedDecorator]__ 

Extract parsed decorators for function, method or class.

### extract_functions

__(node: Union[Module, Class])__ -> __List[ParsedFunction]__ 

Extract parsed functions from node.

### extract_classes

__(node: Module)__ -> __List[ParsedClass]__ 

Extract parsed classes from node.

### extract

__(file\_name: Path)__ -> __ParsedModule__ 

Extract parsed module from file by path.

### find_python

__(base: Path)__ -> __Iterator[Path]__ 

Find python files in directory and subdirectories.

### find_and_extract

__(base: Path)__ -> __Iterator[ParsedModule]__ 

Recursive extract parsed module in directory.

    Extract parsed module for every python files in directory and
    subdirectories.

