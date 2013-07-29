import subprocess

class System():

	def execute(self, executable, params):
		if isinstance(params, str):
			params = [params]
		command = [executable]
		command.extend(params)
		p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out = p.stdout.read()
		err = p.stderr.read()
		if not p.wait():
			return out
		else:
			raise ExecutionException(err)
	
	
class ExecutionException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)