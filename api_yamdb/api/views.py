from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Review, Title
from .permissions import IsAuthorOrStaffOrReadOnly
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly,)

    def get_permissions(self):
        if self.action == 'create':
            return (IsAuthenticatedOrReadOnly(),)
        return super().get_permissions()

    # Создаём ревью, а так же рассчитываем рейтинг прозведения
    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        score = self.request.data.get('score')
        if title.reviews.count() == 0:
            title.rank = score
        else:
            summ_score = sum([
                review.score for review in title.reviews.all()]
            ) + score
            average_score = summ_score / (title.reviews.count() + 1)
            title.rank = average_score
        serializer.save(author=self.request.user, title=title)

    # При использовании метода PATCH может измениться значение
    # score, необходимо пересчитать рейтинг произведения
    def partial_update(self, request, *args, **kwargs):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        previous_score = title.reviews.get(author=self.request.user).score
        score = self.request.data.get('score')
        summ_score = sum([
            review.score for review in title.reviews.all()]
        ) - previous_score + score
        average_score = summ_score / (title.reviews.count() + 1)
        title.rank = round(average_score, 3)
        print(title.rank)
        return super().partial_update(request, *args, **kwargs)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly,)

    def get_permissions(self):
        if self.action == 'create':
            return (IsAuthenticatedOrReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Title, id=title_id)
        review = get_object_or_404(Review, id=review_id, title=title)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()
