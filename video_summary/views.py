from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from video_summary import utils
from youtube_transcript_api import YouTubeTranscriptApi
from django.http import JsonResponse


class MainView(View):
    template_name = "video_summary/video_summary.html"

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(csrf_exempt, name="dispatch")
class VideoSummaryView(View):
    def post(self, request):
        video_url = request.POST.get("link")
        try:
            # Extract video ID from the URL
            video_id = video_url.split("v=")[1].split("&")[0]

            # Fetch transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            full_text = " ".join([entry["text"] for entry in transcript])

            # Generate summary (replace this with your summary logic)
            summary = full_text[:500] + "..."  # Example: First 500 characters
            print(summary)
            # Return JSON response
            return JsonResponse(
                {
                    "title": "Video Summary",
                    "content": summary,
                    "video_url": video_url,
                }
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
