import unittest

from local_system import LocalSystem

class system_test (unittest.TestCase):
	
	def __init__(self, *args, **kwargs):
		super(system_test, self).__init__(*args, **kwargs)
		self.system = LocalSystem(None)

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
		self.assertEqual(self.system.test_availability("127.0.0.1",80), 'testsite1.web')

	def test_fileops(self):
		self.assertEqual(self.fs.touch("/tmp/testfile"), None)
		self.assertEqual(self.fs.mv("/tmp/testfile","/tmp/movedtestfile"), None)
		self.assertEqual(self.fs.cp("/tmp/movedtestfile","/tmp/testfile"), None)
		self.assertEqual(self.fs.rm("/tmp/testfile", False), None)
		self.assertEqual(self.fs.rm("/tmp/movedtestfile", False), None)
		
	def test_write_file(self):
		self.assertEqual(self.fs.write_file("/tmp/testfile.txt", "Hallo Welt"), None)
		self.assertEqual(self.fs.read_file("/tmp/testfile.txt"), "Hallo Welt")
		self.fs.rm("/tmp/testfile.txt", False)