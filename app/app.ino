#include <Adafruit_BNO055.h>

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

Adafruit_BNO055 bno = Adafruit_BNO055(55);

void setup() {
    Serial.begin(9600);
    
    if(!bno.begin()) {
        Serial.println("Error: BNO055 INIT FAIL");
        while(1);
    }

    delay(1000);

    bno.setExtCrystalUse(true);
}

void loop() {
    //-------------------------
    // BNO055 MEASUREMENTS
    //-------------------------
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
    // FORMAT DATA
    //---------------------
    String date = "04/06/2026";
    String time = "99:99:99";
    int num_sat = 3;

    double lat = random(3000, 4000) / 100.0;
    double lon = random(-9000, -8000) / 100.0;
    double alt = random(40000, 41000) / 100.0;

    String csv_line = date + "," + time + "," + String(num_sat) + "," +
                        String(lat) + "," + String(lon) + "," + String(alt) + "," +
                        String(acc_x) + "," + String(acc_y) + "," + String(acc_z) + "," +
                        String(mag_x) + "," + String(mag_y) + "," + String(mag_z) + "," +
                        String(ang_x) + "," + String(ang_y) + "," + String(ang_z);

    Serial.println(csv_line);
    delay(100);
}