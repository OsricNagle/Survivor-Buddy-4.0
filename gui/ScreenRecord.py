#handles the screen recording funtionality of Survivor Buddy 4.0

import subprocess
import time
import datetime
import signal

class ScreenRecorder:

    def __init__(self, filename=None, display_stdout=False, framerate=30):
        """
        Inits ScreenRecorder class
        """
        self.output_filename = filename
        self.output_filepath = '../screen_recordings/'
        self.recording_process = None
        self.process_out = subprocess.DEVNULL
        self.framerate = framerate
        self.file_extension = '.mp4'
        self.recording_running = False

        if display_stdout:
            self.process_out = subprocess.STDOUT

    def generateFilename(self):
        """
        Generates a default filename based on the date and time
        """

        date_str = '-' + datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
        return self.output_filepath + 'SuvivorBuddyRecoding' + date_str + self.file_extension

    def setFilename(self, name):
        """
        Sets the value of output_filename
        """
        self.output_filename = name

    def startRecording(self):
        """
        Starts ffmpeg screen recording process
        """

        out_name = self.output_filename
        if out_name is None:
            out_name = self.generateFilename()

        cmd  = ['ffmpeg', '-f', 'gdigrab', '-framerate', str(self.framerate), '-i', 'desktop', '-pix_fmt', 'yuv420p', out_name]
        self.recording_process = subprocess.Popen(cmd, stdout=self.process_out, stderr=self.process_out)
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
        self.recording_process.send_signal(signal.CTRL_C_EVENT)
        self.recording_running = False
        print("Screen Record Stopped")

    def tenSec(self):

        self.startRecording()
        time.sleep(5)
        self.stopRecording()
        

myr = ScreenRecorder()
myr.tenSec()
