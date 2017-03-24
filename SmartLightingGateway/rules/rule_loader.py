import .configs as confs
import os
import ujson
from rule import Rule
from action import Action
from .modules.converter import Converter
from .modules.window import Window
from .modules.filters import Filter
from .modules.agregator import Aggregator


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

                window = None
                converter = None
                _filter = None
                aggregator = None

                if 'window' in action['function']['listen_data']:
                    if action['function']['listen_data']['window']['type'] == 'time':
                        window = Window.get_window(action['function']['listen_data']['window']['type'],
                        action['function']['listen_data']['window']['value'],
                        action['function']['listen_data']['window']['units'])
                        aggregator = Aggregator.get_aggregator(action['function']['listen_data']['aggregator']['type'])

                    elif action['function']['listen_data']['window']['type'] == 'length':
                        window = Window.get_window(action['function']['listen_data']['window']['type'],
                        action['function']['listen_data']['window']['value'])
                        aggregator = Aggregator.get_aggregator(action['function']['listen_data']['aggregator']['type'])

                if 'converter' in action['function']['listen_data']:

                    converter = Converter.get_converter(action['function']['listen_data']['converter']['type'],
                    action['function']['listen_data']['converter']['max_lux'])

                if 'filters' in action['function']['listen_data']:
                    _filter = Filter(RuleLoader.get_boolean_expression(action['function']['listen_data']['filters']))

                new_action = Action('/SM'+action['target']['topic'],
                    action['function']['name'],
                    _filter, aggregator, window, converter)
                for listener in action['function']['listen_data']['listeners']:
                    Rules.add_action(new_action, '/SM'+listener['topic'].replace("/+","/[^/]+"))

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
