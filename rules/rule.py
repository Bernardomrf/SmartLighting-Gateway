class Rule:

    actions_list = {}

    def __init__(self, action, in_regex, r_id):
        Rule.actions_list[in_regex].append((r_id, action))

    def add_action(action, in_regex, r_id):

        if in_regex in Rule.actions_list:
            Rule.actions_list[in_regex].append((r_id, action))
        else:
            Rule.actions_list[in_regex] = [(r_id, action)]
