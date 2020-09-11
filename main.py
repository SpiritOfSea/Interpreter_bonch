import converter
import translator
import memory
import errors
import executor

Reporter = errors.ErrorReporter('__main.py__')

Converter = converter.Converter('example.cpp', 'example.intpr')
Converter.start_convertation()
Translator = translator.Translator('example.intpr')
OP_LIST = Translator.translate()
Executor = executor.Executor()
Executor.execute(OP_LIST)
print(Executor.dump_mem())
