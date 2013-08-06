'''
Created on 29.07.2013

@author: mhoyer
'''
from mysqldb import MysqlDB
from local_system import LocalSystem
from remote_system import RemoteSystem
from entities import Application

class Actionmanager():
    '''
    classdocs
    '''

    def __init__(self, config):
        if config:
            self.db = MysqlDB(config)
            self.system = LocalSystem(config)
            self.remotesystem = RemoteSystem(config)
        else:
            print "error initializing actionmanager"
    
    def replicate(self, app):
        # prepare replicator temp folder for the target node
        self.remotesystem.prepare_temp(app.slave_node)
        if isinstance(app, Application):
            for database in app.databases:
                print "- replicating %s" % database
                self.db.replicate_database(database, app.slave_node)
            for afile in app.files:
                print "- replicating %s" % afile
                self.remotesystem.transfer_single_file(app.slave_node, afile, afile)
            for folder in app.folders:
                print "- replicating %s" % folder
                self.remotesystem.transfer_folder(app.slave_node, folder, folder)
            self.remotesystem.install(app.slave_node, app.packages)
                
