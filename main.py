import random
import os
import sys
sys.path.insert(0, './objection_engine')
import yaml
import discord
from discord.ext import commands
from message import Message
from objection_engine.renderer import render_comment_list
from objection_engine.beans.comment import Comment
from typing import List

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' is missing!")
else:
    with open("config.yaml") as file:
        configuration = yaml.load(file, Loader=yaml.FullLoader)
        token = configuration["token"].strip()
        prefix = configuration["prefix"].strip()

if not token:
    sys.exit("The 'token' is missing in the 'config.yaml' file!")
if not prefix:
    sys.exit("The 'prefix' is missing in the 'config.yaml' file!")

client = commands.Bot(command_prefix=prefix, intents=discord.Intents.default())

# Removing default help command
client.remove_command("help")

@client.event
async def on_ready():
    print("Bot is ready!")
    print(f"Logged in as {client.user.name}#{client.user.discriminator} ({client.user.id})")
    activity = discord.Game(f"{prefix}help")
    await client.change_presence(activity=activity)

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
    if numberOfMessages.isdigit() and int(numberOfMessages) in range (1, 151):
        messages = []
        async for message in context.channel.history(limit=int(numberOfMessages), oldest_first=False, before=context.message.reference.resolved if context.message.reference else context.message):
            msg = Message(message)
            if msg.text.strip():
                messages.insert(0, msg.to_Comment())

        if (len(messages) >= 1): 
            output_filename = str(context.message.id) + '.mp4'
            render_comment_list(messages, output_filename)
            try:
                await context.send(file=discord.File(output_filename))
            except Exception as e:
                try:
                    embedResponse = discord.Embed(description=f"Error: {e}", color=0xff0000)
                    await context.send(embed=embedResponse, mention_author=False)
                except Exception:
                    pass
            clean(messages, output_filename)
        else:
            embedResponse = discord.Embed(description="There should be at least one person in the conversation", color=0xff0000)
            await context.send(embed=embedResponse, mention_author=False)
    else:
        embedResponse = discord.Embed(description="Number of messages must be between 1 and 150", color=0xff0000)
        await context.reply(embed=embedResponse, mention_author=False)
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

client.run(configuration["token"])
