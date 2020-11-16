import socket
import threading
from tkinter import *
from tkinter.ttk import *

class BuddyMessageClient:

    def __init__(self, server_ip, port_num, frame=None, str_format='utf-8'):

        self.server_ip = server_ip
        self.port_num = port_num
        self.full_addr = (self.server_ip, self.port_num)
        self.str_format = str_format
        self.client_socket = None
        self.app_frame = frame

    def show_error(self, error_msg):
        pass

    def setPortNum(self, new_port):
        self.port_num = new_port
        self.full_addr = (self.server_ip, self.port_num)

    def connect(self, text="DEFAULT_MESSAGE"):
        error_msg = "Message Connection Error:\n"
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print(self.full_addr)
            self.client_socket.connect(self.full_addr)
            return True

        except ConnectionRefusedError:
            #if ip/port is wrong or
            error_msg += (
                "Message Connection Error:"
                "check that the IP and port settings match "
                "those in the Survivor Buddy Android Application."
            )
            self.show_error(error_msg)
            return False

        except TimeoutError:
            error_msg += (
                "Connection timed out,"
                "check that the IP and port settings match"
                " those in the Survivor Buddy Android Application."
            )
            self.show_error(error_msg)
            return False

        except TypeError:
            print("Invalid port")
            error_msg += f'Message port number "{self.port_num}" is and invalid port\n'
            error_msg += "Please change the message port in the IP/Port Menu"
            return False

        return None

    def disconnect(self):
        if(self.client_socket is not None):
            self.client_socket.close()
            self.client_socket = None

    def sendMsg(self, msg_str):
        threading.Thread(target=self.handleSend, args=(msg_str,)).start()

    def handleSend(self, msg_str):
        if self.connect(msg_str):
            self.client_socket.sendall(msg_str.encode(self.str_format))
            self.disconnect()
