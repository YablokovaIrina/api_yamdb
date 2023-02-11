from csv import DictReader
from django.core.management.base import BaseCommand


from reviews.models import (Category, Comment, Genre,
                            Title, Review, User)


def load_users():
    print('loading user data...')
    with open('static/data/users.csv', encoding='utf-8') as file:
        reader = DictReader(file)
        users = []
        for row in reader:
            user = User(
                role=row['role'],
                username=row['username'],
                id=row['id'],
                email=row['email'],
            )
            users.append(user)
        User.objects.bulk_create(users)
    print('user data loaded!')


def load_genres():
    print('loading genre data...')
    with open('static/data/genre.csv', encoding='utf-8') as file:
        reader = DictReader(file)
        genres = []
        for row in reader:
            genre = Genre(
                slug=row['slug'],
                name=row['name'],
                id=row['id'],
            )
            genres.append(genre)
        Genre.objects.bulk_create(genres)
    print('genre data loaded!')


def load_categories():
    print('loading category data...')
    with open('static/data/category.csv', encoding='utf-8') as file:
        reader = DictReader(file)
        categories = []
        for row in reader:
            category = Category(
                slug=row['slug'],
                name=row['name'],
                id=row['id'],
            )
            categories.append(category)
        Category.objects.bulk_create(categories)
    print('category data loaded!')


def load_title():
    print('loading title data...')
    with open('static/data/titles.csv', encoding='utf-8') as file:
        reader = DictReader(file)
        titles = []
        for row in reader:
            category = Category.objects.get(id=row['category'])
            title = Title(
                year=row['year'],
                name=row['name'],
                id=row['id'],
                category=category
            )
            titles.append(title)
        Title.objects.bulk_create(titles)
    print('title data loaded!')


def load_genre_title():
    print('loading genre/title relation data...')
    with open('static/data/genre_title.csv', encoding='utf-8') as file:
        reader = DictReader(file)

        for row in reader:
            genre = Genre.objects.get(id=row['genre_id'])
            title = Title.objects.get(id=row['title_id'])
            title.genre.add(genre)
            title.save()
    print('genre/title relation data loaded!')


def load_reviews():
    print('loading reviews data...')
    with open('static/data/review.csv', encoding='utf-8') as file:
        reader = DictReader(file)
        reviews = []
        for row in reader:
            review = Review(
                title=Title.objects.get(id=row['title_id']),
                id=row['id'],
                text=row['text'],
                author=User.objects.get(id=row['author']),
                score=row['score'],
                pub_date=row['pub_date']
            )
            reviews.append(review)
        Review.objects.bulk_create(reviews)
    print('reviews data loaded!')


def load_comments():
    print('loading comment data...')
    with open('static/data/comments.csv', encoding='utf-8') as file:
        reader = DictReader(file)
        comments = []
        for row in reader:
            comment = Comment(
                review=Review.objects.get(id=row['review_id']),
                id=row['id'],
                text=row['text'],
                author=User.objects.get(id=row['author']),
                pub_date=row['pub_date']
            )
            comments.append(comment)
        Comment.objects.bulk_create(comments)
    print('comment data loaded!')


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            load_users()
            load_genres()
            load_categories()
            load_title()
            load_genre_title()
            load_reviews()
            load_comments()
        except Exception as error:
            print(error)
