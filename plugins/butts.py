class butts:
	bot = None;
	command = "^butts"
	def __init__(self, sbot):
		self.bot = sbot

	def action(self, channel, message, username, host):
		if username == "bugsduggan":
			self.bot.say(channel, "I hear " + username + " likes anal.")
		else:
			self.bot.say(channel, "I GODDAMN LOVE BUTTS")
