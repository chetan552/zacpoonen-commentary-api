from django.core.management.base import BaseCommand
import json
from ...models import Commentary

class Command(BaseCommand):
    help = 'Import commentaries from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file')

    def handle(self, *args, **options):
        with open(options['json_file'], 'r') as f:
            data = json.load(f)
        for item in data:
            Commentary.objects.create(
                book=item['book'],
                chapter=item['chapter'],
                verse=item['verse'],
                text=item['text']
            )
        self.stdout.write(self.style.SUCCESS('Successfully imported commentaries'))
