

class Converter:

    def get_converter(_type, max_lux=None):

        if _type == 'lux_to_percentage':
            return LuxToPercent(max_lux)
        elif _type == 'set_to_1':
            return SetTo1()
        elif _type == 'set_to_0':
            return SetTo0()
        else:
            return None



    def name(self):
        return "Converter"


class LuxToPercent(Converter):

    _type = 'lux_to_percentage'

    def __init__(self, max_lux):
        self.max_lux = max_lux

	def get_dict(self):
		d = dict()
		d['type'] = LuxToPercent._type
		d['max_lux'] = self.max_lux
		return d


class SetTo1(Converter):
	_type = 'set_to_1'

	def get_dict(self):
		d = dict()
		d['type'] = SetTo1._type
		return d


class SetTo0(Converter):
	_type = 'set_to_0'

	def get_dict(self):
		d = dict()
		d['type'] = SetTo0._type
		return d
