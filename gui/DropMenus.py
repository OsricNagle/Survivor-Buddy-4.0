"""
Contains all the drop down menus in the top bar for GUI
"""

import tkinter as Tk
from functools import partial
import subprocess
import webbrowser
#import tkinter.tkk as tkk
#from PyQt5.QtWidgets import QApplication, QLabel
from .headPose import behaviorTracking


class FileMenu(Tk.Menu):
    """
    File menu on main GIU. Contains quit funtion to kill application.

    :param parent: the tkinter parent menu
    :type parent: Tkinter Menu
    :param tearoff: if true the menu can be pulled from it location on gui an dragged around. Defaults to False.
    :type tearoff: boolean, optional
    :param frame: the tkinter frame on which GUI functions can be called. Defaults to None
    :type: Tkinter Frame, optional
    """
    def __init__(self, parent, tearoff=False, frame=None):
        """
        Constructor for FileMenu
        """
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="Quit", command=self.quit)
        self.app_frame = frame
        self.open = False

    def updateMenu(self):
        """
        Called whenever menu is opened. Currenty unused but required.
        """
        print(f"updateMenu: {self.__class__}")

    def quit(self):
        """
        Shuts down the application.
        """
        self.app_frame.close_app()


class DeviceMenu(Tk.Menu):
    """
    Device menu on main GIU. Used to display arduino devices and connect to them.

    :param parent: the tkinter parent menu
    :type parent: Tkinter Menu
    :param tearoff: if true the menu can be pulled from it location on gui an dragged around. Defaults to False.
    :type tearoff: boolean, optional
    :param frame: the tkinter frame on which GUI functions can be called. Defaults to None
    :type: Tkinter Frame, optional
    """
    def __init__(self, parent, tearoff=False, frame=None):
        """
        Constructor for DeviceMenu
        """
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="Refresh Devices", command=self.refreshDevices)
        self.add_separator()
        self.app_frame = frame
        self.open = False

    def updateMenu(self):
        """
        Called whenever menu is opened. Currenty unused but required.
        """
        print(f"updateMenu: {self.__class__}")

    def refreshDevices(self):
        """
        Checks for USB connected arduino devices and displays them on menu in list form. Will show "No Devices" if none found.
        """
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
    """
    Help menu on main GIU. Contains links to helpful documentation about the application.

    :param parent: the tkinter parent menu
    :type parent: Tkinter Menu
    :param tearoff: if true the menu can be pulled from it location on gui an dragged around. Defaults to False.
    :type tearoff: boolean, optional
    """
    def __init__(self, parent, tearoff=False):
        """
        Constructor for HelpMenu
        """
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="About Survivor Buddy 3.0", command=self.openSurvivorBuddyPage)
        self.add_command(label="User Manual", command=self.openUserManual)
        self.add_command(label="Programmer's Reference", command=self.openProgrammerRef)
        self.open = False

    def openSurvivorBuddyPage(self):
        """
        Opens SurvivorBuddy info page in web browser
        """
        webbrowser.open("http://survivorbuddy.cse.tamu.edu/")

    def openUserManual(self):
        """
        Opens survivror buddy user manual in web browser
        """
        webbrowser.open(
            "https://docs.google.com/document/d/1V6gmVehsxrlFoc5FzThtdTNSovUbyU03AUEBfnAclKA/edit?usp=sharing"
        )

    def openProgrammerRef(self):
        """
        Opens survivor buddy programmer's manual in web browser
        """
        webbrowser.open(
            "https://drive.google.com/a/tamu.edu/file/d/1pMKci4BTCTu7H6GREmmWEmBEgZ4klQWn/view?usp=sharing"
        )

    def updateMenu(self):
        """
        Called whenever menu is opened. Currenty unused but required.
        """
        print(f"updateMenu: {self.__class__}")


