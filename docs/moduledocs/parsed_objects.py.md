# Parsed objects



  + [Parsed objects](#parsed-objects)

    + [Require](#require)

    + [Docstring](#docstring)

    + [Configuration](#configuration)

      + [Imports](#imports)

    + [Classes](#classes)

      + [ParsedName](#parsedname)

      + [ParsedOperator](#parsedoperator)

      + [ParsedKeyword](#parsedkeyword)

      + [ParsedLiteral](#parsedliteral)

      + [ParsedDocstring](#parseddocstring)

        + [\_\_post\_init\_\_](#__post_init__)

      + [ParsedImport](#parsedimport)

        + [code](#code)

      + [ParsedStatement](#parsedstatement)

        + [code](#code)

      + [ParsedParameter](#parsedparameter)

      + [ParsedDecorator](#parseddecorator)

      + [ParsedFunction](#parsedfunction)

        + [code\_param](#code_param)

      + [ParsedClass](#parsedclass)

      + [ParsedModule](#parsedmodule)



## Require

_dataclasses, typing, pathlib_ 

## Docstring

Objects that can be handled by documentation builder class.

## Configuration

### Imports

`from dataclasses import dataclass`

`from typing import List, Union, Any`

`from pathlib import Path`

## Classes

### ParsedName

Parsed name.

    Any "variable" is name. For call `spider(9, surname='oleg')` names is
    [spider, surname]. Used for store code lines as it is it code. Solves the
    problem of post-processing imports or expressions.

### ParsedOperator

Parsed operator.

    Used for store code lines as it is it code. Solves the problem of
    post-processing imports or expressions.

### ParsedKeyword

Parsed keyword.

    Used for store code lines as it is it code. Solves the problem of
    post-processing imports or expressions.

### ParsedLiteral

Parsed Literal.

    Used for difine "strings", numbers as 1 or 2.4.

### ParsedDocstring

Parsed docstring from module, class or function.

    If uses style as rst or markdown will be also
    prepaired.



#### __post_init__

__(self)__ 

Magic post processing on module data.

        Render markdown or ReST docstring.

### ParsedImport

Parsed import from module.



#### code

__(self)__ -> __str__ 

Return code recreation for parsed import.

### ParsedStatement

Parsed statement from class or module.



#### code

__(self)__ 

Return code recreation for parsed statement.

### ParsedParameter

Parsed parameter from class, method or funcion definition.

### ParsedDecorator

Parsed decorator from class, method of function.

### ParsedFunction

Parsed function or method.



#### code_param

__(self)__ -> __str__ 

Return code recreation for parsed function parameters.

### ParsedClass

Parsed class.

### ParsedModule

Parsed module.

