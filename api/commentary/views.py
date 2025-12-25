from functools import reduce
from operator import or_, and_
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import connection
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
import json
from .models import Commentary, Book
from .serializers import CommentarySerializer, CommentarySearchSerializer

# Built-in topical keywords for simple expansion
TOPIC_MAP = {
    "grace": ["grace", "favor", "mercy", "undeserved", "gift"],
    "faith": ["faith", "trust", "believe", "belief"],
    "love": ["love", "agape", "compassion", "kindness"],
    "repentance": ["repentance", "repent", "turn", "turning"],
    "forgiveness": ["forgive", "forgiveness", "pardon", "mercy"],
}

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

class CommentarySearchView(ListAPIView):
    serializer_class = CommentarySearchSerializer

    def get_queryset(self):
        keyword_param = self.request.query_params.get('keyword', '').strip()
        match_mode = self.request.query_params.get('match', 'or').lower()
        topics_param = self.request.query_params.get('topics', '')
        expand_topics = self.request.query_params.get('expand_topics', 'true').lower() != 'false'

        terms = self._gather_terms(keyword_param, topics_param, expand_topics)
        if not terms:
            return Commentary.objects.none()

        match_all = match_mode == 'and'
        if connection.vendor == 'postgresql':
            vector = (
                SearchVector('text', weight='A') +
                SearchVector('book__name', weight='B') +
                SearchVector('book__abbreviation', weight='B') +
                SearchVector('verse', weight='C')
            )
            queries = [SearchQuery(term, search_type='plain') for term in terms]
            query = reduce((lambda a, b: a & b) if match_all else (lambda a, b: a | b), queries)
            return (
                Commentary.objects
                .annotate(search=vector)
                .filter(search=query)
                .annotate(rank=SearchRank(vector, query))
                .select_related('book')
                .order_by('-rank', 'book', 'chapter', 'verse')
            )[:20]

        # Fallback for non-Postgres: use icontains filters
        term_filters = [
            (
                Q(text__icontains=term) |
                Q(book__name__icontains=term) |
                Q(book__abbreviation__icontains=term) |
                Q(verse__icontains=term) |
                (Q(chapter=int(term)) if term.isdigit() else Q())
            )
            for term in terms
        ]
        combiner = and_ if match_all else or_
        combined_filter = reduce(combiner, term_filters)

        return (
            Commentary.objects
            .filter(combined_filter)
            .select_related('book')
            .order_by('book', 'chapter', 'verse')
        )[:20]

    def _gather_terms(self, keyword_param: str, topics_param: str, expand_topics: bool) -> list[str]:
        raw_terms = [part.strip().lower() for part in keyword_param.split() if part.strip()]
        # Expand keywords that match known topics
        expanded = []
        for term in raw_terms:
            if expand_topics and term in TOPIC_MAP:
                expanded.extend(TOPIC_MAP[term])
            expanded.append(term)

        # Add explicit topics param expansions
        topic_names = [t.strip().lower() for t in topics_param.split(',') if t.strip()]
        for topic in topic_names:
            if topic in TOPIC_MAP:
                expanded.extend(TOPIC_MAP[topic])

        # Deduplicate while preserving order
        seen = set()
        unique_terms = []
        for term in expanded:
            if term and term not in seen:
                unique_terms.append(term)
                seen.add(term)

        return unique_terms

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['terms'] = self._gather_terms(
            self.request.query_params.get('keyword', '').strip(),
            self.request.query_params.get('topics', ''),
            self.request.query_params.get('expand_topics', 'true').lower() != 'false'
        )
        return context

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
