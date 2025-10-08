from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
import json
from .models import Commentary, Book
from .serializers import CommentarySerializer

class CommentaryListView(ListAPIView):
    serializer_class = CommentarySerializer

    def get_queryset(self):
        queryset = Commentary.objects.all()
        book_param = self.kwargs.get('book')
        chapter = self.kwargs.get('chapter')

        if book_param:
            # Try to find book by name or abbreviation
            book = Book.objects.filter(
                Q(name__iexact=book_param) |
                Q(abbreviation__iexact=book_param)
            ).first()
            if book:
                queryset = queryset.filter(book=book)
            else:
                # If no book found, return empty queryset
                return Commentary.objects.none()

        if chapter:
            queryset = queryset.filter(chapter=chapter)

        return queryset

class ImportCommentariesView(APIView):
    def post(self, request):
        data = request.data
        imported_count = 0
        for item in data:
            # Handle book field conversion from string to Book instance
            book_data = item.get('book')
            if isinstance(book_data, str):
                # Find book by name or abbreviation
                book = Book.objects.filter(
                    Q(name__iexact=book_data) |
                    Q(abbreviation__iexact=book_data)
                ).first()
                if book:
                    item['book'] = book
                else:
                    # Try to create the book if it doesn't exist
                    book = Book.objects.create(
                        name=book_data,
                        abbreviation=book_data[:3].upper()
                    )
                    item['book'] = book

            Commentary.objects.create(**item)
            imported_count += 1

        return Response({
            "message": f"Successfully imported {imported_count} commentaries",
            "count": imported_count
        }, status=status.HTTP_201_CREATED)

def import_commentaries_view(request):
    if request.method == 'POST':
        json_file = request.FILES.get('json_file')
        if json_file:
            try:
                data = json.loads(json_file.read().decode('utf-8'))
                imported_count = 0
                for item in data:
                    # Handle book field conversion from string to Book instance
                    book_data = item.get('book')
                    if isinstance(book_data, str):
                        # Find book by name or abbreviation
                        book = Book.objects.filter(
                            Q(name__iexact=book_data) |
                            Q(abbreviation__iexact=book_data)
                        ).first()
                        if book:
                            item['book'] = book
                        else:
                            # Try to create the book if it doesn't exist
                            book = Book.objects.create(
                                name=book_data,
                                abbreviation=book_data[:3].upper()
                            )
                            item['book'] = book

                    Commentary.objects.create(**item)
                    imported_count += 1

                messages.success(request, f'Successfully imported {imported_count} commentaries.')
            except Exception as e:
                messages.error(request, f'Error importing: {e}')
        return HttpResponseRedirect(reverse('admin:commentary_commentary_changelist'))
    return render(request, 'admin/import_commentaries.html')
