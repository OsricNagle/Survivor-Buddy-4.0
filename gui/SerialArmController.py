# -*- coding: utf-8 -*-
"""
Contains interface to send commands to and receive position updates from the arduino
"""


from serial.tools import list_ports
import serial
from threading import Thread
import time

ARDUINO_VID  = 0x2341
UNO_PID      = 0x0043
LEONARDO_PID = 0x8036

class Command():
    '''
    A class to keep track of command numbers
    '''

    PITCH = 0
    """PITCH variable set to 0 for future use"""

    YAW = 1

    """YAW variable set to 1 for future use"""
    ROLL = 2

    """ROLL variable set to 2 for future use"""
    CLOSE = 3

    """CLOSE variable set to 3 for future use"""
    OPEN = 4

    """OPEN variable set to 4 for future use"""
    PORTRAIT = 5

    """PORTRAIT variable set to 5 for future use"""
    LANDSCAPE = 6

    """LANDSCAPE variable set to 6 for future use"""
    NOD = 7

    """NOD variable set to 7 for future use"""
    SHAKE = 8

    """SHAKE variable set to 8 for future use"""
    TILT = 9

    """TILT variable set to 9 for future use"""
    SHUTDOWN = 0x10

    """SHUTDOWN variable set to 10 for future use"""


class Position:
    """
    A class to store position data

    """



    def __init__(self, pitch=0, yaw=0, roll=0):
        '''
        Constructor for Position

        :param pitch: the pitch value of the robot
        :type pitch: int
        :param yaw: the yaw value of the robot
        :type yaw: int
        :param roll: the roll value of the robot
        :type yaw: int
        '''

        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        
    def __str__(self):
        return "P: {}, Y: {}, R: {}".format(self.pitch, self.yaw, self.roll)

        
class SerialArmController:
    '''
    This class sends commands to the robot arm and receives data from the arm.

    '''

    def __init__(self, _status_bar, _notifications):
        '''
        Constructor for SerialArmController

        :param _status_bar: The status bar of the GUI passed in, allows us to change if it's connected or not
        :type _status_bar: StatusBar
        :param _notifications: The notifications frame of the GUI passed in, allows us to add to the notifications frame
        :type _notifications: NotificationsFrame
        '''

        self.status_bar = _status_bar
        self.notifications = _notifications
        self._com_port = ""
        self._device = None
        self.devs = []
        self.position = Position()
        self.is_connected = False
        

    def update_devs(self):
        '''Updates the list of available devices'''

        devs = list_ports.comports()
        """
        devs is an array of tuples of the form (com port, name)
        """
        self.devs = []
        for dev in devs:
            if dev.vid == ARDUINO_VID and dev.pid == LEONARDO_PID:
                self.devs.append((dev.device, "Leonardo"))
            elif dev.vid == ARDUINO_VID and dev.pid == UNO_PID:
                self.devs.append((dev.device, "Uno"))
           

    def connect(self, comport):
        '''
        Connects to the device at the desired COM port

        :param comport: The name of the COM port to connect to
        :type comport: String
        '''

        if not self.is_connected:
            self._device = serial.Serial(comport, timeout=1)
            self.status_bar.set_status("CONNECTED")
            self.is_connected = True
        
        
    def close(self):
        '''
        Closes the current connection from PC to arduino

        '''

        if self.is_connected:
            self._device.close()
            self.status_bar.set_status("DISCONNECTED")
            self.is_connected = False
        

    def send(self, data):
        '''
        Sends data to the arm

        :param data: Bytes to send
        :type data: Byte
        '''
        if self.is_connected:
            print("Sending: \"{}\"".format(data))
            self._device.write(data)

        
    def recv(self):
        '''
        Receives data from the arm
        
        :returns: data - bytes from the arm
        :rtype: Byte
        '''

        if self.is_connected:
            data = self._device.read(3)
            print("Received: \"{}\"".format(data))
            return data


    def update_position(self):
        '''
        Updates the current stored position

        '''

        pos = self.recv()
        if pos:
            self.position.pitch = int(pos[0])
            self.position.yaw = int(pos[1] - 90)
            self.position.roll = int(pos[2])
            print("pitch: ", self.position.pitch)





    def set_pitch(self, val):
        '''
        Sends a command to the arm to go to the desired pitch

        :param val: Sets the pitch based on the parameter passed in
        :type val: int
        '''

        # val is one byte
        if self.is_connected:
            self.send(bytes((Command.PITCH, val)))
            

    def set_yaw(self, val):
        '''
        Sends a command to the arm to go to the desired yaw

        :param val: Sets the yaw based on the parameter passed in
        :type val: int
        '''

        # val is 1 byte
        if self.is_connected:
            self.send(bytes((Command.YAW, val + 90)))
            

    def set_roll(self, val):
        '''
        Sends a command to the arm to go to the desired roll

        :param val: Sets the roll based on the parameter passed in
        :type val: int
        '''

        # val is one byte
        if self.is_connected:
            self.send(bytes((Command.ROLL, val)))

            
    def close_arm(self):
        '''
        Sends the CLOSE command to the arm

        '''

        if self.position.pitch == 0:
            self.notifications.append_line("WARNING: ARM ALREADY CLOSED")
        else:
            self.send(bytes((Command.CLOSE, 0)))
        

    def open_arm(self):
        '''
        Sends the OPEN command to the arm

        '''

        if self.position.pitch == 90:
            self.notifications.append_line("WARNING: ARM ALREADY OPEN")
        else:
            self.send(bytes((Command.OPEN, 0)))
        

    def portrait(self):
        '''
        Sends the PORTRAIT command to the arm

        '''

        if self.is_connected:
            if self.position.roll == 0:
                self.notifications.append_line("WARNING: ALREADY IN PORTRAIT")
            else:
                self.send(bytes((Command.PORTRAIT, 0)))
                

    def landscape(self):
        '''
        Sends the LANDSCAPE command to the arm

        '''

        if self.is_connected:
            if self.position.roll == 90:
                self.notifications.append_line("WARNING: ALREADY IN LANDSCAPE")
            else:
                self.send(bytes((Command.LANDSCAPE, 0)))
                

    def tilt(self):
        '''
        Sends the TILT command to the arm

        '''

        if self.is_connected:
            self.send(bytes((Command.TILT, 0)))
            

    def nod(self):
        '''
        Sends the NOD command to the arm

        '''

        if self.is_connected:
            self.send(bytes((Command.NOD, 0)))

            
    def shake(self):
        '''
        Sends the SHAKE command to the arm

        '''

        if self.is_connected:
            self.send(bytes((Command.SHAKE, 0)))


    def _shutdown(self):
        '''
        Sends the SHUTDOWN command to the arm

        '''

        if self.is_connected:
            self.send(bytes((Command.SHUTDOWN, 0)))
            time.sleep(4)
            self.close()
        