class Filter:

    def __init__(self, expression):
        self.expression = expression

    def evaluate(self, value):
        return eval(self.expression.replace('value', str(value)))
