'''
Created on 29.07.2013

@author: mhoyer
'''

from system import System
import os.path

class Filesystem():

    def __init__(self, config):
        if config:
            self.system = System(config)
            self.temp_path = config["temp_path"]
        else:
            self.system = System(None)  
            self.temp_path = "/tmp/replicator"  
        
    def touch(self, path):
        self.system.execute("touch", [path])
    
    def mv(self, source, target):
        self.system.execute("mv", [source, target])
    
    def cp(self, source, target):
        self.system.execute("cp", [source, target])
    
    def rm(self, path, recursive):
        if recursive:
            params = ['-rf', path]
        else:
            params = [path]
        self.system.execute("rm",params)

    def mkdir(self, path, recursive):
        if recursive:
            params = ['-p', path]
        else:
            params = [path]
        self.system.execute("mkdir",params)
        
    def write_file(self, path, data):
        fobj = open(path, "w")
        fobj.write(data)
        fobj.close()
        
    def read_file(self, path):
        fobj = open(path, "r")
        return fobj.read()
    
    def prepare_local_temp(self):
        if os.path.isdir(self.temp_path):
            self.rm(self.temp_path, True)
        self.mkdir(self.temp_path, True)
    