#this file contains all code for the drop down menus used by application.py

import tkinter as Tk
from functools import partial
import subprocess
import webbrowser
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
        self.app_frame.close_app()


class DeviceMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False, frame=None):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="Refresh Devices", command=self.refreshDevices)
        self.add_separator()
        self.app_frame = frame
        self.open = False

    def updateMenu(self):
        print(f"updateMenu: {self.__class__}")

    def refreshDevices(self):
        self.app_frame.device_menu.delete(2, Tk.END)
        self.app_frame.serial_arm_controller.update_devs()
        if not self.app_frame.serial_arm_controller.devs:
            self.add_command(label="No devices", state=Tk.DISABLED)
        else:
            for dev in self.app_frame.serial_arm_controller.devs:
                self.add_command(
                    label="{}: {}".format(dev[0], dev[1]),
                    command=lambda: self.connect(dev)
                )

    def connect(self, dev):
        '''
        Connects to the given device
        :param dev: The serial device to connect to
        '''

        self.app_frame.serial_arm_controller.connect(dev[0])
        self.add_command(
            label="Close Connection",
            command=self.close
        )

    def close(self):
        '''Closes the active serial connection'''

        self.delete(2 + len(self.app_frame.serial_arm_controller.devs))
        self.app_frame.serial_arm_controller.close()


class HelpMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="About Survivor Buddy 3.0", command=self.openSurvivorBuddyPage)
        self.add_command(label="User Manual", command=self.openUserManual)
        self.add_command(label="Programmer's Reference", command=self.openProgrammerRef)
        self.open = False

    def openSurvivorBuddyPage(self):
        webbrowser.open("http://survivorbuddy.cse.tamu.edu/")

    def openUserManual(self):
        webbrowser.open(
            "https://docs.google.com/document/d/1V6gmVehsxrlFoc5FzThtdTNSovUbyU03AUEBfnAclKA/edit?usp=sharing"
        )

    def openProgrammerRef(self):
        webbrowser.open(
            "https://drive.google.com/a/tamu.edu/file/d/1pMKci4BTCTu7H6GREmmWEmBEgZ4klQWn/view?usp=sharing"
        )

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
        self.add_command(
            label='Status: Disconnected', 
            foreground='white',
            background='grey',
            activeforeground='white',
            activebackground='grey',
            hidemargin=True,
            font='bold'
        )
        self.add_separator()

        self.add_command(label="Connect Audio", command=self.toggleConnect)
        self.add_command(label="Mute", command=self.toggleMute)
        self.app_frame = frame
        self.audioClient = audioClient
        self.muted = False
        self.open = False


    def updateMenu(self):
        
        if(self.audioClient.is_connected):
            self.entryconfigure(
                0,
                label='Status: Connected',
                foreground='black',
                background='green',
                activeforeground='black',
                activebackground='green',
            )
        else:
            self.entryconfigure(
                0,
                label='Status: Disconnected',
                foreground='white',
                background='grey',
                activeforeground='white',
                activebackground='grey',
            )


        #print(f"updateMenu: {self.__class__}")

    def toggleConnect(self):
        
        if(not self.audioClient.is_connected):
            self.connectAudio()
            self.entryconfigure(2, label='Disconnect Audio')

        else:
            self.disconnectAudio()
            self.entryconfigure(2, label='Connect Audio')


    def connectAudio(self):
        self.audioClient.connect()
        if(not self.muted):
            self.audioClient.startStream(waitForConnect=True)
    
    def disconnectAudio(self):
        if(self.audioClient.isStreaming()):
            self.audioClient.stopStream()
        self.audioClient.disconnect()

    def toggleMute(self):
        if(self.muted):
            self.unmute()
            self.entryconfigure(3, label='Mute')
        else:
            self.mute()
            self.entryconfigure(3, label='Unmute')

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
        self.add_command(label="Open Phone Mirroring", command=self.startMirror)
        self.open = False

    def updateMenu(self):
        print(f"updateMenu: {self.__class__}")

    def startMirror(self):

        subprocess.Popen(['scrcpy', '&'], shell=True)


class ScreenRecordMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False, frame=None, recorder=None):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)

        self.recorder = recorder
        self.app_frame = frame
        self.add_command(label="Start Screen Record", command=self.toggleRecord)
        self.add_command(
            label=f"Require File Password: {self.recorder.encrypt_bool}",
            command=self.toggleEncrypt
        )
        self.add_command(label="Set File Password", command=self.setPassword)
        
        self.open = False

    def updateMenu(self):
        print(f"updateMenu: {self.__class__}")

    def startRecording(self):
        self.recorder.startRecording()
        self.entryconfigure(0, label="Stop Recording Screen")

    def stopRecording(self):
        self.recorder.stopRecording()
        self.entryconfigure(0, label="Start Recording Screen")

    def toggleRecord(self):
        if(self.recorder.isRecording()):
            self.recorder.stopRecording()
            self.entryconfigure(0, label="Start Recording Screen")
        else:
            self.recorder.startRecording()
            self.entryconfigure(0, label="Stop Recording Screen")


    def toggleEncrypt(self):
        self.recorder.encrypt_bool = not self.recorder.encrypt_bool
        self.entryconfigure(
            1,
            label=f"Require File Password: {self.recorder.encrypt_bool}"
        )

    def chooseOuputFolder(self):
        #TODO:
        pass

    def setPassword(self):
        self.app_frame.popup_password()


class IpPortMenu(Tk.Menu):
    def __init__(self, parent, tearoff=False, frame=None):
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        
        self.app_frame = frame
        self.add_command(
            label=f"Set Audio Port: {self.app_frame.audio_port}", 
            command=partial(self.app_frame.popup_port, 'audio')
        )
        self.add_command(
            label=f"Set Message Port: {self.app_frame.message_port}", 
            command=partial(self.app_frame.popup_port, 'message')
        )
        self.add_command(
            label=f"Set Video Port: {self.app_frame.rtsp_port}", 
            command=partial(self.app_frame.popup_port, 'video')
        )
        self.add_command(
            label=f"Set Phone IP: {self.app_frame.host}", 
            command=self.app_frame.popup_ip
        )

    def updateMenu(self):
        print(f"updateMenu: {self.__class__}")

        self.entryconfigure(
            0, 
            label=f"Set Audio Port: {self.app_frame.audio_port}"
        )
        self.entryconfigure(
            1,
            label=f"Set Audio Port: {self.app_frame.message_port}"
        )
        self.entryconfigure(
            2,
            label=f"Set Audio Port: {self.app_frame.rtsp_port}"
        )
        self.entryconfigure(
            3,
            label=f"Set Audio Port: {self.app_frame.host}"
        )
