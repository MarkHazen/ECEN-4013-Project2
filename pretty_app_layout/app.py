import serial
import numpy as np
import tkinter as tk

from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from itertools import product, combinations
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


class app(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.com = -1
        self.baud = -1
        self.usb = None

        container = tk.Frame(self)
        container.pack(side=TOP, fill=BOTH, expand=TRUE)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        pages = [LaunchWindow, MainWindow]

        for F in pages:
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame(LaunchWindow)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        if hasattr(frame, "size"):
            self.geometry(frame.size)

        if hasattr(frame, "on_show"):
            frame.on_show()
            
    def set_connection_param(self, com, baud, usb):
        self.com = com
        self.baud = baud
        self.usb = usb

class LaunchWindow(tk.Frame):
    size = "700x500"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.header_font = ("Leelawadee", 15, "bold")
        self.data_title_font = ("Leelawadee", 12, "bold")

        #--------------------
        # HEADER
        #--------------------
        header = Frame(self, background="#27124d")
        header.pack(side=TOP, expand=False, fill=X)

        title = Label(header, text="Device Monitor", fg="white", background="#27124d")
        title.config(font=self.header_font)
        title.pack(side=LEFT, padx=10, pady=10)

        exit_button = ttk.Button(header, text="Exit", style='W.TButton', command=self.quit)
        exit_button.pack(padx=20, pady=20, side=RIGHT)

        #--------------------
        # BODY
        #--------------------
        body = Frame(self)
        body.pack(side=TOP, expand=True, fill=BOTH)

        section1 = Frame(body)
        section1.pack(side=TOP, expand=False, fill=X)

        instructions = Label(section1, text="Enter your device information:")
        instructions.pack(padx=10, pady=10)

        section2 = Frame(body)
        section2.pack(side=TOP, expand=False, fill=X)

        method_label = Label(section2, text="Choose the method of connection:")
        method_label.pack(padx=10, pady=10)

        self.connection_method = StringVar(self, "1")

        values = {"USB Connection" : "1",
                  "Bluetooth Connection" : "2"}
        
        for (text, value) in values.items():
            Radiobutton(section2, text=text, variable=self.connection_method, value=value, indicator = 0, background="light gray").pack(pady=5)

        section3 = Frame(body)
        section3.pack(side=TOP, expand=False, fill=X)

        com_label = Label(section3, text="Enter the COM port of your device:")
        com_label.pack(padx=10, pady=10)

        self.com_num = Entry(section3)
        self.com_num.insert(0, "")
        self.com_num.pack(padx=5, pady=5)

        section4 = Frame(body)
        section4.pack(side=TOP, expand=False, fill=X)

        baud_label = Label(section4, text="Enter the baud rate of connetion:")
        baud_label.pack(padx=10, pady=10)

        self.baud = Entry(section4)
        self.baud.insert(0, "")
        self.baud.pack(padx=5, pady=5)

        start_button = ttk.Button(section4, text="Start Monitor", style='W.TButton', command=self.start_monitor)
        start_button.pack(padx=20, pady=20, side=BOTTOM)

    def start_monitor(self):
        com_num = self.com_num.get()
        baud = self.baud.get()

        if self.connection_method.get() == "1":
            usb = True
        else:
            usb = False

        print("Starting Monitor at...")
        print(f"Port: COM{com_num}")
        print(f"Baud: {baud}")
        print(f"With USB: {usb}")

        self.controller.set_connection_param(com_num, baud, usb)

        self.controller.show_frame(MainWindow)

    def quit(self):
        self.controller.destroy()

class MainWindow(tk.Frame):
    size = "1000x700"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.ser = None
        self.line = ""

        self.header_font = ("Leelawadee", 15, "bold")
        self.data_title_font = ("Leelawadee", 12, "bold")

        style = ttk.Style()
        style.configure('W.TButton', font=('calibri', 10, 'bold'))

        #--------------------
        # HEADER
        #--------------------
        header = Frame(self, background="#27124d")
        header.pack(side=TOP, expand=False, fill=X)

        self.connected_header = Label(header, text="Device Connected at: COM9, 9600 baud", fg="white", background="#27124d")
        self.connected_header.config(font=self.header_font)
        self.connected_header.pack(padx=20, pady=20, side=LEFT)

        self.battery_header = Label(header, text="Voltage: 3.7V", fg="white", background="#27124d")
        self.battery_header.config(font=self.header_font)
        self.battery_header.pack(padx=0, pady=20, side=LEFT)

        exit_button = ttk.Button(header, text="Exit", style='W.TButton', command=self.quit)
        exit_button.pack(padx=20, pady=20, side=RIGHT)

        #--------------------
        # BODY
        #--------------------
        body = Frame(self, background="pink")
        body.pack(side=TOP, expand=True, fill=BOTH)

        left_half = Frame(body, background="red")
        left_half.pack(side=LEFT, expand=True, fill=BOTH)

        right_half = Frame(body, background="green")
        right_half.pack(side=LEFT, expand=True, fill=BOTH)

        #--------------------
        # LEFT TABS
        #--------------------
        tabControl = ttk.Notebook(left_half)

        tab1 = Frame(tabControl)
        self.tab2 = Frame(tabControl)

        tabControl.add(tab1, text='Serial Monitor')
        tabControl.add(self.tab2, text='Orientation Diagram')

        tabControl.pack(expand=1, fill="both")

        #--------------------
        # SERIAL MONITOR
        #--------------------
        self.serial_output = Text(tab1)
        self.serial_output.pack(fill=BOTH, expand=True)

        # --------------------
        # 3D PLOT
        # --------------------
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax3d = self.fig.add_subplot(111, projection='3d')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab2)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.tab2)
        self.toolbar.update()

        self.current_quat = np.array([0.8446, 0.1913, 0.4619, 0.1913])

        self.init_3d_plot()
        self.update_3d_plot()

        #--------------------
        # IMU DATA
        #--------------------
        top_right = Frame(right_half, borderwidth=1, relief="solid")
        label2_1 = Label(top_right, text="BNO055 IMU Data")
        label2_1.config(font=self.data_title_font)
        label2_1.pack(padx=10, pady=10)
        top_right.pack(side=TOP, expand=True, fill=BOTH)

        ang_title = Label(top_right, text="Angular Rotation")
        ang_title.pack(padx=5, pady=5)

        self.ang_data_label = Label(top_right, text="X: 123.123 | Y: 321.321 | Z: 456.654")
        self.ang_data_label.pack(padx=5, pady=0)

        acc_title = Label(top_right, text="Linear Acceleration")
        acc_title.pack(padx=5, pady=5)

        self.acc_data_label = Label(top_right, text="X: 123.123 | Y: 321.321 | Z: 456.654")
        self.acc_data_label.pack(padx=5, pady=0)

        mag_title = Label(top_right, text="Magnetic Field")
        mag_title.pack(padx=5, pady=5)

        self.mag_data_label = Label(top_right, text="X: 123.123 | Y: 321.321 | Z: 456.654")
        self.mag_data_label.pack(padx=5, pady=0)
    

        #--------------------
        # GPS DATA
        #--------------------
        bottom_right = Frame(right_half, borderwidth=1, relief="solid")
        label2_2 = Label(bottom_right, text="GPS Data")
        label2_2.config(font=self.data_title_font)
        label2_2.pack(padx=20, pady=10)
        bottom_right.pack(side=TOP, expand=True, fill=BOTH)

        self.locked_label = Label(bottom_right, text="GPS Locked: FALSE")
        self.locked_label.pack(padx=5, pady=5)

        self.sat_label = Label(bottom_right, text="Satilites Obtained: 0")
        self.sat_label.pack(padx=5, pady=5)

        dt_title = Label(bottom_right, text="Date and Time")
        dt_title.pack(padx=5, pady=5)

        self.dt_label = Label(bottom_right, text="00/00/0000 | 00:00:00")
        self.dt_label.pack(padx=5, pady=0)

        pos_title = Label(bottom_right, text="Position")
        pos_title.pack(padx=5, pady=5)

        self.pos_label = Label(bottom_right, text="Latitude: 987.789 | Longitude: 789:987")
        self.pos_label.pack(padx=5, pady=0)

        alt_title = Label(bottom_right, text="Altitude")
        alt_title.pack(padx=5, pady=5)

        self.alt_label = Label(bottom_right, text="Height: 687.5309")
        self.alt_label.pack(padx=5, pady=0)

    #--------------------
    # WINDOW FUNCTIONS
    #--------------------
    def on_show(self):
        com = self.controller.com
        baud = self.controller.baud

        self.connected_header.config(text=f"Device Connected at: COM{com}, {baud} baud")

        self.start_serial(com, baud)
    
    def quit(self):
        self.controller.destroy()

    #--------------------
    # SERIAL
    #--------------------
    def start_serial(self, port, baud):
        try:
            self.ser = serial.Serial(port=f"COM{port}", baudrate=int(baud), timeout=1)
            self.read_serial()
        except Exception as e:
            print("Error:", e)
            if self.ser and self.ser.is_open: self.ser.close()
            self.controller.show_frame(LaunchWindow)

    def read_serial(self):
        if self.ser and self.ser.in_waiting:
            try:
                self.line = self.ser.readline().decode('utf-8').strip()
                self.serial_output.insert(tk.END, self.line + "\n")
                self.serial_output.see(tk.END)
            except:
                pass

        print(self.line)
        values = self.line.split(',')
        
        try:
            voltage = values[0]

            date = values[1]
            time = values[2]
            
            sat_num = int(values[3])
            lat = float(values[4])
            lon = float(values[5])
            alt = float(values[6])

            acc_x = float(values[7])
            acc_y = float(values[8])
            acc_z = float(values[9])

            mag_x = float(values[10])
            mag_y = float(values[11])
            mag_z = float(values[12])

            ang_x = float(values[13])
            ang_y = float(values[14])
            ang_z = float(values[15])

            q_w = float(values[16])
            q_x = float(values[17])
            q_y = float(values[18])
            q_z = float(values[19])

            self.update_quaternion(q_w, q_x, q_y, q_z)

            self.battery_header.config(text=f"Voltage: {voltage}V")

            self.ang_data_label.config(text=f"X: {ang_x} | Y: {ang_y} | Z: {ang_z}")
            self.acc_data_label.config(text=f"X: {acc_x} | Y: {acc_y} | Z: {acc_z}")
            self.mag_data_label.config(text=f"X: {mag_x} | Y: {mag_y} | Z: {mag_z}")

            if date == "XX/XX/XXXX":
                self.locked_label.config(text="GPS Locked: FALSE")
                self.sat_label.config(text=f"Satilites Obtained: 0")
                self.dt_label.config(text=f"00/00/0000 | 00:00:00")
                self.pos_label.config(text=f"Latitude: NaN | Longitude: NaN")
                self.alt_label.config(text=f"Height: NaN")
            else:
                self.locked_label.config(text="GPS Locked: TRUE")
                self.sat_label.config(text=f"Satilites Obtained: {sat_num}")
                self.dt_label.config(text=f"{date} | {time}")
                self.pos_label.config(text=f"Latitude: {lat} | Longitude: {lon}")
                self.alt_label.config(text=f"Height: {alt}")

        except:
            pass

        self.after(50, self.read_serial)

    #--------------------
    # PLOTTING
    #--------------------
    def quat_to_euler(self, q):
        w, x, y, z = q

        phi = np.arctan2(
            -2*x*y + 2*w*z,
            x*x + w*w - z*z - y*y
        )

        theta = np.arcsin(2*w*y + 2*x*z)

        psi = np.arctan2(
            -2*y*z + 2*w*x,
            z*z - y*y - x*x + w*w
        )

        elev = -np.rad2deg(theta)
        azim = np.rad2deg(phi)
        roll = np.rad2deg(psi)

        return elev, azim, roll
    
    def init_3d_plot(self):
        r = [-0.5, 0.5]

        self.vertices = np.array(list(product(r, r, r)))

        self.edges = []
        for i, start in enumerate(self.vertices):
            for j, end in enumerate(self.vertices):
                if np.sum(np.abs(start - end)) == 1:
                    self.edges.append((i, j))

        scale = np.array([1, 1, 1])  # normalize cube

        for start, end in combinations(np.array(list(product(r, r, r))), 2):
            if np.sum(np.abs(start - end)) == 1:
                self.ax3d.plot3D(*zip(start*scale, end*scale))

        self.ax3d.set_xlabel("X")
        self.ax3d.set_ylabel("Y")
        self.ax3d.set_zlabel("Z")

        self.ax3d.set_xlim(-1, 1)
        self.ax3d.set_ylim(-1, 1)
        self.ax3d.set_zlim(-1, 1)

    def quat_to_rot_matrix(self, q):
        w, x, y, z = q

        return np.array([
            [1 - 2*(y*y + z*z),     2*(x*y - z*w),     2*(x*z + y*w)],
            [2*(x*y + z*w),         1 - 2*(x*x + z*z), 2*(y*z - x*w)],
            [2*(x*z - y*w),         2*(y*z + x*w),     1 - 2*(x*x + y*y)]
        ])

    def update_quaternion(self, w, x, y, z):
        q = np.array([w, x, y, z])
        q = q / np.linalg.norm(q)
        self.current_quat = q

    def update_3d_plot(self):
        self.ax3d.cla()

        R = self.quat_to_rot_matrix(self.current_quat)
        rotated = self.vertices @ R.T

        for i, j in self.edges:
            self.ax3d.plot3D(*zip(rotated[i], rotated[j]))

        self.ax3d.set_xlim(-1, 1)
        self.ax3d.set_ylim(-1, 1)
        self.ax3d.set_zlim(-1, 1)
        self.ax3d.set_box_aspect([1, 1, 1])

        self.ax3d.set_xlabel("X")
        self.ax3d.set_ylabel("Y")
        self.ax3d.set_zlabel("Z")

        self.canvas.draw_idle()
        self.after(30, self.update_3d_plot)

app = app()
app.mainloop()