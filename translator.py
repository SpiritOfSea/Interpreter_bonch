#  module that translates source code into ordered list of operations

import variables
import re


class Translator:

    def __init__(self):
        self.OP_LIST = []

        # OP LIST INSTRUCTIONS SET:
        # SETVAR (var, content) - set var
        # INCRVAR (var) - increase by 1
        # DECRVAR (var) - decrease by 1


    def translate_string(self, trstr, in_point):
        out_point = in_point
        trstr = trstr[4:]
        key = trstr.split(" ")[0]
        key = key.split(",")[0]
        if key[-3:-1] == "++" or key[-3:-1] == "--":
            key = key[:-3]
        trstr = trstr[len(key):].strip()
        if trstr[-1] == ';':
            trstr = trstr[:-1]
        else:
            print("NO ; AT END")

        if key == "float" or key == "int" or key == "char":
            if len(trstr.split("=")) != 1:
                variables = trstr.split("=")[0].strip()
                content = trstr.split("=")[1].strip()
                for var in variables.split(','):
                    self.OP_LIST.append(('SETVAR', var.strip(), (key, content)))
            else:
                for var in trstr.split(','):
                    self.OP_LIST.append(('SETVAR', var.strip(), key))
        elif key == 'while':
            return 0
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
                    self.OP_LIST.append(('INCRVAR', key))

                elif trstr[0:2] == '--':
                    self.OP_LIST.append(('DECRVAR', key))

                elif trstr[0:1] == ',':
                    variables = key+trstr.split("=")[0].strip()
                    content = trstr.split("=")[1].strip()

                    for var in variables.split(','):
                        self.OP_LIST.append(('SETVAR', var.strip(), content))

                elif trstr[0:1] == '=':
                    content = trstr[1:].strip()
                    self.OP_LIST.append(('SETVAR', key, content))


if __name__ == '__main__':
    Translator = Translator()
    MEM = variables.VAR_MEM()
    Translator.translate_string("008 float test,test2 = 6;", 0)
    Translator.translate_string("009 test = 15;", 0)
    Translator.translate_string("010 test2 = 5;", 0)
    for x in Translator.OP_LIST:
        print(x)