import tkinter as tk
import math

class TrackWindow():
    """
    Controls the operation of drawing the track as an agent drives
    """

    def __init__(self, s, r):
        # Initialise the window
        self.window = tk.Tk()
        self.window.geometry("600x600")
        self.window.title("Track Map")

        # Create the canvas which will house the drawing
        self.canvas = tk.Canvas(self.window, width=600, height=600)
        self.canvas.pack()

        self.x = 300
        self.y = 300
        self.track_edge_coords = [] # reset them every update
        self.old_angle = 0

        self.S = s
        self.R = r

    def update_data(self, s, r):
        """
        Called at every update to gain the curret data
        """
        self.S = s
        self.R = r
    
    def update_coords(self, vel, new_angle):
        """
        Basic kinematics to move the position
        """
        angle = self.old_angle - new_angle

        new_x = self.x + vel * math.sin(angle)
        new_y = self.y - vel * math.cos(angle)

        self.x = new_x
        self.y = new_y
        self.old_angle = angle
    
    def find_track_edge(self, track):
        """
        Uses the track sensor to determine the track edge for drawing
        """

        self.track_edge_coords = []
        a = [-90, -75, -60, -45, -30, -20, -15, -10, -5, 0, 5, 10, 15, 20, 30, 45, 60, 75, 90]

        count = 0
        for i in a:
            if track[count] < 200:
                angle = self.old_angle + math.radians(i)
                x = self.x + (track[count]/200) * math.sin(angle)
                y = self.y - (track[count]/200) * math.cos(angle)
                self.track_edge_coords.append([x,y])
            count+=1

    def update_window(self):
        """
        Determines the velocity vector and the angle to update the position
        Draws each track edge coordinate
        """

        vel = math.sqrt(self.S.d['speedX']**2 + self.S.d['speedY']**2) / 400
        angle = self.R.d['steer'] * 2 * math.pi / 28

        self.find_track_edge(self.S.d['track'])
        self.update_coords(vel, angle)
        
        radius = 1
        for i in self.track_edge_coords:
            self.canvas.create_oval(i[0] - radius, i[1] - radius, i[0] + radius, i[1] + radius, fill="black")

        self.window.update()
        self.window.after(50, self.update_window) # Enables recursion