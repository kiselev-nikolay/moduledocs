"""Base documentation builder class."""

from typing import List
from pathlib import Path
from abc import ABC, abstractmethod
from .parsed_objects import ParsedModule


class BaseBuilder(ABC):
    """Abstract class for converting ParsedModule to a special style string."""

    path: Path
    module: ParsedModule
    text: str

    def __init__(self):
        """Create builder for parsed module."""

    @abstractmethod
    def setting(self, **kwargs):
        """Builder settings for parsed module."""

    def build(self, modules: List[ParsedModule]):
        """Build for parsed module."""
        for module in modules:
            self.feed(module)

    @abstractmethod
    def feed(self, module: ParsedModule):
        """Convert ParsedModule to a string and stores it in self.text."""
        self.text = ''

    def save(self):
        """Save file at location specified on init."""
        with open(self.path.absolute(), 'w') as file:
            file.write(self.text)
