from A02YY_Sensor import A02YY_Sensor, SensorType

port = '/dev/tty.usbserial-A50285BI'

sensor = A02YY_Sensor(port)

# For A02YYTW (controlled):
# sensor = A02YY_Sensor(port, SensorType.CONTROLLED)

measurement = sensor.measure()

if type(measurement) is int:
  print('Distance is', measurement, 'mm')
else:
  print('Error:', measurement)
