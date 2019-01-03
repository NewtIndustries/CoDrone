import bluetooth


class Bluetooth:
    def __init__(self):
        self.id = 1

    def listAvailable(self):
        nearbyDevices = bluetooth.discover_devices(lookup_names=True)
        print("found %d devices" % len(nearbyDevices))

        for addr, name in nearbyDevices:
          print("  %s - %s" % (addr, name))
