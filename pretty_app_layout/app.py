import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import *
import tkinter.font as tkFont
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class LaunchWindow:
    def __init__(self, root):
        self.root = root

        #--------------------
        # HEADER
        #--------------------
        header = Frame(root, background="#27124d")
        header.pack(side=TOP, expand=False, fill=X)

        title = Label(header, text="TITLE")
        title.pack(side=LEFT, padx=10, pady=10)

        #--------------------
        # BODY
        #--------------------
        body = Frame(root)
        body.pack(side=TOP, expand=True, fill=BOTH)

        section1 = Frame(body, background="red")
        section1.pack(side=TOP, expand=False, fill=X)

        instructions = Label(section1, text="Enter your device information:")
        instructions.pack(padx=10, pady=10)

        section2 = Frame(body, background="blue")
        section2.pack(side=TOP, expand=False, fill=X)

        method_label = Label(section2, text="Choose the method of connection:")
        method_label.pack(padx=10, pady=10)

        section3 = Frame(body, background="green")
        section3.pack(side=TOP, expand=False, fill=X)

        com_label = Label(section3, text="Enter the COM port of your device:")
        com_label.pack(padx=10, pady=10)

        section4 = Frame(body, background="yellow")
        section4.pack(side=TOP, expand=False, fill=X)

        baud_label = Label(section1, text="Enter the baud rate of connetion:")
        baud_label.pack(padx=10, pady=10)

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.y = [i**2 for i in range(101)]

        self.header_font = ("Leelawadee", 15, "bold")
        self.data_title_font = ("Leelawadee", 12, "bold")

        style = Style()

        style.configure('W.TButton', font=('calibri', 10, 'bold'))

        #--------------------
        # HEADER
        #--------------------
        header = Frame(root, background="#27124d")
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
        body = Frame(root, background="pink")
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

        #--------------------
        # PLOT
        #--------------------
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab2)
        self.canvas.get_tk_widget().pack()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.tab2)
        self.toolbar.update()

        self.plot()

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

        self.plot()

    def quit(self):
        exit(1)

    def plot(self):
        self.ax.clear()

        self.ax.plot(self.y)

        self.canvas.draw()

        self.root.after(200, self.plot)

root = Tk()
window = LaunchWindow(root)
root.mainloop()