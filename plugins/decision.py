from random import choice

class decision:
	bot = None;
	command = "^{0}: [Ss]hould [Ii]".format(self.bot.nick)
	responses = ["DOO EEET!", "Yeah, sure", "I don't know and I don't care", "Probably not", "NO, DUDE! It's a trap!"]
	def __init__(self, sbot):
		self.bot = sbot

	def action(self, channel, message, username, host):
		self.bot.say(channel, username + ": " + choice(self.responses))
