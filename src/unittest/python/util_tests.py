'''
Created on 29.07.2013

@author: mhoyer
'''
import unittest
import util

class configparser_test(unittest.TestCase):

    def test_path_append(self):
        self.assertEqual(util.path_append(['a','b']),"/a/b")
        self.assertEqual(util.path_append(['/a','/b']),"/a/b")
        self.assertEqual(util.path_append(['/a/','/b']),"/a/b")
        self.assertEqual(util.path_append(['/a/','/b/']),"/a/b")
        self.assertEqual(util.path_append(['/var/spool/','/testfile.txt']),"/var/spool/testfile.txt")
        self.assertEqual(util.path_append(['/tmp/replicator/backups','testsite1','.tar.gz']),"/tmp/replicator/backups/testsite1.tar.gz")
        
    def test_get_folder_from_path(self):
        self.assertEqual(util.get_folder_from_path("/var/log/mail.log"), "/var/log")
        
    def test_get_filename_from_path(self):
        self.assertEqual(util.get_filename_from_path("/var/log/mail.log"), "mail.log")
        self.assertEqual(util.get_filename_from_path("/var/log/mail"), "mail")
        self.assertEqual(util.get_filename_from_path("/var/log/mail/"), "")
