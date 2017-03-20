class Aggregator:

    def get_aggregator(a_type):
        if a_type is 'avg':
            return Avg()
        elif a_type is 'any':
            return Any()
        elif a_type is 'none':
            return NonE()
        else:
            return None

class Avg(Aggregator):
	_type = 'avg'

	def __str__(self):
		return 'Average'

	def get_dict(self):
		d = dict()
		d['type'] = Avg._type
		return d

class Any(Aggregator):
	_type = 'any'

	def __str__(self):
		return 'Any'

	def get_dict(self):
		d = dict()
		d['type'] = Any._type
		return d

	@staticmethod
	def descript():
		d = dict()
		d['name'] = 'Any'
		d['description'] = 'Returns value 1 if at least one of the events has value equal to 1'
		d['type'] = Any._type
		return d

class NonE(Aggregator):
	_type = 'none'

	def __str__(self):
		return 'None'

	def get_dict(self):
		d = dict()
		d['type'] = NonE._type
		return d

	@staticmethod
	def descript():
		d = dict()
		d['name'] = 'None'
		d['description'] = 'Returns value 1 if all events have value equal to 0'
		d['type'] = NonE._type
		return d
