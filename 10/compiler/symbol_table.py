from const import *


class Symbol():
    def __init__(self, name, type, kind, number):
        if kind not in (VAR, STATIC, ARG, FIELD):
            raise Exception("kind must be var or static or arg or field")
        self.kind = kind
        self.name = name
        self.type = type
        self.number = number

    def segment(self):
        if self.kind == VAR:
            return LOCAL
        elif self.kind == ARG:
            return "argument"
        elif self.kind == STATIC:
            return self.kind
        else:
            raise Exception


class SymbolTable():
    def __init__(self):
        self.class_table = {}
        self.routine_table = {}
        self.kind2next_index = {}
        for kind in (STATIC, FIELD, ARG, VAR):
            self.kind2next_index[kind] = 0

    def define(self, name, type, kind):
        if kind in (ARG, VAR):
            if name in self.routine_table or name in self.class_table:
                raise Exception("symbol name {} is already used".format(name))
            symbol = Symbol(name, type, kind, self.kind2next_index[kind])
            self.kind2next_index[kind] += 1
            self.routine_table[name] = symbol
            return symbol
        elif kind in (STATIC, FIELD):
            if name in self.routine_table or name in self.class_table:
                raise Exception("symbol name {} is already used".format(name))
            symbol = Symbol(name, type, kind, self.kind2next_index[kind])
            self.kind2next_index[type] += 1
            self.class_table[name] = symbol
            return symbol
        else:
            raise Exception

    def symbol(self, name) -> Symbol:
        if name in self.routine_table:
            return self.routine_table[name]
        elif name in self.class_table:
            return self.class_table[name]
        else:
            raise Exception("name not defined")

    def var_count(self, kind):
        if kind not in (VAR, STATIC, ARG, FIELD):
            raise Exception("kind must be var or static or arg or field")
        return self.kind2next_index[kind]

    def start_subroutine(self):
        self.routine_table = {}
        self.kind2next_index = {}
        for kind in (ARG, VAR):
            self.kind2next_index[kind] = 0
        return
