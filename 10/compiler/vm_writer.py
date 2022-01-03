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

    def write_arithmetic(self, command):
        self.__write_code_lines([
            command
        ])
