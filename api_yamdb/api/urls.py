from django.urls import include, path
from rest_framework import routers

from .views import (
    CommentsViewSet,
    ReviewViewSet,
    CategoriesViewSet,
    GenresViewSet,
    TitlesViewSet,
    UserViewSet,
    UserCreateViewSet,
    UserReceiveTokenViewSet,
)

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'categories', CategoriesViewSet, basename='categories')
router_v1.register(r'genres', GenresViewSet, basename='genres')
router_v1.register(r'titles', TitlesViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comment'
)


urlpatterns = [
    path('v1/auth/signup/', UserCreateViewSet.as_view({'post': 'create'})),
    path('v1/auth/token/',
         UserReceiveTokenViewSet.as_view({'post': 'create'})),
    path('v1/', include(router_v1.urls)),
]
