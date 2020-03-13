from django.views import View
from django.shortcuts import render, HttpResponseRedirect
import requests

from .forms import ISBNSearch
from .models import Book


class BookSearchView(View):
    template_name = 'isbn_search_form.html'

    def get(self, request, *args, **kwargs):
        form = ISBNSearch
        return render(request, self.template_name, {'form': form})


class BookSearchResultView(View):
    template_name = 'isbn_search_results.html'

    def get(self, request, *args, **kwargs):
        form = ISBNSearch(request.GET)
        if form.is_valid():
            data = form.cleaned_data
            try:
                results = Book.objects.get(ISBN=data['ISBN'])
            except Book.DoesNotExist:
                url = 'https://openlibrary.org/api/books?bibkeys=isbn:' + data['ISBN'] + '&jscmd=data&format=json'
                req_data = requests.get(url)
                req_status = req_data.status_code
                json_data = req_data.json()
                volumeInfo = 'isbn:'+data['ISBN']
                results = {
                    'ISBN': json_data[volumeInfo]['identifiers']['isbn_13'],
                    'title': json_data[volumeInfo]['title'],
                    'author1': json_data[volumeInfo]['authors'][0]['name'],
                    # publisher: volumeInfo[publisher],
                    'pubDate': json_data[volumeInfo]['publish_date'],
                    'coverThumbURL': json_data[volumeInfo]['cover']['medium']
                }

        return render(request, self.template_name, {'data': data, 'results': results})
