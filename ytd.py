import yt_dlp


def get_main_page_videos():
    options = {
        'format': 'best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        main_page_url = 'https://www.youtube.com/'
        main_page_info = ydl.extract_info(main_page_url, download=False)

        if 'entries' in main_page_info:
            main_page_videos = main_page_info['entries']
            return main_page_videos
        else:
            return []


# Example usage
main_page_videos = get_main_page_videos()

for video in main_page_videos:
    print(f"Title: {video['title']}")
    print(f"Video ID: {video['id']}")
    print(f"URL: https://www.youtube.com/watch?v={video['id']}\n")
