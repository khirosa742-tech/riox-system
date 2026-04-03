import discord
from discord.ext import commands

class HelpSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="🛠️ الإدارة", value="admin"),
            discord.SelectOption(label="📢 البرودكاست", value="broadcast"),
            discord.SelectOption(label="🎵 الموسيقى", value="music"),
            discord.SelectOption(label="🎮 الألعاب", value="games"),
            discord.SelectOption(label="🧩 الألعاب التفاعلية", value="interactive"),
            discord.SelectOption(label="🎁 الغيفاوٍ", value="giveaway"),
            discord.SelectOption(label="🎁 جوائز", value="rewards"),
        ]
        super().__init__(
            placeholder="📂 اختر قسم الأوامر",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="🚀 دليل الأوامر | Help Menu", 
                              description="مرحباً بك في نظام أوامر البوت 🤖\nاختر القسم من القائمة أدناه لتظهر لك جميع الأوامر مع الشرح والأمثلة",
                              color=discord.Color.random())
        embed.set_footer(text="✨ اختر أي قسم لتظهر لك الأوامر الخاصة به")

        if self.values[0] == "admin":
            embed.title = "🛠️ أوامر الإدارة الضخمة"
            embed.color = discord.Color.dark_red()
            embed.description = "كل الأوامر الخاصة بإدارة السيرفر منظمة وكاملة مع أمثلة."
            embed.add_field(name="`.clear <عدد>` 🧹", value="مسح عدد محدد من الرسائل.\nمثال: `.clear 10`", inline=False)
            embed.add_field(name="`.lock` 🔒", value="قفل الشات مؤقتاً.", inline=False)
            embed.add_field(name="`.unlock` 🔓", value="فتح الشات بعد القفل.", inline=False)
            embed.add_field(name="`.protection on/off` 🛡️", value="تفعيل أو تعطيل حماية السيرفر.", inline=False)
            embed.add_field(name="`.ban @user <سبب>` ⛔", value="حظر شخص من السيرفر.\nمثال: `.ban @user سبام`", inline=False)
            embed.add_field(name="`.kick @user <سبب>` 🦵", value="طرد شخص من السيرفر.", inline=False)

        elif self.values[0] == "broadcast":
            embed.title = "📢 أوامر البرودكاست"
            embed.color = discord.Color.orange()
            embed.description = "إرسال رسائل جماعية أو خاصة بشكل منظم وسهل."
            embed.add_field(name="`.bc <رسالة>` 📣", value="إرسال رسالة للجميع في السيرفر.\nمثال: `.bc السلام عليكم`", inline=False)
            embed.add_field(name="`.dm @شخص <رسالة>` ✉️", value="إرسال رسالة خاصة لشخص محدد.", inline=False)

        elif self.values[0] == "music":
            embed.title = "🎵 أوامر الموسيقى الاحترافية"
            embed.color = discord.Color.blue()
            embed.description = "تشغيل الأغاني والتحكم الكامل بالصوت بطريقة سهلة."
            embed.add_field(name="`.play <رابط>` ▶️", value="تشغيل الأغنية من اليوتيوب أو رابط مباشر.\nمثال: `.play https://youtu.be/xxxx`", inline=False)
            embed.add_field(name="`.stop` ⏹️", value="إيقاف الأغنية الحالية.", inline=False)
           
        elif self.values[0] == "games":
            embed.title = "🎮 أوامر الألعاب الضخمة"
            embed.color = discord.Color.green()
            embed.description = "كل الألعاب والأوامر الترفيهية مرتبة وجاهزة للعب."
            embed.add_field(name="`.سحب` 🎰", value="السحب العشوائي للألعاب أو الجوائز.\nمثال: `.سحب`", inline=False)
            embed.add_field(name="`.لغز` ❓", value="طرح لغز عشوائي وحله.\nمثال: `.لغز`", inline=False)
            embed.add_field(name="`.كلمة` 🔗", value="لعبة الكلمات المتسلسلة.\nمثال: `.كلمة`", inline=False)

        elif self.values[0] == "interactive":
            embed.title = "🧩 الألعاب التفاعلية"
            embed.color = discord.Color.purple()
            embed.description = "ألعاب ممتعة وتفاعلية لتسلية الأعضاء."
            embed.add_field(name="`.riddle` ❓", value="حل لغز عشوائي.", inline=False)
            embed.add_field(name="`.wordchain` 🔗", value="لعبة الكلمات المتسلسلة.", inline=False)
            embed.add_field(name="`.quiz` 📝", value="مسابقة أسئلة معلومات عامة.", inline=False)
            embed.add_field(name="`.trivia` 🏆", value="مسابقة معلومات عامة مع نقاط.", inline=False)

        elif self.values[0] == "giveaway":
            embed.title = "🎁 أوامر الغيفاوٍ"
            embed.color = discord.Color.gold()
            embed.description = "إدارة السحوبات والهدايا بسهولة."
            embed.add_field(name="`.giveaway <الوقت> <الجائزة>` 🎉", value="بدء سحب تلقائي.\nمثال: `.giveaway 60 Nitro`", inline=False)
            embed.add_field(name="`.reroll` 🔄", value="إعادة سحب للفائز.", inline=False)
            embed.add_field(name="`.end` 🛑", value="إنهاء السحب قبل الوقت المحدد.", inline=False)

        await interaction.response.edit_message(embed=embed, view=self.view)

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HelpSelect())

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="🚀 دليل الأوامر | Help Menu",
            description="مرحباً بك في نظام أوامر البوت 🤖\n📂 اختر القسم من القائمة أدناه لتظهر لك جميع الأوامر مع الأمثلة والشرح.",
            color=discord.Color.blurple()
        )
        embed.set_footer(text="✨ اختر أي قسم لتظهر لك الأوامر الخاصة به")
        await ctx.send(embed=embed, view=HelpView())

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
