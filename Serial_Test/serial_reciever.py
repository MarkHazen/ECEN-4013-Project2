import serial
import time

# TODO: CHANGE TO MATCH PORT OF DEVICE
serialcomm = serial.Serial('COM7', 9600)
serialcomm.timeout = 1

running = True
while running:
    # Get user input
    i = input("Input (on/off): ").strip()

    # Check if done
    if i == 'done':
        print('Finished Program')
        running = False

    # Write to serial
    serialcomm.write(i.encode())
    time.sleep(0.5)
    print(serialcomm.readline().decode('ascii'))

# Close cleanly when done
serialcomm.close()