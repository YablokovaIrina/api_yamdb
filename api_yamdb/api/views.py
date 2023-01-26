from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
#from rest_framework.mixins import CreateModelMixin, ListModelMixin
#from rest_framework.pagination import LimitOffsetPagination
#from rest_framework.permissions import IsAuthenticated

#from .permissions import IsAuthorOrReadOnly
#from .serializers import (
#    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
#)
from reviews.models import Comment, Review, Title


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        summ_score = sum([review.score for review in Title.reviews.all()])
        average_score = summ_score / Title.reviews.count()
        title.rank = average_score
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return Title.comments.all()
