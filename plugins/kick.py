class kick:
	command = "(stallman|trousers)"
	bot = None
	
	def __init__(self, sbot):
		self.bot = sbot

	def action(self, channel, message, username, host):
		self.bot.send("KICK {0} {1} Fuck you and all you stand for".format(channel, username))
