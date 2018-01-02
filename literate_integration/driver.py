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


def get_documentations(module):
    """Yield documentation for each literate test in the module.

    Args:
        module: A module containing literate tests.

    Yields:
        The documentation for each literate test in the module.

    """
    klasses = inspect.getmembers(module, inspect.isclass)
    for name, klass in klasses:
        if inspect.isabstract(klass):
            continue
        if issubclass(klass, LiterateRESTTest):
            yield generate_rest_documentation(klass)


def generate_documentation(files):
    """Generate documentation.

    Prints documentation to standard out.

    Args:
        files: A list of filenames.

    """
    new_files = [
        x.replace('/', '.')[:-3]
        for x in files if x.endswith('.py')
    ]
    documentation = []
    for filename in new_files:
        module = import_module(filename)
        documentation.extend(get_documentations(module))

    print('\n\n'.join(documentation))


def main():
    """Generate documentation.

    Called as a script when setup.py is installed.
    Prints to stdout.

    """
    args = parser.parse_args()
    generate_documentation(args.files)
