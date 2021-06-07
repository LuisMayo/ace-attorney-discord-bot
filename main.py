import re
import random
import os
import sys
sys.path.insert(0, './objection_engine')
import yaml
import discord
from discord.ext import commands, tasks
from message import Message
import threading
import asyncio
from objection_engine.renderer import render_comment_list
from objection_engine.beans.comment import Comment
from typing import List
import requests

currentActivity = ""

# queue Lists
videoRenderQueue = []
messageQueue = []
deletionQueue = []

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' is missing!")
else:
    with open("config.yaml") as file:
        configuration = yaml.load(file, Loader=yaml.FullLoader)
        token = configuration["token"].strip()
        prefix = configuration["prefix"].strip()
        deletionDelay = configuration["deletionDelay"].strip()

if not token:
    sys.exit("The 'token' is missing in the 'config.yaml' file!")
if not prefix:
    sys.exit("The 'prefix' is missing in the 'config.yaml' file!")
if not deletionDelay:
    sys.exit("The 'deletionDelay' is missing in the 'config.yaml' file!")

client = commands.AutoShardedBot(command_prefix=prefix, intents=discord.Intents.default())

# Removing default help command
client.remove_command("help")

async def changeActivity(text):
    try:
        global currentActivity

        if currentActivity == text:
            return
        else:    
            activity = discord.Game(text)
            await client.change_presence(activity=activity)
            currentActivity = text
            print(f"Activity changed to {currentActivity}")
    except Exception as e:
        pass

@client.event
async def on_ready():
    messageLoop.start()
    print("Bot is ready!")
    print(f"Logged in as {client.user.name}#{client.user.discriminator} ({client.user.id})")

@client.event
async def on_message(message):
    # Ignore message if the author is a bot (or the client's logged user)
    if message.author is client.user or message.author.bot:
        return
    if message.channel.type is discord.ChannelType.private:
        embedResponse = discord.Embed(description="I won't process any messages via PM.\nIf you have any problem please go to [the support server](https://discord.gg/pcS4MPbRDU).", color=0xff0000)
        await message.channel.send(embed=embedResponse)
        return

    await client.process_commands(message)

@client.command()
async def help(context):
    dummyAmount = random.randint(2, 150)
    embedHelp = discord.Embed(description="Discord bot that turns message chains into ace attorney scenes.", color=0x3366CC, footer="Do not include these symbols (\"<\" and \">\") when using this command")
    embedHelp.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    embedHelp.add_field(name="How to use?", value=f"`{prefix}render <number_of_messages>`", inline=False)
    embedHelp.add_field(name="Example", value=f"Turn the last {dummyAmount} messages into an ace attorney scene: `{prefix}render {dummyAmount}`", inline=False)
    embedHelp.add_field(name="Starting message", value="By default the bot will load the specified number of messages from the last message (before using the command) going backwards, if you want the message count to start from another message, reply to it when using the command.", inline=False)
    await context.send(embed=embedHelp)

@client.command()
async def render(context, numberOfMessages):
    feedbackMessage = await context.send(content="`Fetching messages...`")
    if numberOfMessages.isdigit() and int(numberOfMessages) in range (1, 151):
        messages = []
        async for message in context.channel.history(limit=int(numberOfMessages), oldest_first=False, before=context.message.reference.resolved if context.message.reference else context.message):
            msg = Message(message)
            if msg.text.strip():
                messages.insert(0, msg.to_Comment())

        if (len(messages) >= 1): 
            
            await feedbackMessage.edit(content="`Fetching messages... Done!`\n`Queued, please wait...`\n")
            videoRender = (False, message.id, messages, "")
            videoRenderQueue.append(videoRender)
            newMessage = (message, context, feedbackMessage.id)
            messageQueue.append(newMessage)
        else:
            embedResponse = discord.Embed(description="There should be at least one person in the conversation", color=0xff0000)
            await feedbackMessage.edit(content="", embed=embedResponse, mention_author=False)
    else:
        embedResponse = discord.Embed(description="Number of messages must be between 1 and 150", color=0xff0000)
        await feedbackMessage.edit(content="", embed=embedResponse, mention_author=False)
        return

def clean(thread: List[Comment], output_filename):
    try:
        os.remove(output_filename)
    except Exception as second_e:
        print(second_e)
    try:
        for comment in thread:
            if (comment.evidence_path is not None):
                os.remove(comment.evidence_path)
    except Exception as second_e:
        print(second_e)

def rendererCall():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(backgroundRenderer())
    loop.close()

async def backgroundRenderer():
    while True:
        try:
            length = len(videoRenderQueue)
            if length <= 0:
                continue
            for index in range(length):
                videoRender = videoRenderQueue[index]
                if videoRender[0] == False:
                    try:
                        output_filename = str(videoRender[1]) + '.mp4'
                        render_comment_list(videoRender[2], output_filename)

                        newVideoRenderTuple = (True, videoRender[1], videoRender[2], output_filename)
                        videoRenderQueue.remove(videoRender)
                        videoRenderQueue.insert(index, newVideoRenderTuple)
                    except Exception as e:
                        newVideoRenderTuple = (True, videoRender[1], videoRender[2], f"failed {e}")
                        videoRenderQueue.remove(videoRender)
                        videoRenderQueue.insert(index, newVideoRenderTuple)
        except Exception as e:
            pass

