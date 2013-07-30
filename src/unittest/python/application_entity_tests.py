'''
Created on 30.07.2013

@author: mhoyer
'''
import unittest
from application import Application

class application_entity_test(unittest.TestCase):

    def test_object_creation(self):
        testdata = {'files': ['/etc/apache2/sites/available/testsite1'], 'folders': ['/var/www/testsite1/'], 'name': 'testsite1', 'url': 'http://www.testsite1.web', 'master_node': 'www1', 'databases': ['testsite1'], 'slave_node': 'www2', 'packages': ['apache2', 'mysql', 'php5']}
        app = Application(testdata)
        self.assertEqual(app.databases, ['testsite1'])
        self.assertEqual(app.files, ['/etc/apache2/sites/available/testsite1'])
        self.assertEqual(app.folders, ['/var/www/testsite1/'])
        self.assertEqual(app.name, 'testsite1')
        self.assertEqual(app.url, 'http://www.testsite1.web')
        self.assertEqual(app.master_node, 'www1')
        self.assertEqual(app.slave_node, 'www2')
        self.assertEqual(app.packages, ['apache2', 'mysql', 'php5'])