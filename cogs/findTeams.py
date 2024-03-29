from discord.ext import commands, tasks
import discord, requests, json
from discord import app_commands
from cogs.Utility import View, LinkButton

gamemodes = requests.get("https://api.brawlapi.com/v1/gamemodes").json()["list"]

with open("jsons/env.json", "r", encoding="UTF-8") as f:
  envData = json.load(f)

with open("jsons/modeEmojis.json", "r", encoding="UTF-8") as f:
  modeEmojis = json.load(f)

# Formular to fill out, creates the Search post
class TicketModal(discord.ui.Modal):
  def __init__(self, bot, trophies):
    super().__init__(title="Create Ticket")
    self.bot = bot
    self.trophies = trophies

  trophyRange = discord.ui.TextInput(label="Desired trophy range", style=discord.TextStyle.short, min_length=4, max_length=25, placeholder="e.g. 600-750")
  gameMode = discord.ui.TextInput(label="Game Mode", style=discord.TextStyle.short, min_length=4, max_length=25, placeholder="e.g. knockout")
  region = discord.ui.TextInput(label="Region", style=discord.TextStyle.short, min_length=4, max_length=25, placeholder="EMEA/NA/SA/APAC")
  teamCode = discord.ui.TextInput(label="Team Code", style=discord.TextStyle.short, min_length=4, max_length=25, placeholder="X??????")


  async def on_submit(self, interaction: discord.Interaction):
    desiredMode = None
    for mode in gamemodes:
      if mode["name"].lower().replace(" ", "") == self.gameMode.lower().replace(" ", ""):
        desiredMode = mode["name"]
    
    if not desiredMode:
      return await interaction.response.send_message("Could not find desired gamemode. ")
    
    user = interaction.user
    searchPost = f"<a:Announcement:1216306085565042710> {user} is looking for Mates"
    searchPost += f"<:right_arrow:1216305900961271859> <:Trophy:1223277455821902046> {self.trophies}"
    searchPost += f"<:right_arrow:1216305900961271859> <:list:1216305645083689111> {self.trophyRange} Lobby"
    searchPost += f"<:right_arrow:1216305900961271859> {modeEmojis[desiredMode]} {desiredMode}"
    searchPost += f"<:right_arrow:1216305900961271859> <a:Global:1223361709729779896> {self.region}"
    searchPost += f"<:right_arrow:1216305900961271859> Team Code: {self.teamCode}"
    JoinButton = LinkButton("Join Team", f"https://link.brawlstars.com/invite/gameroom/en?tag={self.teamCode}")

    findMatesChannel = discord.utils.get(interaction.guild.text_channels, name="find-mates")
    await findMatesChannel.send(searchPost, view=View([JoinButton]))
    

# The Commands
class findTeams(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.create_channels.start()

  @app_commands.command(description="Creates a Support Ticket")
  @app_commands.checks.cooldown(1, 60*5, key=lambda i: (i.guild_id, i.user.id))
  async def find_mates(self, interaction: discord.Interaction, bs_id: str):
    bs_id = bs_id.upper().replace(" ", "").replace("#", "")
    url = f"https://api.brawlstars.com/v1/players/%23{bs_id}"
    headers = {
        "Authorization": f"Bearer {envData['BsApi']}"
    }
    profileData = requests.get(url, headers=headers).json()
    if "trophies" in profileData:
        await interaction.response.send_modal(TicketModal(self.bot, profileData["trophies"]))
    else:
      await interaction.response.send_message(f"No profile found for Id: {bs_id}", ephemeral=True, delete_after=3)

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