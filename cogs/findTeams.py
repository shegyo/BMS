from discord.ext import commands, tasks
import discord, requests
from discord import app_commands
from cogs.Utility import View

gamemodes = requests.get("https://api.brawlapi.com/v1/gamemodes").json()["list"]


# Formular to fill out, creates the Search post
class TicketModal(discord.ui.Modal):
  def __init__(self, bot):
    super().__init__(title="Create Ticket")
    self.bot = bot

  totalTrophies = discord.ui.TextInput(label="Your total trophies", style=discord.TextStyle.short, required=True, min_length=3, max_length=30, placeholder="e.g. 51.000")
  trophyRange = discord.ui.TextInput(label="Desired trophy range", style=discord.TextStyle.short, min_length=4, max_length=25, placeholder="e.g. 600-750")
  gameMode = discord.ui.TextInput(label="Game Mode", style=discord.TextStyle.short, min_length=4, max_length=25, placeholder="e.g. knockout")
  region = discord.ui.TextInput(label="Region", style=discord.TextStyle.short, min_length=4, max_length=25, placeholder="EMEA/NA/SA/APAC")
  teamCode = discord.ui.TextInput(label="Team Code", style=discord.TextStyle.short, min_length=4, max_length=25, placeholder="X??????")

  async def on_submit(self, interaction: discord.Interaction):
    pass

# The Commands
class findTeams(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.create_channels.start()

  @app_commands.command(description="Creates a Support Ticket")
  @app_commands.checks.cooldown(1, 60*5, key=lambda i: (i.guild_id, i.user.id))
  async def find_mates(self, interaction: discord.Interaction, your_total_trophies: int, trophy_minimum: int, game_mode: str, team_code: str):
    await interaction.response.send_modal(TicketModal(self.bot))

  @find_mates.error
  async def ticket_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)

  

  #loop for creating channels
  @tasks.loop(minutes=1)
  async def create_channels(self):
    for guild in self.bot.guilds:
      # Kategorie erstmal finden
      findMatesCategory = discord.utils.get(guild.categories, name="FIND MATES")
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
  await bot.add_cog(findTeams(bot))