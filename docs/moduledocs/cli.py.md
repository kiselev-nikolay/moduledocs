# Cli



  + [Cli](#cli)

    + [Require](#require)

    + [Docstring](#docstring)

    + [Configuration](#configuration)

      + [Imports](#imports)

    + [Functions](#functions)

      + [cli](#cli)

      + [main](#main)



## Require

_fire, pathlib, parse, style\_markdown_ 

## Docstring

Comand line interface apllication.

## Configuration

### Imports

`from fire import Fire`

`from pathlib import Path`

`from .parse import find_and_extract`

`from .style_markdown import MarkdownBuilder`

## Functions



### cli

__(input\_directory: str, output\_directory: str = 'docs', style: str = 'md')__ 

Moduledocs.

    Module for generating documentation for python source code files.

### main

__()__ 

Callable function for command  line interface.