class VideoMenu(Tk.Menu):
    """
    Video menu on main GIU. Contains functions to start and stop reception/display of audio/video stream from
    SurvivorBuddy Mobile App.

    :param parent: the tkinter parent menu
    :type parent: Tkinter Menu
    :param tearoff: if true the menu can be pulled from it location on gui an dragged around. Defaults to False.
    :type tearoff: boolean, optional
    :param frame: the tkinter frame on which GUI functions can be called. Defaults to None
    :type: Tkinter Frame, optional
    """
    def __init__(self, parent, tearoff=False, frame=None):
        """
        Constructor for VideoMenu
        """
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="Connect Video", command=self.connectVideo)
        self.add_command(label="Disconnect Video", command=self.disconnectVideo)
        self.app_frame = frame
        self.open = False

    def updateMenu(self):
        """
        Called whenever menu is opened. Currenty unused but required.
        """
        print(f"updateMenu: {self.__class__}")

    def connectVideo(self):
        """
        Begins the connection and display/output of video/audio content from Survivor Buddy RTSP server
        """
        self.app_frame.player._Play(self.app_frame.video_url)


    def disconnectVideo(self):
        """
        Stops the video/audio display
        """
        self.app_frame.player.OnStop()


class AudioMenu(Tk.Menu):
    """
    Audio menu on main GIU. Contains functions to connect/disconnect to audio server and mute/unmute audio input.

    :param parent: the tkinter parent menu
    :type parent: Tkinter Menu
    :param tearoff: if true the menu can be pulled from it location on gui an dragged around. Defaults to False.
    :type tearoff: boolean, optional
    :param frame: the tkinter frame on which GUI functions can be called. Defaults to None
    :type: Tkinter Frame, optional
    :param audioClient: The BuddyAudioClient used to stream outgoing audio. Defaults to None
    :type autioClient: BuddyAudioClient, optional
    """
    def __init__(self, parent, tearoff=False, frame=None, audioClient=None):
        """
        Constructor for AudioMenu
        """
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
        """
        Called when menu is opened. Updated the displayed connection status and button names in menu.
        """
        
        if(self.audioClient.is_connected):
            self.entryconfigure(
                0,
                label='Status: Connected',
                foreground='black',
                background='green',
                activeforeground='black',
                activebackground='green',
            )
            self.entryconfigure(2, label='Disconnect Audio')
        else:
            self.entryconfigure(
                0,
                label='Status: Disconnected',
                foreground='white',
                background='grey',
                activeforeground='white',
                activebackground='grey',
            )
            self.entryconfigure(2, label='Connect Audio')

    def toggleConnect(self):
        """
        Toggles the connect/diconnect of the audio client based on current status. Will connect if not connected and diconnect
        if currently connected
        """
        
        if(not self.audioClient.is_connected):
            self.connectAudio()
            self.entryconfigure(2, label='Disconnect Audio')

        else:
            self.disconnectAudio()
            self.entryconfigure(2, label='Connect Audio')


    def connectAudio(self):
        """
        Connects to audio server and starts sending audio if not muted.
        """
        self.audioClient.connect()
        if(not self.muted):
            self.audioClient.startStream(waitForConnect=True)
    
    def disconnectAudio(self):
        """
        Disconnects from audio server and stop sending audio
        """
        if(self.audioClient.isStreaming()):
            self.audioClient.stopStream()
        self.audioClient.disconnect()

    def toggleMute(self):
        """
        Toggle mute/unmute based on current status. Will mute if not muted. And unmute if muted.
        """
        if(self.muted):
            self.unmute()
            self.entryconfigure(3, label='Mute')
        else:
            self.mute()
            self.entryconfigure(3, label='Unmute')

    def mute(self):
        """
        Stops sending audio data to server
        """
        self.muted = True
        self.app_frame.displayMuteIcon()
        if(self.audioClient.isStreaming()):
            self.audioClient.stopStream()


    def unmute(self):
        """
        Starts sending audio data to server
        """
        self.muted = False
        self.app_frame.hideMuteIcon()
        if(not self.audioClient.isStreaming()):
            self.audioClient.startStream()



