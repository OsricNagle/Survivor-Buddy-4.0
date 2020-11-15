# -*- coding: utf-8 -*-
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from PyQt5.QtWidgets import QApplication, QLabel
from .PositionFrame import *
from .ControlButtons import *
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
from functools import *


from .DropMenus import *



import threading
# import appscript  # added this


class Application(tk.Frame):
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
        self.taskbar_icon = tk.PhotoImage(file="gui/SBLogo.png")
        self.master.call('wm', 'iconphoto', self.master._w, self.taskbar_icon)
        self.config(padx=16, pady=16)

        #instantiating screen recorder
        self.screen_record = ScreenRecorder()

        try:
            os.mkdir(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')+'\\'+'screen_recordings\\')
        except OSError as error:
            print(error)

        self.screen_record.setOutputFolder(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')+'\\'+'screen_recordings\\')

        #instantiating things for the Audio client and the text client
        self.host = '192.168.42.129'
        self.audio_port = 5050
        self.rtsp_port = 1935
        self.serverString = f"rtsp://{self.host}:{self.rtsp_port}/"
        self.video = expanduser(self.serverString)
        self.player = 0
        self.create_video_frame()
        self.mbac = BuddyAudioClient(self.host, self.audio_port)
        self.microphone = ""
        self.keep_audio_on = False

        self.message_port = 8080
        self.bmc = BuddyMessageClient(
            self.host, self.message_port, self.master)

        #creating stuff for the log file
        now = datetime.now()  # Create unique logfile for notifications and errors
        timestamp = now.strftime("%m_%d_%Y_%H_%M_%S")
        file_name = 'LOGFILE_' + timestamp + '.txt'
        #self.logFile = open(os.path.join(os.path.realpath('../logs/'), file_name), 'w+')  # Save logfile to log folder
        self.logFile = open(os.path.join('./logs/', file_name), 'w+')

        # need the status bar to give to the arm controller
        self.status_bar = StatusBar(self)
        self.notifications_frame = NotificationFrame(self, self.logFile)

        self.serial_arm_controller = SerialArmController(self.status_bar, self.notifications_frame)

        self.menu_bar = tk.Menu(self)

        self.device_arr = self.mbac.getInputDeviceNames()
        self.create_menu(self.menu_bar)

        wrapper_frame = Frame(self)
        wrapper_frame.pack(side="left")

        top_frame = Frame(wrapper_frame)
        top_frame.pack(fill="x")

        # up_button = ttk.Button(self.top_frame,
        #                        text="Move up")
        # up_button.pack(side="top")

        middle_frame = Frame(wrapper_frame)
        middle_frame.pack()

        # left_button = ttk.Button(self.middle_frame,
        #                          text="Move left")
        # left_button.pack(side="left")

        # right_button = ttk.Button(self.middle_frame,
        #                           text="Move right")
        # right_button.pack(side="left")

        bottom_frame = Frame(wrapper_frame)
        bottom_frame.pack(fill="x")

        text_frame = Frame(wrapper_frame)
        text_frame.pack(fill="x")
        self.mute_image = tk.PhotoImage(file="gui/mute.png")
        self.mute_label = tk.Label(text_frame, image=self.mute_image)
        #self.mute_label.pack(side="left")
        self.record_image = tk.PhotoImage(file="gui/recordingbutton.png")
        self.record_label = tk.Label(text_frame, image=self.record_image)
        
        # textbox = ttk.Label(root, text="text")
        # textbox.place(x=800, y=300)
        self.name = tk.StringVar()
        self.nameEntered = ttk.Entry(text_frame, width=15, textvariable=self.name)
        self.send_button = ttk.Button(text_frame, text="send text", command=self.send_text)
        self.send_button.pack(side='right')
        self.nameEntered.pack(side='right')
        # down_button = ttk.Button(self.bottom_frame,
        #                          text="Move down")
        # down_button.pack(side="top")

        self.position_frame = PositionFrame(self, self.serial_arm_controller, self.logFile, top_frame, middle_frame, bottom_frame, self.theroot, self.host)
        self.position_frame.pack(fill="x")

        self.control_buttons = ControlButtons(self, self.serial_arm_controller, self.notifications_frame)
        self.control_buttons.pack(fill="x")
        self.status_bar.pack(fill="x")
        self.notifications_frame.pack(fill="x")



        self.master.config(menu=self.menu_bar)
        # self.button = tk.Button(self, text="Create new window",
        #                         command=self.create_window)
        # self.button.pack(side="right")

    def send_text(self):
        self.bmc.sendMsg(self.name.get())


    #
    # def start_move_up(self):
    #     pos = self.serial_arm_controller.recv()
    #
    #     if pos:
    #         pitch = int[pos[0]]
    #         print(pitch)
    #         if pitch < 90:
    #             self.serial_arm_controller.set_pitch(pos[0])
    #         else:
    #             self.notifications_frame.append_line("already at max pitch")

        # global running
        # running = True

    # def stop_move_up(self):
    # def move_up(self):
    #     pos = self.serial_arm_controller.recv()
    #     if pos:
    #         self.up_counter = int(pos[0])
    #         self.up_counter = self.up_counter + 1
    #         print(self.up_counter)




    # def create_widgets(self):
        '''Creates the widgets seen in the GUI'''

        # self.menu_bar = tk.Menu(self)
        # self.create_menu(self.menu_bar)
        #
        # self.top_frame = Frame(self)
        # self.top_frame.pack(fill="x")
        #
        # up_button = ttk.Button(self.top_frame,
        #     text="Move up")
        # up_button.pack(side="top")
        #
        # self.middle_frame = Frame(self)
        # self.middle_frame.pack(fill="x")
        #
        # left_button = ttk.Button(self.middle_frame,
        #     text="Move left")
        # left_button.pack(side="left")
        #
        #
        # videoFrame = Frame(self.middle_frame, height = 400, width = 600, bg = 'grey')
        # videoFrame.pack(side='left', expand = True, pady = 5)
        #
        # right_button = ttk.Button(self.middle_frame,
        #                          text="Move right")
        # right_button.pack(side="left")
        #
        # self.bottom_frame = Frame(self)
        # self.bottom_frame.pack(fill="x")
        #
        # down_button = ttk.Button(self.bottom_frame,
        #                           text="Move down")
        # down_button.pack(side="top")
        #
        # self.position_frame = PositionFrame(self, self.serial_arm_controller, self.logFile)
        # self.position_frame.pack(fill="x")
        #
        # self.control_buttons = ControlButtons(self, self.serial_arm_controller, self.notifications_frame)
        # self.control_buttons.pack(fill="x")
        #
        # self.notifications_frame.pack(fill="x")
        #
        # self.status_bar.pack(fill="x")
        #
        # self.master.config(menu=self.menu_bar)

    def close_app(self):  # Had to make new quit function to close file
        '''Closes the GUI application'''

        self.logFile.close()
        self.quit()


    def hideMuteIcon(self):
        self.mute_label.pack_forget()

    def displayMuteIcon(self):
        self.mute_label.pack(side='left')

    def create_video_frame(self):
        # videoFrame = tk.Frame(middle_frame, height=400, width=600, bg='grey')
        # videoFrame.pack(side='left', expand=True, pady=5)
        self.player = Player(self.master, video=self.video)
        # self.player.pack(side='right')
        #self.connect_to_video()

    def connect_to_video(self):
        print("connecting to video")
        self.player._Play(self.video)

    def disconnect_to_video(self):
        print("disconnecting from video")
        self.player.OnStop()

    def connect_to_audio(self):
        self.mbac.connectAndStart()
        self.mute_label.pack_forget()
        self.keep_audio_on = True

    def disconnect_to_audio(self):
        self.mbac.disconnectAndStop()
        self.mute_label.pack(side="left")
        self.keep_audio_on = False


    def change_audio(self, device):
        self.mbac.disconnectAndStop()
        self.mbac.setInputDevice(device)
        if(self.keep_audio_on):
            self.mbac.connectAndStart()

    def phone_mirror(self):
        # #app = QApplication([])
        command = "scrcpy &"
        # os.system("scrcpy &")
        # appscript.app('Terminal').do_script(command)
        p = subprocess.Popen(command, shell=True)
        # p.wait()
        # app.exec_()

    def start_screen_record(self):
        if not self.screen_record.isRecording():
            self.screen_record.startRecording()
            self.record_label.pack(side="left")
        else:
            #TODO: Add error message
            pass

    def stop_screen_record(self):
        if self.screen_record.isRecording():
            self.screen_record.stopRecording()
            self.record_label.pack_forget()
        else:
            pass

    def turn_encryption_on(self):
        self.screen_record.encrypt_bool = True
        self.encryption_settings_menu.delete(1)
        self.encryption_settings_menu.add_command(label="Turn Encryption Off", command=self.turn_encryption_off)

    def turn_encryption_off(self):
        self.screen_record.encrypt_bool = False
        self.encryption_settings_menu.delete(1)
        self.encryption_settings_menu.add_command(label="Turn Encryption On", command=self.turn_encryption_on)

    def set_password(self, password):
        self.screen_record.setPassword(password.get())
        self.popup.destroy()

    def popup_password(self):
        self.popup = tk.Toplevel()
        self.popup.wm_title("Set Password")
        password = tk.StringVar()
        password_entered = ttk.Entry(self.popup, width=15, textvariable=password)
        set_button = ttk.Button(self.popup, text="Set Password", command=partial(self.set_password, password))
        password_entered.pack()
        set_button.pack()
        self.popup.geometry("250x100")

    def set_video_port(self, port):
        self.rtsp_port = port
        self.serverString = f"rtsp://{self.host}:{self.rtsp_port}/"
        self.video = self.serverString
        print(self.serverString)
        self.set_ip_port_menu.entryconfigure(2, label=f"Set Video Port: {self.rtsp_port}")
        self.popup_port.destroy()

    def set_ip(self, ip):
        self.host = ip.get()
        self.serverString = f"rtsp://{self.host}:{self.rtsp_port}/"
        print(self.serverString)
        self.set_ip_port_menu.entryconfigure(3, label=f"Set Phone IP: {self.host}")
        self.popup_ip.destroy()

    def set_port(self, device_type, port):
        if device_type == 'audio':
            port_num = int(port.get())
            self.mbac.setPortNum(port_num)
            self.audio_port = port_num
            print(self.mbac.port_num)
            self.set_ip_port_menu.entryconfigure(0, label=f"Set Audio Port: {self.audio_port}")

        elif device_type == 'video':
            port_num = int(port.get())
            self.set_video_port(port_num)
        elif device_type == 'message':
            port_num = int(port.get())
            self.bmc.setPortNum(port_num)
            self.message_port = port_num
            self.set_ip_port_menu.entryconfigure(1, label=f"Set Message Port: {self.message_port}")
            print(self.bmc.port_num)
        self.popup_port.destroy()


    def popup_ip(self):
        self.popup_ip = tk.Toplevel()
        self.popup_ip.wm_title("Set ip")
        ip = tk.StringVar()
        ip_entered = ttk.Entry(self.popup_ip, width=15, textvariable=ip)
        ip_entered.insert(END, self.host)
        set_button = ttk.Button(self.popup_ip, text="Set ip", command=partial(self.set_ip, ip))
        ip_entered.pack()
        set_button.pack()
        self.popup_ip.geometry("250x100")

    def popup_port(self, device_type):
        self.popup_port = tk.Toplevel()
        self.popup_port.wm_title("Set " + device_type + " port")
        port = tk.StringVar()
        port_entered = ttk.Entry(self.popup_port, width=15, textvariable=port)

        if(device_type == 'audio'):
            port_entered.insert(END, self.audio_port)
        elif(device_type == 'video'):
            port_entered.insert(END, self.rtsp_port)
        elif(device_type == 'message'):
            port_entered.insert(END, self.message_port)
        else:
            print("ERROR")



        set_button = ttk.Button(self.popup_port, text="Set " + device_type + " port", command=partial(self.set_port, device_type, port))
        port_entered.pack()
        set_button.pack()
        self.popup_port.geometry("250x100")


    def updateMenuOptions(self, event):

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
        '''
        self.file_menu = tk.Menu(root_menu, tearoff=0)
        # self.file_menu.add_command(label="Preferences", command=self.hello)
        self.file_menu.add_command(label="Quit", command=self.close_app)
        '''
        self.file_menu = FileMenu(root_menu, tearoff=False, frame=self)
        root_menu.add_cascade(label="File", menu=self.file_menu)

        # Device Menu
        '''
        self.device_menu = tk.Menu(root_menu, tearoff=0)

        self.device_menu.add_command(label="Refresh Devices", command=self.refresh_devices)
        self.device_menu.add_separator()
        '''
        self.device_menu = DeviceMenu(root_menu, tearoff=False)

        root_menu.add_cascade(label="Device", menu=self.device_menu)

        # Help Menu
        '''
        self.help_menu = tk.Menu(root_menu, tearoff=0)
        self.help_menu.add_command(label="About Survivor Buddy 3.0", command=self.open_survivor_buddy_page)
        self.help_menu.add_command(label="User Manual", command=self.open_user_manual)
        self.help_menu.add_command(label="Programmer's Reference", command=self.open_programmer_reference)
        '''
        self.help_menu = HelpMenu(root_menu, tearoff=False)
        root_menu.add_cascade(label="Help", menu=self.help_menu)

        #Video Menu
        '''
        self.video_menu = tk.Menu(root_menu, tearoff=0)
        self.video_menu.add_command(label="Connect Video", command=self.connect_to_video)
        self.video_menu.add_command(label="Disconnect Video", command=self.disconnect_to_video)
        '''
        self.video_menu = VideoMenu(root_menu, tearoff=0, frame=self)
        root_menu.add_cascade(label="Video", menu=self.video_menu)

        #Audio Menu
        '''
        self.audio_menu = tk.Menu(root_menu, tearoff=0)
        self.audio_menu.add_command(label="Unmute", command=self.connect_to_audio)
        self.audio_menu.add_command(label="Mute", command=self.disconnect_to_audio)
        '''

        self.audio_menu = AudioMenu(
            root_menu, 
            tearoff=0, 
            frame=self, 
            audioClient=self.mbac
        )

        root_menu.add_cascade(label="Unmute/Mute", menu=self.audio_menu)

        #Audio Devices
        '''
        self.audio_devices_menu = tk.Menu(root_menu, tearoff=0)
        for device in self.device_arr:
            self.audio_devices_menu.add_command(label=device, command=partial(self.change_audio, device))
        '''
        self.audio_devices_menu = AudioDeviceMenu(
            root_menu, 
            tearoff=False, 
            frame=self,
            audioClient=self.mbac
        )
        root_menu.add_cascade(label="Audio Devices", menu=self.audio_devices_menu)

        #Phone Mirroring
        '''
        self.phone_mirroring_menu = tk.Menu(root_menu, tearoff=0)
        self.phone_mirroring_menu.add_command(label="Open Phone Mirroring", command=self.phone_mirror)
        '''
        self.phone_mirroring_menu = PhoneMirrorMenu(root_menu, tearoff=False)
        root_menu.add_cascade(label="Phone Mirroring", menu=self.phone_mirroring_menu)

        #Screen Record
        '''
        self.screen_record_menu = tk.Menu(root_menu, tearoff=0)
        self.screen_record_menu.add_command(label="Start Screen Record", command=self.start_screen_record)
        self.screen_record_menu.add_command(label="Stop Screen Record", command=self.stop_screen_record)
        '''
        self.screen_record_menu = ScreenRecordMenu(root_menu, tearoff=False)
        root_menu.add_cascade(label="Screen Record", menu=self.screen_record_menu)

        #Set Password
        '''
        self.encryption_settings_menu = tk.Menu(root_menu, tearoff=0)
        self.encryption_settings_menu.add_command(label="Set Password", command=self.popup_password)
        self.encryption_settings_menu.add_command(label="Turn Encryption On", command=self.turn_encryption_on)
        '''
        self.encryption_settings_menu = EncryptionMenu(root_menu, tearoff=False)
        root_menu.add_cascade(label="Encryption Settings", menu=self.encryption_settings_menu)

        #Set IP/Port
        '''
        self.set_ip_port_menu = tk.Menu(root_menu, tearoff=0)
        self.set_ip_port_menu.add_command(label=f"Set Audio Port: {self.audio_port}", command=partial(self.popup_port, 'audio'))
        self.set_ip_port_menu.add_command(label=f"Set Message Port: {self.message_port}", command=partial(self.popup_port, 'message'))
        self.set_ip_port_menu.add_command(label=f"Set Video Port: {self.rtsp_port}", command=partial(self.popup_port, 'video'))
        self.set_ip_port_menu.add_command(label=f"Set Phone IP: {self.host}", command=self.popup_ip)
        '''
        self.set_ip_port_menu = IpPortMenu(root_menu, tearoff=False)

        root_menu.add_cascade(label="Set IP/Port", menu=self.set_ip_port_menu)

        root_menu.bind("<<MenuSelect>>", self.updateMenuOptions)


    def refresh_devices(self):
        '''Refreshes the Devices menu'''

        self.device_menu.delete(2, 100)
        self.serial_arm_controller.update_devs()
        if not self.serial_arm_controller.devs:
            self.device_menu.add_command(label="No devices", state=tk.DISABLED)
        else:
            for dev in self.serial_arm_controller.devs:
                self.device_menu.add_command(
                    label="{}: {}".format(dev[0], dev[1]),
                    command=lambda: self.connect(dev)
                )

    def connect(self, dev):
        '''
        Connects to the given device
        :param dev: The serial device to connect to
        '''

        self.serial_arm_controller.connect(dev[0])
        self.device_menu.add_command(
            label="Close Connection",
            command=self.close
        )

    def close(self):
        '''Closes the active serial connection'''

        self.device_menu.delete(2 + len(self.serial_arm_controller.devs))
        self.serial_arm_controller.close()

    def open_survivor_buddy_page(self):
        webbrowser.open("http://survivorbuddy.cse.tamu.edu/")

    def open_user_manual(self):
        webbrowser.open(
            "https://docs.google.com/document/d/1V6gmVehsxrlFoc5FzThtdTNSovUbyU03AUEBfnAclKA/edit?usp=sharing")

    def open_programmer_reference(self):
        webbrowser.open("https://drive.google.com/a/tamu.edu/file/d/1pMKci4BTCTu7H6GREmmWEmBEgZ4klQWn/view?usp=sharing")

    def hello(self):
        '''
        A test function
        Simply prints "Hello from Menu" to the console and the NotificationsFrame
        '''
        print("Hello from Menu")
        self.notifications_frame.append_line("Hello from Menu")





if __name__ == "__main__":
    root = tk.Tk()

    root.geometry("1250x1080")
    # now = datetime.now()  # Create unique logfile for notifications and errors
    # timestamp = now.strftime("%m_%d_%Y_%H_%M_%S")
    # file_name = 'LOGFILE_' + timestamp + '.txt'
    # logFile = open(os.path.join(os.path.realpath('../logs/'), file_name), 'w+')

    # declaration of everything
    app = Application(master=root)
    # diagram_frame = Frame(root, height = 300, width = 700, highlightbackground="black", highlightthickness=1)
    # diagram_frame.place(x=50,y=100)
    # app.position_frame.place(in_=diagram_frame, anchor = CENTER, relx = 0.5, rely=0.1)
    # status_bar = StatusBar(master=root)
    # notifications_frame = NotificationFrame(master = root,_logFile=logFile)
    # serial_arm_controller = SerialArmController(status_bar, notifications_frame)
    # menu_bar = tk.Menu()
    # app.create_menu(menu_bar)
    # position_frame = PositionFrame(master = root,arm_controller=serial_arm_controller, _logFile=logFile)

    # button = Button(root, text="Create new window",
    #                 command=create_window)
    # button.place(x=500, y=700)

    # bottom right buttons
    # button_frame = Frame(root, height=245, width=150, highlightbackground="black", highlightthickness=1)
    # button_frame.place(x=825, y=530)
    # portrait_button = Button(button_frame, text="Portrait").place(in_=button_frame, anchor=CENTER, relx=0.5,
    #                                                                          rely=0.125)
    # landscape_button = Button(button_frame, text="Landscape").place(in_=button_frame, anchor=CENTER, relx=0.5,
    #                                                               rely=0.25)
    # open_arm_button = Button(button_frame, text="Open Arm").place(in_=button_frame, anchor=CENTER, relx=0.5,
    #                                                               rely=0.375)
    # close_arm_button = Button(button_frame, text="Close Arm").place(in_=button_frame, anchor=CENTER, relx=0.5,
    #                                                               rely=0.5)
    # tilt_head_button = Button(button_frame, text="Tilt Head").place(in_=button_frame, anchor=CENTER, relx=0.5,
    #                                                               rely=0.625)
    # nod_head_button = Button(button_frame, text="Nod Head").place(in_=button_frame, anchor=CENTER, relx=0.5,
    #                                                               rely=0.75)
    # shake_head_button = Button(button_frame, text="Shake Head").place(in_=button_frame, anchor=CENTER, relx=0.5,
    #                                                               rely=0.875)

    app.master.title("Survivor Buddy 4.0")
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    app.mainloop()
