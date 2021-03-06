import re
class sed:
	sedFind = re.compile("s/([^/]*)/([^/]*)/?")
	sedFindOther = re.compile("([\w]+): s/([^/]*)/([^/]*)/?")
	command = "(\w+:)? s/(.*)/(.*)/?$"
	bot = None
	history = {}

	def __init__(self, sbot):
		self.bot = sbot
	
	def action(self, channel, message, username, host):
		if self.sedFindOther.search(message) != None:
			data = self.sedFindOther.search(message)
			uname = data.group(1)
			wordFind = data.group(2).strip("/")
			wordOther = data.group(3).strip("/")

			if uname in self.history and re.search(wordFind, self.history[uname]) != None:
				hist = self.history[uname]
				if hist.find("ACTION") != -1:
					hist = hist.strip("\001")
					hist = hist.replace("ACTION", "/me")
				hist = re.sub(wordFind, wordOther, hist)
				self.bot.say(channel, "{0} thought {1} meant: {2}".format(username, uname, hist))
	
		elif self.sedFind.search(message) != None:
			data = self.sedFind.search(message)
			wordFind = data.group(1).strip("/")
			wordReplace = data.group(2).strip("/")
			if username in self.history and re.search(wordFind, self.history[username]) != None:
				hist = self.history[username]
				hist = re.sub(wordFind, wordReplace, hist)
				self.bot.say(channel, "{0}: {1}".format(username, hist))
	
	def clean(self, channel, username, message):
		self.history[username] = message
