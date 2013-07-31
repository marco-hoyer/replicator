import subprocess
import pycurl

class System():
	
	def __init__(self, config):
		if config:
			self.remote_user = config["remote_user"]
			self.temp_path = config["temp_path"]
		else:
			self.remote_user = "root"
			self.temp_path = "/tmp/replicator"

	def execute(self, executable, params):
		if isinstance(params, str):
			params = [params]
		command = [executable]
		command.extend(params)
		print command
		p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out = p.stdout.read()
		err = p.stderr.read()
		if not p.wait():
			return out
		else:
			raise ExecutionException(err)
	
	def execute_on_targethost(self, host, command):
		print host
		print command
		params = ['%s@%s' % (self.remote_user,host),command]
		self.execute("ssh", params)
	
	def transfer_single_file(self, source, destination, remote_host):
		params = [source,"%s@%s:%s" % (self.remote_user, remote_host, destination)]
		self.execute("scp", params)
	
	def transfer_folder(self, source, destination, remote_host):
		params = ['--compress', '--recursive', '--perms', '--owner', '--group', '--times', '--links', '--delete' ,source,"%s@%s:%s" % (self.remote_user, remote_host, destination)]
		self.execute("rsync", params)
		
		
	def test_availability(self, url):
		if str.startswith('http'):
			print "testing availability of: %s" % url
		else:
			print "not implemented yet"

class ExecutionException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)