import subprocess
import pycurl
from local_system import LocalSystem

class RemoteSystem():
    
    def __init__(self, config):
        if config:
            self.localsystem = LocalSystem(config)
            self.remote_user = config["remote_user"]
            self.temp_path = config["temp_path"]
        else:
            self.localsystem = LocalSystem(None)
            self.remote_user = "root"
            self.temp_path = "/tmp/replicator/"
    
    def execute(self, targethost, command):
        params = ['%s@%s' % (self.remote_user,targethost),command]
        self.localsystem.execute("ssh", params)
    
    def transfer_single_file(self, targethost, source, destination):
        params = [source,"%s@%s:%s" % (self.remote_user, targethost, destination)]
        self.localsystem.execute("scp", params)
    
    def transfer_folder(self, targethost, source, destination):
        params = ['--compress', '--recursive', '--perms', '--owner', '--group', '--times', '--links', '--delete' ,source,"%s@%s:%s" % (self.remote_user, targethost, destination)]
        self.localsystem.execute("rsync", params)
        
    def install(self, targethost, packages):
        self.execute(targethost, "aptitude update")    
        self.execute(targethost, "aptitude install -y --quiet %s" % ' '.join(packages) )
            
    def rm(self, targethost, path, recursive):
        if recursive:
            self.execute(targethost, "rm -rf %s" % path)
        else:
            self.execute(targethost, "rm %s" % path)

    def mkdir(self, targethost, path, recursive):
        if recursive:
            self.execute(targethost, "mkdir -p %s" % path)
        else:
            self.execute(targethost, "mkdir %s" % path)
        
    def prepare_temp(self, targethost):
        if self.execute(targethost, "test -d %s" % self.temp_path):
            self.rm(self.temp_path, True)
        self.mkdir(targethost, self.temp_path, True)
        
    def test_availability(self, targethost, port, url):
        if url.startswith('http'):
            print "testing availability of: %s" % url
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, "http://%s" % targethost)
            curl.setopt(pycurl.HTTPHEADER, ['Host: %s' % url])
            curl.setopt(pycurl.FOLLOWLOCATION, 1)
            curl.perform()
            if curl.getinfo(pycurl.HTTP_CODE) == "200":
                return True
            else:
                return False
        else:
            print "not implemented yet"