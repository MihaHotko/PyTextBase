class DatabaseExistsError(Exception):
    def __init__(self):
        Exception.__init__(self, "DATABASE ALREADY EXISTS")


class DatabaseNotExistsError(Exception):
    def __init__(self):
        Exception.__init__(self, "DATABASE DOES NOT EXIST")


class MissingArgumentError(Exception):
    def __init__(self):
        Exception.__init__(self, "MISSING ARGUMENTS TO PUT INTO THE DATABASE")

# raises a custom typevalueerror
class TypeValueError(Exception):
    def __init__(self, typeOf):
        self.__init__(self)
        self.m = "ARGUMENT MUST BE OF TYPE %s" % typeOf

    def __str__(self):
        return self.m
