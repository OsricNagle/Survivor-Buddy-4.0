#this file contains all code for the drop down menus used by application.py

import tkinter as Tk
#import tkinter.tkk as tkk
#from PyQt5.QtWidgets import QApplication, QLabel


class FileMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="Quit")
        self.open = False

    def updateMenu(self):
        print(f"updateMenu: {self.__class__}")


class DeviceMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="Refresh Devices")
        self.open = False

    def updateMenu(self):
        print(f"updateMenu: {self.__class__}")


class HelpMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="About Survivor Buddy 3.0")
        self.add_command(label="User Manual")
        self.add_command(label="Programmer's Reference")
        self.open = False

    def updateMenu(self):
        print(f"updateMenu: {self.__class__}")


class VideoMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="Connect Video")
        self.add_command(label="Disconnect Video")
        self.open = False

    def updateMenu(self):
        print(f"updateMenu: {self.__class__}")


class AudioMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="Audio Option 1")
        self.add_command(label="Audio Option 2")
        self.open = False


    def updateMenu(self):
        print(f"updateMenu: {self.__class__}")



class AudioDeviceMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        #TODO: Needs different things

    def updateMenu(self):
        print(f"updateMenu: {self.__class__}")

    def refreshDeviceList(self):
        pass

class PhoneMirrorMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="Open Phone Mirroring")
        self.open = False

    def updateMenu(self):
        print(f"updateMenu: {self.__class__}")


class ScreenRecordMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="Start Screen Record")
        self.add_command(label="Stop Screen Record")
        self.open = False

    def updateMenu(self):
        print(f"updateMenu: {self.__class__}")


class EncryptionMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="Set Password")
        self.add_command(label="Turn Encryption On")
        self.open = False

    def updateMenu(self):
        print(f"updateMenu: {self.__class__}")


class IpPortMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        #TODO: Different

    def updateMenu(self):
        print(f"updateMenu: {self.__class__}")
