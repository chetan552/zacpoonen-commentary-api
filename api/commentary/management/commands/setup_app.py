from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Setup the app: migrate, populate books and create superuser'

    def handle(self, *args, **options):
        # Run migrate
        self.stdout.write('Running migrations...')
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS('Migrations completed.'))

        # Run populate_books
        self.stdout.write('Populating books...')
        call_command('populate_books')
        self.stdout.write(self.style.SUCCESS('Books populated.'))

        self.stdout.write(self.style.SUCCESS('App setup complete.'))
