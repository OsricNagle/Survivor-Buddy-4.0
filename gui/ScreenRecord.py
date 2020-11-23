#handles the screen recording funtionality of Survivor Buddy 4.0

import subprocess
import time
import datetime
import signal
import pyminizip
import os

class ScreenRecorder:
    """
    Utilizes FFMPEG to record the entire desktop screen. Also allows for setting of 
    output filepath and password protected encrypting of files.

    :param filename: custom filepath of output file. Defaults to None
    :type filename: String, optional
    :param display_stdout: if true prints out ffmpeg execution to terminal, if false hides it. Defaults to False.
    :type display_stdout: boolean, optional
    :param framerate: the framerate at which to record. Defaults to 30
    :type framerate: int, optional
    :param encrypt: if true turns on file encryption. Defaults to False
    :type encrypt: boolean, optional
    :param password: the password of encrypted files. Defaults to 'default'
    :type password: String. optional
    :param output_folder: the folder to which files will be saved. Defaults to './screen_recordings'
    :type output_folder: String, optional
    :param file_type: the file type of the recordings. Defaults to '.mp4'
    :type file_type: String, optional
    """

    def __init__(self, filename=None, display_stdout=False, framerate=30, encrypt=False, password='default', output_folder='./screen_recordings', file_type='.mp4'):
        """
        Constructor for ScreenRecorder
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
        Generates a filename based on the the current date time

        :return: the generated filepath
        :rtype: String
        """
        date_str = '-' + datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
        file_name = 'SuvivorBuddyRecoding' + date_str + self.file_extension
        return os.path.join(self.output_folder, file_name)
        #return self.output_folder + 'SuvivorBuddyRecoding' + date_str + self.file_extension

    def encryptFile(self, filename):
        """
        Encrypts the a file with password protection. Does so by placing it into a zip folder

        :param filename: the file path of the file to encrypt
        :type filename: String
        """
        base = os.path.basename(filename)
        self.zip_path = os.path.join(self.output_folder, os.path.splitext(base)[0] + '.zip')
        pyminizip.compress(filename, None, self.zip_path, self.file_password, 0)
        

    def setPassword(self, password):
        """
        Sets the password to encrypt files with. DOES NOT change password of previously encrypted files

        :param password: the new password
        :type password: String
        """
        self.file_password = password

    def setFilename(self, name):
        """
        Changes the output file name. NOT the output folder

        :param name: the new name
        :type name: String
        """
        self.output_filename = name

    def setOutputFolder(self, path):
        """
        Changed the output folder of recordings

        :param path: the path of the new output folder
        :type path: String
        """
        self.output_folder = path

    def startRecording(self):
        """
        FFMPEG desktop recording as a subprocess in the background.
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
        Checks if currently recording

        :return: true if recording, false otherwise
        :rtype: boolean
        """
        return self.recording_running



    def stopRecording(self):
        """
        Stops the ffmpeg screen recording process. If file encryptions is on the file will be encrypted then
        the unencrypted file will be deleted.
        """
        self.recording_process.communicate(input=b"q")
        if(self.encrypt_bool):
            print("Encrypting")
            self.encryptFile(self.current_recording_path)
            os.remove(self.current_recording_path)
        self.recording_running = False
        print("Screen Record Stopped")
