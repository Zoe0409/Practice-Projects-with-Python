import os
import argparse


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Wechat helper, Version: V0.1.0")
	parser.add_argument('-o', dest='option', help='Choose the function you need, including <analysisFriends>, <antiWithdrawal>, <wechatRobot> and <autoReply>')
													
	parser.add_argument('-k', dest='keywords', help='Keywords for <autoReply>, use "*" to separate if keywords is more than one.')
	parser.add_argument('-c', dest='contents', help='Contents for <autoReply>, use "*" to separate if contents is more than one.')
	args = parser.parse_args()
	if args.option == 'analysisFriends':
		from utils.analysisFriends import analysisFriends
		print('[INFO]: analysisFriends...')
		savedir = os.path.join(os.getcwd(), 'results')
		analysisFriends().run(savedir=savedir)
		print('[INFO]: analysis friends successfully, results saved into %s...' % (savedir, savedir))
	elif args.option == 'antiWithdrawal':
		from utils.antiWithdrawal import antiWithdrawal
		print('[INFO]: antiWithdrawal...')
		antiWithdrawal().run()
	elif args.option == 'wechatRobot':
		from utils.wechatRobot import wechatRobot
		print('[INFO]: wechatRobot...')
		wechatRobot().run()
	elif args.option == 'autoReply':
		from utils.autoReply import autoReply
		print('[INFO]: autoReply...')
		keywords = args.keywords
		contents = args.contents
		if keywords:
			keywords = keywords.split('*')
		if contents:
			contents = contents.split('*')
		autoReply().run(keywords=keywords, replycontents=contents)
	else:
		print('[INFO]: argparse error...<analysisFriends>, <antiWithdrawal>, <wechatRobot> Or <autoReply>')
