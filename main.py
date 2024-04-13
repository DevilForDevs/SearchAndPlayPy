import instaloader
import vlc
from pytube import YouTube, cipher, Search

import TOOLBOX

# L = instaloader.Instaloader()
# post = instaloader.Post.from_shortcode(L.context, "C3kwYSnoKma-Bsg3mA2yjInypoQ_Feq2v7GhMo0")
# # https://www.instagram.com/reel/C3sGQpuyDiX/?utm_source=ig_web_copy_link
# print(post.video_url)
# from yt_dlp import YoutubeDL
#
# ydl_opts = {'quiet': True}
# with YoutubeDL(ydl_opts) as ydl:
#     info_dict = ydl.extract_info("https://www.facebook.com/watch?v=1711932389316369",
#                                  download=False)
#     videos = info_dict["formats"]
#     for item in videos:
#         print(item)
# import requests
#
# url = "https://www.facebook.com/watch?v=638689701187673"
#
# try:
#     response = requests.get(url)
#     response.raise_for_status()  # Raise an HTTPError for bad responses
#
#     if response.status_code == 200:
#         source_code = response.text
#         print(f"Source code of {url}:\n{source_code}")
#     else:
#         print(f"Failed to retrieve source code. HTTP Code: {response.status_code}")
#
# except requests.exceptions.RequestException as e:
#     print(f"Error: {e}")
# yt = YouTube("https://www.youtube.com/watch?v=75V4ClJZME4&pp=ygUZZG9jdG9yIHdobyBvcmlnaW5hbCB0aGVtZQ%3D%3D")
# sts = yt.streams
# for k in sts:
#     print(k.url)

# for s in sts:
#     print(s)
# print(TOOLBOX.scrap_data("kmrzKIJz1KI"))

playlist_url = "https://youtube.com/playlist?list=PLGjplNEQ1it8-0CmoljS5yeV-GlKSUEt0&si=kwM4IsP2t557KlYf"

playlist = Search("haan tu hai")
results = playlist.results
playlist.get_next_results()
