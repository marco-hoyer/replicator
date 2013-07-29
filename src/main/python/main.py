
#!/usr/bin/python

from system import System
from config import Config
from mysqldb import MysqlDB
from actionmanager import Actionmanager

class Main():
	
	if __name__=="__main__":
		config = Config()
		app_config = config.get_config_list()
		system = System(app_config)
		db = MysqlDB(app_config)
		am = Actionmanager(app_config)
		#db.dump_database("test", "/tmp/test.sql")
		am.replicate_database("testdb", "testhost")
