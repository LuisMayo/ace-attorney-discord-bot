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
    UPLOADING = 4
    DONE = 5

class Render:
    def __init__(self, state: State, discordContext: Context, feedbackMessage: Message, messages: List[Comment]):
        self.state = state
        self.discordContext = discordContext
        self.feedbackMessage = feedbackMessage
        self.messages = messages
        self.outputFilename = f"{str(discordContext.message.id)}.mp4"

    def getStateString(self):
        if self.state == State.QUEUED:
            return "Queued"
        if self.state == State.INPROGRESS:
            return "In progress"
        if self.state == State.FAILED:
            return "Failed"
        if self.state == State.RENDERED:
            return "Rendered"
        if self.state == State.UPLOADING:
            return "Uploading"
        if self.state == State.DONE:
            return "Done"

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
            newContent = textwrap.dedent(newContent).strip("\n")
            # Feedback messages will only be updated if their content is different to the new Content, to avoid spamming Discord's API
            if self.feedbackMessage.content != newContent:
                await self.feedbackMessage.edit(content=newContent)
            # If it's unable to edit/get the feedback message, it will raise an exception and that means that it no longer exists
        except Exception as exception:
            # If it doesn't exists, we will repost it.
            print(f"Error: {exception}")
            self.feedbackMessage = await self.discordContext.send(content=newContent)
