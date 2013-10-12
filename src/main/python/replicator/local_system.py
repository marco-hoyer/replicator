import subprocess
import pycurl
import os
import logging
import StringIO

class LocalSystem():
	
	def __init__(self, config):
		self.logger = logging.getLogger(__name__)
		self.config = config.get_config_list()
		self.temp_path = self.config["temp_path"]
		self.backup_path = self.config["backup_path"]

	def execute(self, executable, params):
		if isinstance(params, str):
			params = [params]
		command = [executable]
		command.extend(params)
		self.logger.debug("executing: %s" % " ".join(command))
		p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out = p.stdout.read()
		err = p.stderr.read()
		if not p.wait():
			return out
		else:
			return False	

	def touch(self, path):
		self.execute("touch", [path])
	
	def mv(self, source, target):
		self.execute("mv", [source, target])
	
	def cp(self, source, target, recursive):
		if recursive:
			self.execute("cp", ["-r", source, target])
		else:
			self.execute("cp", [source, target])
	
	def rm(self, path, recursive):
		if recursive:
			self.execute("rm",['-rf', path])
		else:
			self.execute("rm",['-f', path])

	def mkdir(self, path, recursive):
		if recursive:
			self.execute("mkdir",['-p', path])
		else:
			self.execute("mkdir",[path])
			
	def compress(self, source, target):
		self.execute("tar",["-cf", target, source])
		
	def write_file(self, path, data):
		fobj = open(path, "w")
		fobj.write(data)
		fobj.close()
		
	def read_file(self, path):
		fobj = open(path, "r")
		return fobj.read()
	
	def prepare_application_dirs(self):
		if self.directory_exists(self.temp_path):
			self.rm(self.temp_path, True)
		self.mkdir(self.temp_path, True)
		if not self.directory_exists(self.backup_path):
			self.mkdir(self.backup_path, True)
		
	def clear_folder(self, path):
		if os.path.isdir(path):
			self.rm(path, True)
		self.mkdir(path, True)
		
	def get_raw_package_list(self):
		return self.execute("dpkg", ["--get-selections"])
	
	def write_package_list(self, path):
		self.write_file(path, self.get_raw_package_list())
		
	def file_exists(self, path):
		self.execute("test", ["-e",path])
		
	def directory_exists(self, path):
		self.execute("test", ["-d",path])

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