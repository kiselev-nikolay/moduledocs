"""Base documentation builder class."""

from pathlib import Path
from abc import ABC, abstractmethod
from .parsed_objects import ParsedModule


class BaseBuilder(ABC):
    """Abstract class for converting ParsedModule to a special style string."""

    path: Path
    module: ParsedModule
    text: str

    def __init__(self, module: ParsedModule):
        """Create builder for parsed module."""
        self.module = module

    @abstractmethod
    def feed(self):
        """Convert ParsedModule to a string and stores it in self.text."""
        self.text = ''

    def save(self):
        """Save file at location specified on init."""
        with open(self.path.absolute(), 'w') as file:
            file.write(self.text)
