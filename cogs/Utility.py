from discord.ext import commands, tasks
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
    self.create_channels.start()
    
  # Help Command -> get Support
  @app_commands.command(description="bot help")
  async def help(self, interaction: discord.Interaction):
    description = "For help and Support, please contact the System Administrators!\n\n"
    description += "<:discord:1216307276927733800> <@324607583841419276>\n"
    description += "<:discord:1216307276927733800> <@818879706350092298>\n"
    description += "📧 brawltourneysystem@gmail.com"
    embed = discord.Embed(title="SUPPORT", description=description, color=int("000000", 16))
    embed.set_image(url="https://media.discordapp.net/attachments/1216040586348593213/1217918220539789382/BTSystem_Logo.jpg")
    viewItems = [LinkButton("Linktree", "https://linktr.ee/bsystems")]
    await interaction.response.send_message(embed=embed, view=View(viewItems))


  # Invite Command -> get Link
  @app_commands.command(description="get link")
  async def invite(self, interaction: discord.Interaction):
    description = "make use of Cross Server Team Search!\n"
    embed = discord.Embed(title="<:discord:1216307276927733800>  Invite me to your Server!", description=description, color=int("000000", 16))
    viewItems = [LinkButton("Invite me!", "https://discord.com/oauth2/authorize?client_id=1223344546260193280&permissions=8&scope=bot")]
    await interaction.response.send_message(embed=embed, view=View(viewItems))
  

  #loop for creating channels
  @tasks.loop(minutes=1)
  async def create_channels(self):
    for guild in self.bot.guilds:
      # Kategorie erstmal finden
      findMatesCategory = discord.utils.find(guild.categories, name="FIND MATES")
      # Erstellen falls nicht da
      if not findMatesCategory:
        findMatesCategory = await guild.create_category_channel("FIND MATES")
        # Kanäle erstellen
        onlyRead = {
          guild.default_role: discord.PermissionOverwrite(send_messages=False),
        }
        await findMatesCategory.create_text_channel("find-mates", overwrites=onlyRead, topic="find a team to join in this channel")
        await findMatesCategory.create_text_channel("search-mates", topic="run /find_mates to post your search!")


async def setup(bot):
  await bot.add_cog(Utility(bot))