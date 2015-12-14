#!/usr/bin/env python
import Skype4Py
import json
import time
import random
import requests
import sys
import os
from bs4 import BeautifulSoup

#
# J ust
# E xtremely
# R eliable.
# E rected by
# M ichael for
# Y ou
#

# detects for reboot
if len(sys.argv) == 2:
    sys.argv[1].Chat.SendMessage("Reboot successful.")

global commandPrefix
commandPrefix = '$'

def messageRecieved(message, status):
    if status == 'RECEIVED' or status == 'SENT':
        messageContents = message.Body
        fromChat = message.Chat
        fromUser = message.FromHandle
        fromDisplayName = message.FromDisplayName

        print fromDisplayName + ' (' + fromUser + '): ' + messageContents
        
        # Actual message, see if command

        if messageContents[0] == commandPrefix:
            
            # It's a command!
            
            commandComponents = messageContents[1:].split(' ')
            command(message, commandComponents)

        elif messageContents.lower().startswith('okay jeremy,'):
            commandComponents = messageContents[len('Okay Jeremy, '):].split(' ')
            command(message, commandComponents)

        elif messageContents.lower().startswith('ok jeremy,'):
            commandComponents = messageContents[len('Ok Jeremy, '):].split(' ')
            command(message, commandComponents)

        elif messageContents.lower().startswith('hey jeremy,'):
            commandComponents = messageContents[len('Hey Jeremy, '):].split(' ')
            command(message, commandComponents)

        else:
            passiveMessages(message)

def command(message, arguments):
    if arguments[0] == 'help':
        # thankfully, the linebreaks don't matter here
        message.Chat.SendMessage('-=[ Jeremy\'s list of commands ]=-\n' 
        + commandPrefix + 'help - List of commands\n'
        + commandPrefix + 'ping - Pong!\n' 
        + commandPrefix + 'kys - Kills Jeremy D:\n' 
        + commandPrefix + 'kms - Jeremy kills you D:\n'
        + commandPrefix + 'dice - Rolls a die\n'
        + commandPrefix + 'setprefix - Changes command prefix\n'
        + commandPrefix + 'privilege - Checks your privilege\n'
        + commandPrefix + 'shortlink - Shortens a link\n'
        + commandPrefix + 'cashmoney - $$$$$$$$\n'
        + commandPrefix + 'baller - Get dunked on\n'
        + commandPrefix + 'reboot - Reboot Jeremy (he is still a robot)')

    elif arguments[0] == 'ping':
        message.Chat.SendMessage('Pong!')

    elif arguments[0] == 'kys':
        message.Chat.SendMessage('/me dies')

    elif arguments[0] == 'kms':
        message.Chat.SendMessage('/me kills %s' % message.FromDisplayName)

    elif arguments[0] == 'wikipedia' or arguments[0] == 'wiki':
		# duplicate list to get rest of args
        restOfArguments = arguments
        del restOfArguments[0]
        wikipediaPage = '%20'.join(restOfArguments)

        try:
            
            # Search on Wikipedia for closest topic
            
            headers = {'User-agent': 'michaelgira23@gmail.com'}
            
            queryRaw = requests.get('https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&utf8=&srlimit=1&srsearch=' + wikipediaPage, headers=headers)
            queryJSON = queryRaw.json()
            topic = queryJSON['query']['search'][0]['title'];
                
            # Get actual Wikipedia page
            wikipediaURL = 'https://en.wikipedia.org/wiki/%s' % topic.replace(" ", "_")
            queryArticle = requests.get(wikipediaURL)
                
            # Parse Data
            
            soup = BeautifulSoup(queryArticle.text, "lxml")
            
            [s.extract() for s in soup('script')]
            [s.extract() for s in soup('style')]
                        
            snippetText = soup.get_text()
            
            trimmedText = "\n".join(snippetText.split("\n\n"))
            
            doubleTrimmedText = "\n".join(trimmedText.split("\n\n\n"))
            
            tripleTrimmedText = "\n".join(doubleTrimmedText.split("\n\n\n\n"))
            
            message.Chat.SendMessage(tripleTrimmedText)
            
        except Exception, error:
            message.Chat.SendMessage('There was an error with that request! \n(' + str(error) + ')')
    
    elif arguments[0] == 'dice':
        random.seed()
        if len(arguments) <= 1:
            result = random.randint(1, 6)
            message.Chat.SendMessage('You rolled a %s!' % result)
        elif len(arguments) == 2:
            result = random.randint(1, int(arguments[1]))
            message.Chat.SendMessage('You rolled a %s!' % result)
            
    elif arguments[0] == 'privilege':
        random.seed()
        message.Chat.SendMessage('Your privilege is %s.' % random.uniform(0, 10))
    
    elif arguments[0] == 'shortlink':
        if len(arguments) <= 1:
            message.Chat.SendMessage('You need a link as the second parameter.')
        else:
            try:
                r = requests.get('https://hec.su/api?url=%s' % arguments[1])
                response = r.json()
                message.Chat.SendMessage('Shortened %s into %s.' % (response['long'], response['short']))
            except Exception, error:
                message.Chat.SendMessage('There was an error: %s' % error)
        
    elif arguments[0] == 'cashmoney':
        message.Chat.SendMessage('Cash money millionaire \nCash money millionaire \nCash money cash money boats and goats \nCash money millionaire \nCash money millionaire \nCash money cash money boats and goats')
    
    elif arguments[0] == 'baller':
        message.Chat.SendMessage('Ballin\'!')
    
    elif arguments[0] == 'setprefix':
        if len(arguments) <= 1:
            message.Chat.SendMessage('You need a prefix as the second parameter.')
        else:
            global commandPrefix
            message.Chat.SendMessage('Changed the command prefix from "%s" to "%s".' % (commandPrefix, arguments[1]))
            commandPrefix = arguments[1]
         
    elif arguments[0] == 'reboot':
        message.Chat.SendMessage('Attempting reboot...')
        try:
            message.Chat.SendMessage("Message object as string: %s" % message.__str__)
            restartArgs = [message.__str__]
            os.execv(__file__, restartArgs)
        except Exception, error:
            message.Chat.SendMessage('There was an error: %s' % error)
            
    else:
        message.Chat.SendMessage('Command not recognized. Please type in ' + commandPrefix + 'help for list of commands.')

def passiveMessages(message):
    messageContents = message.Body.lower()
    fromChat = message.Chat
    fromUser = message.FromHandle
    fromDisplayName = message.FromDisplayName

    if 'poopyface' in messageContents:
        time.sleep(0.5)
        message.Chat.SendMessage('Hey watch your language, ' + fromDisplayName)

    elif messageContents == 'highfive, jeremy!':
        time.sleep(0.5)
        message.Chat.SendMessage('/me highfives ' + fromDisplayName + ' back')

skype = Skype4Py.Skype()
skype.Attach()
print 'Using bot as account:', skype.CurrentUser.FullName

skype.OnMessageStatus = messageRecieved
while True:
    pass
