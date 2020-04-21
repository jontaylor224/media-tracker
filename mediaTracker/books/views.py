from datetime import datetime
from django.views import View
from django.views.generic import DetailView
from django.shortcuts import render, HttpResponseRedirect, reverse
import requests

from .forms import ISBNSearch, BookEditForm
from .models import Book
from mediaTracker.media_user.models import MediaUser


class NoBookException(Exception):
    pass

class APIException(Exception):
    pass


class BookSearchView(View):
    template_name = 'isbn_search_form.html'

    def get(self, request, *args, **kwargs):
        form = ISBNSearch
        return render(request, self.template_name, {'form': form})


class BookSearchResultView(View):
    template_name = 'isbn_search_results.html'

    def get(self, request, *args, **kwargs):
        form = ISBNSearch(request.GET)
        myBook = None
        built_book = None
        if form.is_valid():
            data = form.cleaned_data
            myBook = Book.objects.filter(ISBN_13=data['ISBN']).first()
            if not myBook:
                myBook = Book.objects.filter(ISBN_10=data['ISBN']).first()
            if myBook:
                if not request.user.mediauser.collection.filter(id=myBook.id).exists():
                    return render(request, self.template_name, {'data': data, 'form': BookEditForm(instance=myBook), 'coverURL': myBook.coverThumbURL})
                else:
                    return HttpResponseRedirect(reverse('book_detail', args=[myBook.pk]))
            else:
                # ISBN not found in database
                try:
                    built_book = create_book(data['ISBN'])
                except NoBookException:
                    return render(request, 'no_book_found.html')

            coverURL = built_book.coverThumbURL
            form = BookEditForm(instance=built_book)
        return render(request, self.template_name, {'data': data, 'form': form, 'coverURL': coverURL})

    def post(self, request, *args, **kwargs):
        form = BookEditForm(request.POST)
        current_book = form.save()
        request.user.mediauser.collection.add(current_book)

        return render(request, 'book_added.html', {'book': current_book})


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# helper functions - to move to separate file at later date
def create_book(isbn: str) -> Book:
    try:
        req_data = get_book_data_from_api(isbn)
    except APIException:
        return render(request, '403.html')

    json_data = process_api_response(req_data)
    return Book.objects.create(**json_data)


def get_book_data_from_api(isbn_str):
    url = 'https://openlibrary.org/api/books?bibkeys=isbn:' + \
        isbn_str + '&jscmd=data&format=json'
    response_data = requests.get(url)
    if response_data.status_code == 403:
        raise APIException()
    else:
        return response_data


def process_api_response(response_data):

    json_data = response_data.json()
    if json_data == {}:
        raise NoBookException('No book was found for the requested ISBN!')
    else:
        volumeInfo = next(iter(json_data))
        book_json = {}
        try:
            book_json['ISBN_13'] = json_data[volumeInfo]['identifiers']['isbn_13'][0]
        except KeyError:
            book_json['ISBN_13'] = None

        try:
            book_json['ISBN_10'] = json_data[volumeInfo]['identifiers']['isbn_10'][0]
        except KeyError:
            book_json['ISBN_10'] = None

        book_json['title'] = json_data[volumeInfo].get(
            'title', 'no title available')

        try:
            book_json['author'] = json_data[volumeInfo]['authors'][0]['name']
        except KeyError:
            book_json['author'] = "no author available"

        try:
            book_json['publisher'] = json_data[volumeInfo]['publishers'][0]['name']
        except KeyError:
            book_json['publisher'] = "no publisher available"

        try:
            book_json['pubDate'] = datetime.strptime(
                json_data[volumeInfo]['publish_date'], '%B %Y')
        except ValueError:
            try:
                book_json['pubDate'] = datetime.strptime(
                    json_data[volumeInfo]['publish_date'], '%b %d, %Y')
            except ValueError:
                try:
                    book_json['pubDate'] = datetime.strptime(
                        json_data[volumeInfo]['publish_date'], '%Y')
                except ValueError:
                    book_json['pubDate'] = None
        except KeyError:
            book_json['pubDate'] = None

        try:
            book_json['coverThumbURL'] = json_data[volumeInfo]['cover']['medium']
        except KeyError:
            book_json['coverThumbURL'] = None

        try:
            book_json['description'] = json_data[volumeInfo]['excerpts'][0]['text']
        except KeyError:
            book_json['description'] = 'No description available'

        return book_json
