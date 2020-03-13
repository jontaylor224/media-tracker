from django.urls import path
from .views import BookSearchView, BookSearchResultView

urlpatterns = [
    path('search/', BookSearchView.as_view(), name='search'),
    path('search_results/', BookSearchResultView.as_view(), name='search_results')
]