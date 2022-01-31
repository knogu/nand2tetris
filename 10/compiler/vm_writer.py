class VMWriter:
    def __init__(self, path):
        self.f = open(path, mode='w')

    def __write_code_lines(self, code_lines):
        self.f.write('\n'.join(code_lines))
        self.f.write('\n')

    def write_push(self, segment, index):
        self.__write_code_lines([
            "push {} {}".format(segment, index)
        ])

    def write_pop(self, segment, index):
        self.__write_code_lines([
            "pop {} {}".format(segment, index)
        ])

    def write_arithmetic(self, command):
        self.__write_code_lines([
            command
        ])

    def write_call(self, func, arg_count):
        self.__write_code_lines([
            "call {} {}".format(func, arg_count)
        ])

    def write_return(self):
        self.__write_code_lines([
            "return"
        ])

    def write_func(self, class_name, func_name, arg_count):
        self.__write_code_lines([
            "function {}.{} {}".format(class_name, func_name, arg_count)
        ])