class AudioDeviceMenu(Tk.Menu):
    """
    Audio Device menu on main GIU. Allows user to choose the current audio device. Also allows for manual refresh of
    device list for when new audio devices are connected/disconnected

    :param parent: the tkinter parent menu
    :type parent: Tkinter Menu
    :param tearoff: if true the menu can be pulled from it location on gui an dragged around. Defaults to False.
    :type tearoff: boolean, optional
    :param frame: the tkinter frame on which GUI functions can be called. Defaults to None
    :type: Tkinter Frame, optional
    :param audioClient: The BuddyAudioClient used to stream outgoing audio and get current devices. Defaults to None
    :type autioClient: BuddyAudioClient, optional
    """
    def __init__(self, parent, tearoff=False, frame=None, audioClient=None):
        """
        Constructor for AudioDeviceMenu
        """
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
        """
        Called whenever menu is opened. Currenty unused but required.
        """
        print(f"updateMenu: {self.__class__}")

    def refreshDeviceList(self):
        """
        Checks for any newly connected or diconnected devices and updates the list of devices in menu.
        """
        self.delete(2, Tk.END)
        with self.audioClient.refreshHandler():
            device_list = self.audioClient.getInputDeviceNames()
            if(self.audioClient.getCurrentDeviceName() not in device_list):
                self.audioClient.setDeviceDictToDefault()

        for device in device_list:    
            self.add_command(label=device, command=partial(self.setDevice, device))

        self.setMenuSelection(self.audioClient.getCurrentDeviceName())

    def setDevice(self, device_name):
        """
        Sets the current audio input device in BuddyAudioClient

        :param device_name: name of device
        :type device_name: String
        """
        with self.audioClient.refreshHandler():
            self.audioClient.setInputDevice(device_name)

        self.setMenuSelection(self.audioClient.getCurrentDeviceName())

    def setMenuSelection(self, name):
        """
        Changes the color of the currently selected input device in the menu to red. Other will be system default.

        :param name: the name of the selected device
        :type name: String
        """
        print("set selection")
        menuLen = self.index(Tk.END)
        for i in range(2, menuLen+1):
            self.entryconfigure(i, background='SystemButtonFace')
            if(self.entrycget(i, 'label') == name):
                self.entryconfigure(i, background='red')



class PhoneMirrorMenu(Tk.Menu):
    """
    Phone Mirroring menu on main GIU. Allows user to start the scrcpy phone mirroring software.

    :param parent: the tkinter parent menu
    :type parent: Tkinter Menu
    :param tearoff: if true the menu can be pulled from it location on gui an dragged around. Defaults to False.
    :type tearoff: boolean, optional
    :param frame: the tkinter frame on which GUI functions can be called. Defaults to None
    :type: Tkinter Frame, optional
    """
    def __init__(self, parent, tearoff=False):
        """
        Constructor for PhoneMirrorMenu
        """
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="Open Phone Mirroring", command=self.startMirror)
        self.open = False

    def updateMenu(self):
        """
        Called whenever menu is opened. Currenty unused but required.
        """
        print(f"updateMenu: {self.__class__}")

    def startMirror(self):
        """
        Starts the scrcpy phone mirror process.
        """
        subprocess.Popen(['scrcpy', '&'], shell=True)


class ScreenRecordMenu(Tk.Menu):
    """
    Screen Record menu on main GIU. Allows user to start/stop screen recording and set options pertaining to that.

    :param parent: the tkinter parent menu
    :type parent: Tkinter Menu
    :param tearoff: if true the menu can be pulled from it location on gui an dragged around. Defaults to False.
    :type tearoff: boolean, optional
    :param frame: the tkinter frame on which GUI functions can be called. Defaults to None
    :type: Tkinter Frame, optional
    :param recorder: The ScreenRecorder instance to be used. Defaults to None
    :type recorder: ScreenRecorder, optional
    """
    def __init__(self, parent, tearoff=False, frame=None, recorder=None):
        """
        Constructor for ScreenRecordMenu
        """
        Tk.Menu.__init__(self, parent, tearoff=tearoff)

        self.recorder = recorder
        self.app_frame = frame
        self.add_command(label="Start Screen Record", command=self.toggleRecord)
        self.add_command(
            label=f"Require File Password: {self.recorder.encrypt_bool}",
            command=self.toggleEncrypt
        )
        self.add_command(label="Set File Password", command=self.setPassword)
        self.add_command(label='Change Output Folder', command=self.changeOuputFolder)
        
        self.open = False

    def updateMenu(self):
        """
        Called whenever menu is opened. Currenty unused but required.
        """
        print(f"updateMenu: {self.__class__}")

    def startRecording(self):
        """
        Starts the desktop screen recording
        """
        self.recorder.startRecording()
        self.entryconfigure(0, label="Stop Recording Screen")
        self.app_frame.displayRecordIcon()

    def stopRecording(self):
        """
        Stops the desktop screen recording. Displays a pop-up message with info about the file.
        """
        self.recorder.stopRecording()
        self.entryconfigure(0, label="Start Recording Screen")
        self.app_frame.hideRecordIcon()
        msg = "Screen Recording Stopped:\n"
        if(self.recorder.encrypt_bool):
            msg += f"File saved to: {self.recorder.zip_path}\n"
            msg += f"With Password: {self.recorder.file_password}\n"
            msg += f"Reminder: This is the only time the password will be shown"
        else:
            msg += f"File saved to: {self.recorder.current_recording_path}"
        self.app_frame.showPopupMessage(
            msg_text=msg
        )

    def toggleRecord(self):
        """
        Toggle function for starting/stopping recording
        """
        if(self.recorder.isRecording()):
            self.stopRecording()
        else:
            self.startRecording()


    def toggleEncrypt(self):
        """
        Toggles on/off file encryption for recordings
        """
        self.recorder.encrypt_bool = not self.recorder.encrypt_bool
        self.entryconfigure(
            1,
            label=f"Require File Password: {self.recorder.encrypt_bool}"
        )

    def changeOuputFolder(self):
        """
        Opens file dialog to select and change output folder of recordings
        """
        folder_path = self.app_frame.displayFileDialog()
        print(f"FP: {folder_path}")
        self.recorder.setOutputFolder(folder_path)

    def setPassword(self):
        """
        Opens a pop-up which asks for input of new recordings password
        """
        self.app_frame.password_popup()


