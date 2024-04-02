from discord.ext import commands
import discord
from discord import app_commands
import mongodb

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


# SelectLanguage Klasse
class SelectLanguage(discord.ui.Select):
    def __init__(self, bot, originalInteraction):
        options = [
            discord.SelectOption(label="German", emoji="🇩🇪", value="German 🇩🇪"),
            discord.SelectOption(label="English", emoji="🇬🇧", value="English 🇬🇧"),
            discord.SelectOption(label="Spanish", emoji="🇪🇸", value="Spanish 🇪🇸"),
            discord.SelectOption(label="French", emoji="🇫🇷", value="French 🇫🇷"),
            discord.SelectOption(label="Russian", emoji="🇷🇺", value="Russian 🇷🇺")
        ]
        
        super().__init__(placeholder="Select a language", options=options)
        self.bot = bot
        self.originalInteraction = originalInteraction

    async def callback(self, interaction: discord.Interaction):
        guild_options = mongodb.findGuildOptions(interaction.guild.id)

        guild_options["language"] = self.values[0].lower().split(" ")[0]
        mongodb.saveGuild(guild_options)
        await self.originalInteraction.edit_original_response(embed=currentSettingEmbed(interaction.guild.id))
        await interaction.response.defer()

        # Channel Names umbenennen

def getNiceFormatLanguage(language):
    if language == "german":
      return "German 🇩🇪"
    elif language == "english":
      return "English 🇬🇧"
    elif language == "spanish":
      return "Spanish 🇪🇸"
    elif language == "russian":
       return "Russian 🇷🇺"
    else:
      return "French 🇫🇷",

def currentSettingEmbed(guild_id):
  guild_options = mongodb.findGuildOptions(guild_id)
  # Sprache anzeigen
  description = f"{getNiceFormatLanguage(guild_options['language'])}"
  
  return discord.Embed(title="Current Language", description=description, color=discord.Color.dark_gray())


class Utility(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    
  # Öffnet Server Einstellungen
  @app_commands.checks.has_permissions(administrator=True, manage_channels=True)
  @app_commands.command(description="sets the language")
  async def set_language(self, interaction: discord.Interaction):
    viewItems = [SelectLanguage(self.bot, interaction)]
    await interaction.response.send_message(embed=currentSettingEmbed(interaction.guild.id), view=View(viewItems), ephemeral=True)


  @set_language.error
  async def set_language_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
      return await interaction.response.send_message("Only the Bot Admins can use this command.", delete_after=5, ephemeral=True)
    elif isinstance(error, app_commands.NoPrivateMessage):
      return await interaction.response.send_message("Command can't be run in Private Messages.", delete_after=5, ephemeral=True)
    else:
      return await interaction.response.send_message(f"Unknown error: {error}", delete_after=5, ephemeral=True)


  # Help Command -> get Support
  @app_commands.command(description="bot help")
  async def help(self, interaction: discord.Interaction, hey : str):
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
    description = "- Make use of FREE Cross Server Team Search!\n"
    description += "- Keep track of current and upcoming maps!\n"
    description += "- Enjoy FREE profile images!"
    embed = discord.Embed(title="<:discord:1216307276927733800>  Invite me to your Server!", description=description, color=int("ffffff", 16))
    viewItems = [LinkButton("Invite me!", "https://discord.com/oauth2/authorize?client_id=1223344546260193280&permissions=8&scope=bot")]
    await interaction.response.send_message(embed=embed, view=View(viewItems))


async def setup(bot):
  await bot.add_cog(Utility(bot))