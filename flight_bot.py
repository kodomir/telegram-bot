#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import json
import urllib2
import telepot

from telepot.delegate import per_chat_id, create_open, pave_event_space

class FlightChecker(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(FlightChecker, self).__init__(*args, **kwargs)
        self._chatId = None

        while 1:
        	self.checkFlight()
        	time.sleep(3600)

    def checkFlight(self):
    	print('checking flight')

    	if self.chat_id != None:
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
    	print('Some msg recived')
    	
		command = msg['text'].strip().lower()
		self.chat_id = msg['chat']['id']

		if (command == '/start') or (command == '/force'):
			self.checkFlight()

        # self.sender.sendMessage()

TOKEN = sys.argv[1]

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, FlightChecker, timeout=1
    ),
])
bot.message_loop(run_forever='Listening ...')
