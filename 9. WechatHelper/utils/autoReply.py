import sys
import random
import itchat
from itchat.content import TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO, NOTE


RELAYCONTENTS = ['[AutoReply]: Hi there, I am currently unavailable. I will get back to you later.']
KEYWORDS = []


'''根据关键词自动回复'''
class autoReply():
	def __init__(self, **kwargs):
		self.info = 'autoReply'
		self.options = kwargs
	'''Define functions'''
	def run(self, keywords=None, replycontents=None):
		if keywords is not None:
			global KEYWORDS
			KEYWORDS = keywords
		if replycontents is not None:
			global RELAYCONTENTS
			RELAYCONTENTS = replycontents
		try:
			itchat.auto_login(hotReload=True)
		except:
			itchat.auto_login(hotReload=True, enableCmdQR=True)
		itchat.run()
	'''Text Messasge'''
	@itchat.msg_register([TEXT], isFriendChat=True)
	def replyText(msg):
		if not KEYWORDS:
			content = random.choice(RELAYCONTENTS)
			itchat.send(content, msg['FromUserName'])
		else:
			for keyword in KEYWORDS:
				if keyword in msg['Text']:
					content = random.choice(RELAYCONTENTS)
					itchat.send(content, msg['FromUserName'])
					break
	'''Other Messages'''
	@itchat.msg_register([PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
	def otherReply(msg):
		if not KEYWORDS:
			content = random.choice(RELAYCONTENTS)
			itchat.send(content, msg['FromUserName'])
