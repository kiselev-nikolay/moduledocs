"""Markdown documentation builder class."""

from typing import List
from .style_base import BaseBuilder
from .parsed_objects import ParsedModule


class MarkdownBuilder(BaseBuilder):
    """Markdown builder for parsed."""

    @staticmethod
    def _escape(text: str) -> str:
        return text.replace('_', '\\_')

    def _format(self, text: str, style: str, escape: bool = True) -> str:
        if not text:
            text = style
        elif escape:
            text = style.format(self._escape(text))
        else:
            text = style.format(text)
        return text + self.paragraph_indentation

    def setting(self, include_index: bool = True, **kwags):
        """Builder settings for parsed module."""
        # Base
        self.e = '.md'
        self.i = include_index
        # Markdown
        self.paragraph_indentation = '\n\n'
        self.plain = '{0}'
        self.bold = '__{0}__'
        self.italic = '_{0}_'
        self.header1 = '# {0}'
        self.header2 = '## {0}'
        self.header3 = '### {0}'
        self.header4 = '#### {0}'
        self.list_element = '+ {0}'
        self.number_element = '1. {0}'
        self.link = '[{0}]({0})'
        self.code = '`{0}`'
        self.code_multiline = '```{0}```'
        self.horizontal_line = '------'

    def index(self, index_items: List[str]) -> str:
        """Render index as text."""
        index_text = ''
        for index_item in index_items:
            index_text += self._format(index_item + self.e, self.link)
        return index_text

    def feed(self, module: ParsedModule) -> str:
        """Convert ParsedModule to a string and stores it in self.text."""
        nice_name = module.name.value
        nice_name = nice_name.replace('_', ' ').replace('  ', '__')  # FIXME
        nice_name = nice_name.capitalize()
        text = self._format(nice_name, self.header1)
        text += self._format('Require', self.header2)
        used: List[str] = []
        for module_import in module.imports:
            require = module_import.from_module
            if require not in used:
                used.append(require)
                text += self._format(require, self.number_element)
        text += self._format('Docstring', self.header2)
        text += self._format(module.docstring.doc, self.plain)
        text += self._format('Configuration', self.header2)
        for module_import in module.imports:
            text += self._format(module_import.code(), self.code, False)
        for module_statement in module.statements:
            text += self._format(module_statement.code(), self.code, False)
        return text
