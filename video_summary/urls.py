from django.urls import path
from video_summary.views import MainView


app_name = "video_summary"
urlpatterns = [
    path("", MainView.as_view(), name="main"),
]
