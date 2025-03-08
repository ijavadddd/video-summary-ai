from django.urls import path
from video_summary.views import MainView, VideoSummaryView


app_name = "video_summary"
urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path("video-summary/", VideoSummaryView.as_view(), name="video_summary"),
]
