import vlc
import os
import queue
import threading
import tkinter
from io import BytesIO
from queue import Queue
from threading import Thread
from tkinter import BOTH, X, RIGHT, LEFT, END, BOTTOM, DISABLED, NORMAL, Y

import PIL.Image
import customtkinter
import requests


import TOOLBOX
import cladd


def getBytes(url, queue):
    u = requests.get(url)
    queue.put(BytesIO(u.content))


def getBytes2(url):
    try:
        u = requests.get(url)
        return BytesIO(u.content)
    except Exception as e:
        print(e)


class App(customtkinter.CTk):
    tabview: customtkinter.CTkTabview
    tab1 = None
    tab2 = None
    tab3 = None
    search_frame = None
    search_box: customtkinter.CTkEntry = None
    search_button = None
    scroll_f = None
    win_height = None
    rsults = None
    thumbnail = {}
    raw_results = []
    final = []
    search_term = None
    app_closed = False
    vlc_player = None
    vlc_int = None
    media_canvas = None
    load_thumbs = True
    conti_token = None
    items_displayed = []
    progressbar = None
    stop_thumbnail_downloader = False
    thumbnail_downloader: threading.Thread = None
    smft = 18
    duration_of_media = 0
    slider: customtkinter.CTkSlider = None
    duration_lab = None
    dialog = None
    downloads_scroll_view: customtkinter.CTkScrollableFrame = None
    progress_dict = {}
    progress_lock = threading.Lock()
    default_range_size = 9437184
    dict_ditem = {}
    df = "Downloads/"
    speed_dict = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.win_height = self.winfo_height()
        self.title("Search&Play")
        self.progress_dict["quite"] = False

        def on_closing():
            self.app_closed = True
            self.progress_dict["quite"] = True
            self.vlc_int.release()
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", on_closing)
        self.setTab1()
        self.player_tab()
        self.downloads_tab()
        self.update_root()
        fld = "Downloads/"
        if not os.path.exists(fld):
            os.mkdir(fld)

    def getSmart(self, input_string, queue2):
        km = TOOLBOX.getSturl(input_string, self.smft)
        queue2.put(km)

    def play_vid(self, vid, resolution):
        self.smft = resolution
        result_queue = Queue()
        thread = Thread(target=self.getSmart, args=(vid, result_queue))
        thread.start()

        def check_que():
            try:
                url = result_queue.get_nowait()
                print(url)
                media = self.vlc_int.media_new(url)
                self.vlc_player.set_media(media)

                if self.media_canvas is None:
                    print("canvas not found")
                else:
                    self.vlc_player.set_hwnd(self.media_canvas.winfo_id())
                    self.vlc_player.play()
                    self.tabview.set("Player")
                    self.after(100, self.checkPlaying)
                    return
            except queue.Empty:
                self.after(100, check_que)

        check_que()
        return

    def save_link(self, vidoeId):
        fileo = open("Savedlinks.txt", "a")
        fileo.write(f'https://www.youtube.com/watch?v={vidoeId}\n')
        fileo.close()

    def addItems(self, item):
        if self.app_closed:
            return
        else:
            testf = customtkinter.CTkFrame(self.scroll_f)
            thumb = customtkinter.CTkLabel(testf, text="",
                                           image=customtkinter.CTkImage(
                                               light_image=PIL.Image.open(item["thumbnail"]),
                                               size=(220, 120)))
            thumb.pack(side=LEFT)
            mt = "    " + item["title"]
            playb = customtkinter.CTkLabel(testf, text=mt, anchor="w")
            playb.pack(fill=X, ipadx=5)
            dub = customtkinter.CTkFrame(testf)
            dub.pack(fill=X)
            due = "    " + item["duration"]
            save_link = customtkinter.CTkButton(dub, text="Save link",
                                                command=lambda i=item: self.save_link(item["videoId"]))
            save_link.pack(side=RIGHT)
            download = customtkinter.CTkButton(dub, text="Download"
                                               , command=lambda i=item: self.ask_resoluti(i))
            download.pack(side=RIGHT, padx=5)
            play_button360 = customtkinter.CTkButton(dub, text="Play 360",
                                                     command=lambda i=item: self.play_vid(item["videoId"], 18))
            play_button360.pack(side=RIGHT)
            playb_720 = customtkinter.CTkButton(dub, text="Play 720",
                                                command=lambda i=item: self.play_vid(item["videoId"], 22))
            playb_720.pack(side=RIGHT, padx=5)
            playb2 = customtkinter.CTkLabel(dub, text=due, anchor="w")
            playb2.pack(fill=X)
            testf.pack(fill=X, pady=2, before=self.load_more)

    def enabled_(self):
        self.load_more.configure(state=DISABLED)

    def dis(self):
        self.load_more.configure(state=NORMAL)

    def thumbd(self):
        self.after(0, self.enabled_)
        for item in self.raw_results:
            if self.app_closed:
                return None
            else:
                if item["title"] not in self.items_displayed:
                    self.items_displayed.append(item["title"])
                    bts = getBytes2(item["thumbnail"])
                    ki = item
                    ki["thumbnail"] = bts
                    self.after(1, lambda: self.addItems(ki))

        self.after(0, self.dis)
        ""

    def searches(self, input_string, queue):
        km = TOOLBOX.search(input_string, self.conti_token)
        queue.put(km)

    def getResults(self, append):
        result_queue = Queue()
        self.search_term = self.search_box.get()
        self.search_box.delete(0, END)
        text = self.search_term.replace("\n", "")
        thread = Thread(target=self.searches, args=(text, result_queue))
        thread.start()

        def check_and_update():
            try:
                if append:
                    new_items, self.conti_token = result_queue.get_nowait()
                    self.raw_results.extend(new_items)
                    self.progressbar.destroy()
                    if not self.thumbnail_downloader.is_alive():
                        self.thumbnail_downloader = threading.Thread(target=self.thumbd)
                        self.thumbnail_downloader.start()

                else:
                    new_items, self.conti_token = result_queue.get_nowait()
                    self.raw_results.extend(new_items)
                    self.thumbnail_downloader = threading.Thread(target=self.thumbd)
                    self.thumbnail_downloader.start()
                    self.progressbar.destroy()

                return

            except queue.Empty:
                self.after(100, check_and_update)

        check_and_update()

    def update_seekbar(self):
        cur = self.vlc_player.get_time()
        percent = int(cur / self.duration_of_media * 100)

        self.slider.set(percent)
        pg = TOOLBOX.seconds_to_dhms_short(cur) + "/" + TOOLBOX.seconds_to_dhms_short(self.duration_of_media)
        self.duration_lab.configure(text=pg)
        self.after(10, self.update_seekbar)
        self.slider.update()

    def checkPlaying(self):
        if self.vlc_player.get_length() == 0:
            self.after(100, self.checkPlaying)
        else:
            self.duration_of_media = self.vlc_player.get_length()
            tsr = "00:00:00/" + TOOLBOX.seconds_to_dhms_short(self.duration_of_media)
            self.duration_lab.configure(text=tsr)
            self.after(0, self.update_seekbar)

    def slider_event(self, value):
        val = int(value)

        self.vlc_player.set_time(int(val / 100 * self.duration_of_media))

    def kep(self, event):
        state = self.vlc_player.get_state()
        if state == vlc.State.Playing:
            self.vlc_player.pause()
        else:
            self.vlc_player.play()

    def set_sped(self):
        mk = self.speed_dict.keys()
        for k in mk:
            self.speed_dict[k] = 0
        self.after(1000, self.set_sped)

    def update_ui(self):
        ks = self.progress_dict.keys()
        for k in ks:
            if k != "quite":
                tbd = self.progress_dict[k]["tbd"]
                ts = self.progress_dict[k]["ts"]
                progress = TOOLBOX.convert_size(tbd) + "/" + TOOLBOX.convert_size(ts) + "     "
                percent = int(tbd * 100 // ts) if ts != 0 else 0
                # elapsed_time = time.time() * 1000 - self.progress_dict[k]["start_time"]
                # speed = TOOLBOX.convert_size(elapsed_time / tbd) if tbd != 0 else 0
                lab = self.dict_ditem[k][0]
                lab.configure(text=progress + str(percent) + "%")
                lab.update()
                PGB = self.dict_ditem[k][1]
                PGB.set(percent / 100)
        self.after(1000, self.update_ui)

    def downloader_thread(self, vid, res):
        def medi():
            dm = cladd.Downloader(vid, res, self.progress_lock, self.progress_dict, "Downloads/")

        threading.Thread(target=medi).start()
        self.update_ui()
        # self.set_sped()

    def download(self, vid, res):
        self.dialog.destroy()
        testf = customtkinter.CTkFrame(self.downloads_scroll_view)
        thumb = customtkinter.CTkLabel(testf, text="",
                                       image=customtkinter.CTkImage(
                                           light_image=PIL.Image.open(vid["thumbnail"]),
                                           size=(220, 120)))
        thumb.pack(side=LEFT)
        mt = TOOLBOX.txt2filename(vid["title"])
        playb = customtkinter.CTkLabel(testf, text=mt, anchor="w")
        playb.pack(fill=X, ipadx=5)
        dub = customtkinter.CTkFrame(testf, height=20)
        dub.pack(fill=X)
        save_link = customtkinter.CTkButton(dub, text="Copy Link")
        save_link.pack(side=RIGHT)
        progress_label = customtkinter.CTkLabel(dub, text="Progress")
        progress_label.pack(side=LEFT)
        peogress = customtkinter.CTkProgressBar(testf, progress_color="red", height=3)
        peogress.pack(fill=X)

        testf.pack(fill=X, pady=2)
        self.dict_ditem[mt] = [progress_label, peogress]
        self.tabview.set("Downloads")
        self.downloader_thread(vid, res)

    def ask_resoluti(self, vid):
        self.dialog = tkinter.Toplevel(self.tab1)
        dialog_width = 700
        dialog_height = 100
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_position = ((screen_width - dialog_width) // 1)
        y_position = ((screen_height - dialog_height) // 2)
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")
        self.dialog.title("Download")

        frame = tkinter.Frame(self.dialog)
        self.after(1000, self.update_ui)
        btn720 = customtkinter.CTkButton(frame, text="720", command=lambda i=vid: self.download(i, 22))
        btn720.pack(side=LEFT)
        btn360 = customtkinter.CTkButton(frame, text="360", command=lambda i=vid: self.download(i, 18))
        btn360.pack(side=LEFT, padx=10)
        btnaudio = customtkinter.CTkButton(frame, text="Audio", command=lambda i=vid: self.download(i, 140))
        btnaudio.pack(side=LEFT)

        frame.pack(pady=25)

    def player_tab(self):
        self.tab2 = self.tabview.add("Player")
        player_frame = customtkinter.CTkFrame(self.tab2)
        self.media_canvas = tkinter.Canvas(player_frame, bg="black", height=self.win_height * 5)
        self.media_canvas.pack(fill=tkinter.BOTH, expand=True)
        self.vlc_int = vlc.Instance()
        self.vlc_player = self.vlc_int.media_player_new()
        progress_frame = customtkinter.CTkFrame(self.tab2)
        progress_frame.pack(fill=X, side=BOTTOM)
        self.slider = customtkinter.CTkSlider(master=progress_frame, from_=0, to=100, command=self.slider_event,
                                              progress_color="blue", button_color="red")
        self.duration_lab = customtkinter.CTkLabel(progress_frame, height=5, text="Duration")
        self.duration_lab.pack(side=RIGHT)
        self.slider.pack(fill=X)
        player_frame.pack(fill=BOTH)
        self.bind("<space>", self.kep)

    def load_more(self):
        self.progressbar = customtkinter.CTkProgressBar(master=self.tab1, mode="indeterminate", indeterminate_speed=2,
                                                        height=3,
                                                        progress_color="#FF0000")
        self.progressbar.pack(fill=X, after=self.search_frame)
        self.progressbar.start()
        print("loading more")
        self.getResults(True)

    def new_search(self):
        children = self.scroll_f.winfo_children()
        for child in children:
            if children.index(child) != 0:
                child.destroy()
        self.progressbar = customtkinter.CTkProgressBar(master=self.tab1, mode="indeterminate", indeterminate_speed=2,
                                                        height=3,
                                                        progress_color="#FF0000")
        self.progressbar.pack(fill=X, after=self.search_frame)
        self.progressbar.start()
        self.conti_token = None
        print("new search")
        self.raw_results.clear()
        self.getResults(False)

        ""

    def askfolder(self):
        command = 'explorer.exe ' + "Downloads"
        os.system(command)

    def downloads_tab(self):
        self.tab3 = self.tabview.add("Downloads")
        fm = customtkinter.CTkFrame(self.tab3)
        fm.pack(fill=X)
        self.show_files = customtkinter.CTkButton(fm, text="Show Downloads", command=self.askfolder)
        self.show_files.pack(side=LEFT)
        self.downloads_scroll_view = customtkinter.CTkScrollableFrame(self.tab3, height=self.win_height * 3)
        self.downloads_scroll_view.pack(fill=X)

        """"""

    def setTab1(self):
        self.thumbnail_downloader = threading.Thread(target=self.thumbd)
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.pack(fill=BOTH)
        self.tab1 = self.tabview.add("Search")
        self.tabview._segmented_button.grid(sticky="W")
        self.search_frame = customtkinter.CTkFrame(self.tab1)
        self.search_frame.pack(fill=X)
        self.search_button = customtkinter.CTkButton(self.search_frame, text="Search",
                                                     command=self.new_search)
        self.search_button.pack(side=RIGHT)
        self.search_box = customtkinter.CTkEntry(self.search_frame)
        self.search_box.pack(fill=X)
        self.scroll_f = customtkinter.CTkScrollableFrame(self.tab1, height=self.winfo_screenheight())
        self.scroll_f.pack(fill=X)
        self.load_more = customtkinter.CTkButton(self.scroll_f, text="Load more", command=self.load_more)
        self.load_more.pack(fill=X)

        def caller(event):
            self.new_search()

        self.bind('<Return>', caller)

    def update_root(self):
        self.update()
        self.after(1000, self.update_root)


if __name__ == "__main__":
    app = App()
    app.mainloop()
