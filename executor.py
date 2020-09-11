import memory
from utility import *
import errors


# OP LIST INSTRUCTIONS SET:
# SETVAR (var, content) - set var

# DO (ID) - start of do with uID
# ENDOFDO (ID) - end of do with uID
# DOWHILE (cond, ID) - start of WHILE block after DO with uID

# WHILE (cond, ID) - start of while with unique ID
# ENDOWHILE (ID) - end of while block with uID

# FOR ((cond), ID) - start of for block with uID
# ENDFOR (ID) - end of FOR block with uID

# IF (cond, ID) - start of IF block with uID
# ENDIF (ID) - end of IF block with uID

# ELSE (ID) - start of ELSE block, uID is same with connected IF
# ENDOFELSE (ID) - end of ELSE block with uID

class Executor:

    def __init__(self):
        self.MEM = memory.VAR_MEM()
        self.OP_LIST = []
        self.reporter = errors.ErrorReporter('__executor.py__')

    def execute(self, OP_block):
        pointer = 0
        while pointer < len(OP_block):
            starting_pointer = pointer
            operation = OP_block[pointer]

            if operation[0] == "SETVAR":
                if type(operation[2]) == str or type(operation[2]) == int or type(operation[2]) == float:
                    if operation[2] == 'float' or operation[2] == 'char' or operation[2] == 'int':
                        self.MEM[operation[1]] = operation[2]
                    elif type(operation[2]) == str and self.MEM.get_type(operation[1]) != 'char':
                        self.MEM[operation[1]] = compute_math(operation[2], self.MEM)
                    else:
                        self.MEM[operation[1]] = operation[2]
                else:
                    if type(operation[2][1]) == str and operation[2][0] != 'char':
                        self.MEM[operation[1]] = operation[2][0], compute_math(operation[2][1], self.MEM)
                    else:
                        self.MEM[operation[1]] = operation[2][0], operation[2][1]

            elif operation[0] == "WHILE":
                exit_adress = OP_block.index(("ENDOFWHILE", operation[2]))
                while compute_boolean(operation[1], self.MEM):
                    self.execute(OP_block[pointer+1:exit_adress])
                pointer = exit_adress+1

            elif operation[0] == "DO":
                exit_adress = OP_block.index(("ENDOFDO", operation[1]))
                condition = OP_block[exit_adress+1][1]
                while compute_boolean(condition, self.MEM):
                    self.execute(OP_block[pointer+1:exit_adress])
                self.execute(OP_block[pointer+1:exit_adress])
                pointer = exit_adress+2

            elif operation[0] == "FOR":
                exit_adress = OP_block.index(("ENDOFFOR", operation[2]))
                condition = operation[1][1]
                iter_item = operation[1][0].split('=')[0].strip()
                iter_value = float(operation[1][0].split('=')[1].strip())

                if operation[1][2].strip()[-2:] == "++" or operation[1][2].strip()[-2:] == "--":
                    loop_method = operation[1][2].strip()[:-2] + '+1'
                else:
                    loop_method = operation[1][2].split("=")[1].strip()

                self.MEM[iter_item] = "float", iter_value

                while compute_boolean(condition, self.MEM):
                    self.execute(OP_block[pointer+1:exit_adress])
                    self.MEM[iter_item] = compute_math(loop_method, self.MEM)
                self.MEM.remove(iter_item)
                pointer = exit_adress+1

            elif operation[0] == "IF":
                exit_adress = OP_block.index(("ENDOFIF", operation[2]))
                try:
                    else_pointer = OP_block.index(("ELSE", operation[2]))
                    else_exit_adress = OP_block.index(("ENDOFELSE", operation[2]))
                    is_else = True
                except ValueError as e:
                    is_else = False

                if is_else:
                    if compute_boolean(operation[1], self.MEM):
                        self.execute(OP_block[pointer+1:exit_adress])
                    else:
                        self.execute(OP_block[else_pointer+1:else_exit_adress])
                    pointer = else_exit_adress+1

                else:
                    if compute_boolean(operation[1], self.MEM):
                        self.execute(OP_block[pointer+1:exit_adress])
                    pointer = exit_adress+1

            if pointer == starting_pointer:
                pointer +=1

    def dump_mem(self):
        return str(self.MEM)