"""Comand line interface apllication."""
from fire import Fire
from pathlib import Path
from .parse import find_and_extract
from .style_markdown import MarkdownBuilder


def cli(input_directory: str, output_directory: str, style: str = 'md'):
    """
    Moduledocs.

    Module for generating documentation for python source code files.
    """
    input_directory = Path(input_directory)
    output_directory = Path(output_directory)
    parsed_modules = find_and_extract(input_directory)
    builder = MarkdownBuilder()
    builder.setting()
    builder.build(parsed_modules)
    builder.save(output_directory)


def main():
    """Callable function for command  line interface."""
    Fire(cli)
