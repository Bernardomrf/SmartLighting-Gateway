class Aggregator:

    def get_aggregator(_type):
        if _type == 'avg':
            return Avg()
        elif _type == 'any':
            return Any()
        elif _type == 'none':
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


class NonE(Aggregator):
	_type = 'none'

	def __str__(self):
		return 'None'

	def get_dict(self):
		d = dict()
		d['type'] = NonE._type
		return d
