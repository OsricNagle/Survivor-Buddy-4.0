# -*- coding: utf-8 -*-
import tkinter as Tk
from tkinter import filedialog

from .PositionFrame import PositionFrame, RenderDiagram, LabelScaleSpinbox, PositionUpdater
from .ControlButtons import ControlButtons
from .NotificationsFrame import NotificationFrame
from .StatusBar import StatusBar
from .SerialArmController import SerialArmController
from .SerialArmController import Command
from .ScreenRecord import ScreenRecorder
from datetime import datetime  # For log file formatting
from .BuddyMessageClient import BuddyMessageClient
from .tkvlc import Player
import os.path
import webbrowser
import subprocess
from .BuddyAudioClient import BuddyAudioClient
from functools import partial


from .DropMenus import *



import threading
# import appscript  # added this


class Application(Tk.Frame):
    '''The main GUI class'''


    def __init__(self, master, **kwargs):
        '''
        The constructor for the Application class
        :param master: the Tk parent widget
        '''


        super().__init__(master, **kwargs)
        self.theroot = master
        self.pack()
        #self.place()
        self.taskbar_icon = Tk.PhotoImage(file="gui/SBLogo.png")
        self.master.call('wm', 'iconphoto', self.master._w, self.taskbar_icon)
        self.config(padx=16, pady=16)

        #instantiating screen recorder
        self.screen_record = ScreenRecorder()

        try:
            os.mkdir(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')+'\\'+'screen_recordings\\')
        except OSError as error:
            print(error)

        self.screen_record.setOutputFolder(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')+'\\'+'screen_recordings\\')

        #default ip and port of the servers running on the phone
        self.host = '192.168.42.129'
        self.audio_port = 5050
        self.rtsp_port = 1935
        self.message_port = 8080


        #init video objects
        self.video_url = f"rtsp://{self.host}:{self.rtsp_port}/"
        self.player = Player(self.master, video=self.video_url)

        #init PC->Phone Audio objs
        self.mbac = BuddyAudioClient(self.host, self.audio_port)
        self.microphone = ""
        self.keep_audio_on = False

        #init PC->Phone text message objs
        self.bmc = BuddyMessageClient(
            self.host, 
            self.message_port, 
            self.master
        )

        #creating stuff for the log file
        now = datetime.now()  # Create unique logfile for notifications and errors
        timestamp = now.strftime("%m_%d_%Y_%H_%M_%S")
        file_name = 'LOGFILE_' + timestamp + '.txt'
        self.logFile = open(os.path.join('./logs/', file_name), 'w+')

        # need the status bar to give to the arm controller
        self.status_bar = StatusBar(self)
        self.notifications_frame = NotificationFrame(self, self.logFile)

        self.serial_arm_controller = SerialArmController(self.status_bar, self.notifications_frame)

        self.menu_bar = Tk.Menu(self)

        self.device_arr = self.mbac.getInputDeviceNames()
        self.create_menu(self.menu_bar)

        wrapper_frame = Tk.Frame(self)
        wrapper_frame.pack(side="left")

        top_frame = Tk.Frame(wrapper_frame)
        top_frame.pack(fill="x")


        middle_frame = Tk.Frame(wrapper_frame)
        middle_frame.pack()


        bottom_frame = Tk.Frame(wrapper_frame)
        bottom_frame.pack(fill="x")

        text_frame = Tk.Frame(wrapper_frame)
        text_frame.pack(fill="x")
        self.mute_image = Tk.PhotoImage(file="gui/mute.png")
        self.mute_label = Tk.Label(text_frame, image=self.mute_image)
        #self.mute_label.pack(side="left")
        self.record_image = Tk.PhotoImage(file="gui/recordingbutton.png")
        self.record_label = Tk.Label(text_frame, image=self.record_image)
        
        # textbox = Tk.ttk.Label(root, text="text")
        # textbox.place(x=800, y=300)
        self.name = Tk.StringVar()
        self.nameEntered = Tk.ttk.Entry(text_frame, width=15, textvariable=self.name)
        self.send_button = Tk.ttk.Button(text_frame, text="send text", command=self.send_text)
        self.send_button.pack(side='right')
        self.nameEntered.pack(side='right')
        # down_button = Tk.ttk.Button(self.bottom_frame,
        #                          text="Move down")
        # down_button.pack(side="top")

        self.position_frame = PositionFrame(self, self.serial_arm_controller, self.logFile, top_frame, middle_frame, bottom_frame, self.theroot, self.host)
        self.position_frame.pack(fill="x")

        self.control_buttons = ControlButtons(self, self.serial_arm_controller, self.notifications_frame)
        self.control_buttons.pack(fill="x")
        self.status_bar.pack(fill="x")
        self.notifications_frame.pack(fill="x")

        self.master.config(menu=self.menu_bar)

    def send_text(self):
        self.bmc.sendMsg(self.name.get())

    def close_app(self):  # Had to make new quit function to close file
        '''Closes the GUI application'''

        self.logFile.close()

        if(self.mbac.isStreaming()):
            self.mbac.stopStream()
            self.mbac.disconnect()


        self.quit()


    def hideMuteIcon(self):
        self.mute_label.pack_forget()

    def displayMuteIcon(self):
        self.mute_label.pack(side='left')

    def displayRecordIcon(self):
        self.record_label.pack(side='left')

    def hideRecordIcon(self):
        self.record_label.pack_forget()

    def set_password(self, password):
        self.screen_record.setPassword(password.get())
        self.popup.destroy()

    def popup_password(self):
        self.popup = Tk.Toplevel()
        self.popup.wm_title("Set Password")
        password = Tk.StringVar()
        password_entered = Tk.ttk.Entry(self.popup, width=15, textvariable=password)
        set_button = Tk.ttk.Button(self.popup, text="Set Password", command=partial(self.set_password, password))
        password_entered.pack()
        set_button.pack()
        self.popup.geometry("250x100")

    def set_video_port(self, port):
        self.rtsp_port = port
        self.video_url = f"rtsp://{self.host}:{self.rtsp_port}/"
        self.port_popup.destroy()

    def set_ip(self, ip):
        self.host = ip.get()
        self.video_url = f"rtsp://{self.host}:{self.rtsp_port}/"
        print(self.video_url)
        self.ip_popup.destroy()

    def set_port(self, device_type, port):
        if device_type == 'audio':
            port_num = int(port.get())
            self.mbac.setPortNum(port_num)
            self.audio_port = port_num
            print(self.mbac.port_num)

        elif device_type == 'video':
            port_num = int(port.get())
            self.set_video_port(port_num)
        elif device_type == 'message':
            port_num = int(port.get())
            self.bmc.setPortNum(port_num)
            self.message_port = port_num
        self.port_popup.destroy()


    def popup_ip(self):
        self.ip_popup = Tk.Toplevel()
        self.ip_popup.wm_title("Set ip")
        ip = Tk.StringVar()
        ip_entered = Tk.ttk.Entry(self.ip_popup, width=15, textvariable=ip)
        ip_entered.insert(Tk.END, self.host)
        set_button = Tk.ttk.Button(self.ip_popup, text="Set ip", command=partial(self.set_ip, ip))
        ip_entered.pack()
        set_button.pack()
        self.ip_popup.geometry("250x100")

    def popup_port(self, device_type):
        self.port_popup = Tk.Toplevel()
        self.port_popup.wm_title("Set " + device_type + " port")
        port = Tk.StringVar()
        port_entered = Tk.ttk.Entry(self.port_popup, width=15, textvariable=port)

        if(device_type == 'audio'):
            port_entered.insert(Tk.END, self.audio_port)
        elif(device_type == 'video'):
            port_entered.insert(Tk.END, self.rtsp_port)
        elif(device_type == 'message'):
            port_entered.insert(Tk.END, self.message_port)
        else:
            print("ERROR")



        set_button = Tk.ttk.Button(self.port_popup, text="Set " + device_type + " port", command=partial(self.set_port, device_type, port))
        port_entered.pack()
        set_button.pack()
        self.port_popup.geometry("250x100")

    def displayFileDialog(self):
        return filedialog.askdirectory()

    def showPopupMessage(self, title="Suvivor Buddy 4.0", msg_text="CONTENT"):
        popup = Tk.Toplevel()
        popup.wm_title(title)
        
        msg = Tk.Message(
            popup, 
            text=msg_text,
            aspect=3000
        )
        msg.pack()

        dismiss_button = Tk.Button(popup, text='Dismiss', command=popup.destroy)
        dismiss_button.pack()

        w = self.theroot.winfo_x() + 100
        h = self.theroot.winfo_y() + 100

        popup.geometry(f"+{w}+{h}")



    def updateMenuOptions(self, event):
        '''
        Callback function to update the drop down menus
        '''

        activeMenuIndex = self.theroot.call(event.widget, 'index', 'active')

        if isinstance(activeMenuIndex, int):
            activeMenu = self.menu_bar.winfo_children()[activeMenuIndex - 1]

            if not activeMenu.open:
                activeMenu.updateMenu()
                activeMenu.open = True

        else:
            for menuWidget in self.menu_bar.winfo_children():
                menuWidget.open = False


    def create_menu(self, root_menu):
        '''
        Creates the main GUI menu
        :param root_menu: The root menu (self.menu_bar) that is instantiated in create_widgets()
        '''

        # File Menu
        self.file_menu = FileMenu(root_menu, tearoff=False, frame=self)
        root_menu.add_cascade(label="File", menu=self.file_menu)

        # Device Menu
        self.device_menu = DeviceMenu(root_menu, tearoff=False, frame=self)
        root_menu.add_cascade(label="Device", menu=self.device_menu)

        # Help Menu
        self.help_menu = HelpMenu(root_menu, tearoff=False)
        root_menu.add_cascade(label="Help", menu=self.help_menu)

        #Video Menu
        self.video_menu = VideoMenu(root_menu, tearoff=0, frame=self)
        root_menu.add_cascade(label="Video", menu=self.video_menu)

        #Audio Menu
        self.audio_menu = AudioMenu(
            root_menu, 
            tearoff=0, 
            frame=self, 
            audioClient=self.mbac
        )

        root_menu.add_cascade(label="Unmute/Mute", menu=self.audio_menu)

        #Audio Devices
        self.audio_devices_menu = AudioDeviceMenu(
            root_menu, 
            tearoff=False, 
            frame=self,
            audioClient=self.mbac
        )
        root_menu.add_cascade(label="Audio Devices", menu=self.audio_devices_menu)

        #Phone Mirroring
        self.phone_mirroring_menu = PhoneMirrorMenu(root_menu, tearoff=False)
        root_menu.add_cascade(label="Phone Mirroring", menu=self.phone_mirroring_menu)

        #Screen Record
        self.screen_record_menu = ScreenRecordMenu(
            root_menu, 
            tearoff=False, 
            frame=self,
            recorder=self.screen_record
        )
        root_menu.add_cascade(label="Screen Record", menu=self.screen_record_menu)

        #Set IP and Ports
        self.set_ip_port_menu = IpPortMenu(root_menu, tearoff=False, frame=self)
        root_menu.add_cascade(label="Set IP/Port", menu=self.set_ip_port_menu)

        root_menu.bind("<<MenuSelect>>", self.updateMenuOptions)


if __name__ == "__main__":
    root = Tk.Tk()

    root.geometry("1250x1080")
    app = Application(master=root)

    app.master.title("Survivor Buddy 4.0")
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    app.mainloop()
