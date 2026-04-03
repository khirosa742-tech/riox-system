import discord
from discord.ext import commands

class Broadcast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bc")
    @commands.has_permissions(administrator=True)
    async def broadcast_dm(self, ctx, *, message):
        sent = 0
        failed = 0

        for member in ctx.guild.members:
            if not member.bot:
                try:
                    await member.send(message)
                    sent += 1
                except:
                    failed += 1

        await ctx.send(f"📢 تم محاولة الإرسال لكل الأعضاء! ✅ وصل لـ {sent} عضو | ❌ فشل لـ {failed}")

    @commands.command(name="dm")
    @commands.has_permissions(administrator=True)
    async def dm_member(self, ctx, member: discord.Member, *, message):
        try:
            await member.send(message)
            await ctx.send(f"✉️ تم إرسال الرسالة إلى {member.mention}")
        except:
            await ctx.send("❌ لا يمكن إرسال الرسالة")

async def setup(bot):
    await bot.add_cog(Broadcast(bot))