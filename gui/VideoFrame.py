#Video frame class which handles display of the video from phone

import tkinter as Tk

from .tkvlc import Player



class VideoFrame(Tk.Frame):


    def __init__(self, master, **kwargs):

        #create frame
        Tk.Frame.__init__(master, **kwargs)

        self.config(
            width=400,
            height=800
        )

        self.pack()

        #default values
        self.phone_ip = '192.168.42.129'
        self.video_port = 1935
        self.video_url = f"rtsp://{self.phone_ip}:{self.video_port}/"

        #init player
        self.player = Player(self, video=self.video_url)


        







