
#!/usr/bin/python

from local_system import LocalSystem
from config import Config
from actionmanager import Actionmanager
from entities import Application
import logging
import argparse

class Replicator:
	
	def __init__(self):
		# init needed modules
		self.config = Config()
		app_config = self.config.get_config_list()
		self.localsystem = LocalSystem(app_config)
		self.am = Actionmanager(app_config)
	
	def init_logger(self):
		logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)
		self.logger = logging.getLogger('Replicator')
	
	def replicate_applications(self):
		for element in self.config.get_applications_list():
			app = Application(element)
			self.logger.info("replicating %s" % app.name)
			self.am.replicate(app)
	
if __name__=="__main__":
	replicator = Replicator()
	# init logger
	replicator.init_logger()
	# prepare local system by cleaning temp f.e.
	replicator.localsystem.prepare_temp()
	# iterate over apps and do the job
	replicator.replicate_applications()
	

