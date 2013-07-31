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
        self.assertEqual(self.app_config.get("applications"), {'files': ['/etc/apache2/sites/available/testsite1'], 'folders': ['/var/www/testsite1/'], 'name': 'testsite1', 'url': 'http://www.testsite1.web', 'needed_services': ['apache2'], 'master_node': 'www1', 'databases': ['testsite1'], 'slave_node': 'www2', 'packages': ['apache2', 'mysql', 'php5']})
