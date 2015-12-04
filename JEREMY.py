import Skype4Py
import urllib2
import json
import html2text
import time
import random

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
        + commandPrefix + 'kys - Nothing\n' 
        + commandPrefix + 'dice - Rolls a die')

    elif arguments[0] == 'ping':
        message.Chat.SendMessage('Pong!')

    elif arguments[0] == 'kys':
        message.Chat.SendMessage('/me dies')

    elif arguments[0] == 'wikipedia' or arguments[0] == 'wiki':
		# duplicate list to get rest of args
        restOfArguments = arguments
        del restOfArguments[0]
        wikipediaPage = '%20'.join(restOfArguments)

        try:
            
            # Search on Wikipedia for closest topic
            
            queryTopic = urllib2.build_opener()
            queryTopic.addheaders = [('User-agent', 'michaelgira23@gmail.com')]
            queryRaw = queryTopic.open('https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&utf8=&srlimit=1&srsearch=' + wikipediaPage)
            queryJSON = json.loads(queryRaw.read())
            topic = queryJSON['query']['search'][0]['title'];
            
            # Get actual Wikipedia page
            #wikipediaURL = str('https://en.wikipedia.org/wiki/' + topic.replace(" ", "_"))
            wikipediaURL = 'https://en.wikipedia.org/wiki/John_Cena'
            print type(wikipediaURL)
            queryArticle = urllib2.build_opener()
            #queryArticle.addheaders = [('User-agent', 'michaelgira23@gmail.com')]
            articleHTML = queryArticle.open(wikipediaURL)
            article = html2text.html2text(articleHTML)
            
            # Parse Data
            
            #snippet = query['query']['search'][0]['snippet']
            #snippetText = html2text.html2text(snippet)
            
            message.Chat.SendMessage(article)
            
        except Exception, error:
            message.Chat.SendMessage('There was an error with that request! With URL: ' + wikipediaURL + '\n(' + str(error) + ')')
    
    elif arguments[0] == 'dice':
        random.seed()
        if len(arguments) <= 1:
            result = random.randint(1, 6)
            message.Chat.SendMessage('You rolled a %s!' % result)
        elif len(arguments) = 2:
            result = random.randint(1, arguments[1])
            message.Chat.SendMessage('You rolled a %s!' % result)
        else:
            message.Chat.SendMessage('Error: Too many parameters for \'$dice!\'')
    
    else:
        message.Chat.SendMessage('Command not recognized. Please type in $help for list of commands')

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
