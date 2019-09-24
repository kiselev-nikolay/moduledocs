# Style markdown

## Require

1. typing

1. style\_base

1. parsed\_objects

## Docstring

Markdown documentation builder class.

## Configuration

### Imports

`from typing import List, Union`

`from .style_base import BaseBuilder`

`from .parsed_objects import ParsedModule, ParsedClass`

## Classes

### MarkdownBuilder

Markdown builder for parsed.

#### \_escape __(text: str)__

_return_ str

{0}

------

#### \_line __(self, text: str, style: str, escape: bool=)__

_return_ str

{0}

------

#### \_append __(self, text: str, style: str)__

_return_ str

{0}

------

#### setting __(self, include\_index: bool=, **kwags)__

_return_ {0}

Builder settings for parsed module.

------

#### index __(self, index\_items: List[str])__

_return_ str

Render index as text.

------

#### \_feed\_func __(self, functions: List[Union[ParsedModule, ParsedClass]], name\_style: str)__

_return_ str

{0}

------

#### feed __(self, module: ParsedModule)__

_return_ str

Convert ParsedModule to a string and stores it in self.text.

------

------

