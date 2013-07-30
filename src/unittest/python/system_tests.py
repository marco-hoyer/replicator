import unittest

from system import System

class system_test (unittest.TestCase):
	
	def __init__(self, *args, **kwargs):
		super(system_test, self).__init__(*args, **kwargs)
		self.system = System(None)

	def test_execute_with_single_param(self):
		self.assertEqual(self.system.execute("which",['python']), '/usr/bin/python\n')
		self.assertEqual(self.system.execute("echo",['Hallo Welt']), 'Hallo Welt\n')
		
	def test_execute_with_multiple_params(self):
		self.assertEqual(self.system.execute("echo",['Hallo','Welt','test','1','2','3']), 'Hallo Welt test 1 2 3\n')
		
	def test_execute_with_empty_param(self):
		self.assertEqual(self.system.execute("echo",[]), '\n')
		self.assertEqual(self.system.execute("pwd",[]), '\n')
		
	def test_execute_with_string_param(self):
		self.assertEqual(self.system.execute("echo","Hallo Welt"), 'Hallo Welt\n')