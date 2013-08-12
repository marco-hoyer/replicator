import subprocess
import pycurl
import os
import logging
import StringIO

class LocalSystem():
	
	def __init__(self, config):
		self.init_logger()
		if config:
			self.temp_path = config["temp_path"]
		else:
			self.temp_path = "/tmp/replicator/"

	def init_logger(self):
		logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)
		self.logger = logging.getLogger('Replicator')

	def execute(self, executable, params):
		if isinstance(params, str):
			params = [params]
		command = [executable]
		command.extend(params)
		self.logger.debug("executing: %s" % command)
		p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out = p.stdout.read()
		err = p.stderr.read()
		if not p.wait():
			return out
		else:
			raise ExecutionException(err)	

	def touch(self, path):
		self.execute("touch", [path])
	
	def mv(self, source, target):
		self.execute("mv", [source, target])
	
	def cp(self, source, target):
		self.execute("cp", [source, target])
	
	def rm(self, path, recursive):
		if recursive:
			params = ['-rf', path]
		else:
			params = [path]
		self.execute("rm",params)

	def mkdir(self, path, recursive):
		if recursive:
			params = ['-p', path]
		else:
			params = [path]
		self.execute("mkdir",params)
		
	def write_file(self, path, data):
		fobj = open(path, "w")
		fobj.write(data)
		fobj.close()
		
	def read_file(self, path):
		fobj = open(path, "r")
		return fobj.read()
	
	def prepare_temp(self):
		if os.path.isdir(self.temp_path):
			self.rm(self.temp_path, True)
		self.mkdir(self.temp_path, True)

	def test_availability(self, targethost, port, url):
		if url.startswith('http'):
			hostheader = url.split('/')[2]
			self.logger.debug("testing availability of %s on %s:%d" % (hostheader, targethost, port))
			curl = pycurl.Curl()
			curl.setopt(pycurl.URL, "http://%s:%d" % (targethost,port))
			curl.setopt(pycurl.HTTPHEADER, ['Host: %s' % hostheader])
			curl.setopt(pycurl.CONNECTTIMEOUT, 2)
			#curl.setopt(pycurl.FOLLOWLOCATION, 1)
			contents = StringIO.StringIO()
			curl.setopt(pycurl.WRITEFUNCTION, contents.write)
			try:
				curl.perform()
			except:
				self.logger.error("Error performing curl query")
				return False
			self.logger.info("server responded with %s" % curl.getinfo(pycurl.HTTP_CODE))
			#self.logger.debug("data received: %s" % contents.getvalue())
			if curl.getinfo(pycurl.HTTP_CODE) == 200:
				return True
			else:
				return False
		else:
			print "not implemented yet"

class ExecutionException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
