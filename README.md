# Setup
```pipenv install```

```pipenv shell```

## Setup database

```python manage.py makemigrations mediaTracker```

```python manage.py migrate```

## Create Superuser

```python manage.py createsuperuser```

Follow prompts to create a superuser

## Start server
```python manage.py runserver```

## Open in Browser

```http://localhost:8000```
Home page

To log in to the admin panel, go to: 
```http://localhost:8000/admin```

Use the superuser credentials you created earlier