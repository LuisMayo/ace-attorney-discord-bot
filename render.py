import textwrap

from discord.ext.commands import Context
from discord.message import Message
from enum import Enum
from objection_engine.beans.comment import Comment
from typing import List

class State(Enum):
    QUEUED = 0
    INPROGRESS = 1
    FAILED = 2
    RENDERED = 3
    DONE = 4

class Render:
    def __init__(self, state: State, discordContext: Context, feedbackMessage: Message, messages: List[Comment]):
        self.state = state
        self.discordContext = discordContext
        self.feedbackMessage = feedbackMessage
        self.messages = messages
        self.outputFilename = f"{str(discordContext.message.id)}.mp4"

    def getState(self):
        return self.state
        
    def getContext(self):
        return self.discordContext

    def getFeedbackMessage(self):
        return self.feedbackMessage

    def getMessages(self):
        return self.messages

    def getOutputFilename(self):
        return self.outputFilename

    def setState(self, state: State):
        self.state = state
        
    async def updateFeedback(self, newContent: str):
        try:
            # If it's unable to edit/get the feedback message, that means that it no longer exists
            if self.feedbackMessage.content != textwrap.dedent(newContent):
                await self.feedbackMessage.edit(content=textwrap.dedent(newContent))
        except Exception as exception:
            # If it doesn't exists, we will repost it.
            print(f"Error: {exception}")
            self.feedbackMessage = await self.discordContext.send(content=textwrap.dedent(newContent))