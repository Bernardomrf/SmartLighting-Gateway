
class Devices:
    devices = {}
    event_id = 0

    def new_event(device):
        Devices.event_id+=1
        Devices.devices[device] = Devices.event_id
        return Devices.event_id
