from random import choice

class butts:
	bot = None;
	command = "^butts"
	sayings = ["I GODDAMN LOVE BUTTS", "\001ACTION wiggles", "Yes butts?", "WIGGLE WIGGLE WIGGLE YEAH", "I see you baby, shaking that butt"]
	def __init__(self, sbot):
		self.bot = sbot

	def action(self, channel, message, username, host):
		self.bot.say(channel, choice(self.sayings))
