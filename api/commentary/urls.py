from django.urls import path
from .views import CommentaryListView, ImportCommentariesView

urlpatterns = [
    path('commentaries/<str:book>/<int:chapter>/', CommentaryListView.as_view(), name='commentary-list'),
    path('import/', ImportCommentariesView.as_view(), name='import-commentaries'),
]
