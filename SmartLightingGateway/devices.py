
class Devices:
    devices = {}
    event_id = 0

    def new_event(device):
        Devices.devices[device] = Devices.event_id
        Devices.event_id+=1
        return Devices.event_id
