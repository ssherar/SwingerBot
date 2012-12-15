import os
<<<<<<< HEAD
=======

>>>>>>> dc9c7f9e6a43454ea4126c2250be5bf058c6840b
class xetk:
	command = "#"
	bot = None

	def __init__(self, sbot):
		self.bot = sbot
		
	def action(self, channel, message, username, host):
<<<<<<< HEAD
		self.bot.say(channel,os.popen('fortune -s').readline())	
	
=======
		p = os.popen('fortune -s',"r")
		while 1:
			line = p.readline()
			if not line: break
			self.bot.say(channel, line)
		
	
>>>>>>> dc9c7f9e6a43454ea4126c2250be5bf058c6840b
