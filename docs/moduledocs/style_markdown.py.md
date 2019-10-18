# Style markdown



  + [Style markdown](#style-markdown)

    + [Require](#require)

    + [Docstring](#docstring)

    + [Configuration](#configuration)

      + [Imports](#imports)

    + [Classes](#classes)

      + [MarkdownBuilder](#markdownbuilder)

        + [\_escape](#_escape)

        + [\_line](#_line)

        + [\_append](#_append)

        + [setting](#setting)

        + [index](#index)

        + [\_local\_link](#_local_link)

        + [\_feed\_func](#_feed_func)

        + [feed](#feed)



## Require

_typing, copy, string, style\_base, parsed\_objects_ 

## Docstring

Markdown documentation builder class.

## Configuration

### Imports

`from typing import List, Union, Tuple`

`from copy import copy`

`from string import ascii_lowercase`

`from .style_base import BaseBuilder`

`from .parsed_objects import ParsedModule, ParsedClass`

## Classes

### MarkdownBuilder

Markdown builder for parsed.



#### _escape

__(body: str)__ -> __str__ 

#### _line

__(self, body: str, style: str, escape: bool = True)__ -> __str__ 

#### _append

__(self, body: str, style: str)__ -> __str__ 

#### setting

__(self, include\_index: bool = True, **kwags)__ 

Builder settings for parsed module.

#### index

__(self, index\_items: List[str])__ -> __str__ 

Render index as string.

#### _local_link

__(self, name: str)__ -> __str__ 

#### _feed_func

__(self, functions: List[Union[ParsedModule, ParsedClass]], name\_style: str)__ -> __str__ 

#### feed

__(self, module: ParsedModule)__ -> __str__ 

Convert ParsedModule to a string and return it.

