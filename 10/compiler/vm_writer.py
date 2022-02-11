class VMWriter:
    def __init__(self, path):
        self.f = open(path, mode='w')
        # バッファが複数必要になったら変更
        self.is_to_buffer = False
        self.buffer_lines = []

    def __write_code_lines(self, code_lines):
        for line in code_lines:
            self.write_one_line(line)

    def write_one_line(self, line):
        if self.is_to_buffer:
            self.buffer_lines.append(line)
        else:
            self.f.write(line)
            self.f.write('\n')

    def write_and_clear_buffer(self):
        self.__write_code_lines(self.buffer_lines)
        self.buffer_lines = []

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

    def write_if(self, target_label):
        self.__write_code_lines([
            "if-goto {}".format(target_label)
        ])

    def write_goto(self, target_label):
        self.__write_code_lines([
            "goto {}".format(target_label)
        ])

    def write_label(self, label_name):
        self.__write_code_lines([
            "label {}".format(label_name)
        ])
