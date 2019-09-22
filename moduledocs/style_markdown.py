"""Markdown documentation builder class."""

from .style_base import BaseBuilder
from .parsed_objects import ParsedModule


class MarkdownBuilder(BaseBuilder):
    """Markdown builder for parsed."""

    def setting(self, **kwags):
        """Builder settings for parsed module."""
        self.e = '.md'

    def feed(self, module: ParsedModule):
        """Convert ParsedModule to a string and stores it in self.text."""
        self.text = ''
