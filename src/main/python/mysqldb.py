#!/usr/bin/python

from system import System

class MysqlDB():

	def __init__(self):
		self.system = System()
		self.mysqlcmd = "/usr/bin/mysqldump"
		self.global_params = ['--defaults-extra-file=/etc/mysql/debian.cnf', '--single-transaction', '--databases', '--add-drop-database']

	def dump_database(self, dbname, target_file):
		
		return None
		#print self.global_params
		#print self.mysqlcmd
		#print self.system.execute(self.mysqlcmd, self.global_params)

	def get_databases(self):
		return None
	def dump_databases(self, target_dir):
		return None
	def restore_database(self, source_file):
		return None
