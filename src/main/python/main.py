
#!/usr/bin/python

from system import System
from config import Config
from mysqldb import MysqlDB
from actionmanager import Actionmanager
from entities import Application

class Main():
	
	if __name__=="__main__":
		config = Config()
		app_config = config.get_config_list()
		system = System(app_config)
		db = MysqlDB(app_config)
		am = Actionmanager(app_config)
		for element in config.get_applications_list():
			app = Application(element)
			am.replicate(app)
