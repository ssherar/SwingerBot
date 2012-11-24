import re
class sed:
	sedFind = re.compile("s/([\w\s]+)/([\w\s]+)/?")
	sedFindOther = re.compile("([\w]+): s/([\w\s]+)/([\w\s]+)/?")
	command = "s/(.*)/(.*)/$"
	bot = None
	history = {}

	def __init__(self, sbot):
		self.bot = sbot
	
	def action(self, channel, message, username, host):
		if self.sedFindOther.search(message) != None:
			data = self.sedFindOther.search(message)
			uname = data.group(1)
			wordFind = data.group(2)
			wordOther = data.group(3)
			if uname in self.history and self.history[uname].find(wordFind) != -1:
				hist = self.history[uname]
				hist = hist.replace(wordFind, wordOther)
				self.bot.say(channel, "{0} thought {1} meant: {2}".format(username, uname, hist))
	
		elif self.sedFind.search(message) != None:
			data = self.sedFind.search(message)
			wordFind = data.group(1)
			wordReplace = data.group(2)
			if username in self.history and self.history[username].find(wordFind) != -1:
				hist = self.history[username]
				hist = hist.replace(wordFind, wordReplace)
				self.bot.say(channel, "{0}: {1}".format(username, hist))
	
	def clean(self, channel, username, message):
		self.history[username] = message
