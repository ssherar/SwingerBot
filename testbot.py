from bot import Bot

Bot.debug = True

channel = "#69"
u1 = "Sambuca"
u2 = "XeTK"
u3 = "acoops"

testbot = Bot("_config.json")
testbot.dlisten(channel, "butts", u1)
testbot.dlisten(channel, "potato", u2)
testbot.dlisten(channel, "{0}: s/potato/test/".format(u2) , u1)
testbot.dlisten(channel, "hello", u1)
testbot.dlisten(channel, "s/hello/butts/", u1)
testbot.dlisten(channel, "asdf", u1)
testbot.dlisten(channel, "s/butts/hello/", u1)
testbot.dlisten(channel, "!reload", u1)
testbot.dlisten(channel, "!reload", u3)
