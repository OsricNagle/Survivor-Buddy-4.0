#handles the screen recording funtionality of Survivor Buddy 4.0

import subprocess
import time
import datetime
import signal
import pyminizip
import os

class ScreenRecorder:
    def __init__(self, filename=None, display_stdout=False, framerate=30, encrypt=False, password='default', output_folder='./screen_recordings', file_type='.mp4'):
        """
        Init ScreenRecorder class
        """
        self.output_filename = filename
        self.output_folder = output_folder  #default output folder is working directory
        self.recording_process = None
        self.process_out = subprocess.DEVNULL
        self.framerate = framerate
        self.file_extension = file_type #default file type is .mp4
        self.recording_running = False
        self.file_password = password
        self.current_recording_path = None
        self.encrypt_bool = encrypt
        self.zip_path = None

        if display_stdout:
            self.process_out = subprocess.STDOUT

    def generateFilepath(self):
        """
        Generates a default filename based on the date and time
        """
        date_str = '-' + datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
        file_name = 'SuvivorBuddyRecoding' + date_str + self.file_extension
        return os.path.join(self.output_folder, file_name)
        #return self.output_folder + 'SuvivorBuddyRecoding' + date_str + self.file_extension

    def encryptFile(self, filename):

        base = os.path.basename(filename)
        self.zip_path = os.path.join(self.output_folder, os.path.splitext(base)[0] + '.zip')
        pyminizip.compress(filename, None, self.zip_path, self.file_password, 0)
        

    def setPassword(self, password):
        self.file_password = password

    def setFilename(self, name):
        """
        Sets the value of output_filename
        """
        self.output_filename = name

    def setOutputFolder(self, path):
        self.output_folder = path

    def startRecording(self):
        """
        Starts ffmpeg screen recording process
        """

        self.current_recording_path = self.output_filename
        if self.current_recording_path is None:
            self.current_recording_path = self.generateFilepath()
        print(self.current_recording_path)
        cmd  = [
            'ffmpeg', 
            '-f', 
            'gdigrab', 
            '-framerate', 
            str(self.framerate), 
            '-i', 
            'desktop', 
            '-pix_fmt', 
            'yuv420p', 
            self.current_recording_path
        ]
        self.recording_process = subprocess.Popen(
            cmd, 
            stdout=self.process_out, 
            stderr=self.process_out, 
            shell=True, 
            stdin=subprocess.PIPE
        )
        self.recording_running = True
        print("Screen Record Started")

    def isRecording(self):
        """
        Returns true if currently recording
        """
        return self.recording_running



    def stopRecording(self):
        """
        Stops the ffmpeg screen recording process
        """
        self.recording_process.communicate(input=b"q")
        if(self.encrypt_bool):
            print("Encrypting")
            self.encryptFile(self.current_recording_path)
            os.remove(self.current_recording_path)
        self.recording_running = False
        print("Screen Record Stopped")

    def testFun(self):

        self.startRecording()
        time.sleep(5)
        self.stopRecording()

"""
time.sleep(2)
myr = ScreenRecorder()
myr.testFun()
"""
