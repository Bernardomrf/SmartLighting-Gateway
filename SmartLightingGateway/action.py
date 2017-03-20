


class Action:

    def __init__(self, in_topic, out_topic, func_type, _filter=None, aggregator=None, window=None, converter=None):
        self.in_topic = in_topic
        self.out_topic = out_topic
        self.func_type = func_type
        self._filter = _filter
        self.aggregator = aggregator
        self.window = window
        self.converter = converter

    async def do_work(out_topic, value, device, time, client):

        if value is 0:
            return

        event_id = Devices.new_event(device)

        data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(value) + '}}}'
        client.publish(out_topic, str.encode(data))

        await asyncio.sleep(time)

        if Devices.devices[device] is event_id:
            data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(0) + '}}}'
            client.publish(out_topic, str.encode(data))
