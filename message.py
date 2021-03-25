from discord import Message
from discord import Emoji
import re

class Message:
    def __init__(self, update: Message):
        self.user = User(update.author)
        temp = update.content
        if (re.search('<:\w{2,32}:\d{18}>', temp)):
            temp = re.sub(r'<:\w{2,32}:\d{18}>', '(emoji)', temp)
        if (re.search('(https?)\S*', temp)):
            temp = re.sub(r'(https?)\S*', '(link)', update.content)
        self.text = temp

class User:
    def __init__(self, user):
        self.name = user.display_name
        self.id = user.id