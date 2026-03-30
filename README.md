# Senior Design Project 2

Colletions of tests and the main program used in the ECEN 4013 Design of Engineering Systems Project 2. The test programs verify the functionality of the components and sections of the program.

### Serial Test
Program has been written, untested with hardware. Sends data between PC and microcontroller using the usb. The value of the serial and com port within `serial_reciever.py` needs to be updated in accordance to the port of the microcontroller

### SD Card Test
Program has been written, untested with hardware. Writes fake data to a `.csv` file on the sd card. Data increases by a value of one each increment. Ensure the value of `chipSelect` is 4 when working with the Adafruit Feather AdaLogger