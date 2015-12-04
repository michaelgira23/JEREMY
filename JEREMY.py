import Skype4Py
import urllib2
import json

#
# J ust
# E xtremely
# R eliable.
# E rected by
# M ichael for
# Y ou
#

commandPrefix = '$'

def messageRecieved(message, status):
    if status == 'SENT' or status == 'RECEIVED':
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

def command(message, arguments):
    if arguments[0] == 'help':
        message.Chat.SendMessage('-=[ Jeremy\'s list of commands ]=-\n' + commandPrefix + 'help - List of commands\n' + commandPrefix + 'kys - Nothing')

    elif arguments[0] == 'ping':
        message.Chat.SendMessage('Pong!')

    elif arguments[0] == 'kys':
        message.Chat.SendMessage('/me dies')

    elif arguments[0] == 'wikipedia' or arguments[0] == 'wiki':

        restOfArguments = arguments
        del restOfArguments[0]
        wikipediaPage = '%20'.join(restOfArguments)
        
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'michaelgira23@gmail.com')]
        infile = opener.open('https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&utf8=&srlimit=1&srsearch=' + wikipediaPage)
        query = json.loads(infile.read())
        message.Chat.SendMessage(query)
    
    else:
        message.Chat.SendMessage('Command not recognized. Please type in /help for list of commands')

skype = Skype4Py.Skype()
skype.Attach()
print 'Using bot as account:', skype.CurrentUser.FullName

skype.OnMessageStatus = messageRecieved
while True:
    pass
