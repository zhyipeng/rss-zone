import importlib
from pathlib import Path

from core.source import Source


def get_sources() -> dict[str, type[Source]]:
    for fp in Path(__file__).parent.iterdir():
        if fp.name.endswith('.py') and fp.name != '__init__.py':
            name = fp.name.removesuffix('.py')
            importlib.import_module(f'.{name}', package=__package__)
    return {s.__name__.lower(): s for s in Source.__subclasses__()}
