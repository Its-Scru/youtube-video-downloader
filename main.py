import pytube
from pytube import YouTube
import os
import requests
from mutagen.mp4 import MP4

def download_youtube_mp3(video_url, download_path="D:/Coding/YTtoFile/Songs"):
    try:
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        os.makedirs(download_path, exist_ok=True)

        output_file = audio_stream.download(output_path=download_path)

        base, ext = os.path.splitext(output_file)
        new_file = base + '.mp3'
        os.rename(output_file, new_file)

        print(f"Downloaded and converted to MP3: {yt.title}")

    except Exception as e:
        print(f"An error occurred: {e}")

def download_youtube_mp4(video_url, download_path="D:/Coding/YTtoFile/Videos"):
    try:
        yt = YouTube(video_url)

        thumbnail_url = yt.thumbnail_url

        video_stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first()
        if video_stream is None:
            pass  

        os.makedirs(download_path, exist_ok=True)
        video_filename = video_stream.download(output_path=download_path)

        response = requests.get(thumbnail_url, stream=True)
        response.raise_for_status()

        video = MP4(video_filename)
        video["covr"] = [response.content]
        video.save()

        print(f"Downloaded video as MP4: {yt.title}")

    except Exception as e:
        print(f"An error occurred: {e}")

print("""
What output would you like?
[1]. MP3
[2]. MP4
""")
choice = int(input("> "))
video_url = input("Enter the YouTube video URL: ")

if choice == 1:
    download_youtube_mp3(video_url)
if choice == 2:
    download_youtube_mp4(video_url)