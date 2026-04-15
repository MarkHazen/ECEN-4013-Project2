import serial
import time

# TODO: CHANGE TO MATCH PORT OF DEVICE
serialcomm = serial.Serial('COM7', 9600)
serialcomm.timeout = 1

running = True
while running:
    # Write to serial
    print(serialcomm.readline().decode('ascii'))

# Close cleanly when done
serialcomm.close()