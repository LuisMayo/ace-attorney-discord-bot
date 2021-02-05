import sys
sys.path.insert(0, './ace-attorney-bot')
import anim
import discord
import re
from message import Message
from collections import Counter
from comment_bridge import Comment
import os


with open('token.txt', 'r') as tokenFile:
    token = tokenFile.read().replace('\r', '').replace('\n', '')



client = discord.Client()

@client.event
async def on_message(mention: discord.Message):
    if mention.author == client.user:
        return

    match = re.match(r'!render (\d+)', mention.content)
    if match:
        number = int(match.group(1))
        messages = []
        async for message in mention.channel.history(limit=number, oldest_first=False, before=mention):
            messages.insert(0, Message(message))
        
        thread = []
        users_to_names = {}
        counter = Counter()
        for message in messages:
            thread.append(Comment(message))
            users_to_names[message.user.id] = message.user.name
            counter.update({message.user.id: 1})
        if (len(users_to_names) >= 2): 
            most_common = [users_to_names[t[0]] for t in counter.most_common()]
            characters = anim.get_characters(most_common)
            output_filename = str(mention.id) + '.mp4'
            anim.comments_to_scene(thread, characters, output_filename=output_filename)
            await mention.channel.send(file=discord.File(output_filename))
            os.remove(output_filename)
        else:
            await mention.channel.send(content='There should be at least two people in the conversation')

client.run(token)
