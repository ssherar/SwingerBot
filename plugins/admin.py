import re
import sys

class admin:
	command = "^!admin"
	bot = None

	def __init__(self, sbot):
		self.bot = sbot

	def action(self, channel, message, username, host):
		data = message.split(" ")
		command = data.pop(1)
		if not self.bot.verify_user(username):
			self.bot.say(channel, "{0}: You're not an admin bitch!".format(username))
			return	
		if command == "quit":
			self.bot.say(channel, "Goodbye Cruel World")
			sys.exit(0)
		elif command == "reload":
			self.bot.say(channel, "Reloading plugins...")
			self.bot.reload_plugins()
		elif command == "join":
			self.bot.send("JOIN :{0}".format(data[1]))
