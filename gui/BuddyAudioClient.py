"""
Handles streaming of microphone audio from PC to Mobile Application
"""

import pyaudio
import socket
import threading
import copy
import time
from contextlib import contextmanager

class BuddyAudioClient:
    """
    A TCP client that sends microphone input audio data.
    Uses pyaudio to get mic input. Then sends audio data as
    raw bytes.

    :param ip_addr: the ip address of the server
    :type ip_addr: string
    :param port: the port number of the server
    :type port: int
    :param frame: frame used in error display, defaults to None
    :type frame: Tkinter Frame, optional
    """

    default_sampling_rate = 44100
    default_width = 2
    default_num_input_channels = 1
    default_chunk_size = 1024

    def __init__(self, ip_addr, port, frame=None):
        """
        Constructor for BuddyAudioClient
        """

        self.server_ip = ip_addr
        self.port_num = port
        self.server_addr = (self.server_ip, self.port_num)
        self.client_socket = None
        self.continue_stream = None

        #running bools
        self.is_connected = False
        self.is_streaming = False

        self.audio_handler = pyaudio.PyAudio()
        #self.device_api_info = self.audio_handler.get_default_host_api_info()
        #self.input_device_info = self.audio_handler.get_default_input_device_info()
        #self.input_device_index = self.audio_handler.get_default_input_device_info()['index']
        self.current_device_dict = self.audio_handler.get_default_input_device_info()
        self.input_device_index = self.current_device_dict['index']

        self.sampling_rate = self.default_sampling_rate
        self.width = self.default_width
        self.num_input_channels = self.default_num_input_channels
        self.chunk_size = self.default_chunk_size

        self.audio_stream = None

        self.app_frame = frame


        self.input_device_list = None

    def showError(self, errorText):
        '''
        Displays an error on the Tkinter frame pass in the constructor

        :param errorText: the text that will be displayed in the error
        :type errorText: String
        '''
        self.app_frame.showPopupMessage(msg_text=errorText)

    def _connect(self):
        """
        Connects to the server and send the chunk size of audio data packets.
        Shows an error message on the frame if connection unsucessful.
        :return: true if connection successful, false otherwise
        :rtype: boolean
        """
        error_msg = "Audio Connection Error:\n"
        if(self.client_socket == None):
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(self.server_addr)
        except ConnectionRefusedError:
            error_msg += (
                "Connection Refused, "
                "check that the IP and port settings match "
                "those in the Survivor Buddy Android Application."
            )
            self.showError(error_msg)
            print(error_msg)
            self.is_connected = False
            return self.is_connected
        except TimeoutError:
            error_msg += (
                "Connection timed out,"
                "check that the IP and port settings match"
                " those in the Survivor Buddy Android Application."
            )
            self.showError(error_msg)
            print(error_msg)

            self.is_connected = False
            return self.is_connected
        except TypeError:
            error_msg += f'Audio port number "{self.port_num}" is and invalid port\n'
            error_msg += "Please change the audio port in the IP/Port Menu" 
            self.showError(error_msg)
            print(error_msg)
            self.is_connected = False
            return self.is_connected

        self.client_socket.sendall(str(self.chunk_size).encode('utf-8'))
        
        self.is_connected = True
        return self.is_connected

    def connect(self):
        """
        Starts a new thread to connect to the server if not connected yet. 
        Does nothing if already connected.
        """
        if(not self.is_connected):
            self.disconnect()
            self.connect_thread = threading.Thread(target=self._connect)
            self.connect_thread.start()

    def startStream(self, waitForConnect=False):
        """
        Starts a thread to begin streaming audio data if connected or if
        waitForConnect is true. Value of waitForConnect is passed to _startStream()

        :param waitForConnect: if true will allow the stream thread to begin before
            connection to server is established. Defaults to False
        :type waitForConnect: boolean, optional
        :return: true if thread is started, false otherwise
        :rtype: boolean
        """
        if(self.is_connected or waitForConnect):
            self.stream_thread = threading.Thread(
                target=self._startStream, 
                kwargs={'waitForConnect':waitForConnect}
            )
            self.stream_thread.start()
            return True
        else:
            return False

    def stopStream(self):
        """
        Stops the stream thread if running.
        """
        if(self.audio_stream is not None):

            self.continue_stream = False
            if(self.audio_stream.is_active()):
                self.audio_stream.close()
            

    def disconnect(self):
        """
        Disconnect from the server.
        """
        if(self.client_socket is not None):
            self.client_socket.close()
        self.client_socket = None
        self.is_connected = False

    def isStreaming(self):
        """
        Checks if pyaudio stream is active

        :return: True if streaming audio data, False otherwise
        :rtype: boolean
        """
        if(self.audio_stream is None):
            return False
        try:
            r_bool = self.audio_stream.is_active()
        except OSError:
            r_bool = False
        return r_bool

    def initAudioHandler(self):
        """
        Resets the pyaudio.Pyaudio() object. Terminates and re inits it.
        """
        if(self.audio_handler is not None):
            self.audio_handler.terminate()
            self.audio_handler = pyaudio.PyAudio()

    def _startStream(self, waitForConnect=False):
        """
        Initializes the stream object and begins the loop to get audio and send it to server

        :param waitForConnect: if true will wait for connect thread to end before
            initilaizing the audio handler and beinging the stream. Defaults to False
        :type waitForConnect: boolean, optional
        """

        if(waitForConnect):
            self.connect_thread.join()
            if(not self.is_connected):
                return
        
        self.initAudioHandler()
        
        self.audio_stream = self.audio_handler.open(
            format=self.audio_handler.get_format_from_width(self.width),
            channels=self.num_input_channels,
            rate=self.sampling_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            input_device_index=self.input_device_index
        )

        self.continue_stream = True
        while self.continue_stream:
            self.streamLoop()


    def streamLoop(self):
        """
        Gets chunk_size bytes of audio data from audio device and sends that data
        as a packet of raw bytes to the server.
        """
        try:
            audio_data = self.audio_stream.read(self.chunk_size)
        except IOError:
            self.continue_stream = False
        if(self.client_socket is None):
            self.continue_stream = False
        elif(self.client_socket._closed):
            self.continue_stream = False
        else:
            try:
                self.client_socket.sendall(audio_data)
            except ConnectionResetError:
                self.continue_stream = False
                self.is_connected = False
            except ConnectionAbortedError:
                self.continue_stream = False
                self.is_connected = False




    def setPortNum(self, new_port):
        """
        Sets the port number used to connect to the server.
        
        :param new_port: the value to set self.port_num to
        :type new_port: int
        """
        self.port_num = new_port
        self.server_addr = (self.server_ip, self.port_num)
    

    def getInputDeviceNames(self):
        """
        Gets the names of all audio input devices on the current instance of
        self.audio_handler. Returns it as a list of strings

        :return: A list of strings which are the device names
        :rtype: list[String]
        """
        device_name_list = []
        for mdict in self.getInputDeviceDicts():
            device_name_list.append(mdict['name'])

        return device_name_list

    def getInputDeviceDicts(self):
        """
        Gets a list of dictionaries which contain info about the input audio devices.

        :return: A list of dictionaries containing audio device info
        :rtype: list[dict]
        """
        dict_list = []

        api_info = self.audio_handler.get_default_host_api_info()
        device_count = api_info['deviceCount']
        host_api_index = api_info['index']

        for device_index in range(0, device_count):
            device_dict = self.audio_handler.get_device_info_by_host_api_device_index(
                host_api_index,
                device_index
            )
            if(device_dict['maxInputChannels'] >= 1):
                dict_list.append(copy.deepcopy(device_dict))

        return dict_list

    def setInputDevice(self, device_name):
        """
        Changes the current input device from which audio data is pulled.

        :param device_name: the name of the device which will become the new input
        :type device_name: String
        """
        print(f'NAME: {device_name}')
        device_dicts = self.getInputDeviceDicts()
        chosen_dict = None

        for d in device_dicts:
            if(d['name'] == device_name):
                chosen_dict = d
                self.current_device_dict = copy.deepcopy(d)
                break

        if(chosen_dict == None):
            print("ERROR: Device not found")
        else:
            self.input_device_index = chosen_dict['index']

    def getCurrentDeviceName(self):
        """
        Returns the current input device name

        :return: The name of the current device
        :rtype: String
        """
        print(f"DEV: {self.current_device_dict['name']}")
        return self.current_device_dict['name']

    def setDeviceDictToDefault(self):
        """
        Sets the current_device_dict back to its default
        """
        self.current_device_dict = self.audio_handler.get_default_input_device_info()


    @contextmanager
    def refreshHandler(self):
        """
        Refreshes the current self.audio_handler pyaudio.Pyaudio object. Stops the stream, terminates the
        current audio_handler, inits a new one, then starts the stream if it was previously running. This function
        uses context manager to prevent premature starting of the stream.
        """
        
        try:
            was_streaming = False
            if(self.isStreaming()):
                was_streaming = True
                self.stopStream()
            if(self.audio_handler is not None):
                self.audio_handler.terminate()
            self.audio_handler = pyaudio.PyAudio()
            yield
        finally:
            if(was_streaming):
                self.startStream()
            
        
