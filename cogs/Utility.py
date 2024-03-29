from discord.ext import commands
import discord
from discord import app_commands

format = "%a, %d %b %Y, %H:%M"

# LinkButton Klasse
class LinkButton(discord.ui.Button):
  def __init__(self, label, url):
    super().__init__(label=label, style=discord.ButtonStyle.link, url=url)


# View Klasse zum Anzeigen der Items wie Buttons und Auswahllisten
class View(discord.ui.View):
    def __init__(self, items):
        super().__init__(timeout=None)
        for item in items:
            self.add_item(item)


class Utility(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    
  # Help Command -> get Support
  @app_commands.command(description="bot help")
  async def help(self, interaction: discord.Interaction):
    description = "For help and Support, please contact the System Administrators!\n\n"
    description += "<:discord:1216307276927733800> <@324607583841419276>\n"
    description += "<:discord:1216307276927733800> <@818879706350092298>\n"
    embed = discord.Embed(title="SUPPORT", description=description, color=int("ffffff", 16))
    embed.set_image(url="https://media.discordapp.net/attachments/1216040586348593213/1223366470088790046/bms_avatar.jpg")
    viewItems = [LinkButton("Linktree", "https://linktr.ee/bsystems")]
    await interaction.response.send_message(embed=embed, view=View(viewItems))


  # Invite Command -> get Link
  @app_commands.command(description="get link")
  async def invite(self, interaction: discord.Interaction):
    description = "- Keep track of current and upcoming maps!\n"
    description += "- Make use of FREE Cross Server Team Search!\n"
    description += "- Enjoy FREE profile images!"
    embed = discord.Embed(title="<:discord:1216307276927733800>  Invite me to your Server!", description=description, color=int("ffffff", 16))
    viewItems = [LinkButton("Invite me!", "https://discord.com/oauth2/authorize?client_id=1223344546260193280&permissions=8&scope=bot")]
    await interaction.response.send_message(embed=embed, view=View(viewItems))


async def setup(bot):
  await bot.add_cog(Utility(bot))