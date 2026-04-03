import discord
from discord.ext import commands

TICKET_CATEGORY_NAME = "Tickets"
SUPPORT_ROLE_ID = 1454568405217575023  # ID رول فريق الدعم

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 فتح تكت", style=discord.ButtonStyle.green, custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        category = discord.utils.get(guild.categories, name=TICKET_CATEGORY_NAME)
        if category is None:
            category = await guild.create_category(TICKET_CATEGORY_NAME)

        for channel in category.channels:
            if channel.name == f"ticket-{user.id}":
                await interaction.response.send_message(
                    "❌ عندك تكت مفتوح بالفعل.", ephemeral=True
                )
                return

        support_role = guild.get_role(SUPPORT_ROLE_ID)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True),
            support_role: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{user.id}",
            category=category,
            overwrites=overwrites
        )

        await channel.send(
            f"🎟️ أهلًا {user.mention}\n"
            f"{support_role.mention} تم إشعار فريق الدعم لمتابعة التكت.\n"
            "اكتب مشكلتك هنا، وسيتم الرد عليك قريبًا.",
            view=CloseTicketView()
        )

        await interaction.response.send_message(
            f"✅ تم فتح التكت: {channel.mention}", ephemeral=True
        )

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 إغلاق التكت", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("⏳ سيتم إغلاق التكت...", ephemeral=True)
        await interaction.channel.delete()


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ticket")
    @commands.has_permissions(administrator=True)
    async def ticket(self, ctx):
        embed = discord.Embed(
            title="🎫 نظام التكت الخاص بالسيرفر",
            description="مرحبًا! اختر الخيار المناسب أدناه لفتح تكت.",
            color=discord.Color.blue()
        )

        embed.add_field(name="💬 فتح تكت حول", value="لطرح مشاكلك أو استفساراتك", inline=False)
        embed.add_field(name="🏆 استلام جوائز", value="للحصول على الجوائز أو الهدايا", inline=False)
        embed.add_field(name="⚙️ مشاكل إدارة", value="للتواصل مع الإدارة حول أي مشاكل", inline=False)
        embed.add_field(name="💡 أفكار واقتراحات", value="لإرسال أفكارك وملاحظاتك", inline=False)
        embed.add_field(name="🤝 شراكة", value="للتعاون والشراكات مع السيرفر", inline=False)

        embed.set_thumbnail(url="https://i.imgur.com/your_image.png")  
        embed.set_footer(text="نظام التكت الخاص بالسيرفر")

        await ctx.send(embed=embed, view=TicketView())

    # ==========================================
    # Listener جديد داخل الكوج لمراقبة "استلام"
    # ==========================================
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # تحقق أن القناة تكت
        if message.channel.name.startswith("ticket-"):
            support_role = message.guild.get_role(SUPPORT_ROLE_ID)
            if support_role in message.author.roles:
                if "استلام" in message.content:
                    await message.channel.send(
                        f"✅ تم استلام التكت من قبل {message.author.mention}"
                    )

async def setup(bot):
    await bot.add_cog(Ticket(bot))
    bot.add_view(TicketView())
    bot.add_view(CloseTicketView())
