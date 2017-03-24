class Rule:

    actions_list = {}

    def __init__(self, action, in_regex):
        Rules.actions_list[in_regex].append(action)

    def add_action(action, in_regex):

        if in_regex in Rules.actions_list:
            Rules.actions_list[in_regex].append(action)
        else:
            Rules.actions_list[in_regex] = [action]
