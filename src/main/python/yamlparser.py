#!/usr/bin/python

from yaml import load, dump
import logging
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class YamlParser():

    def __init__(self, filepath):
        self.init_logger()
        stream = open(filepath, 'r')
        self.data = load(stream, Loader=Loader)
        
    def init_logger(self):
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)
        self.logger = logging.getLogger('Replicator') 

    def get(self, head):
        self.logger.debug("raw yaml data loaded: \n %s" % self.data[head])
        return self.data[head]


#output = dump(data, Dumper=Dumper)
