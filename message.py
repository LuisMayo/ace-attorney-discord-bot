from discord import Message
import re

class Message:
    def __init__(self, update: Message):
        self.user = User(update.author)
        text_temp = update.clean_content
        text_temp = re.sub(r'<:\w{2,32}:\d{18}>', '', text_temp) # emojis
        text_temp = re.sub(r'(https?)\S*', '(link)', text_temp) # links
        self.text = text_temp

class User:
    def __init__(self, user):
        self.name = user.display_name
        self.id = user.id 