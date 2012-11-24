class butts:
	bot = None;
	command = "^butts$"
	def __init__(self, sbot):
		self.bot = sbot

	def action(self, channel, message, username, host):
		self.bot.say(channel, "I LOVE BUTTS")
