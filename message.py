from discord import Message
import re

class Message:
    def __init__(self, update: Message):
        try:
            self.user = User(update.guild.get_member(update.author.id))
        except Exception as e:
            print(e)
            self.user = User(update.author)
        self.text = re.sub(r'(https?)\S*', '(link)', update.clean_content)

class User:
    def __init__(self, user):
        self.name = user.display_name
        self.id = user.id
