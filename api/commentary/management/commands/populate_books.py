from django.core.management.base import BaseCommand
from api.commentary.models import Book

class Command(BaseCommand):
    help = 'Populate the Book model with all books of the Bible'

    def handle(self, *args, **options):
        # Books of the Bible with their common abbreviations
        bible_books = [
            ('Genesis', 'Gen'),
            ('Exodus', 'Exo'),
            ('Leviticus', 'Lev'),
            ('Numbers', 'Num'),
            ('Deuteronomy', 'Deu'),
            ('Joshua', 'Jos'),
            ('Judges', 'Jdg'),
            ('Ruth', 'Rut'),
            ('1 Samuel', '1Sa'),
            ('2 Samuel', '2Sa'),
            ('1 Kings', '1Ki'),
            ('2 Kings', '2Ki'),
            ('1 Chronicles', '1Ch'),
            ('2 Chronicles', '2Ch'),
            ('Ezra', 'Ezr'),
            ('Nehemiah', 'Neh'),
            ('Esther', 'Est'),
            ('Job', 'Job'),
            ('Psalms', 'Psa'),
            ('Proverbs', 'Pro'),
            ('Ecclesiastes', 'Ecc'),
            ('Song Of Solomon', 'SS'),
            ('Isaiah', 'Isa'),
            ('Jeremiah', 'Jer'),
            ('Lamentations', 'Lam'),
            ('Ezekiel', 'Eze'),
            ('Daniel', 'Dan'),
            ('Hosea', 'Hos'),
            ('Joel', 'Joe'),
            ('Amos', 'Amo'),
            ('Obadiah', 'Oba'),
            ('Jonah', 'Jon'),
            ('Micah', 'Mic'),
            ('Nahum', 'Nah'),
            ('Habakkuk', 'Hab'),
            ('Zephaniah', 'Zep'),
            ('Haggai', 'Hag'),
            ('Zechariah', 'Zec'),
            ('Malachi', 'Mal'),
            ('Matthew', 'Mat'),
            ('Mark', 'Mar'),
            ('Luke', 'Luk'),
            ('John', 'Joh'),
            ('Acts', 'Act'),
            ('Romans', 'Rom'),
            ('1 Corinthians', '1Co'),
            ('2 Corinthians', '2Co'),
            ('Galatians', 'Gal'),
            ('Ephesians', 'Eph'),
            ('Philippians', 'Phi'),
            ('Colossians', 'Col'),
            ('1 Thessalonians', '1Th'),
            ('2 Thessalonians', '2Th'),
            ('1 Timothy', '1Ti'),
            ('2 Timothy', '2Ti'),
            ('Titus', 'Tit'),
            ('Philemon', 'Phm'),
            ('Hebrews', 'Heb'),
            ('James', 'Jam'),
            ('1 Peter', '1Pe'),
            ('2 Peter', '2Pe'),
            ('1 John', '1Jo'),
            ('2 John', '2Jo'),
            ('3 John', '3Jo'),
            ('Jude', 'Jud'),
            ('Revelation', 'Rev'),
        ]

        created_count = 0
        for name, abbreviation in bible_books:
            book, created = Book.objects.get_or_create(
                name=name,
                defaults={'abbreviation': abbreviation}
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created book: {name} ({abbreviation})')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully populated {created_count} books of the Bible')
        )
