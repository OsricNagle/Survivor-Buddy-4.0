#this file contains all code for the drop down menus used by application.py

import tkinter as Tk
#import tkinter.tkk as tkk
#from PyQt5.QtWidgets import QApplication, QLabel


class FileMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        pass


class DeviceMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        pass


class HelpMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        pass


class VideoMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        pass


class AudioMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        Tk.Menu.__init__(self, parent, tearoff=tearoff, postcommand=self.updateMenu)
        self.add_command(label="Option 1")
        self.add_command(label="Option 2")


    def updateMenu(self):
        print(f"updateMenu: {AudioMenu.__name__}")



class AudioDeviceMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        pass

class PhoneMirrorMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        pass


class ScreenRecordMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        pass


class EncryptionMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        pass


class IpPortMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        pass
