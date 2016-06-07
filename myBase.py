import re
import os.path
import datetime
from collections import OrderedDict

from mBase import keywords
from mBase import exception


# noinspection PyStatementEffect
class SimpleDatabase():
    def __init__(self, createstr):
        self._s = createstr

    def _createTable(self, dbName, tableName, tableArgs):
        tableArgs = re.split(r'[,]+', tableArgs[1:-1])
        with open(dbName, "a") as f:
            if os.path.isfile(dbName):
                f.write("table:" + tableName + "\n")
                f.write("lenArgs:" + str(len(tableArgs)) + "\n")
                for i in tableArgs:
                    f.write(i + "\n")

    def create(self):
        """create db database with table test of name"""
        file = None
        s = "CREATE DB IF NOT EXISTS database WITH TABLE test(id:AUTO,name:STRING,title:STRING)"
        # regex je tako imenovani lookbehind!!!!

        # CREATE ARGUMENTS
        self._createDB = re.search(r'(?<=\b' + keywords.CREATEDB + r'\s)(\w+)', s)
        self._ifNotExists = re.search(r'(?<=\b' + keywords.CREATEDB + r'\s)' + keywords.IFNOTEXISTS, s)
        self._createExists = re.search(r'(?<=\b' + keywords.IFNOTEXISTS + r'\s)(\w+)', s)
        self._table = re.search(r'(?<=\b' + keywords.TABLE + r'\s)(\w+)', s)
        self._tableArgs = re.search(r'\(([^\)]+)\)', s).group()


        # TYPES
        self._anyType = re.search(r'(?<=\b' + keywords.ANY + r'\s)(\w+)', s)
        self._timeType = re.search(r'(?<=\b' + keywords.TIME + r'\s)(\w+)', s)
        self._integerType = re.search(r'(?<=\b' + keywords.NUMBER + r'\s)(\w+)', s)
        self._stringType = re.search(r'(?<=\b' + keywords.STRING + r'\s)(\w+)', s)
        self._withType = re.search(r'(?<=\b' + keywords.WITH + r'\s)(\w+)', s)

        if not self._fileExists(self._createExists.group() + ".txt"):
            if self._createDB and self._ifNotExists:
                file = self._createExists.group()
            else:
                file = self._createDB.group()

            if self._withType:
                if self._table:
                    tableName = self._table.group()

            self.dbName = file + ".txt"

            if self._withType.group() == keywords.TABLE:
                self._createTable(self.dbName, tableName, self._tableArgs)

        else:
            raise exception.DatabaseExistsError()

        self.insert(self.dbName, argument=("id", 3, "af"))

    def insert(self, tablename, argument=None):
        """ 1 - vrstica je vedno table
            2 - vrstica je vedno stevilo argumentov"""
        d = self._getargdict()
        k = 0
        dictlen = len(self._getargdict())

        if not self._fileExists(self.dbName):
            raise exception.DatabaseNotExistsError()

        if len(argument) != dictlen:
            raise Exception('MISSING ARGUMENTS FOR COLUMNS IN TABLE - columns ' + str(self._getargtuple()))

        if argument is None:
            raise exception.MissingArgumentError()

        for i in self._getargdict():
            if d.get(i) == keywords.STRING and self._isstr(argument[k]):
                print(argument[k])
            elif d.get(i) == keywords.STRING and not self._isstr(argument[k]):
                raise Exception(
                    'ARGUMENT -> %s <- AND TABLE PROPERTY OF -> %s <- DO NOT MATCH!' % (argument[k], d.get(i)))
            else:
                with open(self.dbName, "a") as f:
                    f.write(i+"-"+argument[k])
            k += 1

    def _fileExists(self, filename):
        return os.path.isfile(filename)

    def _isstr(self, argument):
        return type(argument) is str

    def _istime(self, argument):
        return type(argument) is datetime.datetime

    def _isint(self, argument):
        return type(argument) is int

    def _isauto(self, argument):
        return type(argument) is int

    def _getargdict(self):
        args = re.split(r'[,:]+', self._tableArgs[1:-1])
        a = iter(args)
        return OrderedDict(zip(a, a))

    def _getargtuple(self):
        s = self._getargdict()
        return tuple(x for x in s)
