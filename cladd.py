import os.path
import threading

import requests

import TOOLBOX


class Downloader:
    url: str = None
    title = None
    lock: threading.Lock = None
    file_object = None

    def __init__(self, vid: dict, res: int, lock: threading.Lock, progress_dict: dict, folder: str):
        self.lock = lock
        self.title = TOOLBOX.txt2filename(vid["title"])
        self.url = TOOLBOX.getSturl(vid["videoId"], res)
        execute_request = requests.get(self.url, stream=True)
        progress_dict[self.title] = {"ts": int(execute_request.headers.get("Content-Length")), "tbd": 0,
                                     "speed": 1}
        if res == 140:
            file_name = folder + self.title + ".mp3"
        else:
            file_name = folder + self.title + ".mp4"
        if os.path.exists(file_name):
            if os.path.getsize(file_name) == progress_dict[self.title]["ts"]:
                return
            progress_dict[self.title]["tbd"] = os.path.getsize(file_name)
            self.file_object = open(file_name, "ab")
        else:
            print("not exist")
            self.file_object = open(file_name, "wb")
        # progress_dict[self.title]["start_time"] = time.time()*1000
        self.download(progress_dict)

    def download(self, progress_dict: dict):
        end_byte = min(progress_dict[self.title]["tbd"] + 9437184, progress_dict[self.title]["ts"])
        kurl = self.url + f'&range={progress_dict[self.title]["tbd"]}-{end_byte}'
        execute_request = requests.get(kurl, stream=True)
        for data in execute_request.iter_content(chunk_size=1024):
            # print(progress_dict)
            if progress_dict["quite"]:
                print(progress_dict)
                return None
            progress_dict[self.title]["tbd"] += len(data)
            self.file_object.write(data)
        if progress_dict[self.title]["tbd"] == progress_dict[self.title]["ts"]:
            self.file_object.close()
            print("finished")
            return
        if progress_dict[self.title]["tbd"] < progress_dict[self.title]["ts"]:
            self.download(progress_dict)
