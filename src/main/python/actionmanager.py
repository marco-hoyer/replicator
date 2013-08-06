'''
Created on 29.07.2013

@author: mhoyer
'''
from mysqldb import MysqlDB
from local_system import LocalSystem
from remote_system import RemoteSystem
from entities import Application
import logging

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
        # prepare replicator temp folder for the target node
        self.remotesystem.prepare_temp(app.slave_node)
        if isinstance(app, Application):
            for database in app.databases:
                self.logger.debug("- replicating database: %s" % database)
                self.db.replicate_database(database, app.slave_node)
            for afile in app.files:
                self.logger.debug("- replicating file: %s" % afile)
                self.remotesystem.transfer_single_file(app.slave_node, afile, afile)
            for folder in app.folders:
                self.logger.debug("- replicating folder: %s" % folder)
                self.remotesystem.transfer_folder(app.slave_node, folder, folder)
            # ensure installation of needed packages
            self.logger.debug("- installing packages: %s" % ', '.join(app.packages))
            self.remotesystem.install(app.slave_node, app.packages)
            # reload needed services
            for service in app.needed_services:
                self.logger.debug("- reloading service %s on %s" % (service,app.slave_node))
                self.remotesystem.reload_service(app.slave_node, service)
            # test availability
            self.remotesystem.test_availability(app.slave_node, 80, app.url)
                
