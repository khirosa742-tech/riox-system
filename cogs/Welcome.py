import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO
import requests

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1392409832413331537
        self.invites = {}


    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            try:
                self.invites[guild.id] = await guild.invites()
            except:
                pass

    @commands.Cog.listener()
    async def on_member_join(self, member):

        if not self.channel_id:
            return

        channel = member.guild.get_channel(self.channel_id)
        if not channel:
            return

        inviter = "غير معروف"
        try:
            new_invites = await member.guild.invites()
            old_invites = self.invites.get(member.guild.id, [])

            for invite in new_invites:
                for old in old_invites:
                    if invite.code == old.code and invite.uses > old.uses:
                        inviter = invite.inviter.mention

            self.invites[member.guild.id] = new_invites
        except:
            pass

        template_path = os.path.join(os.path.dirname(__file__), "welcome_template.png")
        background = Image.open(template_path).convert("RGBA")
        bg_width, bg_height = background.size

        avatar_url = member.display_avatar.url
        response = requests.get(avatar_url)
        avatar = Image.open(BytesIO(response.content)).convert("RGBA")

        avatar_size = 300
        avatar = avatar.resize((avatar_size, avatar_size))

        mask = Image.new("L", (avatar_size, avatar_size), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, avatar_size, avatar_size), fill=255)
        avatar.putalpha(mask)

        pos_x = (bg_width - avatar_size) // 2
        pos_y = (bg_height - avatar_size) // 2 - 70

        background.paste(avatar, (pos_x, pos_y), avatar)

        draw = ImageDraw.Draw(background)
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()

        text_x = bg_width // 2      # يمين / يسار
        text_y = bg_height - 290    # فوق / تحت

        draw.text(
       (text_x + 4, text_y + 4),
        member.name,
        font=font,
        fill=(0, 0, 0),
        anchor="mm"
    )

# 🔹 تخشين النص (نرسمه عدة مرات)
        for offset_x in range(-2, 3):
            for offset_y in range(-2, 3):
                draw.text(
                    (text_x + offset_x, text_y + offset_y),
                    member.name,
                    font=font,
                    fill=(70, 130, 180),  # ازرق بارد
                    anchor="mm"
                )



        buffer = BytesIO()
        background.save(buffer, format="PNG")
        buffer.seek(0)

        await channel.send(
            content=(
                f"🎉 أهلاً {member.mention}\n"
                f"مرحبا في سيرفر riox family نتمنى لك وقت جميلا و سعيدا\n"
                f"🔹 تمت دعوتك بواسطة: {inviter}"
            ),
            file=discord.File(buffer, filename=f"welcome_{member.id}.png")
        )


async def setup(bot):
    await bot.add_cog(Welcome(bot))
