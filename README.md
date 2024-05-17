# Python library for A02YY ultrasonic sensor

Supports both UART auto (A02YYUW) & UART controlled (A02YYTW) versions.

In controlled mode, the RTS serial pin must be connected to the RX pin of the sensor.

## Usage

```python
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
```