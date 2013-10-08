from local_system import LocalSystem
from remote_system import RemoteSystem
import logging

class MysqlDB():

	def __init__(self, config):
		self.init_logger()
		if config:
			self.localsystem = LocalSystem(config)
			self.remotesystem = RemoteSystem(config)
			self.mysqlcmd = config["mysql_binary_path"]
			self.mysqldumpcmd = config["mysqldump_binary_path"]
			self.global_params = ['--defaults-extra-file=%s' % config["mysql_config_file"]]
			self.temp_path = config["temp_path"]
		else:
			self.localsystem = LocalSystem(None)
			self.remotesystem = RemoteSystem(None)
			self.mysqlcmd = "/usr/bin/mysql"
			self.mysqldumpcmd = "/usr/bin/mysqldump"
			self.global_params = ['--defaults-extra-file=/etc/mysql/debian.cnf']
			self.temp_path = "/tmp/replicator"
			

	def init_logger(self):
		logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)
		self.logger = logging.getLogger('Replicator') 

	def dump_database(self, dbname, target_file):
		params = ['--single-transaction', '--databases', '--add-drop-database', dbname]
		self.localsystem.write_file(target_file, self.localsystem.execute(self.mysqldumpcmd, self.global_params + params))

	def get_databases(self):
		return None
	
	def dump_databases(self, target_dir):
		return None
	
	def restore_database_on_targethost(self, source_file, targethost):
		self.remotesystem.execute(targethost, "%s %s < %s" % (self.mysqlcmd, self.global_params[0], source_file))
	
	def replicate_database(self, dbname, targethost):
		# dumpfile is put in temp with its name being the same as the db name
		dumpfile = "%s/%s.sql" % (self.temp_path,dbname)
		# create mysql dump
		self.dump_database(dbname, dumpfile)
		# transfer dump to target system
		self.remotesystem.transfer_single_file(targethost, dumpfile, self.temp_path)
		# trigger remote db restore
		self.restore_database_on_targethost(dumpfile, targethost)

		self.remotesystem.transfer_single_file(targethost, dumpfile, self.temp_path)
		# trigger remote db restore
		self.restore_database_on_targethost(dumpfile, targethost)
