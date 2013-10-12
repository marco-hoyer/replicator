import unittest

from mysqldb import MysqlDB
from config import Config

class mysqldb_test (unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(mysqldb_test, self).__init__(*args, **kwargs)
        self.config = Config("../../main/python/replicator/config.yaml","../../main/python/replicator/applications.yaml")
        self.db = MysqlDB(self.config)
    
    def test_get_database(self):
        self.assertEqual(self.db.get_databases(), None)
            
    def test_dump_database(self):
        self.assertEqual(self.db.dump_database("mysql","/tmp/mysql.sql"), None)
        
    def test_dump_databases(self):
        self.assertEqual(self.db.dump_databases("/tmp"), None)