# Generated manually for data migration

from django.db import migrations, models
import django.db.models.deletion


def create_books_and_migrate_data(apps, schema_editor):
    # Get the historical models
    Book = apps.get_model('commentary', 'Book')
    Commentary = apps.get_model('commentary', 'Commentary')

    # Create Book records for all unique book names in existing commentaries
    existing_books = Commentary.objects.values_list('book', flat=True).distinct()

    book_mapping = {}
    for book_name in existing_books:
        book, created = Book.objects.get_or_create(
            name=book_name,
            defaults={'abbreviation': book_name[:3].upper()}  # Simple abbreviation
        )
        book_mapping[book_name] = book.id  # Store the ID for later use

    # Use raw SQL to update the book field since the model field hasn't changed yet
    from django.db import connection
    with connection.cursor() as cursor:
        for book_name, book_id in book_mapping.items():
            cursor.execute(
                "UPDATE commentary_commentary SET book = %s WHERE book = %s",
                [str(book_id), book_name]
            )


def reverse_migration(apps, schema_editor):
    # This would be complex to reverse, so we'll leave it empty
    # In production, you'd want a proper reverse migration
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('commentary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('abbreviation', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.RunPython(create_books_and_migrate_data, reverse_migration),
        migrations.AlterModelOptions(
            name='commentary',
            options={'ordering': ['book', 'chapter', 'verse']},
        ),
        migrations.AlterField(
            model_name='commentary',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentaries', to='commentary.book'),
        ),
    ]
