"""
UART Driver for A02YY ultrasonic sensor

Author: Roman Smolka
Link: https://github.com/RomanSmolka/A02YY_Sensor

Frame format:
+--------+--------+--------+-----+
| HEADER | DATA_H | DATA_L | SUM |
+--------+--------+--------+-----+

SUM = (HEADER + DATA_H + DATA_L) & 0x00FF

Frame is sent every 300ms when sensor RX is high or floating, or every 100ms when RX is low (lower accuracy).
"""

import time
from serial import Serial
from enum import Enum

class SensorType(Enum):
  AUTO       = 1
  CONTROLLED = 2

class Error(Enum):
  TIMEOUT      = 'No data'
  INVALID_DATA = 'Invalid data'

class A02YY_Sensor:
  HEADER = 0xFF

  def __init__(self, port: str, type: SensorType = SensorType.AUTO):
    self.serial = Serial(port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1)
    self.type = type

  def _read_data(self):
    data = b''
    now = time.time()

    while True:
      # read one byte
      data = self.serial.read()

      # wait for header byte
      if len(data) and data[0] == self.HEADER:
        # then wait for remaining data bytes
        while (self.serial.in_waiting < 4):
          time.sleep(0.01)

          # data timeout
          if (time.time() - now) > 1:
            return Error.TIMEOUT
        break

      # header timeout
      if (time.time() - now) > 1:
        return Error.TIMEOUT

    # read remaining bytes and flush buffer
    data += self.serial.read(self.serial.in_waiting)
    self.serial.reset_input_buffer()

    return data

  def measure(self) -> int | str:
    """Returns distance in mm or error message"""
    self.serial.rts = 1

    # create falling edge for controlled mode
    if self.type == SensorType.CONTROLLED:
      time.sleep(0.05)
      self.serial.rts = 0

    data = self._read_data()

    self.serial.rts = 1

    if type(data) == Error:
      return data.value

    checksum = (data[0] + data[1] + data[2]) & 0xFF

    if data[3] == checksum:
      distance = data[1] * 256 + data[2]
      return distance

    return Error.INVALID_DATA.value
