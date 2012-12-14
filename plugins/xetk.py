import subprocess as sub

class xetk:
	command = "^~"
	bot = None

	def __init__(self, sbot):
		self.bot = sbot
		
	def action(self, channel, message, username, host):
		#data = message.split(" ")
		#command = data.pop(1)
		p = sub.Popen('fortune -s',stdout=sub.PIPE,stderr=sub.PIPE)
		output, errors = p.communicate()
		self.bot.say(channel, output)
		
	