from django.contrib import admin
from .models import Book, Commentary

class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')
    search_fields = ('name', 'abbreviation')

class CommentaryAdmin(admin.ModelAdmin):
    list_display = ('book', 'chapter', 'verse', 'text')
    list_filter = ('book',)
    search_fields = ('book__name', 'text')
    change_list_template = 'admin/commentary/change_list.html'

admin.site.register(Book, BookAdmin)
admin.site.register(Commentary, CommentaryAdmin)
