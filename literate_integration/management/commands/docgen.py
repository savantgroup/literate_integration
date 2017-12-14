from django.core.management.base import BaseCommand

from ...driver import generate_documentation


class Command(BaseCommand):

    help = (
        'Generate documentation for literate tests.'
    )

    def add_arguments(self, parser):
        parser.add_argument('files', nargs='+', type=str)

    def handle(self, *args, **options):
        generate_documentation(options['files'])
