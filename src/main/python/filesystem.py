'''
Created on 29.07.2013

@author: mhoyer
'''

from system import System

class Filesystem(object):

    def __init__(self):
        self.system = System()    
        
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
            params = ['-rf', path]
        else:
            params = [path]
        self.system.execute("mkdir",params)
        