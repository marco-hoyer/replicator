
#!/usr/bin/python

from system import System
from config import Config

class Main():
	
	if __name__=="__main__":
		config = Config()
		system = System()
		app_config = config.get_config_list()
		print app_config
