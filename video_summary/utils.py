from openai import OpenAI
from decouple import config
from pytube import YouTube
import os


client = OpenAI(
    api_key=config("OPENAI_API_KEY"),
)
prompt = """Analyze the following video transcript and provide the following:

Subject of the Video: A concise statement (1-2 sentences) summarizing the main topic or theme of the video.

Key Details: A bullet-point list of the most important points, ideas, or arguments discussed in the video.

Summary: A brief yet comprehensive paragraph summarizing the video's content, including its purpose, main takeaways, and any conclusions or calls to action.

Here is the transcript:"""


def request_chatgpt(message):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{prompt} {message}",
            }
        ],
        model="gpt-4o",
    )
    return chat_completion


def download_youtube_mp3(url, output_path="."):
    try:
        yt = YouTube(url)
        print(yt.title)
        video = yt.streams.filter(only_audio=True).first()
        video.download(output_path)

        # Convert to MP3
        video_path = os.path.join(output_path, video.default_filename)
        mp3_path = os.path.join(
            output_path, os.path.splitext(video.default_filename)[0] + ".mp3"
        )

        os.remove(video_path)

    except Exception as e:
        print(f"An error occurred: {e}")
