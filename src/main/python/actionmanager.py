'''
Created on 29.07.2013

@author: mhoyer
'''
from mysqldb import MysqlDB
from system import System

class Actionmanager():
    '''
    classdocs
    '''

    def __init__(self, config):
        if config:
            self.db = MysqlDB(config)
            self.system = System(config)
        else:
            self.db = MysqlDB(None)
            self.system = System(None)

    
    def replicate(self, app):
        print "Test"
        
    def replicate_database(self, dbname, targethost):
        dumppath = "/tmp/%s.sql" % dbname
        self.db.dump_database(dbname, dumppath)
        self.system.transfer_folder(dumppath, dumppath, targethost)
        self.db.restore_database_on_targethost(dumppath, targethost)