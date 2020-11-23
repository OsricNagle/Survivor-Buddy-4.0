import socket
import threading

class BuddyMessageClient:
    """
    A TCP client which sends messages in text form. Each message sent connects, sends, 
    then disconnects. 

    :param server_ip: the ip address of the server
    :type server_ip: String
    :param port_num: the port number of the server
    :type port_num: int
    :param frame: the frame on which error messages will be displayed. Defaults to None
    :type frame: Tkinter frame, optional
    :param str_format: the encoding format in which messages are sent
    :type str_format: String
    """

    def __init__(self, server_ip, port_num, frame=None, str_format='utf-8'):
        """
        Constructor for BuddyMessageClient
        """

        self.server_ip = server_ip
        self.port_num = port_num
        self.full_addr = (self.server_ip, self.port_num)
        self.str_format = str_format
        self.client_socket = None
        self.app_frame = frame

    def show_error(self, error_msg):
        """
        Displays the error message on the frame

        :param error_msg: the content of the error message
        :type error_msg: String
        """
        self.app_frame.showPopupMessage(msg_text=error_msg)

    def setPortNum(self, new_port):
        """
        Sets the port number

        :param new_port: the value of the new port number
        :type new_port: int
        """
        self.port_num = new_port
        self.full_addr = (self.server_ip, self.port_num)

    def connect(self, text="DEFAULT_MESSAGE"):
        """
        Connects to the server. Displays error if unsuccessful

        :param text: unused
        :type text: String
        :return: true if connection is successful, false if there is a connection error,
            and None if undefined error occurrs
        :rtype: boolean
        """


        error_msg = "Message Connection Error:\n"
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print(self.full_addr)
            self.client_socket.connect(self.full_addr)
            return True

        except ConnectionRefusedError:
            #if ip/port is wrong or
            error_msg += (
                "Message not sent. Check that the messages screen is showing in the Survivor Buddy Android app\n"
                "and that the IP and port settings match those in the Survivor Buddy Android app."
            )
            self.show_error(error_msg)
            return False

        except TimeoutError:
            error_msg += (
                "Message not sent. Check that the messages screen is showing in the Survivor Buddy Android app\n"
                "and that the IP and port settings match those in the Survivor Buddy Android app."
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
        """
        Disconnects from the server if connected, otherwise does nothing
        """
        if(self.client_socket is not None):
            self.client_socket.close()
            self.client_socket = None

    def sendMsg(self, msg_str):
        """
        Starts handleSend in a new thread which sends a message to the server

        :param msg_str: the message to send to the server
        :type msg_str: String
        """
        threading.Thread(target=self.handleSend, args=(msg_str,)).start()

    def handleSend(self, msg_str):
        """
        Connects to the server, sends a message, then disconnects

        :param msg_str: the message to send to the server
        :type msg_str: String
        """
        if self.connect(msg_str):
            self.client_socket.sendall(msg_str.encode(self.str_format))
            self.disconnect()
