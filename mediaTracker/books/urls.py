from django.urls import path
from .views import BookSearchView, BookSearchResultView, BookDetailView

urlpatterns = [
    path('search/', BookSearchView.as_view(), name='search'),
    path('search_results/', BookSearchResultView.as_view(), name='search_results'),
    path('book_detail/<int:isbn>', BookDetailView.as_view(), name='book_detail')
]
