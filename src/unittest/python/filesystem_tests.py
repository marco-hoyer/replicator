import unittest

from filesystem import Filesystem

class syshelper_test (unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(syshelper_test, self).__init__(*args, **kwargs)
        self.fs = Filesystem(None)

    def test_fileops(self):
        self.assertEqual(self.fs.touch("/tmp/testfile"), None)
        self.assertEqual(self.fs.mv("/tmp/testfile","/tmp/movedtestfile"), None)
        self.assertEqual(self.fs.cp("/tmp/movedtestfile","/tmp/testfile"), None)
        self.assertEqual(self.fs.rm("/tmp/testfile", False), None)
        self.assertEqual(self.fs.rm("/tmp/movedtestfile", False), None)