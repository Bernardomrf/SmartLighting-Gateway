import configs as confs
import os
import ujson
from .rule import Rule
from .action import Action
from modules.converter import Converter
from modules.window import Window
from modules.filters import Filter
from modules.agregator import Aggregator


class RuleLoader:

    def process_rules():
        print('Loading Rules')

        for filename in os.ilistdir(confs.RULES_FOLDER):
            if filename[0].endswith(".json"):
                with open(confs.RULES_FOLDER + filename[0]) as data_file:
                    RuleLoader.load_json(ujson.load(data_file))

    def load_json(data):
        for subrule in data['subrules']:
            for action in subrule['actions']:

                if action['function']['name'] == 'set_value':
                    RuleLoader.get_action_modules(action, 'listen_data')

                elif action['function']['name'] == 'setif_value_percent':
                    value_action = RuleLoader.get_action_modules(action, 'listen_value')
                    RuleLoader.get_action_modules(action, 'listen_boolean', value_action)


    def get_action_modules(action, listen, value_action = None):
        window = None
        converter = None
        _filter = None
        aggregator = None

        if 'window' in action['function'][listen]:
            if action['function'][listen]['window']['type'] == 'time':
                window = Window.get_window(action['function'][listen]['window']['type'],
                action['function'][listen]['window']['value'],
                action['function'][listen]['window']['units'])
                aggregator = Aggregator.get_aggregator(action['function'][listen]['aggregator']['type'])

            elif action['function'][listen]['window']['type'] == 'length':
                window = Window.get_window(action['function'][listen]['window']['type'],
                action['function'][listen]['window']['value'])
                aggregator = Aggregator.get_aggregator(action['function'][listen]['aggregator']['type'])

        if 'converter' in action['function'][listen]:

            converter = Converter.get_converter(action['function'][listen]['converter']['type'],
            action['function'][listen]['converter']['max_lux'])

        if 'filters' in action['function'][listen]:
            _filter = Filter(RuleLoader.get_boolean_expression(action['function'][listen]['filters']))


        if listen == 'listen_data':
            new_action = Action('/SM'+action['target']['topic'],
                action['function']['name'],
                _filter, aggregator, window, converter)
            for listener in action['function'][listen]['listeners']:
                Rule.add_action(new_action, '/SM'+listener['topic'].replace("/+","/[^/]+"))

        elif listen == 'listen_value':
            new_action = Action('/SM'+action['target']['topic'],
                action['function']['name'],
                _filter, aggregator, window, converter, None, action['function']['percent_if_true'], action['function']['percent_if_false'])

            for listener in action['function'][listen]['listeners']:
                Rule.add_action(new_action, '/SM'+listener['topic'].replace("/+","/[^/]+"))

            return new_action

        elif listen == 'listen_boolean':
            new_action = Action('/SM'+action['target']['topic'],
                action['function']['name'],
                _filter, aggregator, window, converter, value_action)

            for listener in action['function'][listen]['listeners']:
                Rule.add_action(new_action, '/SM'+listener['topic'].replace("/+","/[^/]+"))

    def get_boolean_expression(in_filters):
        if 'op' in in_filters:
            return "(" + RuleLoader.get_boolean_expression(in_filters['in_filters'][0]) + in_filters['op'] + RuleLoader.get_boolean_expression(in_filters['in_filters'][1]) + ")"

        else:
            return "(value" + RuleLoader.get_operator(in_filters['type']) + str(in_filters['value']) + ")"


    def get_operator(_type):
        if _type == 'eq':
            return " == "
        elif _type == 'ne':
            return " != "
        elif _type == 'gt':
            return " > "
        elif _type == 'lt':
            return " < "
        elif _type == 'gte':
            return " >= "
        elif _type == 'lte':
            return " <= "
        else:
            return None
