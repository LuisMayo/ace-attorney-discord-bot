from discord import Message
from discord import mentions
import re

class Message:
    def __init__(self, update: Message):
        self.user = User(update.author)
        temp = update.clean_content
        if (match := re.search('<:(\w{2,32}):\d{18}>', temp)): # emojis
            emoji_name = match.group(1)
            temp = re.sub(r'<:\w{2,32}:\d{18}>', ':' + emoji_name + ':', temp)
        if (re.search('(https?)\S*', temp)): # links
            temp = re.sub(r'(https?)\S*', '(link)', update.content)
        self.text = temp

class User:
    def __init__(self, user):
        self.name = user.display_name
        self.id = user.id 