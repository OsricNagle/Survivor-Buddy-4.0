"""
Contains custom Mocks for testing purposes, could/should probably be replaced by using pytest_mock
"""

import io
import threading
import socket
from gui.SerialArmController import Position

class MockSerial:
    """
    Mock of function used from Serial library
    """
    def __init__(self):
        """
        Constructor for MockSerial
        """
        self.byte_buffer = io.BytesIO()
        self.offset = 0
        self.open_bool = True

    def read(self, size):
        """
        Mock read

        :param size: the number of bytes to read
        :type size: int
        :return: the bytes read or None if Buffer is not open
        :rtype: bytes or None
        """
        if(self.open_bool):
            data = self.byte_buffer.read(size)
            self.offset += size
            return data
        return None

    def write(self, data):
        """
        Mock write

        :param data: the bytes to write
        :type data: bytes
        :return: The number of bytes written or None if buffer is not open
        :rtype: int or None
        """
        if(self.open_bool):
            num_written = self.byte_buffer.write(data)
            self.byte_buffer.seek(self.offset)
            return num_written
        return None

    def close(self):
        """
        Closes the buffer
        """
        self.byte_buffer.flush()
        self.offset = 0
        self.open_bool = False

        
class MockNotificationsFrame:
    """
    Mock of NotificationsFrame
    """
    def __init__(self):
        self.lines = []

    def append_line(self, line):
        """
        Mock of append_line. Adds line to self.lines

        :param line: the line to add
        :type line: String
        """
        self.lines.append(line)

    def get_lines(self):
        """
        Returns the lines for testing purposes

        :return: the current list of appended lines
        :rtype: list[String]
        """
        return self.lines

class MockStatusBar:
    """
    Mock of StatusBar
    """
    def __init__(self):
        """
        Constructor for MockStatusBar
        """
        self.status = None

    def set_status(self, status):
        """
        Mock set_status, changes status

        :param status: the status to set
        :type status: String
        """
        self.status = status

    def get_status(self):
        """
        Returns the status for testing purposes

        :return: the status
        :rtype: String or None
        """
        return self.status

class MockSerialArmController:
    """
    Mock of SerialArmController
    """
    def __init__(self):
        """
        Constructor for MockSerialArmController
        """
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
        Mock open_arm
        """
        self.open_arm_bool = True

    def close_arm(self):
        """
        Mock close_arm
        """
        self.close_arm_bool = True

    def portrait(self):
        """
        Mock portrait
        """
        self.portrait_bool = True

    def landscape(self):
        """
        Mock landscape
        """
        self.landscape_bool = True

    def tilt(self):
        """
        Mock tilt
        """
        self.tilt_bool = True

    def nod(self):
        """
        Mock nod
        """
        self.nod_bool = True

    def shake(self):
        """
        Mock shake
        """
        self.shake_bool = True

    def _shutdown(self):
        """
        Mock _shutdown
        """
        self.shutdown_bool = True

    def set_pitch(self, val):
        """
        Mock set_pitch

        :param val: the value to set self.pitch to
        :type val: int
        """
        self.pitch = val

    def set_yaw(self, val):
        """
        Mock set_yaw

        :param val: the value to set self.yaw to
        :type val: int
        """
        self.yaw = val

    def set_roll(self, val):
        """
        Mock set_roll

        :param val: the value to set self.roll to
        :type val: int
        """
        self.roll = val



class MockLogFile():
    """
    Mock of LogFile
    """
    def __init__(self):
        """
        Constructor for MockLogFile
        """
        self.arr = []

    def write(self, text):
        """
        Mock write. Appends text to self.arr

        :param text: the content to append
        :type text: String
        """
        self.arr.append(text)

class MockSpinBox():
    """
    Mock of SpinBox

    :param val: the intial value of val. Defaults to 0
    :type val: int, optional
    """
    def __init__(self, val=0):
        """
        Constructor for MockSpinBox
        """
        self.val = val

    def get(self):
        """
        Mock of get

        :return: self.val
        :rtype: int, optional
        """
        return self.val

    def set(self, val):
        """
        Mock of set

        :param val: the value to set self.val to
        :type val: int
        """
        self.val = val


class MockSlider():
    """
    Mock of Slider

    :param val: the value to set self.val to
    :type val: int
    """
    def __init__(self, val=0):
        """
        Constructor for MockSlider
        """
        self.val = val

    def get(self):
        """
        Mock of get

        :return: self.val
        :rtype: int, optional
        """
        return self.val

    def set(self, val):
        """
        Mock of set

        :param val: the value to set self.val to
        :type val: int
        """
        self.val = val
