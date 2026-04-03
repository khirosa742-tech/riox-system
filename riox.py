import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True   # ← أضف هذا السطر
bot = commands.Bot(command_prefix=".", intents=intents)

bot.remove_command('help')

async def main():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")  

    await bot.start("MTQ2ODY5OTE2OTQ1MDYyNzE1NA.Gk_AyF.4fSjtc-r29PEO0DG24FUA8mQBww8uulkN64ca8")

asyncio.run(main())