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
                myBook = Book.objects.get(ISBN=data['ISBN'])
            except Book.DoesNotExist:
                url = 'https://openlibrary.org/api/books?bibkeys=isbn:' + \
                    data['ISBN'] + '&jscmd=data&format=json'
                req_data = requests.get(url)
                req_status = req_data.status_code
                if req_status == 404:
                    return render(request, '404.html')
                if req_status >= 500:
                    return render(request, '500.html')
                json_data = req_data.json()
                if json_data == {}:
                    return render(request, 'no_book_found.html')
                else:
                    volumeInfo = 'isbn:'+data['ISBN']

                    myBook = Book()
                    try:
                        myBook.ISBN = json_data[volumeInfo]['identifiers']['isbn_13']
                    except KeyError:
                        try:
                            myBook.ISBN = json_data[volumeInfo]['identifiers']['isbn_10']
                        except KeyError:
                            return render(request, 'no_book_found.html')
                    try:
                        myBook.title = json_data[volumeInfo]['title']
                    except KeyError:
                        myBook.title = "no title available"
                    try:
                        myBook.author = json_data[volumeInfo]['authors'][0]['name']
                    except KeyError:
                        myBook.author = "no author available"
                    try:
                        myBook.publisher = json_data[volumeInfo]['publishers'][0]['name']
                    except KeyError:
                        myBook.author = "no publisher available"
                    try:
                        myBook.pubDate = json_data[volumeInfo]['publish_date']
                    except KeyError:
                        myBook.pubDate = ''
                    try:
                        myBook.coverThumbURL = json_data[volumeInfo]['cover']['medium']
                    except KeyError:
                        myBook.coverThumbURL = 'static/images/default_book_cover.jpg'
                    try:
                        myBook.description = json_data[volumeInfo]['excerpts'][0]['text']
                    except KeyError:
                        myBook.description = 'No description available'
                    myBook.collection = MediaUser.objects.get(user=request.user)
            form = BookEditForm(instance=myBook)
        return render(request, self.template_name, {'data': data, 'form': form})
