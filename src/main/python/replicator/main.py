
#!/usr/bin/python

from local_system import LocalSystem
from config import Config
from actionmanager import Actionmanager
from entities import Application
import logging
import argparse
import sys

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
		error = False
		for element in self.config.get_applications_list():
			app = Application(element)
			self.logger.info("replicating %s" % app.name)
			if not self.am.replicate(app):
				error = True
			self.logger.info("saving %s" % app.name)
			if not self.am.backup(app):
				error = True
		if error:
			self.logger.error("There were errors replicating configured applications")
			return False
		else:
			return True
		
	def backup_applications(self):
		error = False
		for element in self.config.get_applications_list():
			app = Application(element)
			self.logger.info("saving %s" % app.name)
			if not self.am.backup(app):
				error = True
		if error:
			self.logger.error("There were errors backing up configured applications")
			return False
		else:
			return True
				
	
if __name__=="__main__":
	replicator = Replicator()
	# init logger
	replicator.init_logger()
	# prepare local system by cleaning temp f.e.
	replicator.localsystem.prepare_temp()
	# iterate over apps and do the job
	if replicator.backup_applications():
		replicator.logger.info("Terminating successfully")
		sys.exit(0)
	else:
		replicator.logger.info("Terminating with errors")
		sys.exit(1)
	

