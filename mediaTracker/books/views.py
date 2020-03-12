from django.views.generic import DetailView

# search for books by isbn

# get isbn from user form
# check if isbn in database.  if in database, display info
# if not in database, send api query and display info
# ask user if want to add to collection. if yes, add to database/collection


class BookDetailView(DetailView):
    pass