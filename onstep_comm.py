# Onstep working ESP32 test program
# Replace with your onstep IP address and port

ip_address = '192.168.1.27'
port = 9996

import socket
import readline
import time
import sys

MAX_LEN = 32
SOCKET_TIMEOUT = 3.0

class ErrorMessageReadError(Exception):
    pass

class ConnectionError(Exception):
    pass

class MissingTerminatingCharacterError(Exception):
    pass

class SocketTimeoutError(Exception):
    pass

class RetryCountExceededError(Exception):
    pass

class OnstepInterface:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Set to allow socket re-use, if available
        self.sock.settimeout(SOCKET_TIMEOUT)  # set a timeout
    
        try:
            self.sock.connect((self.ip_address, self.port))
        except socket.error as e:
            raise ConnectionError(f"Could not connect to onstep device: {e}")

    def close(self):
        if self.sock is not None:
            try:
                self.sock.close()
                self.is_connected = False
            except socket.error as e:
                print(f"Could not close connection to onstep device: {e}")


    def send_command(self, command, delay = 0):
        retry_count = 0
        while retry_count < 3:
            try:
                self.connect()
                self.sock.sendall(command.encode('utf-8'))
                time.sleep(delay)
                return self.read_response()
            except SocketTimeoutError:
                retry_count += 1
                if retry_count >= 3:
                    raise RetryCountExceededError("Retry count exceeded")
                    self.close()
            except (ErrorMessageReadError, MissingTerminatingCharacterError) as e:
                print("Could not send command:")
                print(e)
            #finally: #Ideally we would do this, however, it causes problems with re-using the socket and refactoring is problematic
               # self.close()

    def read_response(self):
        try:
            data = self.sock.recv(MAX_LEN).decode('utf-8')
            if len(data) > 0 and data[-1] != '#' and data not in ['0', '1']:
                raise MissingTerminatingCharacterError("Missing terminating character")
            return data[:-1] if data[-1] == '#' else data
        except socket.timeout:
            raise SocketTimeoutError("Socket Timeout")
        except socket.error as e:
            raise ErrorMessageReadError(str(e))
