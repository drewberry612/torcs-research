import socket
import sys
import time
import subprocess
from server_state import ServerState
from driver_action import DriverAction

data_size = 2**17

class Client(object):
    def __init__(self):
        # Server connection variables (shouldn't change)
        self.host= 'localhost'
        self.port= 3001
        self.sid= 'SCR'

        self.maxSteps = 9000

        self.num = 0
        self.track = 11
        self.command = ["wtorcs.exe", "-r", f"config\\raceman\\{self.track}.xml"]

        # Initialise connection and bot
        self.S = ServerState()
        self.R = DriverAction()
        self.setup_connection()

    def setup_connection(self):
        # == Set Up UDP Socket ==
        try:
            self.so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as emsg:
            self.shutdown()
            self.setup_connection()
            return

        # == Initialize Connection To Server ==
        self.so.settimeout(1)

        n_fails = 30
        while True:
            # This string establishes 'track' sensor angles! You can customize them.
            a= "-90 -75 -60 -45 -30 -20 -15 -10 -5 0 5 10 15 20 30 45 60 75 90"

            initmsg = '%s(init %s)' % (self.sid,a)

            try:
                self.so.sendto(initmsg.encode(), (self.host, self.port))
            except socket.error as emsg:
                self.shutdown()
                self.setup_connection()
                return

            sockdata= str()
            try:
                sockdata,addr = self.so.recvfrom(data_size)
                sockdata = sockdata.decode('utf-8')
            except socket.\
                    error as emsg:
                time.sleep(0.05)
                subprocess.Popen(self.command)
                if (n_fails < 0):
                    quit()
                n_fails -= 1

            identify = '***identified***'
            if identify in sockdata:
                print(self.command)
                #self.track += 1
                # if self.track > 10:
                #     self.track = 1
                self.command = ["wtorcs.exe", "-r", f"config\\raceman\\{self.track}.xml"]
                break

    def get_servers_input(self):
        '''Server's input is stored in a ServerState object'''
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
                self.num += 1
                with open(f'temp/finished.txt', 'w') as file:
                    file.write(f"finished {self.num}")
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
                        
                break # Can now return from this function.

    def update(self, r):
        self.R.d = r

    def respond_to_server(self):
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
