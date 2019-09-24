"""Markdown documentation builder class."""

from typing import List, Union
from .style_base import BaseBuilder
from .parsed_objects import ParsedModule, ParsedClass


class MarkdownBuilder(BaseBuilder):
    """Markdown builder for parsed."""

    @staticmethod
    def _escape(text: str) -> str:
        return text.replace('_', '\\_')

    def _line(self, text: str, style: str, escape: bool = True) -> str:
        if not text:
            text = style
        elif escape:
            text = style.format(self._escape(text))
        else:
            text = style.format(text)
        return text + self.paragraph_indentation

    def _append(self, text: str, style: str) -> str:
        return style.format(self._escape(text)) + ' '

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
            index_text += self._line(index_item + self.e, self.link)
        return index_text

    def _feed_func(self,
                   functions: List[Union[ParsedModule, ParsedClass]],
                   name_style: str) -> str:
        text = ''
        for function in functions:
            function_name = function.name.value
            text += self._append(function_name, name_style)
            text += self._line(function.code_param(), self.bold)
            text += self._append('return', self.italic)
            text += self._line(
                function.return_annotation.annotation.strip(),
                self.plain
            )
            text += self._line(function.docstring.doc, self.plain)
            text += self._line('', self.horizontal_line)
        return text

    def feed(self, module: ParsedModule) -> str:
        """Convert ParsedModule to a string and stores it in self.text."""
        nice_name = module.name.value
        nice_name = nice_name.replace('_', ' ').replace('  ', '__')  # FIXME
        nice_name = nice_name.capitalize()
        text = self._line(nice_name, self.header1)
        text += self._line('Require', self.header2)
        used: List[str] = []
        for module_import in module.imports:
            require = module_import.from_module
            if require not in used:
                used.append(require)
                text += self._line(require, self.number_element)
        if module.docstring.doc:
            text += self._line('Docstring', self.header2)
            text += self._line(module.docstring.doc, self.plain)
        text += self._line('Configuration', self.header2)
        if module.imports:
            text += self._line('Imports', self.header3)
            for module_import in module.imports:
                text += self._line(module_import.code(), self.code, False)
        if module.statements:
            text += self._line('Statements', self.header3)
            for module_statement in module.statements:
                text += self._line(module_statement.code(), self.code, False)
        if module.classes:
            text += self._line('Classes', self.header2)
            for module_class in module.classes:
                module_class_name = module_class.name.value
                text += self._line(module_class_name, self.header3)
                text += self._line(module_class.docstring.doc, self.plain)
                text += self._feed_func(module_class.methods, self.header4)
                text += self._line('', self.horizontal_line)
        if module.functions:
            text += self._line('Functions', self.header2)
            text += self._feed_func(module.functions, self.header3)
        return text
