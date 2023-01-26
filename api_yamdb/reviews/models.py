from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

User = get_user_model()


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delet=models.CASCADE, related_name='comments'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='comments'
    )
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class Review(models.Model):
    text = models.TextField()
    # оценка должна лежать в диапозоне от 1 до 10
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    author = models.ForeignKey(
        User, on_delet=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def save(self):
        # пользователь может оставить только один отзыв на произведение
        # если объект отзыва существует, значит у него есть self.pk (True)
        # и это возможно вызвали метод patch, нужно разрешить сохранить данные
        # если это новый отзыв, значит у него нет self.pk (False) и тут уже
        # проверяется а не существет ли уже отзыва
        # переданного автора к переданному посту
        if not self.pk and Review.objects.filter(
            author=self.author, title=self.title
        ).exists:
            raise ValidationError(
                'Пользователь может оставить только один отзыв на произведнеие'
            )
        return super().save()
