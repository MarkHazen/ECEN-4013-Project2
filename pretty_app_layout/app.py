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

        self.header_font = ("Leelawadee", 15, "bold")
        self.data_title_font = ("Leelawadee", 12, "bold")

        style = ttk.Style()
        style.configure('W.TButton', font=('calibri', 10, 'bold'))

        #--------------------
        # HEADER
        #--------------------
        header = Frame(self, background="#27124d")
        header.pack(side=TOP, expand=False, fill=X)

        connected_header = Label(header, text="Device Connected at: COM9, 9600 baud", fg="white", background="#27124d")
        connected_header.config(font=self.header_font)
        connected_header.pack(padx=20, pady=20, side=LEFT)

        battery_header = Label(header, text="Voltage: 3.7V", fg="white", background="#27124d")
        battery_header.config(font=self.header_font)
        battery_header.pack(padx=0, pady=20, side=LEFT)

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
        serial_output = Text(tab1)
        serial_output.pack(fill=BOTH, expand=True)

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

        ang_data_label = Label(top_right, text="X: 123.123 | Y: 321.321 | Z: 456.654")
        ang_data_label.pack(padx=5, pady=0)

        acc_title = Label(top_right, text="Linear Acceleration")
        acc_title.pack(padx=5, pady=5)

        acc_data_label = Label(top_right, text="X: 123.123 | Y: 321.321 | Z: 456.654")
        acc_data_label.pack(padx=5, pady=0)

        mag_title = Label(top_right, text="Magnetic Field")
        mag_title.pack(padx=5, pady=5)

        mag_data_label = Label(top_right, text="X: 123.123 | Y: 321.321 | Z: 456.654")
        mag_data_label.pack(padx=5, pady=0)
    

        #--------------------
        # GPS DATA
        #--------------------
        bottom_right = Frame(right_half, borderwidth=1, relief="solid")
        label2_2 = Label(bottom_right, text="GPS Data")
        label2_2.config(font=self.data_title_font)
        label2_2.pack(padx=20, pady=10)
        bottom_right.pack(side=TOP, expand=True, fill=BOTH)

        locked_label = Label(bottom_right, text="GPS Locked: FALSE")
        locked_label.pack(padx=5, pady=5)

        sat_label = Label(bottom_right, text="Satilites Obtained: 0")
        sat_label.pack(padx=5, pady=5)

        dt_title = Label(bottom_right, text="Date and Time")
        dt_title.pack(padx=5, pady=5)

        dt_label = Label(bottom_right, text="00/00/0000 | 00:00:00")
        dt_label.pack(padx=5, pady=0)

        pos_title = Label(bottom_right, text="Position")
        pos_title.pack(padx=5, pady=5)

        pos_label = Label(bottom_right, text="Latitude: 987.789 | Longitude: 789:987")
        pos_label.pack(padx=5, pady=0)

        alt_title = Label(bottom_right, text="Altitude")
        alt_title.pack(padx=5, pady=5)

        alt_title = Label(bottom_right, text="Height: 687.5309")
        alt_title.pack(padx=5, pady=0)

    def quit(self):
        self.controller.destroy()

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
        r = [0, 1]
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

    def update_quaternion(self, w, x, y, z):
        self.current_quat = np.array([w, x, y, z])

    def update_3d_plot(self):
        q = self.current_quat

        elev, azim, roll = self.quat_to_euler(q)

        self.ax3d.view_init(elev=elev, azim=azim)
        self.ax3d.set_title(f"elev={elev:.1f}, azim={azim:.1f}, roll={roll:.1f}")

        self.canvas.draw()

        self.after(30, self.update_3d_plot)

app = app()
app.mainloop()