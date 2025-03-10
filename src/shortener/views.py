from analytics.models import Visit
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from shortener.models import ShortenedURL
from shortener.serializers import ShortenedURLSerializer


class ShortenedURLViewSet(viewsets.ModelViewSet):
    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer
    lookup_field = "short_code"
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        original_url = serializer.validated_data["original_url"]
        existing_url = ShortenedURL.objects.filter(original_url=original_url).first()

        if existing_url:
            return Response(self.get_serializer(existing_url).data, status=status.HTTP_200_OK)

        short_code = ShortenedURL.create_short_code()
        shortened_url = ShortenedURL.objects.create(
            original_url=original_url,
            short_code=short_code,
            creator_ip=request.META.get("REMOTE_ADDR"),
            creator_user_agent=request.META.get("HTTP_USER_AGENT"),
        )

        return Response(self.get_serializer(shortened_url).data, status=status.HTTP_201_CREATED)


def redirect_to_original(request, short_code):
    shortened_url = get_object_or_404(ShortenedURL, short_code=short_code)

    Visit.objects.create(
        shortened_url=shortened_url,
        ip_address=request.META.get("REMOTE_ADDR"),
    )

    return redirect(shortened_url.original_url)
