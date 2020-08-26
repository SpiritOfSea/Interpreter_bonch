import variables
import re


def compute_math(eq, MEM):
    counter = 0
    last_end = 0
    new_eq = ''
    for element in re.finditer(r'([^<>+/*\-()]+)', eq):
        if MEM.check(element.group()):
            new_eq += eq[last_end:element.start()] + str(MEM[element.group()])
            last_end = element.end()
        counter += 1
    new_eq += eq[last_end:]

    res = eval(new_eq)
    return res


def compute_boolean(eq, MEM):
    counter = 0
    last_end = 0
    new_eq = ''
    for element in re.finditer(r'([^+/*\^\-()<>!=]+)', eq):
        if MEM.check(element.group()):
            new_eq += eq[last_end:element.start()] + str(MEM[element.group()])
            last_end = element.end()
        counter += 1
    new_eq += eq[last_end:]
    if eval(new_eq):
        return True
    else:
        return False


def get_line_number(line):
    if line[:3].lstrip("0") == '':
        return 0
    else:
        return int(line[:4].lstrip("0"))


def get_block_dict(src_file):
    start_list = []
    block_dict = dict()
    with open(src_file) as file:
        for line in file:
            if line[4] == '{':
                start_list.append(get_line_number(line))
            elif line[4] == '}':
                block_dict.update({start_list.pop():get_line_number(line)})
    return block_dict

#
#
VAR_MEM = variables.VAR_MEM()
VAR_MEM["var_int_ex"] = "int", 6
VAR_MEM["var_char_ex"] = "int", 6
VAR_MEM["var_float_ex"] = "float", 3.0
#
# eq = "1+1"
# print(compute_math(VAR_MEM, eq))

print(get_block_dict("example.intpr"))