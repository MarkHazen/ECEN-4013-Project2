#include <SPI.h>
#include <SD.h>

// Select is 4 for Adafruit Feather AdaLogger
const int chipSelect = 4;

const String HEADER = "Data 1, Data 2, Data 3";

// Test Data
int data1 = 1;
int data2 = 10;
int data3 = 100;

void setup() {
    Serial.begin(9600);
    while(!Serial);

    Serial.print("Initialize SD card...");

    if(!SD.begin(chipSelect)) {
        Serial.println("Initialization failed: Could not open card.");
        while(true);
    }

    File dataFile = SD.open("datalog.csv", FILE_WRITE);

    if(!dataFile) {
        Serial.println("Initialization failed: Could not open file.");
        while(true);
    }

    dataFile.println(HEADER);
    dataFile.close();

    Serial.println("Initialization complete.");
}

void loop() {
    String line = "";

    line += String(data1);
    line += ", ";
    line += String(data2);
    line += ", ";
    line += String(data3);

    File dataFile = SD.open("datalog.csv", FILE_WRITE);

    if(dataFile) {
        dataFile.println(line);
        dataFile.close();
    } else {
        Serial.println("Error opening datalog.csv");
    }

    data1++;
    data2++;
    data3++;
}