import serial

Ping = 0x01

class Arduino:
    def __init__(self):
        # self.ser = serial.Serial('COM3', 9600, timeout=0)
        self.ser = serial.Serial(
          port = 'COM3',
          baudrate = 115200,
          parity = serial.PARITY_NONE,
          stopbits = serial.STOPBITS_ONE,
          bytesize = serial.EIGHTBITS,
          timeout = 0
        )
        self.settings = self.ser.get_settings()
        self.ser.write(Ping)
        while True:
          byteValue = self.ser.read()

          print(self.ser.read())
