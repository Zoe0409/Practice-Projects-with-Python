from wxpy import *

class wechatRobot():
	def __init__(self, **kwargs):
		self.info = 'wechatRobot'
		self.options = kwargs
	'''Define functions'''
	def run(self):
		bot = Bot()
		tuling = Tuling(api_key='a65aa00b424047d88554b744eaf07597')
		@bot.register(msg_types=TEXT)
		def auto_reply_all(msg):
			tuling.do_reply(msg)
		bot.join()
