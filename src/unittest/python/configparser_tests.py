'''
Created on 29.07.2013

@author: mhoyer
'''
import unittest
from configparser import ConfigParser


class configparser_test(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(configparser_test, self).__init__(*args, **kwargs)
        self.app_config = ConfigParser("/tmp/applications.yaml")

    def test_yaml_file_parsing(self):
        self.assertEqual(self.app_config.get("applications"), None)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()