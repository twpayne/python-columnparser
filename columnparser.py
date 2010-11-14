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

    def keys(self):
        return self.columns.keys()

    def parse(self, line):
        result = {}
        for key, (start, end) in self.columns.items():
            result[key] = line[start:end].rstrip()
        return result

    @classmethod
    def parse_file(self, io):
        lines = iter(io)
        parser = self(lines.next())
        for line in lines:
            yield parser.parse(line)


if __name__ == '__main__':
    import sys
    for row in ColumnParser.parse_file(sys.stdin):
        print repr(row)
