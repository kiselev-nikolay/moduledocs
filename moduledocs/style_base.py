"""Base documentation builder class."""

from typing import List, Dict, Tuple
from pathlib import Path
from abc import ABC, abstractmethod
from .parsed_objects import ParsedModule
import warnings


class BaseBuilder(ABC):
    """Abstract class for converting ParsedModule to a special style string."""

    def __init__(self):
        """Create builder for parsed module."""

    @abstractmethod
    def setting(self, **kwargs):
        """Builder settings for parsed module."""
        self.e = '.txt'
        self.i = True

    @abstractmethod
    def index(self, index_items: List[str]) -> str:
        """Render index as text."""
        return '\n'.join(index_items)

    def build(self, modules: List[ParsedModule]):
        """Build for parsed module."""
        if not hasattr(self, 'e') or not getattr(self, 'e'):
            warnings.warn('Using default building setting.', RuntimeWarning)
            self.setting()
        self.texts: List[Tuple[Path, str]] = []
        self.indexes: Dict[Path, List[Path]] = dict()
        for module in modules:
            module_dir = module.path.parent
            if not self.indexes.get(module_dir):
                self.indexes[module_dir] = [module.path]
            else:
                self.indexes[module_dir].append(module.path)
            module_text = self.feed(module)
            self.texts.append((module.path, module_text))
        if hasattr(self, 'i') and self.i:
            total_index: List[str] = []
            for folder, index in self.indexes.items():
                index_str_paths = [str(i) for i in index]
                self.texts.append((folder / 'index',
                                   self.index(index_str_paths)))
                total_index.extend(index_str_paths)
            self.texts.append((Path('index'), self.index(total_index)))

    @abstractmethod
    def feed(self, module: ParsedModule):
        """Convert ParsedModule to a string and stores it in self.text."""
        return module.name.value

    def save(self, docs_path: Path):
        """Save file at location specified on init."""
        for path, text in self.texts:
            path = docs_path / path
            if not path.parent.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
            save_path = '{}{}'.format(path.absolute(), self.e)
            with open(save_path, 'w') as file:
                file.write(text)
