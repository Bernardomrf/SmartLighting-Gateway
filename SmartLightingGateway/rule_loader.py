import configs as confs
import os
import ujson
from rules import Rules
from converter import Converter
from window import Window
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
                    if 'window' in action['function']['listen_data']:
                        module = Window(action['function']['listen_data']['window']['type'],
                        action['function']['listen_data']['window']['value'],
                        action['function']['listen_data']['window']['units'])

                    elif 'converter' in action['function']['listen_data']:

                        module = Converter(action['function']['listen_data']['converter']['type'],
                        action['function']['listen_data']['converter']['max_lux'])

                    new_action = Action(listener['topic'],
                    '/SM'+action['target']['topic'],
                    action['function']['name'],
                    module)

                    Rules.add_action(new_action, '/SM'+listener['topic'].replace("/+","/[^/]+"))
