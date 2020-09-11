#  module that translates source code into ordered list of operations

from utility import *
import errors


class Translator:

    def __init__(self, translating_file):
        self.OP_LIST = []  # Generate empty FINAL list of operations
        self.blocks_dict = get_block_dict(translating_file)  # Generate block map
        self.translating_file = translating_file  # Source file
        self.unique_counter = 0  # Unique counter for commands
        self.reporter = errors.ErrorReporter("__translator.py__")

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

    def translate(self):  # Source translate function, which start recursive loop
        with open(self.translating_file) as file:
            self.block = [line.strip() for line in file]
        self.OP_LIST = self.translate_block(0, len(self.block))  # First "block" consists of whole file
        return self.OP_LIST

    def translate_block(self, start, end):  # Operation that translates 'block', takes start an end of block
        OP_LIST = []  # Generate block, inner OP_LIST
        cur = start  # While end of block not reached, continue translation
        while cur < end:
            cur, temp_OP = self.translate_string(self.block[cur], cur, OP_LIST)
            for a in temp_OP:
                OP_LIST.append(a)  # We recursively taking string_OP_LIST, adding it to inner block OP_LIST
        return OP_LIST

    def translate_string(self, trstr, in_point, block_OP_LIST):
        OP_LIST = []  # Inner string OP_LIST
        out_point = in_point  # By default, after completing one string we move to the next one
        line_number = get_line_number(trstr)  # Getting current line number as integer
        trstr = trstr[4:]  # Current string, that contains everything but number of string
        key = trstr.split(" ")[0]  # We trying to get keyword by splitting by space...
        key = key.split(",")[0]  # ...or by commas, if we have variables list

        if key[-3:-1] == "++" or key[-3:-1] == "--":  # Holding special case with easy +1 or -1
            key = key[:-3]
        trstr = trstr[len(key):].strip()  # Deleting keyword from string
        try:  # Also, deleting ; at the end of current string
            if trstr[-1] == ';':
                trstr = trstr[:-1]
            else:
                pass
        except IndexError as e:
            pass
            # self.reporter.raise_error("Index error while trying to delete ';'", e)

        if key == "float" or key == "int" or key == "char":  # If string starts with keywords
            if len(trstr.split("=")) != 1:  # If we have construction like "type var1, ..., varN = ..."
                variables = trstr.split("=")[0].strip()
                content = trstr.split("=")[1].strip()
                for var in variables.split(','):
                    OP_LIST.append(('SETVAR', var.strip(), (key, content)))  # For each operation we add separate command
            else:  # If we just declare variables
                for var in trstr.split(','):
                    OP_LIST.append(('SETVAR', var.strip(), key))

        elif key == 'while':  # Holding of "while" key
            if block_OP_LIST[-1][0] == "ENDOFDO":  # If while stands right after end of "do" block
                cond = re.search(r'(\(.*\))', trstr).group(0)[1:-1]  # Catch while conditions in brackets
                out_point += 3  # Skip empty block
                unique_counter = block_OP_LIST[-1][-1]  # Set same ID as "do" block has
                OP_LIST.append(("DOWHILE", cond, unique_counter))  # Place corresponding command
            else:  # If while stands independant
                cond = re.search(r'(\(.*\))', trstr).group(0)[1:-1]
                out_point = self.blocks_dict[line_number+1]

                temp_OP_LIST = self.translate_block(in_point+1, out_point)

                OP_LIST.append(("WHILE", cond, self.unique_counter))
                for x in temp_OP_LIST:
                    OP_LIST.append(x)
                OP_LIST.append(("ENDOFWHILE", self.unique_counter))
                self.unique_counter += 1  # Continue global ID counter

        elif key == 'for':  # Holding of "for"
            cond = trstr[1:-1].split(';')  # Parse (a;b;c) params as list of conditions
            out_point = self.blocks_dict[line_number+1]

            temp_OP_LIST = self.translate_block(in_point+1, out_point)

            OP_LIST.append(("FOR", cond, self.unique_counter))
            for x in temp_OP_LIST:
                OP_LIST.append(x)
            OP_LIST.append(("ENDOFFOR", self.unique_counter))
            self.unique_counter += 1

        elif key == 'if':
            try:
                cond = re.search(r'(\(.*\))', trstr).group(0)[1:-1]
                out_point = self.blocks_dict[line_number+1]

                temp_OP_LIST = self.translate_block(in_point+1, out_point)

                OP_LIST.append(("IF", cond, self.unique_counter))
                for x in temp_OP_LIST:
                    OP_LIST.append(x)
                OP_LIST.append(("ENDOFIF", self.unique_counter))
                self.unique_counter += 1
            except AttributeError as e:
                self.reporter.raise_error("Wrong IF handle(condition error)", e)

        elif key == 'else':
            out_point = self.blocks_dict[line_number+1]

            temp_OP_LIST = self.translate_block(in_point+1, out_point)
            unique_counter = block_OP_LIST[-1][-1]
            OP_LIST.append(("ELSE", unique_counter))
            for x in temp_OP_LIST:
                OP_LIST.append(x)
            OP_LIST.append(("ENDOFELSE", unique_counter))

        elif key == 'do':
            out_point = self.blocks_dict[line_number+1]
            temp_OP_LIST = self.translate_block(in_point+1, out_point)

            OP_LIST.append(("DO", self.unique_counter))
            for x in temp_OP_LIST:
                OP_LIST.append(x)
            OP_LIST.append(("ENDOFDO", self.unique_counter))
            self.unique_counter += 1

        elif key == 'switch':
            return 0

        else:  # If string starts with unknown keyword, place it as var name
                if trstr[0:2] == '++':  # Increase by 1 operation
                    OP_LIST.append(('SETVAR', key, key+'+1'))

                elif trstr[0:2] == '--':  # Decrease by 1 operation
                    OP_LIST.append(('SETVAR', key, key+'-1'))

                elif trstr[0:1] == ',':  # If we are working with multiple variables
                    variables = key+trstr.split("=")[0].strip()
                    content = trstr.split("=")[1].strip()

                    for var in variables.split(','):
                        OP_LIST.append(('SETVAR', var.strip(), content))

                elif trstr[0:1] == '=':  # If we work with single variable
                    content = trstr[1:].strip()
                    OP_LIST.append(('SETVAR', key, content))
        if out_point == in_point:
            out_point += 1  # Default one-by-one line workout
        else:
            pass
        return out_point, OP_LIST


if __name__ == '__main__':
    Translator = Translator("example.intpr")
    Translator.translate()
    for x in Translator.OP_LIST:
        print(x)