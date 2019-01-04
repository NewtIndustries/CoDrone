import traceback
import threading
import os
import CoDrone
import tkinter as tk
import sched
import time
import sys
import serial
from CoDrone import Mode, Color, Direction
from sched import scheduler
from src.Util.Bluetooth import Bluetooth
from src.Util.Arduino import Arduino
from src.Util.Camera import Camera

# class ENUM_STATE(Enum):
#     READY="READY"
#     #READY, TAKE_OFF, FLIGHT, FLIP, STOP, LANDING, REVERSE, ACCIDENT, ERROR
STATE_READY = "READY"
STATE_TAKE_OFF = "TAKE_OFF"
STATE_FLIGHT = "FLIGHT"
STATE_FLIP = "FLIP"
STATE_STOP = "STOP"
STATE_LANDING = "LANDING"
STATE_REVERSE = "REVERSE"
STATE_ACCIDENT = "ACCIDENT"
STATE_ERROR = "ERROR"

closing = False


class CoDroneControl(tk.Frame):
    def __init__(self, parent, drone):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.drone = drone
        self.statusVal = ""
        self.status = tk.StringVar()
        self.batteryLevel = tk.StringVar()
        self.altitude = tk.StringVar()
        self.gyroscope = tk.StringVar()
        self.initialize_user_interface()
        self.updater = sched.scheduler(time.time, time.sleep)
        self.updater.enter(2, 1, self.updateLoop)
        # self.bluetooth = Bluetooth()
        # self.bluetooth.listAvailable()
        # self.arduino = Arduino()
        self.camera = Camera()
        if self.camera.isCameraConnected:
          self.camera.readFrame()
        threading.Timer(1, self.updater.run).start()

    def updateLoop(self):
        if not(closing):
            self.updateDroneStatus()
            self.updater.enter(2, 1, self.updateLoop)

    def initialize_user_interface(self):
        self.parent.geometry("640x1080")
        self.parent.title("CoDrone Command Module")

        self.buttonOpen = tk.Button(
            self.parent, text="Open", command=self.open)
        self.buttonOpen.pack()

        self.buttonConnect = tk.Button(
            self.parent, text="Connect", command=self.connect)
        self.buttonConnect.pack()

        self.buttonPair = tk.Button(
            self.parent, text="Pair", command=self.pairNearest)
        self.buttonPair.pack()

        self.buttonRecalibrate = tk.Button(
            self.parent, text="Recalibrate", command=self.recalibrate)
        self.buttonRecalibrate.pack()

        self.buttonTakeoff = tk.Button(
            self.parent, text="Take Off", command=self.takeOff)
        self.buttonTakeoff.pack()

        self.buttonLand = tk.Button(
            self.parent, text="Land", command=self.land)
        self.buttonLand.pack()

        self.buttonMoveUp = tk.Button(
            self.parent, text="Move Up", command=lambda: (self.changeAltitude(10)))
        self.buttonMoveUp.pack()

        self.buttonMoveDown = tk.Button(
            self.parent, text="Move Down", command=lambda: (self.changeAltitude(-10)))
        self.buttonMoveDown.pack()

        self.buttonSpin = tk.Button(
            self.parent, text="SpinnyTown!", command=self.spin)
        self.buttonSpin.pack()

        self.buttonSetPurple = tk.Button(
            self.parent, text="Purple Eyes", command=self.purplize)
        self.buttonSetPurple.pack()

        self.buttonSetDefaultColor = tk.Button(
            self.parent, text="Reset Color", command=self.resetColor)
        self.buttonSetDefaultColor.pack()

        self.labelStatus = tk.Label(self.parent, textvariable=self.status)
        self.labelStatus.pack()

        self.buttonExit = tk.Button(
            self.parent, text="QUIT", command=self.shutdown)
        self.buttonExit.pack()

    def open(self):
        try:
            if self.drone.isOpen():
                self.drone.close()
            else:
                self.drone.open()
                print(self.drone.get_state())
        except Exception:
            print("Error in Open")

    def connect(self):
        try:
            print(self.drone.isConnected())

            if self.drone.isConnected():
                print("Drone is connected - disconnecting")
                self.drone.disconnect()
            else:
                print("Drone is not connected - connecting")
                self.drone.connect()
                print("Drone finished connecting")
        except Exception:
            print("Error In Connect")

    def pairNearest(self):
        try:
            if self.drone.Nearest != "0000":
                self.drone.pair(self.drone.Nearest)
        except Exception:
            print("Error in Piar")

    def takeOff(self):
        try:
            self.drone.takeoff()
        except Exception:
            print(traceback.format_exc())

    def land(self):
        try:
            self.drone.land()
        except Exception:
            print(traceback.format_exc())

    def purplize(self):
        try:
            self.drone.set_eye_led(120, 0, 120, Mode.SOLID)
        except Exception:
            print(traceback.format_exc())

    def resetColor(self):
        try:
            self.drone.set_all_default_led(255, 255, 255, Mode.SOLID)
        except Exception:
            print("Failed setting color")

    def spin(self):
        try:
            self.drone.turn(Direction.RIGHT, 2)
        except Exception:
            print("Spin failed")

    def updateDroneStatus(self):
        try:
            self.statusVal = ""
            self.appendState("Open", self.drone.isOpen())
            self.appendState("Connected", self.drone.isConnected())
            # self.appendState("Paired", self.drone.)
            if self.drone.isOpen():
                # print(self.drone.isOpen())
                try:
                    self.appendState("State", self.drone.get_state())
                except Exception:
                    print("Error in get state")

            if self.drone.isOpen() and (self.drone.get_state() == STATE_READY or self.drone.get_state() == STATE_FLIGHT):
                # print("Open and Ready")
                self.appendState(
                    "Battery Level", self.drone.get_battery_percentage())
                self.appendState("Battery Voltage",
                                 self.drone.get_battery_voltage())
                self.appendState("Pressure", self.drone.get_pressure())
                self.appendState("Height", self.drone.get_height())
                self.appendState(
                    "Temperature", self.drone.get_drone_temp() * 9 / 5 + 32)
                self.appendState("Accelerometer", self.getAxisString(
                    self.drone.get_accelerometer()))
                self.appendState("Gyroscope", self.getAngleString(
                    self.drone.get_gyro_angles()))
                self.appendState("Angular Speed", self.getAngleString(
                    self.drone.get_angular_speed()))
                self.appendState("Flow Opt Position", self.getPositionString(
                    self.drone.get_opt_flow_position()))
                self.appendState(
                    "Trim", self.getFlightString(self.drone.get_trim()))

        except Exception:
            print(traceback.format_exc())

        self.status.set(self.statusVal)

    def appendState(self, label, val):
        self.statusVal = self.statusVal + label + " - " + str(val) + os.linesep

    def emergencyAbort(self):
        self.drone.land()
        self.drone.close()

    def recalibrate(self):
        self.drone.calibrate()

    def changeAltitude(self, delta):
        alt = self.drone.get_height() + delta
        if alt > 0:
            self.drone.go_to_height(alt)
        else:
            self.drone.land()

    def getAxisString(self, axis: CoDrone.system.Axis):
        return "X: " + str(axis.X) + " Y: " + str(axis.Y) + " Z: " + str(axis.Z)

    def getAngleString(self, angle: CoDrone.system.Angle):
        return "PITCH: " + str(angle.PITCH) + " ROLL: " + str(angle.ROLL) + " YAW: " + str(angle.YAW)

    def getPositionString(self, position: CoDrone.system.Position):
        return "X: " + str(position.X) + " Y: " + str(position.Y)

    def getFlightString(self, flight: CoDrone.system.Flight):
        return "PITCH: " + str(flight.PITCH) + " ROLL: " + str(flight.ROLL) + " YAW: " + str(flight.YAW) + " THROTTLE: " + str(flight.THROTTLE)

    def shutdown(self):
        root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    drone = CoDrone.CoDrone()
    drone.disconnect()
    drone.close()

    def onClosing():
        closing = True
        try:
            if drone.isOpen():
                if drone.isConnected():
                    if drone.is_flying():
                        drone.land()
                    drone.disconnect()
                drone.close()
        except TypeError:
            print("Drone Not Closed for not existing")
        except Exception:
            print(traceback.format_exc())
        except:
            print("Error on closing - closing")

        root.destroy()

    run = CoDroneControl(root, drone)
    root.protocol("WM_DELETE_WINDOW", onClosing)
    root.mainloop()
