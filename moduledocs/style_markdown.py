"""Markdown documentation builder class."""

from typing import List
from .style_base import BaseBuilder
from .parsed_objects import ParsedModule


class MarkdownBuilder(BaseBuilder):
    """Markdown builder for parsed."""

    def setting(self, **kwags):
        """Builder settings for parsed module."""
        self.e = '.md'

    def index(self, index_items: List[str]) -> str:
        """Render index as text."""
        return '\n'.join(['[{0}]({0})'.format(i) for i in index_items])

    def feed(self, module: ParsedModule) -> str:
        """Convert ParsedModule to a string and stores it in self.text."""
        return module.name.value
