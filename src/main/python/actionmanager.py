'''
Created on 29.07.2013

@author: mhoyer
'''
from mysqldb import MysqlDB
from system import System
from entities import Application

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
        if isinstance(app, Application):
            for db in app.databases:
                print "replicating %s" % db
                self.db.replicate_database(db, app.slave_node)
            for afile in app.files:
                print "replicating %s" % afile
                self.system.transfer_single_file(afile, afile, app.slave_node)
            for folder in app.folders:
                print "replicating %s" % folder
                self.system.transfer_folder(folder, folder, app.slave_node)
                
