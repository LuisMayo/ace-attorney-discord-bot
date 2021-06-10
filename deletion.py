from discord.message import Message

class Deletion:
    def __init__(self, message: Message, remainingTime: int):
        self.message = message
        self.remainingTime = remainingTime
    
    async def update(self):
        self.remainingTime = self.remainingTime - 1
        if (self.remainingTime <= 0):
            try:
                await self.message.delete()
            except Exception as exception:
                print(f"Error: {exception}")
            finally:
                return True
        else:
            return False
