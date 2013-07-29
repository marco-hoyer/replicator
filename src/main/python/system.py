import subprocess

class System():
	
	def __init__(self, config):
		self.remote_user = config["remote_user"]

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
		params = []
		self.execute("ssh", params)
	
	def transfer_single_file(self, source, destination, remote_host):
		params = [source,"%s@%s:%s" % (self.remote_user, remote_host, destination)]
		self.execute("scp", params)
	
	def transfer_folder(self, source, destination, remote_host):
		params = ['--compress', '--recursive', '--perms', '--owner', '--group', '--times', '--links', '--delete' ,source,"%s@%s:%s" % (self.remote_user, remote_host, destination)]
		self.execute("rsync", params)
	
class ExecutionException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)