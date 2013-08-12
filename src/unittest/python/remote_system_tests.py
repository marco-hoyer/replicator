import unittest

from remote_system import RemoteSystem

class remote_system_test (unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(remote_system_test, self).__init__(*args, **kwargs)
        self.system = RemoteSystem(None)
