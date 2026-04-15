#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <Adafruit_GPS.h>
#include <SPI.h>
#include <SD.h>

Adafruit_BNO055 bno = Adafruit_BNO055(55);
Adafruit_GPS GPS(&Wire);

const int chipSelect = 4;

const int gps_search_led = 13;
const int gps_lock_led = 0;
const bool use_multiple_led = false;
const int blink_ticks = 10;

bool search_led_on = false;
int current_ticks = 0;

bool imu_not_loaded = false;
bool sd_not_loaded = false;
bool gps_not_loaded = false;

float approxLat = 36.1156;
float approxLon = -97.0584;
float approxAlt = 300;

void search_led_pattern(int led_pin) {
    if(current_ticks >= blink_ticks) {
        if(search_led_on) {
            digitalWrite(led_pin, LOW);
            search_led_on = false;
        } else {
            digitalWrite(led_pin, HIGH);
            search_led_on = true;
        }

        current_ticks = 0;
    } else {
        current_ticks++;
    }
}

void setup() {
    Serial.begin(9600);
    
    pinMode(gps_search_led, OUTPUT);

    digitalWrite(gps_search_led, HIGH);
    delay(1000);
    digitalWrite(gps_search_led, LOW);
    delay(1000);

    digitalWrite(gps_search_led, HIGH);
    delay(100);
    digitalWrite(gps_search_led, LOW);
    delay(100);

    digitalWrite(gps_search_led, HIGH);
    delay(100);
    digitalWrite(gps_search_led, LOW);
    delay(100);

    if(use_multiple_led) pinMode(gps_lock_led, OUTPUT);

    while(!Serial);
    
    if(!bno.begin()) {
        Serial.println("[Error]: BNO055 INIT FAIL");
        while(1);
    }

    if(!SD.begin(chipSelect)) {
        Serial.println("[Error]: SD CARD INIT FAIL");
        while(1);
    }

    delay(1000);

    bno.setExtCrystalUse(true);

    if(!GPS.begin(0x10)) {
        Serial.println("[Error]: GPS INIT FAIL");
    }

    GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
    GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);
    GPS.sendCommand(PGCMD_ANTENNA);     

    delay(1000);

    char cmd[50];

    sprintf(cmd, "$PMTK740,%.6f,%.6f,%.1f*00", approxLat, approxLon, approxAlt);
    GPS.sendCommand(cmd);
}

void loop() {
    //---------------------
    // BNO055 MEASUREMENTS
    //---------------------
    sensors_event_t orientationData, linearAccelData, magnetometerData;
    bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
    bno.getEvent(&linearAccelData, Adafruit_BNO055::VECTOR_LINEARACCEL);
    bno.getEvent(&magnetometerData, Adafruit_BNO055::VECTOR_MAGNETOMETER);

    float ang_x = orientationData.orientation.x;
    float ang_y = orientationData.orientation.y;
    float ang_z = orientationData.orientation.z;

    float acc_x = linearAccelData.acceleration.x;
    float acc_y = linearAccelData.acceleration.y;
    float acc_z = linearAccelData.acceleration.z;

    float mag_x = magnetometerData.magnetic.x;
    float mag_y = magnetometerData.magnetic.y;
    float mag_z = magnetometerData.magnetic.z;

    //---------------------
    // GPS MEASUREMENTS
    //---------------------
    char c = GPS.read();
    
    if(GPS.newNMEAreceived()) {
        GPS.parse(GPS.lastNMEA());
    }

    int fix = (int)GPS.fix;

    char date[11];
    char time[9];

    int day, month, year;
    int hour, minute, second;
    int sat;
    float lat, lon, alt;

    if(fix != 0) {
        if(use_multiple_led) {
            digitalWrite(gps_lock_led, HIGH);
        } else {
            digitalWrite(gps_search_led, HIGH);
        }

        day = GPS.day;
        month = GPS.month;
        year = GPS.year;

        sprintf(date, "%02d/%02d/%04d", month, day, year);

        hour = GPS.hour;
        minute = GPS.minute;
        second = GPS.seconds;

        sprintf(time, "%02d:%02d:%02d", hour, minute, second);

        sat = (int)GPS.satellites;
        lat = GPS.latitude;
        lon = GPS.longitude;
        alt = GPS.altitude;
    } else {
        search_led_pattern(gps_search_led);

        sprintf(date, "XX/XX/XXXX");
        sprintf(time, "XX:XX:XX");
        sat = 0;
        lat = 0.0;
        lon = 0.0;
        alt = 0.0;
    }
    
    //---------------------
    // FORMAT DATA
    //---------------------
    String dataString = "";

    dataString += String(date); dataString += String(",");
    dataString += String(time); dataString += String(",");

    dataString += String(sat); dataString += String(",");
    dataString += String(lat); dataString += String(",");
    dataString += String(lon); dataString += String(",");
    dataString += String(alt); dataString += String(",");

    dataString += String(acc_x); dataString += String(",");
    dataString += String(acc_y); dataString += String(",");
    dataString += String(acc_z); dataString += String(",");

    dataString += String(mag_x); dataString += String(",");
    dataString += String(mag_y); dataString += String(",");
    dataString += String(mag_z); dataString += String(",");

    dataString += String(ang_x); dataString += String(",");
    dataString += String(ang_y); dataString += String(",");
    dataString += String(ang_z); dataString += String("||");
    dataString += String(current_ticks);

    Serial.println(dataString);

    //---------------------
    // SD CARD LOGGING
    //---------------------
    File dataFile = SD.open("data.csv", FILE_WRITE);

    if(dataFile) {
        dataFile.println(dataString);
        dataFile.close();
    } else {
        Serial.println("[Error]: DATA.CSV ACCESS FAIL");
    }

    delay(100);
}