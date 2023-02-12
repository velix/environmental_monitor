import time
import board
import busio
import adafruit_scd30
import prometheus_client

# SCD-30 has tempremental I2C with clock stretching, datasheet recommends
# starting at 50KHz
i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)
# scd.temperature_offset = 10
print("Temperature offset:", scd.temperature_offset)

scd.measurement_interval = 15
print("Measurement interval:", scd.measurement_interval)

# scd.self_calibration_enabled = True
print("Self-calibration enabled:", scd.self_calibration_enabled)

# scd.ambient_pressure = 1100
print("Ambient Pressure:", scd.ambient_pressure)

# scd.altitude = 100
print("Altitude:", scd.altitude, "meters above sea level")

# scd.forced_recalibration_reference = 409
print("Forced recalibration reference:", scd.forced_recalibration_reference)
print("")


prometheus_client.start_http_server(9999)

co2_metric = prometheus_client.Gauge('co2_ppm', 'CO2 measurement, in PPM',['SCD30_CO2']) 
temp_metric = prometheus_client.Gauge('temp_c_deg', 'Temperature measurement in C',['SCD30_TEMP'])
humidity_metric = prometheus_client.Gauge('hum_rel', 'Humidity measurement, in %RH (relative)',['SCD30_HUM']) 

while True:
    data = scd.data_available
    print("Checking for data...")
    if data:
        print("Data Available!")
        co2 = scd.CO2
        co2_metric.labels("co2").set(co2)

        temp = scd.temperature
        temp = round(temp, 1)
        temp_metric.labels("temp_c").set(temp) 
        
        humidity = scd.relative_humidity
        humidity_metric.labels("humidity_rel").set(humidity)

    time.sleep(10)
