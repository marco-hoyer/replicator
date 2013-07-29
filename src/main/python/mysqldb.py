#!/usr/bin/python

from system import System

class MysqlDB():

	def __init__(self, config):
		self.system = System(config)
		self.mysqlcmd = config["mysql_binary_path"]
		self.global_params = ['--defaults-extra-file=%s' % config["mysql_config_file"]]

	def dump_database(self, dbname, target_file):
		params = ['--databases', '--databases', '--single-transaction', dbname, " > %s" % target_file]
		self.system.execute(self.mysqlcmd, self.global_params + params)

	def get_databases(self):
		return None
	def dump_databases(self, target_dir):
		return None
	def restore_database_on_targethost(self, source_file, targethost):
		return None