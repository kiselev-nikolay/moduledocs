"""Base documentation builder class."""

from typing import List
from pathlib import Path
from abc import ABC, abstractmethod
from .parsed_objects import ParsedModule


class BaseBuilder(ABC):
    """Abstract class for converting ParsedModule to a special style string."""

    def __init__(self):
        """Create builder for parsed module."""

    @abstractmethod
    def setting(self, **kwargs):
        """Builder settings for parsed module."""
        self.e = '.txt'

    def build(self, modules: List[ParsedModule]):
        """Build for parsed module."""
        for module in modules:
            self.feed(module)

    @abstractmethod
    def feed(self, module: ParsedModule):
        """Convert ParsedModule to a string and stores it in self.text."""
        self.text = ''

    def save(self, path: Path):
        """Save file at location specified on init."""
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        save_path = path.joinpath('test{}'.format(self.e)).absolute()
        with open(save_path, 'w') as file:
            file.write(self.text)
