import numpy
from lab2 import create_truth_table, construct_list, create_sdnf, create_sknf


ROW_NUM = 2
COLOMN_NUM = 4


def check_negative(string, char):
    if char.find('!') == -1:
        index = string.find(char)
        if index != -1 and string[index - 1] != '!':
            return True
        return False
    else:
        return string.find(char) != -1


def check_argument(string, tuple_arg):
    return check_negative(string, tuple_arg[0]) and check_negative(string, tuple_arg[1])


def create_dict():
    arguments_list = ['x', 'y', 'z', '!x', '!y', '!z']
    comb = [(a, b) for a in arguments_list for b in arguments_list if a != b]
    tuple_list = [tuple(sorted(sub)) for sub in comb]
    tuple_list = list(set(tuple_list))
    implicant_dict = {}
    for element in tuple_list:
        implicant_dict[element] = 0
    return implicant_dict


def create_table_calculation_result(implicant_to_constituent_list, is_sdnf):
    result = ''
    for i in implicant_to_constituent_list:
        if len(i) == 1 and is_sdnf:
            result += '({} * {}) + '.format(i[0][0], i[0][1])
        elif len(i) == 1 and not is_sdnf:
            result += '({} + {}) * '.format(i[0][0], i[0][1])
    return result[:len(result) - 2]


def create_constituent_list(expression, is_sdnf):
    if is_sdnf:
        return expression.split(' + ')
    else:
        return expression.split(' * ')


def create_implicant_list(constituent_list):
    implicant_dict = create_dict()
    for constituent in constituent_list:
        for implicant in implicant_dict:
            if check_argument(constituent, implicant):
                implicant_dict[implicant] += 1
    implicant_list = []
    for implicant in implicant_dict:
        if implicant_dict[implicant] >= 2:
            implicant_list.append(implicant)
    return implicant_list


def print_matrix(constituent_list, implicant_list, matrix):
    print('Table for table calculation method')
    print('\t\t'+'\t'.join(map(str, constituent_list)))
    for i, j in zip(matrix, implicant_list):
        print('{} {}\t\t'.format(j[0], j[1]) + '\t\t\t\t'.join(map(str, i)))


def minimization_table_calculation_method(expression, is_sdnf):
    constituent_list = create_constituent_list(expression, is_sdnf)
    implicant_list = create_implicant_list(constituent_list)
    matrix = numpy.zeros((len(implicant_list), len(constituent_list)))
    implicant_to_constituent_list = []
    for i in range(len(constituent_list)):
        implicant_to_constituent_list.append([])
        for j in range(len(implicant_list)):
            if check_argument(constituent_list[i], implicant_list[j]):
                matrix[j][i] = 1
                implicant_to_constituent_list[i].append(implicant_list[j])
    print_matrix(constituent_list, implicant_list, matrix)
    return create_table_calculation_result(implicant_to_constituent_list, is_sdnf)


def implicant_set(implicant, is_sdnf):
    implicant_value_dict = {}
    if implicant[0][0] == '!':
        implicant_value_dict[implicant[0][1]] = int(not is_sdnf)
    else:
        implicant_value_dict[implicant[0]] = is_sdnf
    if implicant[1][0] == '!':
        implicant_value_dict[implicant[1][1]] = int(not is_sdnf)
    else:
        implicant_value_dict[implicant[1]] = is_sdnf
    return implicant_value_dict


def replace_implicant(arg_list, implicant_value_dict):
    for i in implicant_value_dict:
        arg_list = list(map(lambda x: x.replace(i, str(implicant_value_dict[i])), arg_list))
    arg_list = list(map(lambda x: x.replace('!0', '1'), arg_list))
    arg_list = list(map(lambda x: x.replace('!1', '0'), arg_list))
    return arg_list


def check_arg_list(arg_list):
    temp_list = [x for x in arg_list if not x.isdigit()]
    temp_list = list(set(temp_list))
    return len(temp_list) == 1


def check_excess_implicant(implicant_list, implicant, implicant_value_dict):
    arg_list = []
    for i in implicant_list:
        if i != implicant:
            arg_list.append(i[0])
            arg_list.append(i[1])
    arg_list = replace_implicant(arg_list, implicant_value_dict)
    return check_arg_list(arg_list)


