import pytest

from mediaTracker.books.models import Book



class TestViewHelpers():

    def test_get_book_data_from_api(self):
        test_isbn = '9780812550290'
        assert views.get_book_data_from_api(test_isbn).json()['isbn:9780812550290']['identifiers']['isbn_13'][0] == test_isbn


    def test_process_api_response_for_valid_response(self):
        response_data = views.get_book_data_from_api('9780812550290')
        assert views.process_api_response(response_data)['ISBN_13'] == '9780812550290'


    # def test_process_api_response_for_response_with_empty_json(self):

    @pytest.mark.django_db
    def test_create_book(self):
        test_book = views.create_book('9780812550290')
        assert isinstance(test_book, Book)
