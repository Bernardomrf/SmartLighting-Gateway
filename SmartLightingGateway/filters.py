class Filter:

    def get_filter(f_type, f_value):
        if f_type is 'eq':
            return EQ(value)
        elif f_type is 'ne':
            return NE(value)
        elif f_type is 'gt':
            return GT(value)
        elif f_type is 'lt':
            return LT(value)
        elif f_type is 'gte':
            return GTE(value)
        elif f_type is 'lte':
            return LTE(value)
        else:
            return None

class EQ(Filter):

    f_type = 'eq'

    def __str__(self):
        return 'Equal to %d'%self.value

    def __init__(self, value):
        self.value = value

	def get_dict(self):
		d = dict()
		d['type'] = EQ._type
		d['value'] = self.value
		return d


class NE(Filter):

    f_type = 'ne'

    def __str__(self):
        return 'Not Equal to %d'%self.value

    def __init__(self, value):
        self.value = value
        self.f_type = 'ne'

	def get_dict(self):
		d = dict()
		d['type'] = NE.f_type
		d['value'] = self.value
		return d


class GT(Filter):

    f_type = 'gt'

    def __str__(self):
        return 'Greater than %d'%self.value

    def __init__(self, value):
        self.value = value

	def get_dict(self):
		d = dict()
		d['type'] = GT.f_type
		d['value'] = self.value
		return d


class LT(Filter):

    f_type = 'lt'

    def __str__(self):
        return 'Less than %d'%self.value

    def __init__(self, value):
        self.value = value

	def get_dict(self):
		d = dict()
		d['type'] = LT.f_type
		d['value'] = self.value
		return d


class GTE(Filter):

    f_type = 'gte'

    def __str__(self):
		return 'Greater or Equal than %d'%self.value

    def __init__(self, value):
        self.value = value

	def get_dict(self):
		d = dict()
		d['type'] = GTE.f_type
		d['value'] = self.value
		return d


class LTE(Filter):

    f_type = 'lte'

    def __str__(self):
        return 'Less or Equal than %d'%self.value

    def __init__(self, value):
        self.value = value

	def get_dict(self):
		d = dict()
		d['type'] = LTE.f_type
		d['value'] = self.value
		return d
