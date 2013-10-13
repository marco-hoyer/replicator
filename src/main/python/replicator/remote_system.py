from local_system import LocalSystem
import subprocess
import pycurl
import logging
import StringIO
import util

class RemoteSystem():
    
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config.get_config_list()
        self.localsystem = LocalSystem(config)
        self.remote_user = self.config["remote_user"]
        self.temp_path =self. config["temp_path"]
    
    def execute(self, targethost, command):
        params = ['%s@%s' % (self.remote_user,targethost),command]
        self.logger.debug("executing on " + targethost + " - " + " ".join(params) )
        self.localsystem.execute("ssh", params)
        
    def execute_with_success_status(self, targethost, command):
        try:
            self.execute(targethost, command)
        except Exception as e:
            print str(e)
            return False
        return True
        
    def reload_service(self, targethost, service):
        self.execute(targethost, "/etc/init.d/%s reload" % service)
    
    def transfer_single_file(self, targethost, source, destination):
        #params = [source,"%s@%s:%s" % (self.remote_user, targethost, destination)]
        #self.localsystem.execute("scp", params)
        self.transfer_folder(targethost, source, destination)
    
    def transfer_folder(self, targethost, source, destination):
        params = ['--compress', '--recursive', '--perms', '--owner', '--group', '--times', '--links', '--delete' ,source,"%s@%s:%s" % (self.remote_user, targethost, destination)]
        self.localsystem.execute("rsync", params)
        
    def install(self, targethost, packages):
        self.execute(targethost, "aptitude update")    
        self.execute(targethost, "aptitude install -y --quiet %s" % ' '.join(packages) )
            
    def rm(self, targethost, path, recursive):
        if recursive:
            self.execute(targethost, "rm -rf " + path)
        else:
            self.execute(targethost, "rm " + path)

    def mkdir(self, targethost, path, recursive):
        if recursive:
            self.execute(targethost, "mkdir -p %s" % path)
        else:
            self.execute(targethost, "mkdir %s" % path)
            
    def file_exists(self, targethost, path):
        return self.execute_with_success_status(targethost, "test -e " + path)
        
    def directory_exists(self, targethost, path):
        return self.execute_with_success_status(targethost, "test -d " + path)
    
    def prepare_application_dirs(self, targethost):
        self.clear_folder(targethost, self.temp_path)
        
    def clear_folder(self, targethost, path):
        if self.directory_exists(targethost, path):
            self.rm(targethost, util.path_append([path,"*"] ), True)
        else:
            self.mkdir(targethost, path, True)
        
    def test_availability(self, targethost, port, url):
        return self.localsystem.test_availability(targethost, port, url)