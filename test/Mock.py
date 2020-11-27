"""
Contains custom Mocks for testing purposes
"""

import io
import threading
import socket
from gui.SerialArmController import Position

class MockSerial:
    """
    Class to mock a serial connection

    """
    def __init__(self):
        self.byte_buffer = io.BytesIO()
        self.offset = 0
        self.open_bool = True

    def read(self, size):
        """
        read a certain amount from a buffer

        :param size: the size to read from the buffer
        :type size: int
        """
        if(self.open_bool):
            data = self.byte_buffer.read(size)
            self.offset += size
            return data
        return None

    def write(self, data):
        """
        write data to the buffer

        :param data: the data sent to the buffer
        :type data: Bytes
        """
        if(self.open_bool):
            num_written = self.byte_buffer.write(data)
            self.byte_buffer.seek(self.offset)
            return num_written
        return None

    def close(self):
        """
        Closes the connection and flushes the buffer
        """
        self.byte_buffer.flush()
        self.offset = 0
        self.open_bool = False

        
class MockNotificationsFrame:
    """
    Class to mock a notifications frame

    """

    def __init__(self):
        self.lines = []

    def append_line(self, line):
        """
        Append a string to the array that is the notifications frame

        :param line: line that is appended to the array
        :type line: String
        """
        self.lines.append(line)

    def get_lines(self):
        """
        returns the notifications box array
        """
        return self.lines

class MockStatusBar:
    """
    Class to mock a status bar

    """
    def __init__(self):
        self.status = None

    def set_status(self, status):
        """
        Sets the status based on what is passed in

        :param status: Passed in value that is either "CONNECTED" or "DISCONNECTED"
        :type status: String
        """
        self.status = status

    def get_status(self):
        """
        Returns the status
        """
        return self.status

class MockSerialArmController:
    """
    Class to mock a SerialArmController

    """
    def __init__(self):
        self.is_connected = False
        self.open_arm_bool = False
        self.close_arm_bool = False
        self.portrait_bool = False
        self.landscape_bool = False
        self.tilt_bool = False
        self.nod_bool = False
        self.shake_bool = False
        self.shutdown_bool = False
        self.pitch = 0
        self.yaw = 0
        self.roll = 0

    def open_arm(self):
        """
        Sets open_arm_bool to true
        """
        self.open_arm_bool = True

    def close_arm(self):
        """
        Sets close_arm_bool to true
        """
        self.close_arm_bool = True

    def portrait(self):
        """
        Sets portrait_bool to true
        """
        self.portrait_bool = True

    def landscape(self):
        """
        Sets landscape_bool to true
        """
        self.landscape_bool = True

    def tilt(self):
        """
        Sets tilt_bool to true
        """
        self.tilt_bool = True

    def nod(self):
        """
        Sets nod_bool to true
        """
        self.nod_bool = True

    def shake(self):
        """
        Sets shake_bool to true
        """
        self.shake_bool = True

    def _shutdown(self):
        """
        Sets shutdown_bool to true
        """
        self.shutdown_bool = True

    def set_pitch(self, val):
        """
        Sets pitch to value passed in

        :param val: pitch passed in
        :type val: int
        """
        self.pitch = val

    def set_yaw(self, val):
        """
        Sets yaw to value passed in

        :param val: yaw passed in
        :type val: int
        """
        self.yaw = val

    def set_roll(self, val):
        """
        Sets roll to value passed in

        :param val: roll passed in
        :type val: int
        """
        self.roll = val



class MockLogFile():
    """
    Class to mock a Log File

    """
    def __init__(self):
        self.arr = []

    def write(self, text):
        """
        appends text passed in to the array

        :param text: variable that is appended to the array
        :type text: String
        """
        self.arr.append(text)

class MockSpinBox():
    """
    Class to mock a spinbox

    """
    def __init__(self, val=0):
        self.val = val

    def get(self):
        """getter for val"""
        return self.val

    def set(self, val):
        """
        setter for val

        :param val: value passed int to set to variable "val"
        :type val: int
        """
        self.val = val


class MockSlider():
    """
    Class to mock a slider

    """
    def __init__(self, val=0):
        self.val = val

    def get(self):
        """getter for val"""
        return self.val

    def set(self, val):
        """
        setter for val

        :param val: value passed int to set to variable "val"
        :type val: int
        """
        self.val = val
