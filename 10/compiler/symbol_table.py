from const import *

class Symbol():
    def __init__(self, name, type, kind, number):
        self.name = name
        self.type = type
        # static or field or arg or var
        self.kind = kind
        self.number = number

class SymbolTable():
    def __init__(self):
        self.class_table = {}
        self.routine_table = {}
        self.kind2next_index = {}
        for kind in (STATIC, FIELD, ARG, VAR):
            self.kind2next_index[kind] = 0

    def define(self, name, type, kind):
        if kind in (ARG, VAR):
            if name in self.routine_table:
                raise Exception("symbol name {} is already used".format(name))
            symbol = Symbol(name, type, kind, self.kind2next_index[kind])
            self.kind2next_index[kind] += 1
            self.routine_table[name] = symbol
            return symbol
        elif kind in (STATIC, FIELD):
            if name in self.class_table:
                raise Exception("symbol name {} is already used".format(name))
            symbol = Symbol(name, type, kind, self.kind2next_index[kind])
            self.kind2next_index[type] += 1
            self.class_table[name] = symbol
            return symbol
        else:
            raise Exception
