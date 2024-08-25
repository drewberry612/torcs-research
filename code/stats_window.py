import math
import tkinter as tk

class StatsWindow():
    def __init__(self, s, r):
        self.window = tk.Tk()
        self.window.geometry("1400x800")
        self.window.title("Car Statistics")
        self.window.state('zoomed')

        self.S = s
        self.R = r

        self.create_grid()

    def update_data(self, s, r):
        self.S = s
        self.R = r

    def create_grid(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill='both')

        # Configure the main frame to have a uniform grid
        for i in range(2):  # Two rows
            frame.grid_rowconfigure(i, weight=1, uniform="equal_height")
        for j in range(3):  # Three columns
            frame.grid_columnconfigure(j, weight=1, uniform="equal_width")

        angle = tk.Frame(frame, borderwidth=1, relief="solid")
        angle.grid(row=0, column=0, sticky="nsew")
        self.angle_cell(angle)

        stats = tk.Frame(frame, borderwidth=1, relief="solid")
        stats.grid(row=0, column=1, sticky="nsew")
        self.stats_cell(stats)

        steer = tk.Frame(frame, borderwidth=1, relief="solid")
        steer.grid(row=0, column=2, sticky="nsew")
        self.steer_cell(steer)

        speeds = tk.Frame(frame, borderwidth=1, relief="solid")
        speeds.grid(row=1, column=0, sticky="nsew")
        self.speed_cell(speeds)

        rpm = tk.Frame(frame, borderwidth=1, relief="solid")
        rpm.grid(row=1, column=1, sticky="nsew")
        self.rpm_cell(rpm)

        actuators = tk.Frame(frame, borderwidth=1, relief="solid")
        actuators.grid(row=1, column=2, sticky="nsew")
        self.actuator_cell(actuators)

    def angle_cell(self, angle):
        angle.grid_rowconfigure(0, weight=1)
        angle.grid_rowconfigure(1, weight=2)
        angle.grid_rowconfigure(2, weight=1)
        angle.grid_columnconfigure(0, weight=1)

        frame1 = tk.Frame(angle)
        frame1.grid(row=0, column=0, sticky="ew")
        tk.Label(frame1, text="Angle from Track Axis").pack(expand=True, pady=10, anchor="center")

        frame2 = tk.Frame(angle)
        frame2.grid(row=1, column=0, sticky="ew")

        self.angle_dial = tk.Canvas(frame2, width=340, height=340)
        self.angle_dial.pack()

        self.angle_dial.create_line(10, 300, 330, 300, width=2)
        self.needle1 = self.angle_dial.create_line(170, 300, 170, 140, width=2, fill='red')

        frame3 = tk.Frame(angle)
        frame3.grid(row=2, column=0, sticky="ew")

        self.trackPos = tk.Label(frame3, text="Distance from the track axis: ", anchor="w")
        self.trackPos.pack(side="top", padx=10, fill="x")

    def stats_cell(self, stats):
        stats.grid_rowconfigure(0, weight=2)
        stats.grid_rowconfigure(1, weight=1)
        stats.grid_columnconfigure(0, weight=1)

        # make this whole cell into 2 boxes stacked on top of eachother
        frame1 = tk.Frame(stats)
        frame1.grid(row=0, column=0, sticky="ew")
        tk.Label(frame1, text="Race Stats").pack(expand=True, pady=10, anchor="center")

        # each label is saved as the name of its variable
        self.distRaced = tk.Label(frame1, text="Distance travelled: ", anchor="w")
        self.distRaced.pack(side="top", padx=10, fill="x")
        self.distFromStart = tk.Label(frame1, text="Distance from start of lap: ", anchor="w")
        self.distFromStart.pack(side="top", padx=10, fill="x")
        self.curLapTime = tk.Label(frame1, text="Current lap time: ", anchor="w")
        self.curLapTime.pack(side="top", padx=10, fill="x")
        self.lastLapTime = tk.Label(frame1, text="Last lap time: ", anchor="w")
        self.lastLapTime.pack(side="top", padx=10, fill="x")
        self.racePos = tk.Label(frame1, text="Position in race: ", anchor="w")
        self.racePos.pack(side="top", padx=10, fill="x")

        tk.Label(frame1, text="Car Stats").pack(expand=True, pady=10, anchor="center")
        self.fuel = tk.Label(frame1, text="Remaining Fuel Percentage: ", anchor="w")
        self.fuel.pack(side="top", padx=10, fill="x")
        self.damage = tk.Label(frame1, text="Damage Percentage: ", anchor="w")
        self.damage.pack(side="top", padx=10, fill="x")

        tk.Label(frame1, text="Wheel Spin Velocity").pack(expand=True, pady=10, anchor="center")

        frame2 = tk.Frame(stats)
        frame2.grid(row=1, column=0, sticky="ew")

        for i in range(2):  # Two rows
            frame2.grid_rowconfigure(i, weight=1, uniform="equal_height")
        for j in range(2):  # Three columns
            frame2.grid_columnconfigure(j, weight=1, uniform="equal_width")
        
        self.flwheel = tk.Label(frame2, text="Front left: ", anchor="w")
        self.flwheel.grid(row=0, column=0, sticky="nsew", padx=10)
        self.frwheel = tk.Label(frame2, text="Front right: ", anchor="w")
        self.frwheel.grid(row=0, column=1, sticky="nsew", padx=10)
        self.blwheel = tk.Label(frame2, text="Back left: ", anchor="w")
        self.blwheel.grid(row=1, column=0, sticky="nsew", padx=10)
        self.brwheel = tk.Label(frame2, text="Back right: ", anchor="w")
        self.brwheel.grid(row=1, column=1, sticky="nsew", padx=10)

    def steer_cell(self, steer):
        steer.grid_rowconfigure(0, weight=1)
        steer.grid_rowconfigure(1, weight=2)
        steer.grid_columnconfigure(0, weight=1)

        frame1 = tk.Frame(steer)
        frame1.grid(row=0, column=0, sticky="ew")
        tk.Label(frame1, text="Steering Angle").pack(expand=True, pady=10, anchor="center")

        frame2 = tk.Frame(steer)
        frame2.grid(row=1, column=0, sticky="ew")

        self.steer_dial = tk.Canvas(frame2, width=340, height=340)
        self.steer_dial.pack()

        self.steer_dial.create_line(10, 300, 330, 300, width=2)
        self.needle2 = self.steer_dial.create_line(170, 300, 170, 140, width=2, fill='red')

    def speed_cell(self, speeds):
        speeds.grid_rowconfigure(0, weight=1)
        speeds.grid_rowconfigure(1, weight=2)
        speeds.grid_columnconfigure(0, weight=1)

        frame1 = tk.Frame(speeds)
        frame1.grid(row=0, sticky="ew")
        tk.Label(frame1, text="Directional Speeds").pack(expand=True, pady=10, anchor="center")

        frame2 = tk.Frame(speeds)
        frame2.grid(row=1, sticky="ew")

        frame2.grid_rowconfigure(0, weight=1)
        frame2.grid_columnconfigure(0, weight=1)
        frame2.grid_columnconfigure(1, weight=1)
        frame2.grid_columnconfigure(2, weight=1)

        # x
        subframe1 = tk.Frame(frame2)
        subframe1.grid(row=0, column=0)

        self.speeds_bar1 = tk.Canvas(subframe1, width=150, height=200)
        self.speeds_bar1.pack()
        self.create_bar(self.speeds_bar1, 0)

        tk.Label(subframe1, text="x").pack(expand=True, pady=10, anchor="center")

        # y
        subframe2 = tk.Frame(frame2)
        subframe2.grid(row=0, column=1)

        self.speeds_bar2 = tk.Canvas(subframe2, width=150, height=200)
        self.speeds_bar2.pack()
        self.create_bar(self.speeds_bar2, 0)

        tk.Label(subframe2, text="y").pack(expand=True, pady=10, anchor="center")

        # z
        subframe3 = tk.Frame(frame2)
        subframe3.grid(row=0, column=2)

        self.speeds_bar3 = tk.Canvas(subframe3, width=150, height=200)
        self.speeds_bar3.pack()
        self.create_bar(self.speeds_bar3, 0)

        tk.Label(subframe3, text="z").pack(expand=True, pady=10, anchor="center")

    def create_bar(self, canvas, value):
        canvas.delete("bar")  # Remove the previous bar
        bar_height = 200 * value  # Scale the value to the canvas height
        canvas.create_rectangle(20, 200 - bar_height, 130, 200, fill="blue", tags="bar")

    def rpm_cell(self, rpm):
        rpm.grid_rowconfigure(0, weight=1)
        rpm.grid_rowconfigure(1, weight=2)
        rpm.grid_columnconfigure(0, weight=1)

        frame1 = tk.Frame(rpm)
        frame1.grid(row=0, column=0, sticky="ew")
        frame1.grid_columnconfigure(0, weight=1)
        frame1.grid_columnconfigure(1, weight=1)
        tk.Label(frame1, text="RPM", anchor="center").grid(row=0, column=0, sticky="ew", padx=10)
        self.gear = tk.Label(frame1, text="Gear: ", anchor="center")
        self.gear.grid(row=0, column=1, sticky="ew", padx=10)

        frame2 = tk.Frame(rpm)
        frame2.grid(row=1, column=0, sticky="ew")

        self.rpm_dial = tk.Canvas(frame2, width=360, height=360)
        self.rpm_dial.pack()

        # Draw the outer circle
        self.rpm_dial.create_oval(50, 50, 350, 350)

        # Draw tick marks
        count = 0
        for i in range(-30, 211, 12):
            width = 2
            if count % 2 == 0:
                width = 4
            angle = math.radians(180 - i)
            x0 = 200 + (120 - 3 * width) * math.cos(angle)
            y0 = 200 - (120 - 3 * width) * math.sin(angle)
            x1 = 200 + 150 * math.cos(angle)
            y1 = 200 - 150 * math.sin(angle)
            
            self.rpm_dial.create_line(x0, y0, x1, y1, width=width)
            count+=1

        self.needle3 = self.rpm_dial.create_line(200, 200, 200 + 120 * math.cos(math.radians(210)), 200 - 120 * math.sin(math.radians(210)), width=2, fill='red')

        self.rpm_num = self.rpm_dial.create_text(200, 250, text="", anchor="center")

    def actuator_cell(self, actuators):
        actuators.grid_rowconfigure(0, weight=1)
        actuators.grid_rowconfigure(1, weight=2)
        actuators.grid_columnconfigure(0, weight=1)

        frame1 = tk.Frame(actuators)
        frame1.grid(row=0, sticky="ew")
        tk.Label(frame1, text="Actuators").pack(expand=True, pady=10, anchor="center")

        frame2 = tk.Frame(actuators)
        frame2.grid(row=1, sticky="ew")

        frame2.grid_rowconfigure(0, weight=1)
        frame2.grid_columnconfigure(0, weight=1)
        frame2.grid_columnconfigure(1, weight=1)
        frame2.grid_columnconfigure(2, weight=1)

        # Accelerator
        subframe1 = tk.Frame(frame2)
        subframe1.grid(row=0, column=0)

        self.actuator_bar1 = tk.Canvas(subframe1, width=150, height=200)
        self.actuator_bar1.pack()
        self.create_bar(self.actuator_bar1, 0)

        tk.Label(subframe1, text="Accelator").pack(expand=True, pady=10, anchor="center")

        # Brake
        subframe2 = tk.Frame(frame2)
        subframe2.grid(row=0, column=1)

        self.actuator_bar2 = tk.Canvas(subframe2, width=150, height=200)
        self.actuator_bar2.pack()
        self.create_bar(self.actuator_bar2, 0)

        tk.Label(subframe2, text="Brake").pack(expand=True, pady=10, anchor="center")

        # Clutch
        subframe3 = tk.Frame(frame2)
        subframe3.grid(row=0, column=2)

        self.actuator_bar3 = tk.Canvas(subframe3, width=150, height=200)
        self.actuator_bar3.pack()
        self.create_bar(self.actuator_bar3, 0)

        tk.Label(subframe3, text="Clutch").pack(expand=True, pady=10, anchor="center")

    def update_window(self):
        # Calculate needle end point
        x = 170 + 160 * math.sin(self.S.d['angle']/2)
        y = 300 - 160 * math.cos(self.S.d['angle']/2)

        # Update needle position
        self.angle_dial.coords(self.needle1, 170, 300, x, y)

        self.trackPos.config(text="Distance from the track axis: " + "{:.3f}".format(self.S.d['trackPos']) + "m")
        
        # Stats
        self.distRaced.config(text="Distance travelled: " + "{:.1f}".format(self.S.d['distRaced']) + "m")
        self.distFromStart.config(text="Distance from start of lap: " + "{:.1f}".format(self.S.d['distFromStart']) + "m")
        self.curLapTime.config(text="Current lap time: " + "{:.3f}".format(self.S.d['curLapTime']) + "s")
        self.lastLapTime.config(text="Last lap time: " + "{:.3f}".format(self.S.d['lastLapTime']) + "s")
        self.racePos.config(text="Position in race: " + "{:.0f}".format(self.S.d['racePos']))

        self.fuel.config(text="Remaining Fuel Percentage: " + "{:.1f}".format(self.S.d['fuel']) + "%")
        self.damage.config(text="Damage Percentage: " + "{:.1f}".format(self.S.d['damage']) + "%")

        self.flwheel.config(text="Front left: " + "{:.1f}".format(self.S.d['wheelSpinVel'][0]) + "rad/s")
        self.frwheel.config(text="Front right: " + "{:.1f}".format(self.S.d['wheelSpinVel'][1]) + "rad/s")
        self.blwheel.config(text="Back left: " + "{:.1f}".format(self.S.d['wheelSpinVel'][2]) + "rad/s")
        self.brwheel.config(text="Back right: " + "{:.1f}".format(self.S.d['wheelSpinVel'][3]) + "rad/s")

        # Calculate needle end point
        x = 170 + 160 * math.sin(self.R.d['steer'] * -1 * math.pi/2)
        y = 300 - 160 * math.cos(self.R.d['steer'] * -1 * math.pi/2)

        # Update needle position
        self.steer_dial.coords(self.needle2, 170, 300, x, y)

        # Speeds
        self.create_bar(self.speeds_bar1, 1 - ((200 - abs(self.S.d['speedX'])) / 200))
        self.create_bar(self.speeds_bar2, 1 - ((200 - abs(self.S.d['speedY'])) / 200))
        self.create_bar(self.speeds_bar3, 1 - ((200 - abs(self.S.d['speedZ'])) / 200))

        # RPM
        if self.S.d['gear'] == 0:
            self.gear.config(text="Gear: N")
        elif self.S.d['gear'] == -1:
            self.gear.config(text="Gear: 1")
        else:
            self.gear.config(text="Gear: " + "{:.0f}".format(self.S.d['gear']))

        self.draw_needle(self.S.d['rpm'])
        self.rpm_dial.itemconfig(self.rpm_num, text="{:.0f}".format(self.S.d['rpm']))

        # Actuators
        self.create_bar(self.actuator_bar1, self.R.d['accel'])
        self.create_bar(self.actuator_bar2, self.R.d['brake'])
        self.create_bar(self.actuator_bar3, self.R.d['clutch'])

        self.window.update()
        self.window.after(50, self.update_window)

    def draw_needle(self, revs):
        angle = 240 * (revs / 10000) - 30

        angle_rad = math.radians(180 - angle)

        # Calculate needle end point
        x = 200 + 120 * math.cos(angle_rad)
        y = 200 - 120 * math.sin(angle_rad)

        # Update needle position
        self.rpm_dial.coords(self.needle3, 200, 200, x, y)