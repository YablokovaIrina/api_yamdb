from django.contrib import admin

from .models import Title, Comment, Review, Genre, Category


admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Review)
