from rest_framework import filters, permissions, status, viewsets, mixins
from rest_framework.response import Response

from reviews.models import (
    Title,
    Genre,
    Category
)


class CategoriesGenresBaseViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (AdminPermission | ReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class CategoriesViewSet(CategoriesGenresBaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenresViewSet(CategoriesGenresBaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (AdminPermission | ReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitleWriteSerializer
        return TitleReadSerializer
