from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# User = get_user_model()


# class Title(models.Model):
#     name = models.TextField(max_length=256, verbose_name='Название')
#     year = models.IntegerField(verbose_name='Год выпуска')
#     rank = models.IntegerField(default=0, editable=False)
#     description = models.TextField(
#         blank=True,
#         verbose_name='Описание'
#     )

#     class Meta:
#         ordering = ('name',)
#         verbose_name = 'Произведение'
#         verbose_name_plural = 'Произведения'

#     def __str__(self):
#         return self.name


class Review(models.Model):
    text = models.TextField()
    # оценка должна лежать в диапозоне от 1 до 10
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def save(self, *args, **kwargs):
        # пользователь может оставить только один отзыв на произведение
        # если объект отзыва существует, значит у него есть self.pk (True)
        # и это возможно вызвали метод patch, нужно разрешить сохранить данные
        # если это новый отзыв, значит у него нет self.pk (False) и тут уже
        # проверяется а не существет ли уже отзыва
        # переданного автора к переданному посту
        if not self.pk and Review.objects.filter(
            author=self.author, title=self.title
        ).exists():
            raise ValidationError(
                'Пользователь может оставить только один отзыв на произведнеие'
            )
        return super().save()


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
