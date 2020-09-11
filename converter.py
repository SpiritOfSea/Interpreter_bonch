import re
import errors


class Converter:

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.content = ""
        self.reporter = errors.ErrorReporter("__converter.py__")

    def file_load_as_string(self):  # loads file content as single string
        file = open(self.input_path, "r")
        file_content = file.read()
        file.close()
        self.content = file_content

    def save_file(self):  # saves "content" string into file, with error check
        try:
            file = open(self.output_path, 'wt')
            file.write(self.content)
            file.close()
        except Exception as e:
            self.reporter.raise_error("Error during file saving", e)

    def find_singleline_comments(self):  # function that finds and deletes all comments in line
        while (re.search(r"(//).*$", self.content, re.MULTILINE)) is not None:
            escaped_group = re.search(r"(//).*", self.content, re.MULTILINE)
            self.content = self.content[:escaped_group.start()] + self.content[escaped_group.end():]

    def find_multiline_comments(self):  # function that deletes block comments
        while (re.search(r"(/\*).*?(\*/)", self.content, re.DOTALL)) is not None:
            escaped_group = re.search(r"(/\*).*?(\*/)", self.content, re.DOTALL)
            self.content = self.content[:escaped_group.start()] + self.content[escaped_group.end():]

    @staticmethod
    def del_all_newlines(text_to_cleanup):  # delete all the newlines inside string
        new_string = text_to_cleanup
        while re.search(r"(\n)", new_string, re.DOTALL) is not None:
            escaped_group = re.search(r"(\n)", new_string, re.DOTALL)
            new_string = new_string[:escaped_group.start()] + new_string[escaped_group.end():]
        return new_string

    def del_spaces(self):  # delete spaces
        in_quotes = False  # bool to check surrounding quotes
        prev_char = ''  # previous char to catch sequence
        cor = 0  # correction to avoid "out of range" problem
        for char_pos in range(len(self.content)):
            char = self.content[char_pos - cor]
            if char == r'"' and in_quotes is False:
                in_quotes = True
            elif char == r'"' and in_quotes is True:
                in_quotes = False
            elif char == r' ' and prev_char == r' ' and in_quotes is False:  # delete double spaces not in quotes
                self.content = self.content[:char_pos - cor] + self.content[char_pos + 1 - cor:]
                cor += 1
            elif char == r' ' and prev_char == "\n":  # delete spaces at the beginning of the line
                self.content = self.content[:char_pos - cor] + self.content[char_pos + 1 - cor:]
                cor += 1
            elif char == "\n" and prev_char == r' ':  # delete spaces at the end of the line
                self.content = self.content[:char_pos - cor - 1] + self.content[char_pos - cor:]
                cor += 1
            else:
                prev_char = char
        self.content = self.content.replace(" ;", ";")  # also fixing ;'s here
        self.content = self.content.replace("\n;", ";")
        self.content = self.content.replace(";", ";\n")

    def cleanup_params(self):  # cleanup newlines and spaces in brackets ()
        while re.search(r"(\([^(]*(\n|\s)[^(]*\))", self.content,
                        re.DOTALL) is not None:  # deleting all empty lines in middle
            escaped_group = re.search(r"(\([^(]*(\n|\s)[^(]*\))", self.content, re.DOTALL)
            self.content = self.content[:escaped_group.start()] \
                           + self.del_all_newlines(self.content[escaped_group.start():escaped_group.end()]).replace(' ','') \
                           + '\n' + self.content[escaped_group.end():]

    def check_for_paired_brackets(self):  # check { and } for pairs, also add newlines
        self.content = self.content.replace("{", "\n${\n")
        self.content = self.content.replace("}", "\n$}\n")  # add marks to both { and }, also add newlines
        while re.search(r"(\$})", self.content, re.DOTALL):  # while closing brackets exist...
            closest_bracket = re.search(r"(\$})", self.content, re.DOTALL).start()
            if self.content[:closest_bracket].rfind("${") != -1:  # ...find opening brackets for them
                self.content = self.content[:closest_bracket] + self.content[closest_bracket + 1:]  # delete marks
                self.content = self.content[:self.content[:closest_bracket].rfind("${")] \
                               + self.content[self.content[:closest_bracket].rfind("${") + 1:]
            else:  # if closing bracket exist, but opening does not
                error_pos = closest_bracket
                self.reporter.raise_error("'{' missing at "+str(error_pos)+" position", '')
                self.content = self.content[:closest_bracket] + self.content[closest_bracket + 1:]
        if re.search(r"(\${)", self.content, re.DOTALL):  # if opening bracket exist, but closing does not
            error_pos = re.search(r"(\${)", self.content, re.DOTALL).start()
            self.content = self.content[:error_pos] + self.content[error_pos + 1:]
            self.reporter.raise_error("'}' missing at "+str(error_pos)+" position", '')

    def del_empty_lines(self):  # clearing all the empty lines
        while re.search(r"(\n\s).*?(\S)", self.content, re.DOTALL) is not None:  # deleting all empty lines in middle
            escaped_group = re.search(r"(\n\s).*?(\S)", self.content, re.DOTALL)
            self.content = self.content[:escaped_group.start()] + "\n" + self.content[escaped_group.end() - 1:]

        while self.content[:1] == "\n":  # deleting all empty lines at the beginning
            self.content = self.content[1:]

        while self.content[-1:] == "\n":  # deleting all empty lines at the end
            self.content = self.content[:-1]

    def add_counter(self):  # add three digits at the beggining of the line
        counter = 0
        modified_content = ""
        for line in self.content.split("\n"):
            modified_content = modified_content + '\n' + str(counter).zfill(3) + ' ' + line
            counter += 1
        self.content = modified_content[1:]

    def correct_short_functions(self):  # add brackets to one-line-functions
        while re.search(r'((if|while|else)\(\S*?\)[^\n])', self.content, re.DOTALL):
            escaped_group = re.search(r'((if|while|else)\(\S*?\)[^\n])', self.content, re.DOTALL)
            self.content = self.content[:escaped_group.end() - 1] + '\n' + self.content[escaped_group.end():]
        while re.search(r'((if\([^{]*?\)?|while\([^{]*?\)?|else)\n[^{]*?\n)', self.content, re.DOTALL):
            escaped_group = re.search(r'((if\([^{]*?\)?|while\([^{]*?\)?|else)\n[^{]*?\n)', self.content, re.DOTALL)
            modified_group = escaped_group.group(1).split('\n')[0] + '\n{\n' + escaped_group.group(1).split('\n')[
                1] + '\n}\n'
            self.content = self.content[:escaped_group.start()] + modified_group + self.content[escaped_group.end():]

    def singleline_vars(self):  # collapse all text after aloat\int\char in one line
        while re.search(r'((float|char|int)[^()]*?\n+?[^()]*?;)', self.content, re.DOTALL):
            escaped_group = re.search(r'((float|char|int)[^()]*?\n+?[^()]*?;)', self.content, re.DOTALL)
            modified_group = escaped_group.group(0).replace('\n', '')
            self.content = self.content[:escaped_group.start()] + modified_group + self.content[escaped_group.end():]

    def check_text_at_end(self):
        if self.content[-1] != '}':
            self.reporter.raise_error("Text after last '}'", '')

    def parse(self):  # method that unites all 'parse' methods

        # Parse order:
        # 1. Delete all single-line comments
        # 2. Delete all multi-line comments
        # 3. Singleline '(' and ')'s
        # 4. Check paired { }
        # 5. Expand one line functions
        # 6. Place variable definitions in one line
        # 7. Delete double spaces not in quotes
        # 8. Clear empty lines
        # 9. Check for text after ending }
        # 10. Add counter
        try:
            self.find_singleline_comments()
            self.find_multiline_comments()
            self.check_for_paired_brackets()
            self.correct_short_functions()
            self.singleline_vars()
            self.del_spaces()
            self.cleanup_params()
            self.del_empty_lines()
            self.check_text_at_end()
            self.add_counter()
        except Exception as e:
            self.reporter.raise_error("Error during parsing", e)

    def start_convertation(self):
        self.file_load_as_string()
        self.parse()
        self.save_file()


if __name__ == '__main__':
    convert = Converter("example.cpp", "example.intpr")
    convert.start_convertation()
