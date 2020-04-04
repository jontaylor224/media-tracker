from datetime import datetime
from django.views import View
from django.shortcuts import render, HttpResponseRedirect
import requests

from .forms import ISBNSearch, BookEditForm
from .models import Book
from mediaTracker.media_user.models import MediaUser


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
                myBook = Book.objects.get(ISBN_13=data['ISBN'])
            except Book.DoesNotExist:
                try:
                    myBook = Book.objects.get(ISBN_10=data['ISBN'])
                except Book.DoesNotExist:
                    # raise Exception()
                    url = 'https://openlibrary.org/api/books?bibkeys=isbn:' + \
                        data['ISBN'] + '&jscmd=data&format=json'
                    req_data = requests.get(url)
                    req_status = req_data.status_code
                    if req_status == 403:
                        return render(request, '403.html')
                    json_data = req_data.json()
                    if json_data == {}:
                        return render(request, 'no_book_found.html')
                    else:
                        volumeInfo = 'isbn:'+data['ISBN']

                        myBook = Book()
                        try:
                            myBook.ISBN_13 = json_data[volumeInfo]['identifiers']['isbn_13'][0]
                        except KeyError:
                            myBook.ISBN_13 = None
                            try:
                                myBook.ISBN_10 = json_data[volumeInfo]['identifiers']['isbn_10'][0]
                            except KeyError:
                                return render(request, 'no_book_found.html')
                        myBook.title = json_data[volumeInfo].get(
                            'title', 'no title available')
                        try:
                            myBook.author = json_data[volumeInfo]['authors'][0]['name']
                        except KeyError:
                            myBook.author = "no author available"
                        try:
                            myBook.publisher = json_data[volumeInfo]['publishers'][0]['name']
                        except KeyError:
                            myBook.author = "no publisher available"
                        try:
                            myBook.pubDate = datetime.strptime(
                                json_data[volumeInfo]['publish_date'], '%B %Y')
                        except ValueError:
                            try:
                                myBook.pubDate = datetime.strptime(
                                    json_data[volumeInfo]['publish_date'], '%b %d, %Y')
                            except KeyError:
                                myBook.pubDate = None
                        try:
                            myBook.coverThumbURL = json_data[volumeInfo]['cover']['medium']
                        except KeyError:
                            myBook.coverThumbURL = 'static/images/default_book_cover.jpg'
                        try:
                            myBook.description = json_data[volumeInfo]['excerpts'][0]['text']
                        except KeyError:
                            myBook.description = 'No description available'
            form = BookEditForm(instance=myBook)
        return render(request, self.template_name, {'data': data, 'form': form})

    def post(self, request, *args, **kwargs):
        form = BookEditForm(request.POST)
        # breakpoint()
        current_book = form.save()
        request.user.mediauser.collection.add(current_book)

        return render(request, 'book_added.html', {'book': current_book})


class BookDetailView(View):
    model = Book
    template_name = 'book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
