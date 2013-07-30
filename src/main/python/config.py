'''
Created on 29.07.2013

@author: mhoyer
'''

from yamlparser import YamlParser

class Config():

    def __init__(self):
        apps_parser = YamlParser("/tmp/applications.yaml")
        self.applications = apps_parser.get("applications")
        config_parser = YamlParser("/tmp/config.yaml")
        self.config = config_parser.get("config")
    
    def get_applications_list(self):
        return self.applications
    
    def get_config_list(self):
        return self.config