# Style base

## Require

1. typing

1. pathlib

1. abc

1. parsed\_objects

1. warnings

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

#### \_\_init\_\_ __(self)__

_return_ {0}

Create builder for parsed module.

------

#### setting __(self, **kwargs)__

_return_ {0}

Builder settings for parsed module.

------

#### index __(self, index\_items: List[str])__

_return_ str

Render index as text.

------

#### build __(self, modules: List[ParsedModule])__

_return_ {0}

Build for parsed module.

------

#### feed __(self, module: ParsedModule)__

_return_ {0}

Convert ParsedModule to a string and stores it in self.text.

------

#### save __(self, docs\_path: Path)__

_return_ {0}

Save file at location specified on init.

------

------

