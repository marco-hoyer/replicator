#!/usr/bin/python

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class YamlParser():

    def __init__(self, filepath):
        stream = open(filepath, 'r')
        self.data = load(stream, Loader=Loader)

    def get(self, head):
	print self.data[head]
        return self.data[head]


#output = dump(data, Dumper=Dumper)
