import unittest

from filesystem import Filesystem

class filesystem_test (unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(filesystem_test, self).__init__(*args, **kwargs)
        self.fs = Filesystem(None)

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