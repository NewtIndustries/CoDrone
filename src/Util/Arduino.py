import serial

class Arduino:
    def __init__(self):
        self.ser = serial.Serial('COM3', 9600, timeout=0)
        self.settings = self.ser.get_settings()