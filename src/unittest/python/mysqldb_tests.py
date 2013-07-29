import unittest

from mysqldb import MysqlDB

class mysqldb_test (unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(mysqldb_test, self).__init__(*args, **kwargs)
        self.db = MysqlDB()
    
    def test_get_database(self):
        self.assertEqual(self.db.get_databases(), None)
            
    def test_dump_database(self):
        self.assertEqual(self.db.dump_database("testdb","/tmp"), None)
        
    def test_dump_databases(self):
        self.assertEqual(self.db.dump_databases("/tmp"), None)
    
    def test_restore_database(self):
        self.assertEqual(self.db.restore_database("/tmp/testdb.sql"), None)
            
