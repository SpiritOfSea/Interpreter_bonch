# module that holds errors and writes them to error.txt file
import time
from datetime import *


class ErrorReporter:
    def __init__(self, module):
        self.module = module
        self.file = "errors.txt"

    def change_file(self, file):
        self.file = file

    def raise_error(self, error, error_message):
        file = open(self.file, 'a')
        file.write(str(datetime.now())+"   "+self.module+": "+repr(error)+". Error content: "+repr(error_message)+"\n")
        file.close()
        return 1
