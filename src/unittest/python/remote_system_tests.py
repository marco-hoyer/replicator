import unittest

from remote_system import RemoteSystem
from config import Config

class remote_system_test (unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(remote_system_test, self).__init__(*args, **kwargs)
        self.config = Config("../../main/python/replicator/config.yaml","../../main/python/replicator/applications.yaml")
        self.system = RemoteSystem(self.config)
