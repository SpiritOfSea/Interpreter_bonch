import re


# TODO: remake as a class
# TODO: add "{" and "}" escape


def initialize(file_name):  # resetting all settings and starting converting for each file
    return 0


def find_singleline_comments(raw_string):  # function that finds and deletes all comments in line
    new_string = raw_string
    while (re.search(r"(//).*$", new_string, re.MULTILINE)) is not None:
        escaped_group = re.search(r"(//).*", new_string, re.MULTILINE)
        new_string = new_string[:escaped_group.start()] + new_string[escaped_group.end():]
    return new_string


def delete_empty_lines(raw_string):  # clearing all the empty lines
    new_string = raw_string

    while re.search(r"(\n\n)", new_string, re.MULTILINE) is not None:  # deleting all empty lines in middle
        escaped_group = re.search(r"(\n\n)", new_string, re.MULTILINE)
        new_string = new_string[:escaped_group.start()] + "\n" + new_string[escaped_group.end():]

    while new_string[:1] == "\n":  # deleting all empty lines at the beginning
        new_string = new_string[1:]

    while new_string[-1:] == "\n":  # deleting all empty lines at the end
        new_string = new_string[:-1]

    return new_string


def parse(raw_string):  # function that unites all 'parse' methods

    # Parse order:
    # 1. Delete all single-line comments
    # 2. Delete all multi-line comments
    # 3. Clear empty lines

    new_string = find_singleline_comments(raw_string)
    new_string = delete_empty_lines(new_string)
    return new_string


if __name__ == '__main__':
    file_to_transfer = "./test.txt"
    initialize(file_to_transfer)
    print(parse("\n\n\nTest //Test //Test \n\nTest2 //Test2\nTest3//Test3//Test3\n//Test4\n\n\n"))
