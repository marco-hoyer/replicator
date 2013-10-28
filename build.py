from pybuilder.core import use_plugin, init, Author

use_plugin("python.install_dependencies")
#use_plugin("copy_resources")
use_plugin("python.core")
#use_plugin("python.unittest")
use_plugin("python.distutils")

authors = [Author('Marco Hoyer', 'marco_hoyer@gmx.de')]
description = """replicator: a toolsuite replicating nearly every applications data running on linux.

for more documentation, visit https://github.com/marco-hoyer/replicator
"""

name = 'replicator'
license = 'GNU GPL v3'
summary = 'replicator: a toolsuite replicating nearly every applications data running on linux'
url = 'https://github.com/marco-hoyer/replicator'
version = '1.0.1'

default_task = ['publish']


@init
def initialize(project):

    project.install_file('/etc/replicator/', 'res/config.yaml')
    project.install_file('/etc/replicator/', 'res/applications.yaml.example')

    project.set_property('distutils_classifiers', [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Monitoring',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: Jython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ])
