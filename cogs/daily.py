import discord
from discord.ext import commands
from datetime import datetime

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.count = {}
        self.date = datetime.now().date()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        today = datetime.now().date()
        if today != self.date:
            self.count = {}
            self.date = today

        user_id = message.author.id
        self.count[user_id] = self.count.get(user_id, 0) + 1

        if self.count[user_id] == 300:
            await message.channel.send(
                f"🎉 مبروك {message.author.mention}! وصلت 300 رسالة\n"
                f"🎟️ افتح تكت واستلم جائزتك"
            )

async def setup(bot):
    await bot.add_cog(Daily(bot))