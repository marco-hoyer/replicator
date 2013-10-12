
#!/usr/bin/python

from local_system import LocalSystem
from config import Config
from actionmanager import Actionmanager
import logging
import argparse
import sys

class Replicator:
	
	def init_logger(self, log_level):
		logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S',level=logging.DEBUG)
		self.logger = logging.getLogger(__name__)
		logging.getLogger().setLevel(log_level)
	
	def main(self, args):
		
		replicator = Replicator()
		
		# init logging
		if args.debug:
			replicator.init_logger(logging.DEBUG)
		else:
			replicator.init_logger(logging.INFO)
			
		# init application
		replicator = Replicator()
		config = Config(args.config, args.applicationslist)
		localsystem = LocalSystem(config)
		am = Actionmanager(config)

		# clear temp and ensure existence of needed directories
		localsystem.prepare_application_dirs()
		
		# action management
		if args.replicate:
			logging.getLogger(__name__).info("Starting replication of applications")
			am.replicate_applications()
		elif not args.backup:
			logging.getLogger(__name__).info("Starting backup of applications")
			am.backup_applications()
		else:
			print "nothing to do"
			sys.exit(1)

if __name__ == '__main__':
	replicator = Replicator()
	# parameter handling
	parser = argparse.ArgumentParser(description='Instruments backup and replication of applications configured in a yaml config file')
	parser.add_argument("--debug", help="show debug output", action="store_true", default=False)
	parser.add_argument("--replicate", help="replicate applications", action="store_true")
	parser.add_argument("--backup", help="backup applications", action="store_true")
	parser.add_argument("applicationslist", help="yaml file containing applications definition", type=str, default="applications.yaml")
	parser.add_argument("config", help="yaml file containing global application config",type=str, default="config.yaml")
	args = parser.parse_args()
	replicator.main(args)

