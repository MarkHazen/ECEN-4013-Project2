import tkinter as tk

root = tk.Tk()

root.title("Window Name")
root.geometry("400x300")

def start_monitor():
    print("starting monitor")

def exit_program():
    print("Exiting Program")
    exit(0)

#TODO: Turn into instruuctions
tk.Label(root, text="This is a label.").pack()

#TODO: Enter COM and baud

#TODO: Start Button
button = tk.Button(root, text="Start Monitor", command=start_monitor,).pack(padx=5, pady=5)

#TODO: Exit Button
button = tk.Button(root, text="Exit Program", command=exit_program).pack(padx=5, pady=5)

root.mainloop()