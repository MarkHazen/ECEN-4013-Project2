#include <Wire.h>
#include <Adafruit_GPS.h>

// Connect to GPS via I2C
Adafruit_GPS GPS(&Wire);

// Set to true to see all NMEA sentences
#define GPSECHO true

uint32_t timer = 0;

// --- Approximate location for hot start ---
float approxLat = 36.1156;  // Stillwater, OK N positive
float approxLon = -97.0584; // W negative
float approxAlt = 300;      // Approx altitude in meters

void setup() {
  Serial.begin(9600);
  Serial.println("GPS Hot Start Satellite Monitor - Adafruit I2C GPS");

  GPS.begin(0x10); // I2C address
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA); // RMC + GGA
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);    // 1 Hz update
  GPS.sendCommand(PGCMD_ANTENNA);               // antenna status query
  delay(1000);

  // --- Hot start: provide approximate location ---
  char cmd[50];
  // MTK commands for approximate position: $PMTK740,<lat>,<lon>,<alt>*CS
  sprintf(cmd, "$PMTK740,%.6f,%.6f,%.1f*00", approxLat, approxLon, approxAlt);
  GPS.sendCommand(cmd);

  Serial.println("Hot start location sent to GPS.");
}

void loop() {
  // Read from GPS
  char c = GPS.read();
  if (GPSECHO && c) Serial.print(c);

  // Parse new NMEA sentences
  if (GPS.newNMEAreceived()) {
    GPS.parse(GPS.lastNMEA());
  }

  // Every 2 seconds, print stats
  if (millis() - timer > 2000) {
    timer = millis();
    Serial.print("\nFix: "); Serial.print((int)GPS.fix);
    Serial.print(" | Quality: "); Serial.print((int)GPS.fixquality);
    Serial.print(" | Satellites: "); Serial.println((int)GPS.satellites);

    if (GPS.fix) {
      Serial.print("Lat: "); Serial.print(GPS.latitude, 6); Serial.print(GPS.lat);
      Serial.print(" | Lon: "); Serial.print(GPS.longitude, 6); Serial.println(GPS.lon);
      Serial.print("Alt: "); Serial.println(GPS.altitude);
      Serial.print("Speed (knots): "); Serial.println(GPS.speed);
      Serial.print("Angle: "); Serial.println(GPS.angle);
    }
  }
}