import tkinter as tk
from tkinter import ttk
import serial

class app(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.com = -1
        self.baud = -1

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        pages = [StartPage, MonitorPage]

        for F in pages:
            frame = F(container, self)

            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        if hasattr(frame, "size"):
            self.geometry(frame.size)

        if hasattr(frame, "on_show"):
            frame.on_show()

    def set_usb_param(self, com, baud):
        self.com = com
        self.baud = baud

class StartPage(tk.Frame):
    size = "600x400"
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        tk.Label(self, text="Enter the COM number of the device:").pack()
        self.com_num = tk.Entry(self)
        self.com_num.insert(0, "")
        self.com_num.pack(padx=5, pady=5, fill="x")

        tk.Label(self, text="Enter the baud rate of operation:").pack()
        self.baud = tk.Entry(self)
        self.baud.insert(0, "")
        self.baud.pack(padx=5, pady=5, fill="x")

        #TODO: Start Button
        button = tk.Button(self, text="Start Monitor", command=self.start_monitor,).pack(padx=5, pady=5)

        button = tk.Button(self, text="Exit Program", command=self.exit_program).pack(padx=5, pady=5)

    def start_monitor(self):
        com_num = self.com_num.get()
        baud = self.baud.get()
        print("Starting Monitor at...")
        print(f"Port: COM{com_num}")
        print(f"Baud: {baud}")
        self.controller.set_usb_param(com_num, baud)
        self.controller.show_frame(MonitorPage)

    def exit_program(self):
        print("Exiting Program")
        self.controller.destroy()

class MonitorPage(tk.Frame):
    size = "1200x800"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.ser = None
        self.line = ""
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self. grid_columnconfigure(0, weight=0)

        quad_frame = tk.Frame(self, width=1200, height=800)
        quad_frame.grid(row=0, column=0)
        quad_frame.grid_propagate(False)

        self.q1 = tk.Frame(quad_frame, bg="white", borderwidth=1, relief="solid")
        self.q2 = tk.Frame(quad_frame, bg="white", borderwidth=1, relief="solid")
        self.q3 = tk.Frame(quad_frame, bg="white", borderwidth=1, relief="solid")
        self.q4 = tk.Frame(quad_frame, bg="white", borderwidth=1, relief="solid")

        self.q1.place(x=0, y=0, width=600, height=400)
        self.q2.place(x=600, y=0, width=600, height=400)
        self.q3.place(x=0, y=400, width=600, height=400)
        self.q4.place(x=600, y=400, width=600, height=400)

        #---------------------
        # Quad 1
        #---------------------
        tk.Label(self.q1, text="Serial Output").pack()
        self.serial_output = tk.Text(self.q1)
        self.serial_output.pack(fill="both", expand=True)

        #---------------------
        # Quad 2
        #---------------------
        tk.Label(self.q2, text="IMU Data").pack()
        self.angle_label = tk.Label(self.q2, text=f"X: 60.00, Y:70.00, Z:80.00")
        self.angle_label.pack()

        self.accel_label = tk.Label(self.q2, text=f"X: 1, Y:2, Z:3")
        self.accel_label.pack()

        self.mag_label = tk.Label(self.q2, text=f"X: 20, Y:40, Z:60")
        self.mag_label.pack()

        #---------------------
        # Quad 3
        #---------------------
        tk.Label(self.q3, text="Component Status").pack()
        self.usb_param = tk.Label(self.q3, text=f"USB Connected: COM{controller.com} @ {controller.baud}")
        self.usb_param.pack()

        self.bt_param = tk.Label(self.q3, text=f"Bluetooth: NONE")
        self.bt_param.pack()

        self.sd_state = tk.Label(self.q3, text=f"SD Card: Inactive")
        self.sd_state.pack()

        self.imu_state = tk.Label(self.q3, text=f"IMU: Inactive")
        self.imu_state.pack()

        self.gps_state = tk.Label(self.q3, text=f"GPS: Inactive")
        self.gps_state.pack()

        #---------------------
        # Quad 4
        #---------------------
        tk.Label(self.q4, text="GPS Data").pack()
        self.sat_num_label = tk.Label(self.q4, text=f"Connected Satellites: {3}")
        self.sat_num_label.pack()

        self.date_time_label = tk.Label(self.q4, text=f"Date: {'1/1/1'}, Time: {'99:99:99'}")
        self.date_time_label.pack()

        self.sat_pos_label = tk.Label(self.q4, text=f"Latitude: {400.000}, Longitude: {300.000}")
        self.sat_pos_label.pack()

        self.elevation_label = tk.Label(self.q4, text=f"Altitude: {300.000} (Method)")
        self.elevation_label.pack()

        #---------------------
        # Footer
        #---------------------
        footer = tk.Frame(self, bd=2, relief="raised")
        footer.grid(row=1, column=0, sticky="ew")

        footer.grid_columnconfigure(0, weight=1)
        footer.grid_columnconfigure(1, weight=1)

        tk.Button(
            footer,
            text="Change COM",
            command = lambda : controller.show_frame(StartPage)
        ).grid(row=0, column=0, padx=10, pady=10)

        tk.Button(
            footer,
            text="Exit",
            command=controller.destroy
        ).grid(row=0, column=1, padx=10, pady=10)

    def on_show(self):
        com = self.controller.com
        baud = self.controller.baud

        self.usb_param.config(text=f"USB Connected: COM{com} @ {baud}")

        self.start_serial(com, baud)

    def start_serial(self, port, baud):
        try:
            self.ser = serial.Serial(port=f"COM{port}", baudrate=int(baud), timeout=1)
            self.read_serial()
        except Exception as e:
            print("Error:", e)
            if self.ser and self.ser.is_open: self.ser.close()
            self.controller.show_frame(StartPage)

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
            date = values[0]
            time = values[1]
            
            sat_num = int(values[2])
            lat = float(values[3])
            lon = float(values[4])
            alt = float(values[5])

            acc_x = float(values[6])
            acc_y = float(values[7])
            acc_z = float(values[8])

            mag_x = float(values[9])
            mag_y = float(values[10])
            mag_z = float(values[11])

            ang_x = float(values[12])
            ang_y = float(values[13])
            ang_z = float(values[14])

            self.angle_label.config(text=f"X: {ang_x}, Y: {ang_y}, Z: {ang_z}")
            self.accel_label.config(text=f"X: {acc_x}, Y: {acc_y}, Z: {acc_z}")
            self.mag_label.config(text=f"X: {mag_x}, Y: {mag_y}, Z: {mag_z}")

            self.sat_num_label.config(text=f"Connected Satellites: {sat_num}")
            self.date_time_label.config(text=f"Date: {date}, Time: {time}")
            self.sat_pos_label.config(text=f"Latitude: {lat}, Longitude: {lon}")
            self.elevation_label.config(text=f"Altitude: {alt} (Mehtod)")
        except:
            pass

        self.after(50, self.read_serial)

app = app()
app.mainloop()