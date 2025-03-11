from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from video_summary import utils
from youtube_transcript_api import YouTubeTranscriptApi
from django.http import JsonResponse
from video_summary.models import Post
from rich.console import Console
console = Console()
class MainView(View):
    template_name = "video_summary/video_summary.html"

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(csrf_exempt, name="dispatch")
class VideoSummaryView(View):
    def post(self, request):
        video_url = request.POST.get("link")
        # try:
        # Extract video ID from the URL
        # video_id = video_url.split("v=")[1].split("&")[0]

        from pytube import YouTube
        SAVE_PATH = r"./"
        link = video_url

        yt = YouTube(video_url)
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(SAVE_PATH, 'videoFilename', 'mp4')
        # print(summary)
        # Return JSON response
        return JsonResponse(
            {
                "title": "Video Summary",
                # "content": summary,
                "video_url": video_url,
            }
        )
        # except Exception as e:
        #     console.print(e, style="bold red")
        #     return JsonResponse({"error": str(e)}, status=400)


class PostListView(ListView):
    template_name = "video_summary/posts.html"
    queryset = Post.objects.all()
