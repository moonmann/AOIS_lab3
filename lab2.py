def construct_list():
    value_list = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                value_list.append({'x': i, 'y': j, 'z': k, 'rez': 0})
    return value_list


def bracket_check(expression):
    bracket = 0
    for char in expression:
        if char == "(":
            bracket += 1
        if char == ")":
            if bracket == 0:
                return False
            bracket -= 1
    return bracket == 0


def negation(expression, values_dict):
    return not parse_expression(expression, values_dict)


def conjunction(expression_1, expression_2, values_dict):
    return parse_expression(expression_1, values_dict) and parse_expression(expression_2, values_dict)


def disjunction(expression_1, expression_2, values_dict):
    return parse_expression(expression_1, values_dict) or parse_expression(expression_2, values_dict)


def parse_part_expression(expression, char):
    bracket = 0
    for i in reversed(range(len(expression))):
        if expression[i] == "(":
            bracket += 1
        if expression[i] == ")":
            bracket -= 1
        if expression[i] == char and bracket == 0:
            return i
    return -1


def parse_expression(expression, values_dict):
    expression = expression.replace(" ", "")

    if not bracket_check(expression):
        return "Error"

    while expression[0] == "(" and expression[-1] == ")" and bracket_check(expression[1:len(expression) - 1]):
        expression = expression[1:len(expression) - 1]

    if len(expression) == 1:
        return values_dict[expression]

    if parse_part_expression(expression, '+') != -1:
        num_char = parse_part_expression(expression, '+')
        return disjunction(expression[0:num_char], expression[num_char + 1:], values_dict)

    if parse_part_expression(expression, '*') != -1:
        num_char = parse_part_expression(expression, '*')
        return conjunction(expression[0:num_char], expression[num_char + 1:], values_dict)

    if parse_part_expression(expression, '!') != -1:
        num_char = parse_part_expression(expression, '!')
        return negation(expression[num_char + 1:], values_dict)


def create_truth_table(expression, value_list):
    for values_dict in value_list:
        values_dict['rez'] = parse_expression(expression, values_dict)


def create_sdnf(value_list):
    result = ''
    num_form = []
    count = 0
    for values_dict in value_list:
        if values_dict['rez']:
            result += '({}x * {}y * {}z) + '.format(values_dict['x'], values_dict['y'], values_dict['z'])
            num_form.append(count)
        count += 1
    result = result.replace('1', '')
    result = result.replace('0', '!')
    return result[:len(result) - 2]


def create_sknf(value_list):
    result = ''
    num_form = []
    count = 0
    for values_dict in value_list:
        if not values_dict['rez']:
            result += '({}x + {}y + {}z) * '.format(values_dict['x'], values_dict['y'], values_dict['z'])
            num_form.append(count)
        count += 1
    result = result.replace('0', '')
    result = result.replace('1', '!')
    return result[:len(result) - 2]


def create_index_form(value_list):
    result = 0
    i = 7
    for values_dict in value_list:
        if values_dict['rez']:
            result += 2**i
        i -= 1
    return result


def main():
    expression = '!((x+y)*!(x*!(z)))'
    value_list = construct_list()
    create_truth_table(expression, value_list)
    print('Expression: ' + expression)
    print('x\ty\tz\tresult')
    for values_dict in value_list:
        print('{}\t{}\t{}\t{}'.format(values_dict['x'], values_dict['y'], values_dict['z'], values_dict['rez']))
    print('SDNF: ' + create_sdnf(value_list))
    print('SKNF: ' + create_sknf(value_list))
    print('Index form: ' + str(create_index_form(value_list)))
