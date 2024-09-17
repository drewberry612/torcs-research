import socket
import sys
import time
import subprocess
from server_state import ServerState
from driver_action import DriverAction

data_size = 2**17

class Client(object):
    """
    Runs the game and connects to the game server without displaying the graphics
    """

    def __init__(self):
        # Server connection variables
        self.host= 'localhost'
        self.port= 3001
        self.sid= 'SCR'

        self.maxSteps = 9000 # Maximum timesteps to run GA for

        self.track = 1 # Used for switching between tracks
        self.command = ["wtorcs.exe", "-r", f"config\\raceman\\{self.track}.xml"]

        # Initialise the game and connection
        self.S = ServerState()
        self.R = DriverAction()
        self.setup_connection()

    def setup_connection(self):
        """
        Controls the execution of the game and the creation of server connections
        """

        # Set up UDP socket
        try:
            self.so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as emsg:
            self.shutdown()
            self.setup_connection()
            return

        # Initialize connection to server
        self.so.settimeout(1)
        n_fails = 30
        while True:
            # This string establishes 'track' sensor angles, you can customize them
            a = "-90 -75 -60 -45 -30 -20 -15 -10 -5 0 5 10 15 20 30 45 60 75 90"
            initmsg = '%s(init %s)' % (self.sid,a)

            # Send initialisation message
            try:
                self.so.sendto(initmsg.encode(), (self.host, self.port))
            except socket.error as emsg:
                self.shutdown()
                self.setup_connection()
                return

            # Wait for response from socket
            sockdata= str()
            try:
                sockdata,addr = self.so.recvfrom(data_size)
                sockdata = sockdata.decode('utf-8')
            except socket.\
                    error as emsg: # if no response
                time.sleep(0.05)
                subprocess.Popen(self.command) # reopen the game
                if (n_fails < 0):
                    quit()
                n_fails -= 1

            identify = '***identified***'
            if identify in sockdata: # when the connection is identified
                print(self.command)
                self.track += 1
                if self.track > 10:
                    self.track = 1
                self.command = ["wtorcs.exe", "-r", f"config\\raceman\\{self.track}.xml"]
                break

    def get_servers_input(self):
        '''
        Receives the socket data and interprets it
        Server's input is stored in a ServerState object
        Controls the ending of a server connection
        '''
        if not self.so: return
        sockdata = str()

        while True:
            try:
                # Receive server data
                sockdata,addr = self.so.recvfrom(data_size)
                sockdata = sockdata.decode('utf-8')
            except socket.error as emsg:
                self.shutdown()
                self.setup_connection()

            if '***identified***' in sockdata:
                continue
            elif '***shutdown***' in sockdata:
                print((("Server has stopped the race on %d. ") %
                        (self.port)))
                self.shutdown()
                self.setup_connection()

                return
            elif '***restart***' in sockdata:
                self.R.d['meta'] = 0
                self.setup_connection()
                
                return
            elif not sockdata: # Empty?
                continue       # Try again.
            else:
                self.S.parse_server_str(sockdata)
                        
                break # Can now return from this function

    def update(self, r):
        self.R.d = r

    def respond_to_server(self):
        """
        Returns the actuator data to the server for use in-game
        """

        if not self.so: return
        try:
            message = repr(self.R)
            self.so.sendto(message.encode(), (self.host, self.port))
        except socket.error as emsg:
            print("Error sending to server: %s Message %s" % (emsg[1],str(emsg[0])))
            sys.exit(-1)

    def shutdown(self):
        if not self.so: return
        print(("Race terminated. Shutting down %d."
               % (self.port)))
        self.so.close()
        self.so = None
