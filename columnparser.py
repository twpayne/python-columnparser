#!/usr/bin/python

from collections import defaultdict
import re


INT_RE = re.compile(r'\A-?\d+\Z')
FLOAT_RE = re.compile(r'\A-?\d+(?:\.\d*)?\Z')


def guess_type(s):
    if INT_RE.match(s):
        return int
    elif FLOAT_RE.match(s):
        return float
    else:
        return str


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

    @classmethod
    def autoparse_file(self, io):
        lines = iter(io)
        parser = self(lines.next())
        rows = map(parser.parse, lines)
        types = defaultdict(set)
        for row in rows:
            for key, value in row.items():
                types[key].add(guess_type(value))
        dict_mapper = DictMapper()
        for key in parser.keys():
            for type in (str, float, int):
                if type in types[key]:
                    dict_mapper[key] = type
                    break
        for row in rows:
            yield dict_mapper(row)


class DictMapper(dict):

    def __call__(self, d, copy=False):
        if copy:
            d = d.copy()
        for key, function in self.items():
            if key in d:
                d[key] = function(d[key])
        return d


if __name__ == '__main__':
    import sys
    print repr(list(ColumnParser.autoparse_file(sys.stdin)))
