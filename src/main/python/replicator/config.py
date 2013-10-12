'''
Created on 29.07.2013

@author: mhoyer
'''

from yamlparser import YamlParser
import logging

class Config():

    def __init__(self, config_path, applications_list_path):
        self.logger = logging.getLogger(__name__) 
        self.logger.info("loading configuration")
        apps_parser = YamlParser(applications_list_path)
        self.applications = apps_parser.get("applications")
        config_parser = YamlParser(config_path)
        self.config = config_parser.get("config")
    
    def get_applications_list(self):
        return self.applications
    
    def get_config_list(self):
        return self.config