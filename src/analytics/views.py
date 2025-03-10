from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from analytics.serializers import URLStatsSerializer
from shortener.models import ShortenedURL


class URLStatsView(generics.RetrieveAPIView):
    """
    View to retrieve statistics for a shortened URL.
    """

    serializer_class = URLStatsSerializer
    lookup_field = "short_code"
    lookup_url_kwarg = "short_code"
    queryset = ShortenedURL.objects.all()
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        """
        Get statistics for a shortened URL with paginated visit logs.
        """
        instance = self.get_object()

        paginator = self.pagination_class()
        visits = instance.visit_logs.all().order_by("-created_at")
        paginated_visits = paginator.paginate_queryset(visits, request)

        stats_data = {"visit_details": paginated_visits}

        serializer = self.get_serializer(stats_data)

        return paginator.get_paginated_response(serializer.data)
