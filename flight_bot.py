# import sys
# import telepot
# from telepot.delegate import per_chat_id, create_open, pave_event_space

# """
# $ python2.7 counter.py <token>
# Counts number of messages a user has sent. Starts over if silent for 10 seconds.
# Illustrates the basic usage of `DelegateBot` and `ChatHandler`.
# """

# class MessageCounter(telepot.helper.ChatHandler):
#     def __init__(self, *args, **kwargs):
#         super(MessageCounter, self).__init__(*args, **kwargs)
#         self._count = 0

#     def on_chat_message(self, msg):
#         self._count += 1
#         self.sender.sendMessage(self._count)


# TOKEN = sys.argv[1]  # get token from command-line

# bot = telepot.DelegatorBot(TOKEN, [
#     pave_event_space()(
#         per_chat_id(), create_open, MessageCounter, timeout=10
#     ),
# ])
# bot.message_loop(run_forever='Listening ...')

#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import json
import urllib2
import telepot
import threading

from telepot.delegate import per_chat_id, create_open, pave_event_space

class FlightChecker(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
    	super(FlightChecker, self).__init__(*args, **kwargs)

    	threading.Timer(3600.0, self.checkFlight).start()

    def checkFlight(self):
		print('checking flight')

		response = urllib2.urlopen('http://www.pulkovoairport.ru/f/flights/cur/ru_dep_2.js?0.17094681738165363')
		data = json.load(response)

		found = False
		if data['data'] != None:
			for flight in data['data']:
				if flight['company'] == 'Royal Flight airlines':
					found = True
					if flight['date'] != '2016-11-12 13:00:00':
						print('Ooops something wrong')
						self.sender.sendMessage('Date changed! Panic!\nFlight date: ' + flight['date'] + '\n\n Check it! http://www.pulkovoairport.ru/')
					else:
						print('All right')
						self.sender.sendMessage('All right, ceep calrm.\nFlight date: ' + flight['date'])

		if found == False:
			self.sender.sendMessage('Can\'t find flight check it. http://www.pulkovoairport.ru')
			print('Flight not found')


    def on_chat_message(self, msg):
		message = msg
		command = message['text'].strip().lower()

		print('Some msg recived')

		if (command == '/start') or (command == '/force'):
			self.checkFlight()

        # self.sender.sendMessage()

TOKEN = sys.argv[1]

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, FlightChecker, timeout=100
    ),
])
bot.message_loop(run_forever='Listening ...')