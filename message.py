from discord import Message
import re
from emoji.core import demojize
import requests
from objection_engine.beans.comment import Comment

class Message:
    def __init__(self, update: Message):
        try:
            self.user = User(update.guild.get_member(update.author.id))
        except Exception as e:
            self.user = User(update.author)
            print(e)
        self.evidence = None
        tmp = update.clean_content
        tmp = re.sub(r'(https?)\S*', '(link)', tmp) # links
        tmp = demojize(tmp)
        tmp = re.sub(r'<[a]?:\w{2,32}:\d{18}>', '', tmp) # custom static and animated emojis
        tmp = re.sub(r':\w{2,32}:', '', tmp) # stock emojis
        tmp = re.sub(r'​', '', tmp) # @everyone, @here 
        for file in update.attachments: # attachments
            if file.filename.split('.')[-1] in {'jpg', 'jpeg', 'JPG', 'JPEG', 'png', 'PNG'}:
                tmp += ' (image)'
                name = str(file.id) + '.png'
                response = requests.get(file.url)
                with open(name, 'wb') as file:
                    file.write(response.content)
                self.evidence = name
            elif file.filename.split('.')[-1] in {'gif', 'gifv'}:
                tmp += ' (gif)'
            elif file.filename.split('.')[-1] in {'mp4', 'webm'}:
                tmp += ' (video)'
            elif file.filename.split('.')[-1] in {'mp3', 'wav', 'ogg'}:
                tmp += ' (audio)'
            else:
                tmp += ' (file)'
        self.text = tmp
    def to_Comment(self):
        return Comment(user_id=self.user.id, user_name=self.user.name, text_content=self.text, evidence_path=self.evidence)

class User:
    def __init__(self, user):
        self.name = user.display_name
        self.id = user.id
