SwingerBot
==========

An irc bot written in Python as a little side project.

How to write a plugin
---------------------

a plugin has to have certain things for it to function properly: these are

* a command - any regex string which you want to check input against
* a bot variable
* a constructor which has the signature `__init__(self, sbot):` in which you assign `sbot` to `self.bot`
* a method action with signature `action(self, channel, message, username, host)`

* (optional) method clean with signature `clean(self, channel, message, username, host)` This is run after each listen.
* (optional) method onJoin with signature `onJoin(self, channel, username, host)`, which listens for a `JOIN` command from the IRC server

for example

```python
class butts:
	command = "$butts"
	bot = None
	def __init__(self, sbot):
		self.bot = sbot
	def action(self, channel, message, username, host):
		self.bot.say(channel, "butts")
```

Config file example
-------------------

```json
{
	"nick" : "Bot",
	"server" : "irc.example.com",
	"port" : 6667,
	"password" : "nickservpasswd",
	"admins" : ["admin", "admin2"],
	"channels" : ["#channel1", "#channel2"]
}
	
```
