import os
class xetk:
	command = "#"
	bot = None

	def __init__(self, sbot):
		self.bot = sbot
		
	def action(self, channel, message, username, host):
		self.bot.say(channel,os.popen('fortune -s').readline())	
	
