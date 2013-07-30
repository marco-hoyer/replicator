'''
Created on 29.07.2013

@author: mhoyer
'''
import unittest
from yamlparser import YamlParser

class configparser_test(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(configparser_test, self).__init__(*args, **kwargs)
        # must be ../../../res/applications.yaml if running inside eclipse
        self.app_config = YamlParser("res/applications.yaml")
        

    def test_yaml_file_parsing(self):
        self.assertEqual(self.app_config.get("applications"), None)
