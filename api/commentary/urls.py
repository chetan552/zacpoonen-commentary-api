from django.urls import path
from .views import CommentaryListView, CommentarySearchView, ImportCommentariesView

urlpatterns = [
    path('search/', CommentarySearchView.as_view(), name='commentary-search'),
    path('commentaries/<str:book>/<int:chapter>/', CommentaryListView.as_view(), name='commentary-list'),
    path('import/', ImportCommentariesView.as_view(), name='import-commentaries'),
]
