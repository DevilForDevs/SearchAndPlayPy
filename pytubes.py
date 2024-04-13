from pytube import YouTube

yt=YouTube("https://www.youtube.com/watch?v=75V4ClJZME4")
yt.streams.get_by_itag(18).download()