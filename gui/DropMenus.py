#this file contains all code for the drop down menus used by application.py

import tkinter as Tk
from functools import partial
#import tkinter.tkk as tkk
#from PyQt5.QtWidgets import QApplication, QLabel


class FileMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False, frame=None):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="Quit", command=self.quit)
        self.app_frame = frame
        self.open = False

    def updateMenu(self):
        print(f"updateMenu: {self.__class__}")

    def quit(self):
        self.app_frame.logFile.close()
        self.app_frame.quit()


class DeviceMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False, frame=None):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="Refresh Devices")
        self.app_frame = frame
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
    def __init__(self, parent, tearoff=False, frame=None):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="Connect Video", command=self.connectVideo)
        self.add_command(label="Disconnect Video", command=self.disconnectVideo)
        self.app_frame = frame
        self.open = False

    def updateMenu(self):
        print(f"updateMenu: {self.__class__}")

    def connectVideo(self):
        self.app_frame.player._Play(self.app_frame.video)


    def disconnectVideo(self):
        self.app_frame.player.OnStop()


class AudioMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False, frame=None, audioClient=None):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="Connect Audio", command=self.connectAudio)
        self.add_command(label="Disconnect Audio", command=self.disconnectAudio)
        self.add_command(label="Mute", command=self.mute)
        self.add_command(label="Unmute", command=self.unmute)
        self.app_frame = frame
        self.audioClient = audioClient
        self.muted = False
        self.open = False


    def updateMenu(self):
        pass
        #print(f"updateMenu: {self.__class__}")

    def connectAudio(self):
        self.audioClient.connect()
        if(not self.muted):
            self.audioClient.startStream(waitForConnect=True)
    
    def disconnectAudio(self):
        if(self.audioClient.isStreaming()):
            self.audioClient.stopStream()
        self.audioClient.disconnect()

    def mute(self):
        self.muted = True
        self.app_frame.displayMuteIcon()
        if(self.audioClient.isStreaming()):
            self.audioClient.stopStream()

    def unmute(self):
        self.muted = False
        self.app_frame.hideMuteIcon()
        if(not self.audioClient.isStreaming()):
            self.audioClient.startStream()



class AudioDeviceMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False, frame=None, audioClient=None):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.audioClient = audioClient
        self.app_frame = frame


        self.add_command(label='Refresh Devices', command=self.refreshDeviceList)
        self.add_separator()
        #add all devices
        for device in self.audioClient.getInputDeviceNames():
            self.add_command(label=device, command=partial(self.setDevice, device))

        self.setMenuSelection(self.audioClient.getCurrentDeviceName())



    def updateMenu(self):
        print(f"updateMenu: {self.__class__}")

    def refreshDeviceList(self):

        self.delete(2, Tk.END)
        with self.audioClient.refreshHandler():
            device_list = self.audioClient.getInputDeviceNames()
            if(self.audioClient.getCurrentDeviceName() not in device_list):
                self.audioClient.setDeviceDictToDefault()

        for device in device_list:    
            self.add_command(label=device, command=partial(self.setDevice, device))

        self.setMenuSelection(self.audioClient.getCurrentDeviceName())

        



    def setDevice(self, device_name):
        
        with self.audioClient.refreshHandler():
            self.audioClient.setInputDevice(device_name)

        self.setMenuSelection(self.audioClient.getCurrentDeviceName())

    def setMenuSelection(self, name):
        print("set selection")
        menuLen = self.index(Tk.END)
        for i in range(2, menuLen+1):
            self.entryconfigure(i, background='SystemButtonFace')
            if(self.entrycget(i, 'label') == name):
                self.entryconfigure(i, background='red')



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
