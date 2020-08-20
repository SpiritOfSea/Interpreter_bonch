import re

# module that parses all the variables into VAR_MEM

class VAR_MEM:

    def __init__(self):
        self.IN_MEM = dict()
        self.FULL_MODE = False

    def __setitem__(self, key, value):
        if value == "float" or value == "int" or value == "char":
            if value == "float":
                self.IN_MEM[key] = ("float", 0.0)
            elif value == "int":
                self.IN_MEM[key] = ("int", 0)
            else:
                self.IN_MEM[key] = ("char", '')
        elif type(value) == tuple:
            if value[0] == "float":
                try:
                    if type(value[1]) == float:
                        self.IN_MEM[key] = ("float", float(value[1]))
                    else:
                        raise TypeError
                except (TypeError, ValueError) as e:
                    print("WRONG VARIABLE TYPE:")
                    print(e)
            elif value[0] == "int":
                try:
                    self.IN_MEM[key] = ("int", int(value[1]))
                except (TypeError, ValueError) as e:
                    print("WRONG VARIABLE TYPE:")
                    print(e)
            elif value[0] == "char":
                try:
                    if value[1].isalpha() and len(value[1]) == 1:
                        self.IN_MEM[key] = ("char", str(value[1]))
                    else:
                        raise TypeError
                except (TypeError, ValueError, AttributeError) as e:
                    print("WRONG VARIABLE TYPE:")
                    print(e)
            else:
                print("UNKNOWN VARIABLE TYPE")
        else:
            try:
                if str(type(value)) == self.IN_MEM[key][0]:
                    self.IN_MEM[key] = self.IN_MEM[key][0], value
                else:
                    raise TypeError
            except KeyError as e:
                print("VARIABLE DOES NOT EXIST: "+key)
            except TypeError as e:
                print("got gotted")
                print(e)

    def set_full_mode(self, switch):
        if switch:
            self.FULL_MODE = True
        else:
            self.FULL_MODE = False

    def __getitem__(self, item):
        if self.FULL_MODE:
            return self.IN_MEM[item]
        else:
            return self.IN_MEM[item][1]

    def __str__(self):
        str_repr = "\nVARIABLES MEMORY STATUS:\n\n"
        for variable in self.IN_MEM:
            str_repr += hex(id(self.IN_MEM[variable])) + ' name: "' + variable + '" type: "' + self.IN_MEM[variable][0] + '" content: "' + str(self.IN_MEM[variable][1]) + '";\n'
        return str_repr


VAR_MEM = VAR_MEM()
VAR_MEM["var_int_ex"] = "int"
VAR_MEM["var_char_ex"] = "int", 6
VAR_MEM["var_int_ex"] = "char", 'y'
VAR_MEM["var_float_ex"] = "float", 4.5
print(VAR_MEM["var_float_ex"])
VAR_MEM.set_full_mode(True)
print(VAR_MEM["var_float_ex"])

