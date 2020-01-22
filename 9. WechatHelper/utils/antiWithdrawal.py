'''Set Up'''

import re
import os
import time
import itchat
from itchat.content import TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO, NOTE

MSGINFO = {}
FACEPACKAGE = None

'''Define antiwithdrawal function'''

class antiWithdrawal():
	def __init__(self, **kwargs):
		self.info = 'antiWithdrawal'
		self.options = kwargs
	'''Define Function'''
	def run(self):
		try:
			itchat.auto_login(hotReload=True)
		except:
			itchat.auto_login(hotReload=True, enableCmdQR=True)
		itchat.run()
	'''Process received message'''
	@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True, isGroupChat=True, isMpChat=True)
	def saveReceiveMsg(msg):
		msg_receive_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		# Message sender
		if 'ActualNickName' in msg:
			msg_from_nickname = msg['ActualNickName']
			msg_from = msg_from_nickname
			msg_from_username = msg['ActualUserName']
			friends = itchat.get_friends(update=True)
			for friend in friends:
				if msg_from_username == friend['UserName']:
					if friend['RemarkName']:
						msg_from = friend['RemarkName']
					else:
						msg_from = friend['NickName']
					break
			groups = itchat.get_chatrooms(update=True)
			for group in groups:
				if msg['FromUserName'] == group['UserName']:
					group_name = group['NickName']
					group_menber_count = group['MemberCount']
					break
			if not group_name:
				group_name = 'Unknown group'
			group_name = group_name + '(%s人)' % str(group_menber_count)
			msg_from = group_name + '-->' + msg_from
		else:
			try:
				msg_from = itchat.search_friends(userName=msg['FromUserName'])['RemarkName']
				if not msg_from:
					msg_from = itchat.search_friends(userName=msg['FromUserName'])['NickName']
			except:
				msg_from = 'WeChat Official Accounts'
		msg_send_time = msg['CreateTime']
		msg_id = msg['MsgId']
		msg_content = None
		msg_link = None
		# Text or Friends
		if msg['Type'] == 'Text' or msg['Type'] == 'Friends':
			msg_content = msg['Text']
			print('[Text/Friends]: %s' % msg_content)
		# Attachment/Video/Picture/Recording
		elif msg['Type'] == 'Attachment' or msg['Type'] == "Video" or msg['Type'] == 'Picture' or msg['Type'] == 'Recording':
			msg_content = msg['FileName']
			msg['Text'](str(msg_content))
			print('[Attachment/Video/Picture/Recording]: %s' % msg_content)
		# Location
		elif msg['Type'] == 'Map':
			x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
			if location is None:
				msg_content = r"latitude:" + x.__str__() + ", longitude:" + y.__str__()
			else:
				msg_content = r"" + location
			print('[Map]: %s' % msg_content)
		# Shared movie/music
		elif msg['Type'] == 'Sharing':
			msg_content = msg['Text']
			msg_link = msg['Url']
			print('[Sharing]: %s' % msg_content)
		FACEPACKAGE = msg_content
		MSGINFO.update(
				{
				msg_id: {
					"msg_from": msg_from,
					"msg_send_time": msg_send_time,
					"msg_receive_time": msg_receive_time,
					"msg_type": msg["Type"],
					"msg_content": msg_content,
					"msg_link": msg_link
					}
				}
			)
		antiWithdrawal.updateMsgInfo()
	'''Check if there is any message withdrawed'''
	@itchat.msg_register(NOTE, isFriendChat=True, isGroupChat=True, isMpChat=True)
	def monitorMsg(msg):
		if 'withdrawed a message' in msg['Content']:
			recall_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
			recall_msg = MSGINFO.get(recall_msg_id)
			print('[Recall]: %s' % recall_msg)
			if len(recall_msg_id) < 11:
				itchat.send_file(FACEPACKAGE, toUserName='filehelper')
			else:
				prompt = '+++' + recall_msg.get('msg_from') + 'withdrawed a message+++\n' \
							'--Message type：' + recall_msg.get('msg_type') + '\n' \
							'--Received time：' + recall_msg.get('msg_receive_time') + '\n' \
							'--Message content：' + recall_msg.get('msg_content')
				if recall_msg['msg_type'] == 'Sharing':
					prompt += '\nlink：' + recall_msg.get('msg_link')
				itchat.send_msg(prompt, toUserName='filehelper')
				if recall_msg['msg_type'] == 'Attachment' or recall_msg['msg_type'] == "Video" or recall_msg['msg_type'] == 'Picture' or recall_msg['msg_type'] == 'Recording':
					file = '@fil@%s' % (recall_msg['msg_content'])
					itchat.send(msg=file, toUserName='filehelper')
					os.remove(recall_msg['msg_content'])
				MSGINFO.pop(recall_msg_id)
	'''Updated Message (Delete the message from 120 seconds ago)'''
	@staticmethod
	def updateMsgInfo():
		need_del_msgs = []
		for msg in MSGINFO:
			msg_time_interval = int(time.time()) - MSGINFO[msg]['msg_send_time']
			if msg_time_interval > 120:
				need_del_msgs.append(msg)
		if need_del_msgs:
			for msg in need_del_msgs:
				MSGINFO.pop(msg)
