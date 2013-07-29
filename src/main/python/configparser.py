#!/usr/bin/python

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class ConfigParser():

    def __init__(self):
        applications_config_stream = open("/tmp/applications.yaml", 'r')
        self.applications_config_data = load(applications_config_stream, Loader=Loader)

    def get_applications(self):
        return self.applications_config_data["applications"]


#output = dump(data, Dumper=Dumper)
