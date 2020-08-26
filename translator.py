#  module that translates source code into ordered list of operations

import variables
import re
from utility import *


class Translator:

    def __init__(self, translating_file):
        self.OP_LIST = []
        self.blocks_dict = get_block_dict(translating_file)
        self.translating_file = translating_file
        self.unique_counter = 0
        # OP LIST INSTRUCTIONS SET:
        # SETVAR (var, content) - set var
        # INCRVAR (var) - increase by 1
        # DECRVAR (var) - decrease by 1

    def translate(self):
        with open(self.translating_file) as file:
            self.block = [line.strip() for line in file]
        self.OP_LIST, last_OP = self.translate_block(0, len(self.block), 0)

    def translate_block(self, start, end, last_OP):
        OP_LIST = []
        cur = start
        while cur < end:
            cur, temp_OP, last_OP = self.translate_string(self.block[cur], cur, last_OP)
            print(cur, end)
            for a in temp_OP:
                OP_LIST.append(a)
        return OP_LIST, last_OP

    def translate_string(self, trstr, in_point, last_OP):
        OP_LIST = []
        out_point = in_point
        line_number = get_line_number(trstr)
        trstr = trstr[4:]
        key = trstr.split(" ")[0]
        key = key.split(",")[0]
        if key[-3:-1] == "++" or key[-3:-1] == "--":
            key = key[:-3]
        trstr = trstr[len(key):].strip()
        try:
            if trstr[-1] == ';':
                trstr = trstr[:-1]
            else:
                # print("NO ; AT END")
                pass
        except IndexError as e:
            pass

        if key == "float" or key == "int" or key == "char":
            if len(trstr.split("=")) != 1:
                variables = trstr.split("=")[0].strip()
                content = trstr.split("=")[1].strip()
                for var in variables.split(','):
                    OP_LIST.append(('SETVAR', var.strip(), (key, content)))
            else:
                for var in trstr.split(','):
                    OP_LIST.append(('SETVAR', var.strip(), key))
        elif key == 'while':
            print("T")
            OP_starting_adress = last_OP
            cond = '1'
            out_point = self.blocks_dict[line_number+1]

            temp_OP_LIST, last_OP = self.translate_block(in_point+1, out_point, last_OP)

            OP_LIST.append(("WHILE", cond, self.unique_counter))
            for x in temp_OP_LIST:
                OP_LIST.append(x)
            OP_LIST.append(("ENDOFWHILE", self.unique_counter))
            self.unique_counter +=1
        elif key == 'for':
            return 0
        elif key == 'if':
            return 0
        elif key == 'else':
            return 0
        elif key == 'do':
            return 0
        elif key == 'switch':
            return 0
        else:
                if trstr[0:2] == '++':
                    OP_LIST.append(('INCRVAR', key))

                elif trstr[0:2] == '--':
                    OP_LIST.append(('DECRVAR', key))

                elif trstr[0:1] == ',':
                    variables = key+trstr.split("=")[0].strip()
                    content = trstr.split("=")[1].strip()

                    for var in variables.split(','):
                        OP_LIST.append(('SETVAR', var.strip(), content))

                elif trstr[0:1] == '=':
                    content = trstr[1:].strip()
                    OP_LIST.append(('SETVAR', key, content))
        if out_point == in_point:
            out_point += 1
        else:
            print('QQ' + str(out_point))
        return out_point, OP_LIST, last_OP+len(OP_LIST)

if __name__ == '__main__':
    Translator = Translator("example.intpr")
    MEM = variables.VAR_MEM()
    Translator.translate()
    for x in Translator.OP_LIST:
        print(x)