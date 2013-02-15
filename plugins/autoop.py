class autoop:
	bot = None
	command = 12356123123
	
	def __init__(self, sbot):
		self.bot = sbot

	def onJoin(self, channel, username, host):
		self.bot.send("MODE {0} +o {1}".format(channel, username))
