# Style base



  + [Style base](#style-base)

    + [Require](#require)

    + [Docstring](#docstring)

    + [Configuration](#configuration)

      + [Imports](#imports)

    + [Classes](#classes)

      + [BaseBuilder](#basebuilder)

        + [\_\_init\_\_](#__init__)

        + [setting](#setting)

        + [index](#index)

        + [build](#build)

        + [feed](#feed)

        + [save](#save)



## Require

_typing, pathlib, abc, parsed\_objects, warnings_ 

## Docstring

Base documentation builder class.

## Configuration

### Imports

`from typing import List, Dict, Tuple`

`from pathlib import Path`

`from abc import ABC, abstractmethod`

`from .parsed_objects import ParsedModule`

`import warnings`

## Classes

### BaseBuilder

Abstract class for converting ParsedModule to a special style string.



#### __init__

__(self)__ 

Create builder for parsed module.

#### setting

__(self, **kwargs)__ 

Builder settings for parsed module.

#### index

__(self, index\_items: List[str])__ -> __str__ 

Render index as text.

#### build

__(self, modules: List[ParsedModule])__ 

Build for parsed module.

#### feed

__(self, module: ParsedModule)__ 

Convert ParsedModule to a string and stores it in self.text.

#### save

__(self, docs\_path: Path)__ 

Save file at location specified on init.

