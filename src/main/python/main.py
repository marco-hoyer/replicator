
#!/usr/bin/python

from system import System
from mysqldb import MysqlDB
from configparser import ConfigParser

class Replicator():

	system = System()
	mysqldb = MysqlDB()
	config = ConfigParser()

	if __name__=="__main__":
		print config.get_applications()		
		print "executing ls"
		print system.execute('ls','-al')
		print "executing mysql "
		print mysqldb.dump_database('test','/tmp')
