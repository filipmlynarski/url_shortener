from django.urls import include, path
from rest_framework.routers import DefaultRouter

from shortener.views import ShortenedURLViewSet, redirect_to_original

router = DefaultRouter()
router.register(r"shortener", ShortenedURLViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("<str:short_code>/", redirect_to_original, name="redirect_to_original"),
]
