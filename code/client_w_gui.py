import socket
import sys
import time
import threading
from stats_window import StatsWindow
from track_window import TrackWindow
from server_state import ServerState
from driver_action import DriverAction

data_size = 2**17

class Client_w_GUI(object):
    def __init__(self):
        # Server connection variables (shouldn't change)
        self.host = 'localhost'
        self.port = 3001
        self.sid = 'SCR'

        self.maxSteps = 10000000

        self.debug = False
        self.draw_track = False
        self.valid1 = True
        self.valid2 = True

        # Initialise connection
        self.S = ServerState()
        self.R = DriverAction()
        self.stat_window = None
        self.track_window = None
        self.setup_connection()

    def stat_gui(self):
        self.stat_window = StatsWindow(self.S, self.R)
        self.stat_window.window.mainloop()
    
    def track_gui(self):
        self.track_window = TrackWindow(self.S, self.R)
        self.track_window.window.mainloop()

    def setup_connection(self):
        # == Set Up UDP Socket ==
        try:
            self.so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as emsg:
            print('Error: Could not create socket...')
            sys.exit(-1)

        # == Initialize Connection To Server ==
        self.so.settimeout(1)

        n_fail = 5
        while True:
            # This string establishes track sensor angles! You can customize them.
            a= "-90 -75 -60 -45 -30 -20 -15 -10 -5 0 5 10 15 20 30 45 60 75 90"

            initmsg = '%s(init %s)' % (self.sid,a)

            try:
                self.so.sendto(initmsg.encode(), (self.host, self.port))
            except socket.error as emsg:
                sys.exit(-1)

            sockdata= str()
            try:
                sockdata,addr = self.so.recvfrom(data_size)
                sockdata = sockdata.decode('utf-8')
            except socket.\
                    error as emsg:
                time.sleep(1.0)

            identify = '***identified***'
            if identify in sockdata:
                # Start the Tkinter window on another thread
                if self.debug and self.stat_window == None:
                    gui_thread = threading.Thread(target=self.stat_gui)
                    gui_thread.daemon = True
                    gui_thread.start()
                if self.draw_track and self.track_window == None:
                    gui_thread = threading.Thread(target=self.track_gui)
                    gui_thread.daemon = True
                    gui_thread.start()
                
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
                pass

            if '***identified***' in sockdata:
                continue
            elif '***shutdown***' in sockdata:
                print((("Server has stopped the race on %d. ") %
                        (self.port)))
                self.shutdown()
                return
            elif '***restart***' in sockdata:
                self.R.d['meta'] = 0
                self.setup_connection()
                return
            elif not sockdata: # Empty?
                continue       # Try again.
            else:
                self.S.parse_server_str(sockdata)
                if self.debug:
                    self.stat_window.update_data(self.S, self.R)
                    if self.valid1: # starts the recursive updates for stats gui
                        self.stat_window.update_window()
                        self.valid1 = False
                if self.draw_track:
                    self.track_window.update_data(self.S, self.R)
                    if self.valid2: # starts the recursive updates for track gui
                        self.track_window.update_window()
                        self.valid2 = False
                        
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