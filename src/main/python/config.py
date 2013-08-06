'''
Created on 29.07.2013

@author: mhoyer
'''

from yamlparser import YamlParser
import logging

class Config():

    def __init__(self):
        self.init_logger()
        self.logger.info("loading configuration")
        apps_parser = YamlParser("../../../res/applications.yaml")
        self.applications = apps_parser.get("applications")
        config_parser = YamlParser("../../../res/config.yaml")
        self.config = config_parser.get("config")
    
    def init_logger(self):
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)
        self.logger = logging.getLogger('Replicator') 
    
    def get_applications_list(self):
        return self.applications
    
    def get_config_list(self):
        return self.config