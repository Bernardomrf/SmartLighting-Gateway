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

    def process_rules(msg):
        print('Loading Rule')
        #print(msg)
        topics = RuleLoader.load_json(ujson.loads(msg))

        return topics

    def load_json(data):
        topics = []

        for action in data['rule']['actions']:

            if action['function']['name'] == 'set_value':
                topics += RuleLoader.get_action_modules(action, data['id'], 'listen_data')

            elif action['function']['name'] == 'setif_value_percent':

                returns = RuleLoader.get_action_modules(action, data['id'], 'listen_value')
                value_action = returns[0]
                topics += returns[1]
                topics += RuleLoader.get_action_modules(action, data['id'], 'listen_boolean', value_action)
        return topics
        print("Rule added")

    def get_action_modules(action, r_id, listen, value_action = None):
        window = None
        converter = None
        _filter = None
        aggregator = None
        topics = []

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
                topics.append('/SM'+listener['topic'])
                Rule.add_action(new_action, '/SM'+listener['topic'].replace("/+","/[^/]+"), r_id)
            return topics

        elif listen == 'listen_value':
            new_action = Action('/SM'+action['target']['topic'],
                action['function']['name'],
                _filter, aggregator, window, converter, None, action['function']['percent_if_true'], action['function']['percent_if_false'])

            for listener in action['function'][listen]['listeners']:
                topics.append('/SM'+listener['topic'])
                Rule.add_action(new_action, '/SM'+listener['topic'].replace("/+","/[^/]+"), r_id)

            return (new_action, topics)

        elif listen == 'listen_boolean':
            new_action = Action('/SM'+action['target']['topic'],
                action['function']['name'],
                _filter, aggregator, window, converter, value_action)

            for listener in action['function'][listen]['listeners']:
                topics.append('/SM'+listener['topic'])
                Rule.add_action(new_action, '/SM'+listener['topic'].replace("/+","/[^/]+"), r_id)

            return topics

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
