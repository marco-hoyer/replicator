#!/usr/bin/python

from system import System
from filesystem import Filesystem

class MysqlDB():

	def __init__(self, config):
		if config:
			self.system = System(config)
			self.fs = Filesystem(config)
			self.mysqlcmd = config["mysql_binary_path"]
			self.mysqldumpcmd = config["mysqldump_binary_path"]
			self.global_params = ['--defaults-extra-file=%s' % config["mysql_config_file"]]
		else:
			self.system = System(None)
			self.fs = Filesystem(None)
			self.mysqlcmd = "/usr/bin/mysql"
			self.mysqldumpcmd = "/usr/bin/mysqldump"
			self.global_params = ['--defaults-extra-file=/etc/mysql/debian.cnf']

	def dump_database(self, dbname, target_file):
		params = ['--single-transaction', '--databases', '--add-drop-database', dbname]
		self.fs.write_file(target_file, self.system.execute(self.mysqldumpcmd, self.global_params + params))

	def get_databases(self):
		return None
	
	def dump_databases(self, target_dir):
		return None
	
	def restore_database_on_targethost(self, source_file, targethost):
		return None
