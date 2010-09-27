#!/usr/bin/python

import re

class ColumnParser(object):

    def __init__(self, header):
        self.columns = {}
        index = 0
        for m in re.finditer(r' (?=\S)', header):
            self.columns[header[index:m.start()].rstrip()] = (index, m.start())
            index = m.start() + 1
        self.columns[header[index:].rstrip()] = (index, None)

    def parse(self, line):
        result = {}
        for key, (start, end) in self.columns.items():
            result[key] = line[start:end].rstrip()
        return result
