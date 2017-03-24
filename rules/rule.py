class Rule:

    actions_list = {}

    def __init__(self, action, in_regex):
        Rule.actions_list[in_regex].append(action)

    def add_action(action, in_regex):

        if in_regex in Rule.actions_list:
            Rule.actions_list[in_regex].append(action)
        else:
            Rule.actions_list[in_regex] = [action]
