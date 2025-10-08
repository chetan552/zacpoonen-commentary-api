from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Commentary(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='commentaries')
    chapter = models.IntegerField()
    verse = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return f"{self.book.name} {self.chapter}:{self.verse}"

    class Meta:
        ordering = ['book', 'chapter', 'verse']