def check_impicant(implicant_list, is_sdnf):
    result = ''
    for i in implicant_list:
        if is_sdnf:
            if check_excess_implicant(implicant_list, i, implicant_set(i, is_sdnf)):
                result += '({} * {}) + '.format(i[0], i[1])
        else:
            if check_excess_implicant(implicant_list, i, implicant_set(i, is_sdnf)):
                result += '({} + {}) * '.format(i[0], i[1])
    return result[:len(result) - 2]


def minimization_calculation_method(expression, is_sdnf):
    constituent_list = create_constituent_list(expression, is_sdnf)
    implicant_list = create_implicant_list(constituent_list)
    return check_impicant(implicant_list, is_sdnf)


def check_pairs_horizontally(matrix, char):
    pairs_list = []
    for i in range(ROW_NUM):
        for j in range(COLOMN_NUM):
            if j == 3 and matrix[i][j] == matrix[i][0] == char:
                pairs_list.append((i, j))
            elif j != 3 and matrix[i][j] == matrix[i][j + 1] == char:
                pairs_list.append((i, j))
    return pairs_list


def check_pairs_vertically(matrix, char):
    pairs_list = []
    for i in range(COLOMN_NUM):
        if matrix[0][i] == matrix[1][i] == char:
            pairs_list.append(i)
    return pairs_list


def create_karnaugh_map(expression):
    value_list = construct_list()
    create_truth_table(expression, value_list)
    for value in value_list:
        value['rez'] = int(value['rez'])
    matrix = numpy.zeros((ROW_NUM, COLOMN_NUM))
    index = 0
    for j in range(ROW_NUM):
        for k in range(COLOMN_NUM):
            matrix[j][k] = value_list[index]['rez']
            index += 1
    matrix[:, [2, 3]] = matrix[:, [3, 2]]
    return matrix


def pairs_to_implicant_horizontally(pair, is_sdnf):
    if is_sdnf:
        value_dict_x = {0: '!x', 1: 'x'}
        value_dict_y_z = {0: '!y', 1: 'z', 2: 'y', 3: '!z'}
    else:
        value_dict_x = {0: 'x', 1: '!x'}
        value_dict_y_z = {0: 'y', 1: '!z', 2: '!y', 3: 'z'}
    return value_dict_x[pair[0]], value_dict_y_z[pair[1]]


def pairs_to_implicant_vertically(pair, is_sdnf):
    if is_sdnf:
        value_dict = {0: ('!y', '!z'), 1: ('!y', 'z'), 2: ('y', 'z'), 3: ('y', '!z')}
    else:
        value_dict = {0: ('y', 'z'), 1: ('y', '!z'), 2: ('!y', '!z'), 3: ('y', '!z')}
    return value_dict[pair]


def print_karnaugh_map(matrix):
    print('Table for table method')
    print('x\\yz\t00\t01\t11\t10')
    for i in range(ROW_NUM):
        print(str(i)+'\t\t'+' '.join(map(str, matrix[i])))


def minimization_table_method(expression, is_sdnf):
    matrix = create_karnaugh_map(expression)
    print_karnaugh_map(matrix)
    pairs_horizontally = check_pairs_horizontally(matrix, is_sdnf)
    pairs_vertically = check_pairs_vertically(matrix, is_sdnf)
    implicant_list = []
    for i in pairs_horizontally:
        implicant_list.append(pairs_to_implicant_horizontally(i, is_sdnf))
    for i in pairs_vertically:
        implicant_list.append(pairs_to_implicant_vertically(i, is_sdnf))
    return check_impicant(implicant_list, is_sdnf)


def print_rezult(expression, is_sdnf):
    print('Calculation method: \n' + minimization_calculation_method(expression, is_sdnf))
    print('Table calculation method: \n' + minimization_table_calculation_method(expression, is_sdnf))
    print('Table method: \n' + minimization_table_method(expression, is_sdnf))


def main():
    expression = '(x+y)*z'
    print('Expression: \n'+expression)
    value_list = construct_list()
    create_truth_table(expression, value_list)
    sdnf = create_sdnf(value_list)
    sknf = create_sknf(value_list)
    print('SDNF: \n' + sdnf)
    print_rezult(create_sdnf(value_list), 1)
    print('\nSKNF: \n' + sknf)
    print_rezult(create_sknf(value_list), 0)


if __name__ == '__main__':
    main()
