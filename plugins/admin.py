import re
import sys
from git import *

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
		elif command == "quit":
			self.bot.say(channel, "Goodbye Cruel World")
			sys.exit(0)
		elif command == "reload":
			self.bot.say(channel, "Reloading plugins...")
			self.bot.reload_plugins()
		elif command == "join":
			self.bot.send("JOIN :{0}".format(data[1]))
		elif command == "gload":
			self.gitload(channel)
		elif command == "leave":
			self.bot.send("PART {0) :Screw you guys I'm going home".format(channel))

	def gitload(self, channel):
		self.bot.say(channel, "Pulling from origin...")
		repo = Repo("~/bot/")
		o = repo.remotes.origin
		o.pull()
		self.bot.say(channel, "Pull complete! Reloading Plugins...")
		self.bot.reload_plugins()
