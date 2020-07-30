import re


# TODO: remake as a class
# TODO: add "{" and "}" escape


def file_load_as_string(file_path):  # loads file content as single string
    file = open(file_path, "r")
    file_content = file.read()
    file.close()
    return file_content


def save_file(file_path, content):  # saves "content" string into file, with error check
    try:
        file_path = file_path.split(".cpp")[0]  # TODO: make correct format change
        file = open(file_path + '.intpr', 'wt')  # TODO: delete temporary file after completion (?)
        file.write(content)
        file.close()
        return 0
    except:
        return 1


def find_singleline_comments(raw_string):  # function that finds and deletes all comments in line
    new_string = raw_string
    while (re.search(r"(//).*$", new_string, re.MULTILINE)) is not None:
        escaped_group = re.search(r"(//).*", new_string, re.MULTILINE)
        new_string = new_string[:escaped_group.start()] + new_string[escaped_group.end():]
    return new_string


def find_multiline_comments(raw_string):
    new_string = raw_string
    while (re.search(r"(/\*).*?(\*/)", new_string, re.DOTALL)) is not None:
        escaped_group = re.search(r"(/\*).*?(\*/)", new_string, re.DOTALL)
        new_string = new_string[:escaped_group.start()] + new_string[escaped_group.end():]
    return new_string


def del_all_newlines(raw_string):  # delete all the newlines inside string
    new_string = raw_string
    while re.search(r"(\n)", new_string, re.DOTALL) is not None:  # deleting all empty lines in middle
        escaped_group = re.search(r"(\n)", new_string, re.DOTALL)
        new_string = new_string[:escaped_group.start()] + new_string[escaped_group.end():]
    return new_string


def del_multiple_spaces(raw_string):
    new_string = raw_string
    while re.search(r"(\n\s).*?(\S)", new_string, re.DOTALL) is not None:  # deleting all empty lines in middle
        escaped_group = re.search(r"(\n\s).*?(\S)", new_string, re.DOTALL)
        new_string = new_string[:escaped_group.start()] + "\n" + new_string[escaped_group.end() - 1:]


def cleanup_params(raw_string):  # cleanup newlines in brackets ()
    new_string = raw_string
    while re.search(r"(\().*.(\n).*?(\))", new_string, re.DOTALL) is not None:  # deleting all empty lines in middle
        escaped_group = re.search(r"(\().*.(\n).*?(\))", new_string, re.DOTALL)
        new_string = new_string[:escaped_group.start()] \
                     + del_all_newlines(new_string[escaped_group.start():escaped_group.end()]).replace(' ', '') \
                     + new_string[escaped_group.end():]
    return new_string


def del_empty_lines(raw_string):  # clearing all the empty lines
    new_string = raw_string

    while re.search(r"(\n\s).*?(\S)", new_string, re.DOTALL) is not None:  # deleting all empty lines in middle
        escaped_group = re.search(r"(\n\s).*?(\S)", new_string, re.DOTALL)
        new_string = new_string[:escaped_group.start()] + "\n" + new_string[escaped_group.end() - 1:]

    while new_string[:1] == "\n":  # deleting all empty lines at the beginning
        new_string = new_string[1:]

    while new_string[-1:] == "\n":  # deleting all empty lines at the end
        new_string = new_string[:-1]

    return new_string


def parse(raw_string):  # function that unites all 'parse' methods

    # Parse order:
    # 1. Delete all single-line comments
    # 2. Delete all multi-line comments
    # 3. Singleline '(' and ')'s
    # 4. Delete double spaces
    # 5. Clear empty lines

    new_string = find_singleline_comments(raw_string)
    new_string = find_multiline_comments(new_string)
    new_string = cleanup_params(new_string)
    new_string = del_empty_lines(new_string)
    return new_string


def initialize(file_name):  # resetting all settings and starting converting for each file
    content = file_load_as_string(file_name)
    parsed_content = parse(content)
    error_check = save_file(file_name, parsed_content)  # TODO: make not that dumb error check
    if error_check == 1:
        print("Got an error during save operation")
    return 0


if __name__ == '__main__':
    file_to_transfer = "example.cpp"
    initialize(file_to_transfer)
