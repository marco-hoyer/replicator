'''
Created on 29.07.2013

@author: mhoyer
'''
from mysqldb import MysqlDB
from local_system import LocalSystem
from remote_system import RemoteSystem
from entities import Application
import logging
import util

class Actionmanager():
    '''
    classdocs
    '''

    def __init__(self, config):
        self.init_logger()
        if config:
            self.db = MysqlDB(config)
            self.system = LocalSystem(config)
            self.remotesystem = RemoteSystem(config)

    def init_logger(self):
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)
        self.logger = logging.getLogger('Replicator')   

    def replicate(self, app):
        if isinstance(app, Application):
            # prepare replicator temp folder for the target node
            self.remotesystem.prepare_temp(app.slave_node)
            for database in app.databases:
                self.logger.debug("replicating database: %s" % database)
                self.db.replicate_database(database, app.slave_node)
            for afile in app.files:
                self.logger.debug("replicating file: %s" % afile)
                self.remotesystem.transfer_single_file(app.slave_node, afile, afile)
            for afolder in app.folders:
                self.logger.debug("replicating folder: %s" % afolder)
                self.remotesystem.transfer_folder(app.slave_node, afolder, afolder)
            # ensure installation of needed packages
            #self.logger.debug("- installing packages: %s" % ', '.join(app.packages))
            #self.remotesystem.install(app.slave_node, app.packages)
            # reload needed services
            for service in app.needed_services:
                self.logger.debug("reloading service %s on %s" % (service,app.slave_node))
                self.remotesystem.reload_service(app.slave_node, service)
            # test availability
            return self.remotesystem.test_availability(app.slave_node, 80, app.url)
        else:
            return False
        
    def backup(self, app):
        if isinstance(app, Application):
            # define path
            backup_path = util.path_append([self.system.temp_path,app.name])
            db_backup_path = util.path_append([backup_path,"databases"])
            file_backup_path = util.path_append([backup_path,"files"])
            
            # clear and prepare temp directories
            self.system.clear_folder(backup_path)
            self.system.mkdir(db_backup_path, True)
            self.system.mkdir(file_backup_path, True)
            
            # backup all components of the application
            for database in app.databases:
                self.logger.debug("saving database: %s" % database)
                self.db.dump_database(database, util.path_append([db_backup_path ,database + ".sql"]))
            for afile in app.files:
                self.logger.debug("saving file: %s" % afile)
                self.system.mkdir(util.get_folder_from_path( util.path_append([file_backup_path, afile]) ), True)
                self.system.cp(afile, util.path_append([file_backup_path, afile]), False)
            for folder in app.folders:
                self.logger.debug("saving folder: %s" % folder)
                self.system.mkdir(util.path_append([file_backup_path, folder]), True)
                self.system.cp(folder, util.path_append([file_backup_path, folder]), True)
            
            # save compressed backup of application data
            self.logger.debug("Saving compressed backup to: %s" % self.system.temp_path)
            self.system.compress(backup_path, backup_path + ".tar.gz")
            self.system.clear_folder(backup_path)
            return True
        else:
            return False
            