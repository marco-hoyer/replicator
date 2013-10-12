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
        self.logger = logging.getLogger(__name__)
        self.config = config.get_config_list()
        self.app_config = config.get_applications_list()
        
        self.db = MysqlDB(config)
        self.system = LocalSystem(config)
        self.remotesystem = RemoteSystem(config)

    def replicate_applications(self):
        error = False
        for element in self.app_config:
            app = Application(element)
            self.logger.info("replicating %s" % app.name)
            if not self.replicate(app):
                error = True
        if error:
            self.logger.error("There were errors replicating configured applications")
            return False
        else:
            return True
        
    def backup_applications(self):
        error = False
        for element in self.app_config:
            app = Application(element)
            self.logger.info("saving %s" % app.name)
            if not self.backup(app):
                error = True
        if error:
            self.logger.error("There were errors backing up configured applications")
            return False
        else:
            return True

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
            temp_path = util.path_append([self.system.temp_path,app.name])
            db_temp_path = util.path_append([temp_path,"databases"])
            file_temp_path = util.path_append([temp_path,"files"])
            
            # clear and prepare temp directories
            self.system.clear_folder(temp_path)
            self.system.mkdir(db_temp_path, True)
            self.system.mkdir(file_temp_path, True)
            
            # backup all components of the application
            for database in app.databases:
                self.logger.debug("saving database: %s" % database)
                self.db.dump_database(database, util.path_append([db_temp_path ,database + ".sql"]))
            for afile in app.files:
                self.logger.debug("saving file: %s" % afile)
                self.system.mkdir(util.get_folder_from_path( util.path_append([file_temp_path, afile]) ), True)
                self.system.cp(afile, util.path_append([file_temp_path, afile]), False)
            for folder in app.folders:
                self.logger.debug("saving folder: %s" % folder)
                self.system.mkdir(util.path_append([file_temp_path, folder]), True)
                self.system.cp(folder, util.path_append([file_temp_path, folder]), True)

            # write package list
            self.system.write_package_list(util.path_append([temp_path, "package_list.txt"]))
            
            # save compressed backup of application data
            backup_file = util.path_append([self.system.backup_path, app.name, ".tar.gz"])
            self.logger.info("Saving compressed backup to: %s" % backup_file)
            self.system.compress(temp_path, backup_file)
            self.system.rm(temp_path, True)
            return True
        else:
            return False
            