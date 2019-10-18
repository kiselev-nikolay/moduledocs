"""Markdown documentation builder class."""

from typing import List, Union, Tuple
from copy import copy
from string import ascii_lowercase
from .style_base import BaseBuilder
from .parsed_objects import ParsedModule, ParsedClass


class MarkdownBuilder(BaseBuilder):
    """Markdown builder for parsed."""

    @staticmethod
    def _escape(body: str) -> str:
        return body.replace('_', '\\_')

    def _line(self, body: str, style: str, escape: bool = True) -> str:
        if style in self.headings.values():
            level = self.headings_levels[style]
            self.content_table.append((body, level))
        if not body:
            body = style
        elif escape:
            body = style.format(self._escape(body))
        else:
            body = style.format(body)
        return body + self.paragraph_indentation

    def _append(self, body: str, style: str) -> str:
        return style.format(self._escape(body)) + ' '

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
        self.headings = {
            1: '# {0}',
            2: '## {0}',
            3: '### {0}',
            4: '#### {0}'
        }
        self.headings_levels = dict(zip(self.headings.values(),
                                        self.headings.keys()))
        self.list_element = '+ {0}'
        self.number_element = '1. {0}'
        self.link = '[{0}]({0})'
        self.code = '`{0}`'
        self.code_multiline = '```{0}```'
        self.horizontal_line = '------'

    def index(self, index_items: List[str]) -> str:
        """Render index as string."""
        index_body = ''
        position = ''
        for index_item in sorted(index_items):
            *path, item = index_item.split('/')
            link = ''
            if path[-1] != position:
                index_body += '+ /' + self._line('/'.join(path), self.plain)
            link += '  + [{0}]({1})'.format(item, index_item + self.e)
            index_body += self._line(link, self.plain)
            position = path[-1]
        return index_body

    def _local_link(self, name: str) -> str:
        link = copy(name)
        real_link = '#'
        for letter in link.lower():
            if letter == '_' or letter in ascii_lowercase:
                real_link += letter
            elif real_link[-1] != '-':
                real_link += '-'
        return '[{0}]({1})'.format(self._escape(name), real_link)

    def _feed_func(self,
                   functions: List[Union[ParsedModule, ParsedClass]],
                   name_style: str) -> str:
        body = self.paragraph_indentation
        for function in functions:
            function_name = function.name.value
            function_body = self._line(function_name, name_style, False)
            function_body += self._append(function.code_param(), self.bold)
            if function.return_annotation.annotation:
                function_body += self._append('->', self.plain)
                function_body += self._append(
                    function.return_annotation.annotation.strip(),
                    self.bold
                )
            body += self._line(function_body, self.plain, False)
            if function.docstring.doc:
                body += self._line(function.docstring.doc, self.plain)
            # body += self._line('', self.horizontal_line)
        return body

    def feed(self, module: ParsedModule) -> str:
        """Convert ParsedModule to a string and return it."""
        nice_name = module.name.value
        nice_name = nice_name.replace('_', ' ').replace('  ', '__')  # FIXME
        nice_name = nice_name.capitalize()
        title = self._line(nice_name, self.headings[1])
        body = self.paragraph_indentation
        used: List[str] = []
        for module_import in module.imports:
            require = module_import.from_module
            if require not in used:
                used.append(require)
        if used:
            body += self._line('Require', self.headings[2])
            body += self._append(', '.join(used), self.italic)
            body += self.paragraph_indentation
        if module.docstring.doc:
            body += self._line('Docstring', self.headings[2])
            body += self._line(module.docstring.doc, self.plain)
        body += self._line('Configuration', self.headings[2])
        if module.imports:
            body += self._line('Imports', self.headings[3])
            for module_import in module.imports:
                body += self._line(module_import.code(), self.code, False)
        if module.statements:
            body += self._line('Statements', self.headings[3])
            for module_statement in module.statements:
                body += self._line(module_statement.code(), self.code, False)
        if module.classes:
            body += self._line('Classes', self.headings[2])
            for module_class in module.classes:
                module_class_name = module_class.name.value
                body += self._line(module_class_name, self.headings[3])
                if module_class.docstring.doc:
                    body += self._line(module_class.docstring.doc, self.plain)
                if module_class.methods:
                    body += self._feed_func(module_class.methods,
                                            self.headings[4])
                # body += self._line('', self.horizontal_line)
        if module.functions:
            body += self._line('Functions', self.headings[2])
            body += self._feed_func(module.functions, self.headings[3])
        content_links = self.paragraph_indentation
        for content in self.content_table:
            link_body = '  ' * content[1] + '+ '
            link_body += self._local_link(content[0])
            content_links += self._line(link_body, self.plain, False)
        self.content_table: List[Tuple[str, int]] = []
        return title + content_links + body
