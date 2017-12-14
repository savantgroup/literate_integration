import argparse
import inspect
from importlib import import_module

from .document import generate_rest_documentation
from .models import LiterateRESTTest

parser = argparse.ArgumentParser(
    description='Generate documentation from literate integration tests.'
)

parser.add_argument(
    'files',
    nargs='+',
    help=(
        'The files containing the tests to generate documentation from.'
    )
)


def _get_documentations(module):
    """Yield documentation for each literate test in the module."""
    klasses = inspect.getmembers(module, inspect.isclass)
    for name, klass in klasses:
        if inspect.isabstract(klass):
            continue
        if issubclass(klass, LiterateRESTTest):
            yield generate_rest_documentation(klass)


def main():
    """Generate documentation.

    Called as a script when setup.py is installed.
    Prints to stdout.

    """
    args = parser.parse_args()
    files = [
        x.replace('/', '.')[:-3]
        for x in args.files if x.endswith('.py')
    ]
    documentation = []
    for filename in files:
        module = import_module(filename)
        documentation.extend(_get_documentations(module))

    print('\n\n'.join(documentation))
