from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoriesViewSet,
    CommentsViewSet,
    GenresViewSet,
    ReviewViewSet,
    signup_post,
    TitlesViewSet,
    token_post,
    UserViewSet,
)

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register('users', UserViewSet)

router_v1.register(
    'titles',
    TitlesViewSet,
    basename='titles',
)
router_v1.register(
    'categories',
    CategoriesViewSet,
    basename='categories',
)
router_v1.register(
    'genres',
    GenresViewSet,
    basename='genres',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', signup_post, name='auth_signup'),
    path('v1/auth/token/', token_post, name='auth_token')
]
