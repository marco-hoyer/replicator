
#!/usr/bin/python

from syshelper import System
from mysqldb import MysqlDB

class Replicator():

	system = System()
	mysqldb = MysqlDB()

	if __name__=="__main__":		
		print "executing ls"
		print system.execute('ls','-al')
		print "executing mysql "
		print mysqldb.dump_database('test','/tmp')
