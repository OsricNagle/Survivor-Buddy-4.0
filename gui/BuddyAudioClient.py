import pyaudio
import socket
import threading
import copy
import time
from contextlib import contextmanager

class BuddyAudioClient:

    default_sampling_rate = 44100
    default_width = 2
    default_num_input_channels = 1
    default_chunk_size = 1024

    def __init__(self, ip_addr, port, frame=None):

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
        self.app_frame.showPopupMessage(msg_text=errorText)

    def _connect(self):
        error_msg = "Audio Connection Error:\n"
        if(self.client_socket == None):
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(self.server_addr)
        except ConnectionRefusedError:
            error_msg += (
                "Connection timed out, "
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
                "check that the IP and ports match"
                " those in the android app's settings."
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

    '''
    def connectAndStart(self):
        if(not self.is_connected):
            threading.Thread(target=self.handleConnectAndStart).start()
    '''



    def connect(self):
        if(not self.is_connected):
            self.disconnect()
            self.connect_thread = threading.Thread(target=self._connect)
            self.connect_thread.start()

    def startStream(self, waitForConnect=False):
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
        if(self.audio_stream is not None):

            self.continue_stream = False
            if(self.audio_stream.is_active()):
                self.audio_stream.close()
            

    def disconnect(self):
        if(self.client_socket is not None):
            self.client_socket.close()
        self.client_socket = None
        self.is_connected = False

    def isStreaming(self):
        if(self.audio_stream is None):
            return False
        try:
            r_bool = self.audio_stream.is_active()
        except OSError:
            r_bool = False
        return r_bool

    '''
    def handleConnectAndStart(self):
        time.sleep(1)
        if(self.connect()):
            self.is_connected = True
            self.start_stream()
    '''

    '''
    def disconnectAndStop(self):
        self.continue_stream = False
        print(self.client_socket)
        if(self.client_socket is not None):
            self.client_socket.close()
        self.client_socket = None
        self.is_connected = False
    '''

    def initAudioHandler(self):
        if(self.audio_handler is not None):
            self.audio_handler.terminate()
            self.audio_handler = pyaudio.PyAudio()

    def _startStream(self, waitForConnect=False):

        
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
        self.port_num = new_port
        self.server_addr = (self.server_ip, self.port_num)
    

    def getInputDeviceNames(self):
        #returns a list[str] of input device names
        device_name_list = []
        for mdict in self.getInputDeviceDicts():
            device_name_list.append(mdict['name'])

        return device_name_list

    def getInputDeviceDicts(self):
        dict_list = []
        #TODO: May need to set device count dynamically here

        api_info = self.audio_handler.get_default_host_api_info()#self.device_api_info['deviceCount']
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
        print(f"DEV: {self.current_device_dict['name']}")
        return self.current_device_dict['name']

    def setDeviceDictToDefault(self):
        self.current_device_dict = self.audio_handler.get_default_input_device_info()


    @contextmanager
    def refreshHandler(self):

        
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
            
        