@tasks.loop(seconds=1)
async def messageLoop():
    await changeActivity(f"{prefix}help | queue: {len(messageQueue)}")
    try:
        length = len(messageQueue)
        if length > 0:
            for index in range(length-1, -1, -1):
                currentMessage = messageQueue[index]
                message = currentMessage[0]
                context = currentMessage[1]
                feedbackMessageId = currentMessage[2]
                feedbackMessage = await context.channel.fetch_message(feedbackMessageId)

                if index == 0:
                    # Updates message (only if it hasn't already been updated) to reflect that it's first in the queue. 
                    newContent = "`Fetching messages... Done!`\n`Your video is being generated...`\n"
                    if feedbackMessage.content != newContent:
                        await feedbackMessage.edit(content = newContent)
                    
                for videoRender in videoRenderQueue:
                    if videoRender[1] == message.id:
                        if videoRender[0]:
                            fileSizeBytes = 0
                            try:
                                if re.match("^failed\s", videoRender[3]):
                                    await feedbackMessage.edit(content=f"`Fetching messages... Done!`\n`Your video is being generated... Failed!`")
                                    error = re.sub("^failed", "", videoRender[3])
                                    embedResponse = discord.Embed(description=f"Error: {error}", color=0xff0000)
                                    errorMessage = await context.send(embed=embedResponse)
                                    messageToBeDeleted = (context, errorMessage.id, int(deletionDelay))
                                    deletionQueue.append(messageToBeDeleted)
                                else:
                                    await feedbackMessage.edit(content=f"`Fetching messages... Done!`\n`Your video is being generated... Done!`\n`Uploading file to Discord...`")
                                    fileSizeBytes = round((os.path.getsize(videoRender[3])/1000000), 2)
                                    if (fileSizeBytes) >= 8:
                                        raise Exception()
                                    else:
                                        await context.send(file=discord.File(videoRender[3]))
                                        await feedbackMessage.edit(content=f"`Fetching messages... Done!`\n`Your video is being generated... Done!`\n`Uploading file to Discord... Done!`")
                            except Exception as e:
                                try:
                                    try:
                                        if (fileSizeBytes) >= 8:
                                            await feedbackMessage.edit(content=f"`Fetching messages... Done!`\n`Your video is being generated... Done!`\n`Video file too big for discord! ({fileSizeBytes} MB)`\n`Trying to upload file to an external server...`")
                                            with open(videoRender[3], 'rb') as videoFile:
                                                files = {'files[]': (videoRender[3], videoFile)}
                                                response = requests.post('https://tmp.ninja/upload.php?output=text', files=files)
                                            await feedbackMessage.edit(content=f"`Fetching messages... Done!`\n`Your video is being generated... Done!`\n`Video file too big for discord! ({fileSizeBytes} MB)`\n`Trying to upload file to an external server... Done!`")
                                            url = response.content.decode("utf-8").strip()
                                            await context.send(content=f"{url}\n_This video will be deleted in 48 hours_")
                                        else:
                                            raise Exception(e)
                                    except Exception as e:
                                        await feedbackMessage.edit(content=f"`Fetching messages... Done!`\n`Your video is being generated... Done!`\n`Video file too big for discord! ({fileSizeBytes} MB)`\n`Trying to upload file to an external server... Failed!`")
                                        embedResponse = discord.Embed(description=f"Error: {e}", color=0xff0000)
                                        errorMessage = await context.send(embed=embedResponse)
                                        messageToBeDeleted = (context, errorMessage.id, int(deletionDelay))
                                        deletionQueue.append(messageToBeDeleted)
                                except Exception:
                                    pass
                            
                            # The "feedback" message is added to the deletion queue
                            messageToBeDeleted = (context, feedbackMessageId, int(deletionDelay))
                            deletionQueue.append(messageToBeDeleted)

                            # clean function called
                            clean(videoRender[2], videoRender[3])

                            # both the video and the message are removed from the queue, once posted/failed
                            videoRenderQueue.remove(videoRender)
                            messageQueue.remove(currentMessage)
                            
                            break
    except Exception as e:
        pass
    try:
        if int(deletionDelay) > 0:
            length = len(deletionQueue)
            if length > 0:
                for index in range(length-1, -1, -1):
                    if (index > len(deletionQueue)-1):
                        break
                    currentMessage = deletionQueue[index]
                    newMessageTuple = (currentMessage[0], currentMessage[1], int(currentMessage[2])-1)
                    deletionQueue.remove(currentMessage)
                    if (int(newMessageTuple[2]) > 0):
                        deletionQueue.insert(index, newMessageTuple)
                    else:
                        message = await currentMessage[0].channel.fetch_message(currentMessage[1])
                        await message.delete()
                        index = index - 1
    except Exception as e:
        pass
                    

th = threading.Thread(target=rendererCall)
th.start()

client.run(token)
th.join()
