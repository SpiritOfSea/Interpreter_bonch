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

    def set_content_type(self, type, content):
        try:
            if type == "float":
                content = float(content)
            elif type == "int":
                content = int(content)
        except (TypeError, ValueError) as e:
            print("TYPEERROR")  # RAISE ERROR
        return content

    def translate_string(self, trstr, in_point):
        out_point = in_point
        trstr = trstr[4:]
        key = trstr.split(" ")[0]
        key = key.split(",")[0]
        trstr = trstr[len(key):].strip()
        if trstr[-1] == ';':
            trstr = trstr[:-1]
        else:
            print("NO ; AT END")

        if key == "float" or key == "int" or key == "char":
            if len(trstr.split("=")) != 1:
                variables = trstr.split("=")[0].strip()
                content = trstr.split("=")[1].strip()
                content = self.set_content_type(key, content)
                for var in variables.split(','):
                    MEM[var.strip()] = key, content
                    self.OP_LIST.append(('SETVAR', var.strip(), (key, content)))
            else:
                for var in trstr.split(','):
                    MEM[var.strip()] = key  # TIME
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
            if MEM.check(key):
                if trstr[0:2] == '++':
                    self.OP_LIST.append(('INCRVAR', key))

                elif trstr[0:2] == '--':
                    self.OP_LIST.append(('DECRVAR', key))

                elif trstr[0:1] == ',':
                    variables = key+trstr.split("=")[0].strip()
                    type = MEM.get_type(key)
                    content = trstr.split("=")[1].strip()
                    content = self.set_content_type(type, content)

                    for var in variables.split(','):
                        MEM[var.strip()] = type, content  # TIME
                        self.OP_LIST.append(('SETVAR', var.strip(), (type, content)))

                elif trstr[0:1] == '=':
                    type = MEM.get_type(key)
                    content = trstr[1:].strip()
                    content = self.set_content_type(type, content)
                    self.OP_LIST.append(('SETVAR', key, content))
            else:
                print('ERROR OCCURRED')


if __name__ == '__main__':
    Translator = Translator()
    MEM = variables.VAR_MEM()
    Translator.translate_string("008 float test,test2;", 0)
    Translator.translate_string("009 test = 0;", 0)
    Translator.translate_string("010 test,test2 = 2.0;", 0)
    for x in Translator.OP_LIST:
        print(x)