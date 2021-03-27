from discord import Message
import re

class Message:
    def __init__(self, update: Message):
        self.user = User(update.author)
        tmp = update.clean_content
        tmp = re.sub(r'<:\w{2,32}:\d{18}>', '', tmp) # emojis
        tmp = re.sub(r'(https?)\S*', '(link)', tmp) # links
        for file in update.attachments: # attachments
            if file.filename.split('.')[-1] in {'jpg', 'jpeg', 'JPG', 'JPEG', 'png', 'PNG'}:
                tmp += ' (image)'
            elif file.filename.split('.')[-1] in {'gif', 'gifv'}:
                tmp += ' (gif)'
            elif file.filename.split('.')[-1] in {'mp4', 'webm'}:
                tmp += ' (video)'
            elif file.filename.split('.')[-1] in {'mp3', 'wav', 'ogg'}:
                tmp += ' (audio)'
            else:
                tmp += ' (file)'
        self.text = tmp

class User:
    def __init__(self, user):
        self.name = user.display_name
        self.id = user.id 