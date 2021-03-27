from discord import Message
import re

class Message:
    def __init__(self, update: Message):
        self.user = User(update.author)
        tmp = update.clean_content
        tmp = re.sub(r'<:\w{2,32}:\d{18}>', '', tmp) # emojis
        tmp = re.sub(r'(https?)\S*', '(link)', tmp) # links
        self.text = tmp

class User:
    def __init__(self, user):
        self.name = user.display_name
        self.id = user.id 