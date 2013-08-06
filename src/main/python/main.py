
#!/usr/bin/python

from local_system import LocalSystem
from config import Config
from actionmanager import Actionmanager
from entities import Application

class Main():
	
	if __name__=="__main__":
		# init needed modules
		config = Config()
		app_config = config.get_config_list()
		localsystem = LocalSystem(app_config)
		am = Actionmanager(app_config)
		
		# prepare local system by cleaning temp f.e.
		localsystem.prepare_temp()
		
		# iterate over apps and do the job
		for element in config.get_applications_list():
			app = Application(element)
			am.replicate(app)
