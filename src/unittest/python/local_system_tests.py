import unittest

from local_system import LocalSystem
from config import Config

class system_test (unittest.TestCase):
	
	def __init__(self, *args, **kwargs):
		super(system_test, self).__init__(*args, **kwargs)
		self.config = Config("../../main/python/replicator/config.yaml.example","../../main/python/replicator/applications.yaml.example")
		self.system = LocalSystem(self.config)

	def test_execute_with_single_param(self):
		self.assertEqual(self.system.execute("which",['python']), '/usr/bin/python\n')
		self.assertEqual(self.system.execute("echo",['Hallo Welt']), 'Hallo Welt\n')
		
	def test_execute_with_multiple_params(self):
		self.assertEqual(self.system.execute("echo",['Hallo','Welt','test','1','2','3']), 'Hallo Welt test 1 2 3\n')
		
	def test_execute_with_empty_param(self):
		self.assertEqual(self.system.execute("echo",[]), '\n')
		
	def test_execute_with_string_param(self):
		self.assertEqual(self.system.execute("echo","Hallo Welt"), 'Hallo Welt\n')

	def test_test_availability(self):
		self.assertTrue(self.system.test_availability("www.google.de",80, "http://www.google.de"), "Website should be available but was considered to be down")
		self.assertFalse(self.system.test_availability("www.google.de",546, "http://www.google.de"), "Website shouldn't be considered up")

	def test_fileops(self):
		self.assertEqual(self.system.mkdir("/tmp/replicator-test", True), None)
		self.assertTrue(self.system.directory_exists("/tmp/replicator-test"))
		self.assertEqual(self.system.touch("/tmp/replicator-test/testfile"), None)
		self.assertTrue(self.system.file_exists("/tmp/replicator-test/testfile"))
		self.assertEqual(self.system.mv("/tmp/replicator-test/testfile","/tmp/replicator-test/movedtestfile"), None)
		self.assertFalse(self.system.file_exists("/tmp/replicator-test/testfile"))
		self.assertEqual(self.system.cp("/tmp/replicator-test/movedtestfile","/tmp/replicator-test/testfile", False), None)
		self.assertTrue(self.system.file_exists("/tmp/replicator-test/testfile"))
		self.assertEqual(self.system.rm("/tmp/replicator-test/testfile", False), None)
		self.assertFalse(self.system.file_exists("/tmp/replicator-test/testfile"))
		self.assertEqual(self.system.rm("/tmp/replicator-test/movedtestfile", False), None)
		self.assertEqual(self.system.rm("/tmp/replicator-test", True), None)
		self.assertFalse(self.system.directory_exists("/tmp/replicator-test"))
		
	def test_write_file(self):
		self.assertEqual(self.system.write_file("/tmp/testfile.txt", "Hallo Welt"), None)
		self.assertEqual(self.system.read_file("/tmp/testfile.txt"), "Hallo Welt")
		self.system.rm("/tmp/testfile.txt", False)