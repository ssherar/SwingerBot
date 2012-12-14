import os

class xetk:
	command = "^~"
	bot = None

	def __init__(self, sbot):
		self.bot = sbot
		
	def action(self, channel, message, username, host):
		p = os.popen('fortune -s',"r")
		while 1:
		line = p.readline()
		if not line: break
		self.bot.say(channel, line)
		
	