#!/usr/bin/python
import socket
import sys
import json
import re
import os

class Bot:
	# The class wide variables loaded fron the config json file
	server = ""
	nick = ""
	password = ""
	port = 6667
	channels = []
	admins = []


	# Matches any PRIVMSG sent
	matchMessage = re.compile("^:([\w_\-]+)!\w+@([\w\d\.-]+) PRIVMSG (#?\w+) :(.*)$")
	# Matches any user joining  
	matchJoin = re.compile("^:([\w_\-]+)!\w+@([\w\d.\-]+) JOIN :(#?\w+)")

	# Holds default calls
	# Deprecated
	default_calls = {}
	# Holds the commands for loaded plugins
	plugins = {}
	# Holds the names of the plugins which have the method clean()
	clean = []
	# Holds the names of the plugins which have the method onJoin()
	onJoin = []
	ircsock = None

	def __init__(self, config_file):
		"""
			Loads the json file passed into the class and
			and loads all the plugins associated to the
			bot
		"""
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
		"""
			Creates a socket to the server, identifies itself
			and then starts listening
		"""
		self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ircsock.connect((self.server, self.port))
		self.send("USER " + self.nick + " " + self.nick + " " + self.nick + ": " + self.nick)
		self.send("NICK " + self.nick)
		self.send("PRIVMSG zippy : IDENTIFY " + self.password)
		for channel in self.channels:
			self.send("JOIN " + channel)
		self.listen()

	def listen(self): 
		"""
			Main loop of the program: takes data from the socket
			and then sanitises it, to be able to pass to relevant functions
		"""
		channel = ""
		while 1:
			ircmesg = self.ircsock.recv(2048).strip("\n\r")
			data = self.matchMessage.search(ircmesg)
			joinData = self.matchJoin.search(ircmesg)
			if ircmesg.find("PING") != -1:
				host = ircmesg.split(" ")[1]
				self.send("PING " + host)
			try:
				if data != None:
					username = data.group(1)
					host = data.group(2)
					channel = data.group(3)
					message = data.group(4)

					for name in self.plugins:
						if re.search(name, message) != None:
							self.plugins[name].action(channel, message, username, host)
	
					self.cleaner(channel, username, message)
				if joinData != None:
					username = joinData.group(1)
					host = joinData.group(2)
					channel = joinData.group(3)
					self.onJoined(channel, host, username)

			except Exception as e:
				exc_type, exc_value, exc_traceback = sys.exc_info()
				self.say(channel, "Error: {0}".format(exc_type))
				pass

	def onJoined(self, channel, host, username):
		"""
			Calls the onJoin() method which can be found in 
			certain plugins
		"""
		for name in self.onJoin:
			self.plugins[name].onJoin(channel, host, username)

	def send(self, cmd):
		"""
			Sends raw data to the IRC server
		"""
		self.ircsock.send(cmd+ " \n")

	def say(self, channel, message):
		"""
			Sends a PRIVMSG to the specified channel
		"""
		tosay = "PRIVMSG {0} :{1}".format(channel, message)
		self.send(tosay)

	def action(self, channel, message):
		"""
			Adds null character to the start of the message
			to change it into an ACTION, then usies say(self, channel, messag)
		"""
		self.say(channel, "\001ACTION {0} ".format(message))

	# Could load admin plugin to check
	def reload_plugins(self):
		"""
			unloads all modules which are available in the 
			plugins directory, then loads them back in
		"""
		for root, dirs, files in os.walk("plugins/"):
			for currentFile in files:
				if currentFile.endswith(".py") and currentFile.find("init") == -1:
					currentFile = currentFile.strip(".py")
					print "plugins."+currentFile
					# Problem with loading new plugins as they are not existing yet
					if "plugins.{0}".format(currentFile) in sys.modules:
						del(sys.modules["plugins.{0}".format(currentFile)])	
		self.load_plugins()

	def load_plugins(self):
		"""
			Loads all plugins which can be found in the plugins/ directory
		"""
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

				try:
					getattr(klass, "onJoin")
					self.onJoin.append(klass.command)
				except:
					pass

				print "%s loaded" % file_name

	def my_import(self, name):
		"""
			imports the class from the parameter name
			from the directory plugins
		"""
		path = "plugins.%s" % name
		mod = __import__(path,fromlist=[name]) 
		components = path.split(".")
		for comp in components[1:]:
			mod = getattr(mod, comp)
		return mod

	def cleaner(self, channel, username, message):
		"""
			Calls all plugins which have the cleaner()
			methods.
		"""
		for name in self.clean:
			self.plugins[name].clean(channel, username, message)

	def verify_user(self, username):
		"""
			Verify the user who sent the message against
			the admin list
		"""
		for admin in self.admins:
			if username == admin:
				return True
		return False

if __name__ == "__main__":
	bot = Bot("_config.json")
	bot.connect()
