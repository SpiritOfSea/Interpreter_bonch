# module that parses all the variables into VAR_MEM
import errors


class VAR_MEM:

    def __init__(self):
        self.IN_MEM = dict()  # variable memory dictionary, which contains data as {'variable': (type, content)}
        self.FULL_MODE = False
        self.reporter = errors.ErrorReporter("__memory.py__")

    def __setitem__(self, key, value):  # reloading an attribute setting method to handle different situations
        if value == "float" or value == "int" or value == "char":  # if there is no starting value of variable, set default
            if value == "float":
                self.IN_MEM[key] = ("float", 0.0)
            elif value == "int":
                self.IN_MEM[key] = ("int", 0)
            else:
                self.IN_MEM[key] = ("char", '')
        elif type(value) == tuple:  # if we parse TYPE and VALUE, we create new variable with value
            if value[0] == "float":
                try:
                    if type(value[1]) == float:  # check for correct value type
                        self.IN_MEM[key] = ("float", float(value[1]))
                    else:
                        raise TypeError
                except (TypeError, ValueError) as e:  # there and after: trying to set wrong value type
                    self.reporter.raise_error("Trying to set variable wrong type(float)", e)
            elif value[0] == "int":
                try:
                    self.IN_MEM[key] = ("int", int(value[1]))
                except (TypeError, ValueError) as e:
                    self.reporter.raise_error("Trying to set variable wrong type(int)", e)
            elif value[0] == "char":
                try:
                    if value[1].isalpha() and len(value[1]) == 1:
                        self.IN_MEM[key] = ("char", str(value[1]))
                    else:
                        raise TypeError
                except (TypeError, ValueError, AttributeError) as e:
                    self.reporter.raise_error("Trying to set variable wrong type(char)", e)
            else:
                self.reporter.raise_error("Unknown variable type: "+value[0], '')
        else:  # if we parse only value, trying to set it to existing value
            try:
                if str(type(value)).split("'")[1] == self.IN_MEM[key][0]:  # check for value type compatibility
                    self.IN_MEM[key] = self.IN_MEM[key][0], value
                elif str(type(value)).split("'")[1] == 'str' and self.IN_MEM[key][0] == 'char' and len(value) == 1:
                    self.IN_MEM[key] = self.IN_MEM[key][0], value
                else:
                    raise TypeError
            except KeyError as e:  # if trying to set to non existing variable
                self.reporter.raise_error("Variable does not exist: "+key, e)
            except TypeError as e:  # not correct value error
                self.reporter.raise_error("Trying to set variable wrong type", e)

    def set_full_mode(self, switch):  # when turned on, VAR call outputs not only content, but type of var also
        if switch:
            self.FULL_MODE = True
        else:
            self.FULL_MODE = False

    def remove(self, item):
        try:
            self.IN_MEM.pop(item)
        except Exception as e:
            self.reporter.raise_error("Error occured during deletion "+item+" variable from memory", e)

    def __getitem__(self, item):  # when requesting variable from memory...
        if self.FULL_MODE:  # ...return type and value
            return self.IN_MEM[item]
        else:  # ...return only value
            return self.IN_MEM[item][1]

    def __str__(self):  # sweet string representation with memory address, name, type and content of all variables
        str_repr = "\nVARIABLES MEMORY STATUS:\n\n"
        for variable in self.IN_MEM:
            str_repr += hex(id(self.IN_MEM[variable])) \
                        + ' name: "' + variable \
                        + '" type: "' + self.IN_MEM[variable][0] \
                        + '" content: "' + str(self.IN_MEM[variable][1]) + '";\n'
        return str_repr

    def check(self, key):  # check does variable exist in memory
        if key in self.IN_MEM:
            return True
        else:
            return False

    def get_type(self, key):  # get type of variable
        return self.IN_MEM[key][0]