class IpPortMenu(Tk.Menu):
    """
    IP/Port menu on main GIU. Allows user to change the IP/port settings for connecting to the various servers.

    :param parent: the tkinter parent menu
    :type parent: Tkinter Menu
    :param tearoff: if true the menu can be pulled from it location on gui an dragged around. Defaults to False.
    :type tearoff: boolean, optional
    :param frame: the tkinter frame on which GUI functions can be called. Defaults to None
    :type: Tkinter Frame, optional
    """
    def __init__(self, parent, tearoff=False, frame=None):
        """
        Constructor for IpPortMenu
        """
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        
        self.app_frame = frame
        
        self.add_command(
            label=f"Set Video Port: {self.app_frame.rtsp_port}", 
            command=partial(self.app_frame.popup_port, 'video')
        )
        self.add_command(
            label=f"Set Audio Port: {self.app_frame.audio_port}",
            command=partial(self.app_frame.popup_port, 'audio')
        )
        self.add_command(
            label=f"Set Message Port: {self.app_frame.message_port}",
            command=partial(self.app_frame.popup_port, 'message')
        )
        self.add_command(
            label=f"Set Phone IP: {self.app_frame.host}", 
            command=self.app_frame.popup_ip
        )

    def updateMenu(self):
        """
        Called whenever menu is opened. Updates the menu button labels to show current port/ip values
        """
        print(f"updateMenu: {self.__class__}")

        self.entryconfigure(
            0, 
            label=f"Set Video Port: {self.app_frame.rtsp_port}"
        )
        self.entryconfigure(
            1,
            label=f"Set Audio Port: {self.app_frame.audio_port}"
        )
        self.entryconfigure(
            2,
            label=f"Set Message Port: {self.app_frame.message_port}"
        )
        self.entryconfigure(
            3,
            label=f"Set Phone IP: {self.app_frame.host}"
        )

class BehaviorTrackingMenu(Tk.Menu):
    """
    Behavior tracking menu on main GIU. Contains run function to trigger behavior mode.

    :param parent: the tkinter parent menu
    :type parent: Tkinter Menu
    :param tearoff: if true the menu can be pulled from it location on gui an dragged around. Defaults to False.
    :type tearoff: boolean, optional
    :param frame: the tkinter frame on which GUI functions can be called. Defaults to None
    :type: Tkinter Frame, optional
    """
    def __init__(self, parent, tearoff=False, frame=None):
        """
        Constructor for FileMenu
        """
        Tk.Menu.__init__(self, parent, tearoff=tearoff)
        self.add_command(label="Begin", command=self.begin)
        self.app_frame = frame
        self.open = False

    def updateMenu(self):
        """
        Called whenever menu is opened. Currenty unused but required.
        """
        print(f"updateMenu: {self.__class__}")

    def begin(self):
        """
        TESTING: print out hello world
        """
        print("beginning headPose functionality")
        # self.app_frame.serial_arm_controller
        behaviorTracking(self.app_frame.serial_arm_controller)
