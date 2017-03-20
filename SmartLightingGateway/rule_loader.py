import configs as confs
import os
import ujson
from rules import Rules
from converter import Converter
from window import Window
from filters import Filter
from agregator import Aggregator
from action import Action

class RuleLoader:

    def process_rules():
        print('loading')
        for filename in os.listdir(confs.RULES_FOLDER):
            if filename.endswith(".json"):
                path = confs.RULES_FOLDER + "/" + filename
                with open(confs.RULES_FOLDER + filename) as data_file:
                    RuleLoader.load_json(ujson.load(data_file))

    def load_json(data):
        for subrule in data['subrules']:
            for action in subrule['actions']:
                for listener in action['function']['listen_data']['listeners']:
                    window = None
                    converter = None
                    _filter = None
                    aggregator = None

                    if 'window' in action['function']['listen_data']:
                        print('window')
                        window = Window.get_window(action['function']['listen_data']['window']['type'],
                        action['function']['listen_data']['window']['value'],
                        action['function']['listen_data']['window']['units'])
                        print(window.__str__())

                    elif 'converter' in action['function']['listen_data']:
                        print('converter')
                        converter = Converter.get_converter(action['function']['listen_data']['converter']['type'],
                        action['function']['listen_data']['converter']['max_lux'])

                    elif 'filters' in action['function']['listen_data']:
                        print('filter')
                        _filter = Filter.get_filter(action['function']['listen_data']['filters']['type'],
                        action['function']['listen_data']['filters']['value'])

                    elif 'aggregator' in action['function']['listen_data']:
                        print('aggregator')
                        aggregator = Aggregator.get_aggregator(action['function']['listen_data']['aggregator']['type'])

                    new_action = Action(listener['topic'],
                    '/SM'+action['target']['topic'],
                    action['function']['name'],
                    _filter, aggregator, window, converter)

                    Rules.add_action(new_action, '/SM'+listener['topic'].replace("/+","/[^/]+"))
