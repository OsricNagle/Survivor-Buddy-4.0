# -*- coding: utf-8 -*-
"""
Handles display of connection status for arduino/arm hardware
"""

import tkinter as tk
import tkinter.ttk as ttk

class StatusBar(tk.Frame):
    '''
    Displays the connection status of the GUI to the arm

    '''

    def __init__(self, master, **kwargs):
        '''
        Constructor for StatusBar

        :param master: The Tk parent widget
        :type master: Tk
        '''

        super().__init__(master, **kwargs)
        
        # STATUS #
        self.status_frame = tk.Frame(self)
        self.status_frame.pack(side="left")
        
        self.status_label = ttk.Label(self.status_frame, text="Status:")
        self.status_label.pack(side="left")
        
        self.status_text = tk.StringVar()
        self.status_text.set("DISCONNECTED")
        self.status_text_label = ttk.Label(
            self.status_frame, textvariable=self.status_text)
        self.status_text_label.pack(side="left")


    def set_status(self, status):
        '''
        Sets the status of the GUI to the arm

        :param status: The status to set to
        :type status: String
        '''

        self.status_text.set(status)
        