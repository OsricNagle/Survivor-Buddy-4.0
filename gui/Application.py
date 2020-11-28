"""
Starts and handles GUI application. Contains the main Tkinter frame
"""
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

class Application(Tk.Frame):
    """
    Main gui class. Everything that the GUI controls or displays is instantiated in this class

    :param master: The Tkinter root
    :type master: Tkinter widget
    :param kwargs: the extra tkinter options
    :type kwargs: kwargs 
    """


    def __init__(self, master, **kwargs):
        """
        Constructor for Application
        Inits all controlled elements and objects
        """


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
        self.player = None #Player(self.master, video=self.video_url)
        
        #init PC->Phone Audio objs
        self.mbac = BuddyAudioClient(self.host, self.audio_port, frame=self)
        self.microphone = ""
        self.keep_audio_on = False

        #init PC->Phone text message objs
        self.bmc = BuddyMessageClient(
            self.host, 
            self.message_port, 
            frame=self
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


        wrapper_frame = Tk.Frame(self)
        wrapper_frame.pack(side="left")

        top_frame = Tk.Frame(wrapper_frame)
        top_frame.pack(fill="x")


        middle_frame = Tk.Frame(wrapper_frame)
        middle_frame.pack()
         #Player(middle_frame, video=self.video_url)
        #self.player.config(
        #    background='purple'
        #)
        #self.player.pack()
        #self.player.pack()





        bottom_frame = Tk.Frame(wrapper_frame)
        bottom_frame.pack(fill="x")

        text_frame = Tk.Frame(wrapper_frame, height=55)
        text_frame.pack(fill="x")
        self.mute_image = Tk.PhotoImage(file="gui/mute.png")
        self.mute_label = Tk.Label(text_frame, image=self.mute_image)
        #self.mute_label.pack(side="left")
        self.record_image = Tk.PhotoImage(file="gui/recordingbutton.png")
        self.record_label = Tk.Label(text_frame, image=self.record_image)
        
        # textbox = Tk.ttk.Label(root, text="text")
        # textbox.place(x=800, y=300)
        self.name = Tk.StringVar()
        self.text_box = Tk.Text(self, width=73, height=5)
        self.send_button = Tk.Button(self, text="Send Text", height=5, width=7, command=self.send_text)

        # down_button = Tk.ttk.Button(self.bottom_frame,
        #                          text="Move down")
        # down_button.pack(side="top")
        self.control_buttons = None
        self.position_frame = PositionFrame(self, self.serial_arm_controller, self.logFile, top_frame, middle_frame, bottom_frame, self.theroot, self.notifications_frame)
        self.position_frame.pack(fill="x")
        self.create_menu(self.menu_bar)


        # self.control_buttons.pack(fill="x")
        self.status_bar.pack(fill="x")
        self.notifications_frame.pack(fill="x")
        self.send_button.pack(side='right', pady=20)
        self.text_box.pack(side='right', pady=20)

        self.master.config(menu=self.menu_bar)

    def send_text(self):
        """
        Gets string input from popup box and sends it to message server
        """
        input = self.text_box.get("1.0", Tk.END)
        print(input)
        self.bmc.sendMsg(input)

    def close_app(self):  # Had to make new quit function to close file
        '''Closes the GUI application'''

        self.logFile.close()

        if(self.mbac.isStreaming()):
            self.mbac.stopStream()
            self.mbac.disconnect()


        self.quit()


    def hideMuteIcon(self):
        """Hides the mute icon on the GUI"""
        self.mute_label.pack_forget()

    def displayMuteIcon(self):
        """Shows the mute icon on the GUI"""
        self.mute_label.pack(side='left')

    def displayRecordIcon(self):
        """Shows the record icon on the GUI"""
        self.record_label.pack(side='left')

    def hideRecordIcon(self):
        """Hides the record icon on the GUI"""
        self.record_label.pack_forget()

    def set_password(self, password):
        """
        sets the password for screen recording

        :param password: the new password
        :type password: String
        """
        self.screen_record.setPassword(password.get())
        self.popup_password.destroy()

    def password_popup(self):
        """
        Opens a popup to allow for entry of new password string
        """
        self.popup_password = Tk.Toplevel()
        self.popup_password.wm_title("Set Password")
        password = Tk.StringVar()
        password_entered = Tk.ttk.Entry(self.popup_password, width=15, textvariable=password)
        set_button = Tk.ttk.Button(self.popup_password, text="Set Password", command=partial(self.set_password, password))
        password_entered.pack()
        set_button.pack()

        w = self.theroot.winfo_x() + 100
        h = self.theroot.winfo_y() + 100

        self.popup_password.geometry(f"250x100+{w}+{h}")

    def validatePort(self, portNum):
        """
        Validates that the given portNum is a valid port number
        
        :param portNum: the port number to be validated
        :type portNum: String or int
        """
        try:
            port = int(portNum)
        except ValueError:
            return False
        
        return (port in range(1, 65535+1))


    def set_video_port(self, port):
        """
        Changes the port number in the rtsp url for receiving video/audio from
        android

        :param port: the new port number
        :type port: String or int
        """
        self.rtsp_port = port
        self.video_url = f"rtsp://{self.host}:{self.rtsp_port}/"
        self.port_popup.destroy()

    def set_ip(self, ip):
        """
        Changed the ip address that a connection will be attempted to when sending/receiving
        data from the mobile application

        :param ip: the new ip address
        :type ip: String
        """
        self.host = ip.get()
        self.video_url = f"rtsp://{self.host}:{self.rtsp_port}/"
        print(self.video_url)
        self.ip_popup.destroy()

    def set_port(self, device_type, port):
        """
        Changes the port number based on the chosen device type. 
        If port is invalid an error box will be displayed

        :param device_type: denotes which port number to change, current valid options are:
            'audio', 'video', 'message'
        :type device_type: String
        :param port: the new port number
        :type port: Tk.StringVar
        """
        if(self.validatePort(port.get())):
            port_num = int(port.get())

            if device_type == 'audio':
                self.mbac.setPortNum(port_num)
                self.audio_port = port_num

            elif device_type == 'video':
                self.video_url = f"rtsp://{self.host}:{port_num}/"
                #self.set_video_port(port_num)

            elif device_type == 'message':
                self.bmc.setPortNum(port_num)
                self.message_port = port_num
            else:
                print("ERROR: set_port invalid device_type")

        else:
            self.showPopupMessage(
                msg_text=(
                    f"Invalid {device_type.capitalize()} " 
                    f"Port Number: {device_type.capitalize()} "
                    "Port must be a whole number in range [1-65535]"
                )
            )
           
        self.port_popup.destroy()


    def popup_ip(self):
        """
        Opens a popup box allowing for entry of a new ip address to attempt to connect to
        when sending data to the mobile device
        """
        self.ip_popup = Tk.Toplevel()
        self.ip_popup.wm_title("Set ip")
        ip = Tk.StringVar()
        ip_entered = Tk.ttk.Entry(self.ip_popup, width=15, textvariable=ip)
        ip_entered.insert(Tk.END, self.host)
        set_button = Tk.ttk.Button(self.ip_popup, text="Set ip", command=partial(self.set_ip, ip))
        ip_entered.pack()
        set_button.pack()

        w = self.theroot.winfo_x() + 100
        h = self.theroot.winfo_y() + 100

        self.ip_popup.geometry(f"200x100+{w}+{h}")

    def popup_port(self, device_type):
        """
        Opens a popup box allowing for entry of a new port number for the chosen device_type.

        :param device_type: The device on which the port will be set. Valid inputs include:
            'audio', 'video', 'message'
        "type device_type: String
        """
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

        w = self.theroot.winfo_x() + 100
        h = self.theroot.winfo_y() + 100

        self.port_popup.geometry(f"200x100+{w}+{h}")

    def displayFileDialog(self):
        """
        Opens a file dialog asking for a choice of folder

        :return: the path of the chosen folder
        :rtype: String
        """
        return filedialog.askdirectory()

    def showPopupMessage(self, title="Suvivor Buddy 4.0", msg_text="CONTENT"):
        """
        Displays a popup box with the input message and title

        :param title: The title of the popup box. Defaults to "Survivor Buddy 4.0"
        "type title: String
        :param msg_text: The text content of the popup box. Defaults to "CONTENT"
        :type msg_text: String
        """
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
        """
        Callback function to update the drop down menus in the top menu bar.
        Figures out which drop down menu was opened and calls the updateMenu() function
        member of that menu

        :param event: Tkinter event which is used to figure out the menu opened
        :type event: Tkinter event
        """

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
        Initializes the menu bar of the main GUI.
        :param root_menu: The root menu (self.menu_bar) that is instantiated in create_widgets()
        :type root_menu: Tkinter Menu
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

        root_menu.add_cascade(label="Audio", menu=self.audio_menu)

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

    root.geometry("1300x1080")
    app = Application(master=root)

    app.master.title("Survivor Buddy 4.0")
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    app.mainloop()
