#!/usr/bin/python
import socket
import sys
import json
import re
import os

class Bot:
	server = ""
	nick = ""
	password = ""
	port = 6667
	channels = []
	admins = []
	debug = False

	matchMessage = re.compile("^:(\w+)!\w+@([\w\d\.-]+) PRIVMSG (#?\w+) :(.*)$")

	default_calls = {}
	plugins = {}
	clean = []
	ircsock = None

	def __init__(self, config_file):
		data = json.loads(open("./" + config_file).read())
		self.server = data['server']
		self.nick = data['nick']
		if "password" in data:
			self.password = data['password']
		if "port" in data:
			self.port = data['port']
		self.admins = data['admins']
		self.channels = data['channels']
		self.load_plugins()

	def connect(self):
		self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ircsock.connect((self.server, self.port))
		self.send("USER " + self.nick + " " + self.nick + " " + self.nick + ": " + self.nick)
		self.send("NICK " + self.nick)
		self.send("PRIVMSG zippy : IDENTIFY " + self.password)
		for channel in self.channels:
			self.send("JOIN " + channel)
		self.listen()

	def listen(self): 
		while 1:
			ircmesg = self.ircsock.recv(2048).strip("\n\r")
			data = self.matchMessage.search(ircmesg)
			if ircmesg != None:
				print ircmesg
			if ircmesg.find("PING") != -1:
				host = ircmesg.split(" ")[1]
				print host
				self.send("PING " + host)
			if data != None:
				username = data.group(1)
				host = data.group(2)
				channel = data.group(3)
				message = data.group(4)

				for name in self.plugins:
					if re.search(name, message) != None:
						self.plugins[name].action(channel, message, username, host)

				self.cleaner(channel, username, message)
	
	def send(self, cmd):
		self.ircsock.send(cmd+ " \n")

	def say(self, channel, message):
		tosay = "PRIVMSG {0} :{1}".format(channel, message)
		if self.debug:
			print tosay
		else:
			self.send(tosay)
	
	def action(self, channel, message):
		self.say(channel, "\001ACTION {0} ".format(message))

	# Could load admin plugin to check
	def reload_plugins(self):
		for root, dirs, files in os.walk("plugins/"):
			for currentFile in files:
				if currentFile.endswith(".py") and currentFile.find("init") == -1:
					currentFile = currentFile.strip(".py")
					print "plugins."+currentFile
					del(sys.modules["plugins.{0}".format(currentFile)])	
		self.load_plugins()

	def load_plugins(self):
		import os

		for file_name in os.listdir("plugins/"):
			if file_name.endswith(".py") and file_name != "__init__.py":
				klass = self.my_import(file_name.replace(".py", ""))
				regex = klass.command
				self.plugins[regex] = klass(self)
				try:
					getattr(klass, "clean")
					self.clean.append(klass.command)
				except:
					pass
		
				print "%s loaded" % file_name
		
	def my_import(self, name):
		path = "plugins.%s" % name
		mod = __import__(path,fromlist=[name]) 
		components = path.split(".")
		for comp in components[1:]:
			mod = getattr(mod, comp)
		return mod
	
	def cleaner(self, channel, username, message):
		for name in self.clean:
			self.plugins[name].clean(channel, username, message)
	
	def dlisten(self,channel, message, username, host=""):
		if self.debug != False:
			self.say(channel, "-> %s " % message)
			for name in self.default_calls:
				if re.search(name, message) != None:
					if self.verify_user(username):
						self.default_calls[name]()
					else:
						self.say(channel, "Not admin, bitch")
			for name in self.plugins:
				if re.search(name, message) != None:
					self.plugins[name].action(channel, message, username, host)

			self.cleaner(channel, username, message)
		else:
			print "Not in debug mode"
			sys.exit(1)
	def verify_user(self, username):
		for admin in self.admins:
			if username == admin:
				return True
		return False

if __name__ == "__main__":
	bot = Bot("_config.json")
	bot.connect()
