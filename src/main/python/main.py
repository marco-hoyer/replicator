
#!/usr/bin/python

from system import System
from config import Config
from actionmanager import Actionmanager
from entities import Application
from filesystem import Filesystem

class Main():
	
	if __name__=="__main__":
		# init needed modules
		config = Config()
		app_config = config.get_config_list()
		system = System(app_config)
		fs = Filesystem(app_config)
		am = Actionmanager(app_config)
		
		# prepare local system by cleaning temp f.e.
		fs.prepare_local_temp()
		
		# iterate over apps and do the job
		for element in config.get_applications_list():
			app = Application(element)
			am.replicate(app)
