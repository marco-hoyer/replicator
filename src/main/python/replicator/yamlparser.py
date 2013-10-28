#!/usr/bin/python

from yaml import load, dump
import logging
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class YamlParser():

    def __init__(self, filepath):
        self.logger = logging.getLogger(__name__) 
        try:
            stream = open(filepath, 'r')
            self.data = load(stream, Loader=Loader)
        except Exception as e:
            self.logger.error("Error reading yaml file: " + str(e))
            raise Exception("Config error")


    def get(self, head):
        self.logger.debug("raw yaml data loaded: \n %s" % self.data[head])
        return self.data[head]


#output = dump(data, Dumper=Dumper)
