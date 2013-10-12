from local_system import LocalSystem
from remote_system import RemoteSystem
import logging
import util

class MysqlDB():

	def __init__(self, config):
		self.logger = logging.getLogger(__name__)
		self.config = config.get_config_list()
		self.localsystem = LocalSystem(config)
		self.remotesystem = RemoteSystem(config)
		self.mysqlcmd = self.config["mysql_binary_path"]
		self.mysqldumpcmd = self.config["mysqldump_binary_path"]
		self.global_params = ['--defaults-extra-file=%s' % self.config["mysql_config_file"]]
		self.temp_path = self.config["temp_path"]

	def dump_database(self, dbname, target_file):
		params = ['--single-transaction', '--databases', '--add-drop-database', dbname]
		try:
			self.localsystem.execute_with_file_output(self.mysqldumpcmd, self.global_params + params, target_file)
		except Exception as e:
			self.logger.error("Could not dump database " + dbname + ": " + str(e))
			raise Exception()

	def get_databases(self):
		return None
	
	def dump_databases(self, target_dir):
		return None
	
	def restore_database_on_targethost(self, source_file, targethost):
		self.remotesystem.execute(targethost, "%s %s < %s" % (self.mysqlcmd, self.global_params[0], source_file))
	
	def replicate_database(self, dbname, targethost):
		# dumpfile is put in temp with its name being the same as the db name
		dumpfile = util.path_append([self.temp_path, dbname, ".sql"])
		try:
			# create mysql dump
			self.dump_database(dbname, dumpfile)
			# transfer dump to target system
			self.remotesystem.transfer_single_file(targethost, dumpfile, self.temp_path)
			# trigger remote db restore
			self.restore_database_on_targethost(dumpfile, targethost)

			self.remotesystem.transfer_single_file(targethost, dumpfile, self.temp_path)
			# trigger remote db restore
			self.restore_database_on_targethost(dumpfile, targethost)
		except Exception as e:
			self.logger.error("Could not replicate database " + dbname + ": " + str(e))
			raise Exception()