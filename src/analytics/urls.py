from django.urls import path

from analytics.views import URLStatsView

urlpatterns = [
    path("analytics/<str:short_code>/", URLStatsView.as_view(), name="url-stats"),
]
