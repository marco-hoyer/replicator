
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
	
	def init_logger(self, log_level):
		logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)
		self.logger = logging.getLogger('Replicator')
		self.logger.setLevel(log_level)
	
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
	
	def main(self, args):
		replicator = Replicator()
		
		if args.debug:
			replicator.init_logger(logging.DEBUG)
		else:
			replicator.init_logger(logging.INFO)
		
		if args.replicate:
			replicator.logger.info("Starting replication of applications")
			replicator.replicate_applications()
		elif not args.backup:
			replicator.logger.info("Starting backup of applications")
			replicator.backup_applications()
		else:
			print "nothing to do"
			sys.exit(1)

	
if __name__ == '__main__':
	replicator = Replicator()
	# parameter handling
	parser = argparse.ArgumentParser(description='Instruments backup and replication of applications configured in a yaml config file')
	parser.add_argument("--debug", help="show debug output", action="store_true")
	parser.add_argument("--replicate", help="replicate applications", action="store_true")
	parser.add_argument("--backup", help="backup applications", action="store_true")
	# parser.add_argument("applications-list", help="hostname", type=str)
	# parser.add_argument("config", help="port",type=str)
	args = parser.parse_args()
	replicator.main(args)

