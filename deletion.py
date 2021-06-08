from discord.message import Message

class Deletion:
    def __init__(self, message: Message, remainingTime: int):
        self.message = message
        self.remainingTime = remainingTime
    
    async def update(self):
        self.remainingTime = self.remainingTime - 1
        if (self.remainingTime <= 0):
            await self.message.delete()
            return True
        else:
            return False
