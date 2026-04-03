import discord
from discord.ext import commands
import asyncio
import random

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_giveaways = {}  # لتخزين الرسائل النشطة

    @commands.command(name="giveaway")
    async def giveaway(self, ctx, minutes: int, *, prize: str):
        if minutes <= 0:
            return await ctx.send("❌ يجب أن يكون الوقت أكبر من 0 دقيقة.")

        total_seconds = minutes * 60

        embed = discord.Embed(
            title="🎉🎁 GIVEAWAY 🎁🎉",
            description=f"🏆 **الجائزة:** {prize}\n⏳ **ينتهي بعد:** {self.format_time(total_seconds)}\n🎉 اضغط على الرياكشن للمشاركة!",
            color=0x2ecc71  # أخضر في البداية
        )
        embed.set_footer(text=f"بدأ بواسطة {ctx.author}", icon_url=ctx.author.avatar.url)

        message = await ctx.send("@everyone @here 🎉 غيف أواي جديد!", embed=embed)
        await message.add_reaction("🎉")

        # حفظ الغيف أواي النشط
        self.active_giveaways[message.id] = {
            "channel": ctx.channel.id,
            "prize": prize,
            "author": ctx.author.id,
            "time": total_seconds
        }

        # تشغيل المؤقت في الخلفية
        self.bot.loop.create_task(self.run_giveaway(message.id))

    async def run_giveaway(self, message_id):
        giveaway = self.active_giveaways.get(message_id)
        if not giveaway:
            return

        channel = self.bot.get_channel(giveaway["channel"])
        if not channel:
            return

        try:
            message = await channel.fetch_message(message_id)
        except:
            return

        time_left = giveaway["time"]
        emoji = "🎉"

        while time_left > 0:
            # تغيير اللون إذا تبقى أقل من دقيقة
            color = 0xe74c3c if time_left <= 60 else 0x2ecc71  # أحمر أقل من دقيقة، أخضر بخلاف ذلك

            # تحديث الـ embed
            embed = discord.Embed(
                title="🎉🎁 GIVEAWAY 🎁🎉",
                description=f"🏆 **الجائزة:** {giveaway['prize']}\n⏳ **ينتهي بعد:** {self.format_time(time_left)}\n🎉 اضغط على الرياكشن للمشاركة!",
                color=color
            )
            embed.set_footer(text=f"بدأ بواسطة <@{giveaway['author']}>")
            await message.edit(embed=embed)

            # تنبيه صوتي عن طريق رسالة mention @everyone عند الدقيقة الأخيرة
            if time_left == 60:
                await channel.send("||@everyone @here||\n# ⏰ دقيقة واحدة متبقية على انتهاء الغيف أواي!")

            await asyncio.sleep(1)
            time_left -= 1

        # انتهاء الغيف أواي
        users = []
        for reaction in message.reactions:
            if str(reaction.emoji) == emoji:
                async for user in reaction.users():
                    if not user.bot and user.id != giveaway["author"]:
                        users.append(user)

        if not users:
            await channel.send("❌ لم يشارك أحد في الغيف أواي 😢")
            self.active_giveaways.pop(message_id)
            return

        winner = random.choice(users)
        end_embed = discord.Embed(
            title="🎊 GIVEAWAY ENDED 🎊",
            description=f"🏆 **الجائزة:** {giveaway['prize']}\n👑 **الفائز:** {winner.mention}\n👥 عدد المشاركين: {len(users)}",
            color=0xe67e22
        )

        await channel.send(embed=end_embed)
        self.active_giveaways.pop(message_id)

    def format_time(self, seconds):
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}:{secs:02}"  # صيغة MM:SS

async def setup(bot):
    await bot.add_cog(Giveaway(bot))
