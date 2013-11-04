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

    def replicate_all(self):
        for element in self.app_config:
            app = Application(element)
            if app.slave_node:
                self.logger.info("replicating %s" % app.name)
                self.replicate(app)
        self.logger.info("Replication completed successfully")
        
    def replicate_single(self, app_name):
        app = None
        # iterate over app config and load app object if there is a matching name
        for item in self.app_config:
            if item["name"] == app_name:
                app = Application(item)
                
        if app:
            if app.slave_node:
                self.replicate(app)
            else:
                self.logger.warning("Application has no slave node configured")
                raise Exception("Configuration Error")
        else:
            self.logger.error("No application configured with name: " + app_name)
            raise Exception("Configuration Error")
        self.logger.info("Replication completed successfully")
        
    def backup_all(self):
        for element in self.app_config:
            app = Application(element)
            self.logger.info("saving %s" % app.name)
            self.backup(app)
        self.logger.info("Backup completed successfully")
        
    def backup_single(self, app_name):
        app = None
        # iterate over app config and load app object if there is a matching name
        for item in self.app_config:
            if item["name"] == app_name:
                app = Application(item)
        if app:
            self.backup(app)
        else:
            self.logger.error("No application configured with name: " + app_name)
            raise Exception("Configuration Error")
        self.logger.info("Backup completed successfully")

    def replicate(self, app):
        try:
            # prepare replicator temp folder for the target node
            self.system.prepare_application_dirs()
            self.remotesystem.prepare_application_dirs(app.slave_node)
            if app.packages:
                self.logger.debug("ensuring packages installed: %s" % ', '.join(app.packages))
                self.remotesystem.install(app.slave_node, app.packages)
            if app.databases:
                for database in app.databases:
                    self.logger.debug("replicating database: %s" % database)
                    self.db.replicate_database(database, app.slave_node)
            if app.files:
                for afile in app.files:
                    self.logger.debug("replicating file: %s" % afile)
                    self.remotesystem.transfer_single_file(app.slave_node, afile, afile)
            if app.folders:
                for afolder in app.folders:
                    self.logger.debug("replicating folder: %s" % afolder)
                    self.remotesystem.transfer_folder(app.slave_node, afolder, afolder)
            # reload needed services
            if app.needed_services:
                for service in app.needed_services:
                    self.logger.debug("reloading service %s on %s" % (service,app.slave_node))
                    self.remotesystem.reload_service(app.slave_node, service)
            self.remotesystem.prepare_application_dirs(app.slave_node)
            # test availability
            if app.url:
                return self.remotesystem.test_availability(app.slave_node, 80, app.url)
        except Exception as e:
            self.logger.error("Stopping after error: " + str(e))
            raise Exception("Error replicating " + app.name) 
        
    def backup(self, app):
        # define path
        app_temp_path = util.path_append([self.system.temp_path,app.name])
        db_temp_path = util.path_append([app_temp_path,"databases"])
        file_temp_path = util.path_append([app_temp_path,"files"])
            
        # clear and prepare temp directories
        self.system.prepare_application_dirs()
        self.system.clear_folder(app_temp_path)
        self.system.clear_folder(db_temp_path)
        self.system.clear_folder(file_temp_path)
        
        try:
            # backup all components of the application
            if app.databases:
                for database in app.databases:
                    self.logger.debug("saving database: %s" % database)
                    self.db.dump_database(database, util.path_append([db_temp_path ,database + ".sql"]))
            if app.files:
                for afile in app.files:
                    self.logger.debug("saving file: %s" % afile)
                    self.system.mkdir(util.get_folder_from_path( util.path_append([file_temp_path, afile]) ), True)
                    self.system.cp(afile, util.path_append([file_temp_path, afile]), False)
            if app.folders:
                for folder in app.folders:
                    self.logger.debug("saving folder: %s" % folder)
                    self.system.mkdir(util.path_append([file_temp_path, folder]), True)
                    self.system.cp(folder, util.path_append([file_temp_path, folder]), True)

                # write package list
                self.system.write_package_list(util.path_append([app_temp_path, "package_list.txt"]))
            
                # save compressed backup of application data
                backup_file = util.path_append([self.system.backup_path, app.name + "_" + util.get_timestamp(), ".tar.gz"])
                self.logger.debug("Saving compressed backup to: %s" % backup_file)
                self.system.compress(app_temp_path, backup_file)
                self.system.rm(app_temp_path, True)
        except Exception as e:
            self.logger.error("Stopping after error: " + str(e))
            raise Exception("Error saving " + app.name) 