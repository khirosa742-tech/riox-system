import discord
from discord.ext import commands

class Protection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enabled = False

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def protection(self, ctx, mode):
        if mode == "on":
            self.enabled = True
            await ctx.send("🛡️ تم تشغيل الحماية")
        elif mode == "off":
            self.enabled = False
            await ctx.send("❌ تم إيقاف الحماية")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.enabled and member.bot:
            await member.kick(reason="Protection enabled")


async def setup(bot):
    await bot.add_cog(Protection(bot))