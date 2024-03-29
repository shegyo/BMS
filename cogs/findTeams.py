from discord.ext import commands
import discord, requests, json
from discord import app_commands
from cogs.Utility import View, LinkButton

gamemodes = requests.get("https://api.brawlapi.com/v1/gamemodes").json()["list"]
gamemodes.append({"name" : "Ranked"})
gamemodes.append({"name" : "Friendly Battle"})

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
  region = discord.ui.TextInput(label="Region", style=discord.TextStyle.short, min_length=2, max_length=25, placeholder="EMEA/NA/SA/APAC")
  teamCode = discord.ui.TextInput(label="Team Code", style=discord.TextStyle.short, min_length=4, max_length=25, placeholder="X??????")


  async def on_submit(self, interaction: discord.Interaction):
    desiredMode = None
    for mode in gamemodes:
      if mode["name"].lower().replace(" ", "") == self.gameMode.value.lower().replace(" ", ""):
        desiredMode = mode["name"]
    
    if not desiredMode:
      return await interaction.response.send_message("Could not find desired gamemode.")
    
    searchPost = f"<:right_arrow:1216305900961271859> <:Trophy:1223277455821902046> {self.trophies}\n"
    searchPost += f"<:right_arrow:1216305900961271859> <:list:1216305645083689111> {self.trophyRange.value} Lobby\n"
    searchPost += f"<:right_arrow:1216305900961271859> {modeEmojis[desiredMode]} {desiredMode}\n"
    searchPost += f"<:right_arrow:1216305900961271859> <a:Global:1223361709729779896> {self.region.value}\n"
    searchPost += f"<:right_arrow:1216305900961271859> Team Code: {self.teamCode.value}"
    embed = discord.Embed(title=f"<a:Announcement:1216306085565042710> {interaction.user}", description=searchPost, color=int("ffffff", 16))

    JoinButton = LinkButton("Join Team", f"https://link.brawlstars.com/invite/gameroom/en?tag={self.teamCode.value}")

    await interaction.response.send_message("sending Search post on all servers...", ephemeral=True, delete_after=5)

    for guild in self.bot.guilds:
      findMatesChannel = discord.utils.get(guild.text_channels, name="find-mates")
      if findMatesChannel:
        await findMatesChannel.send(embed=embed, view=View([JoinButton]))

    await interaction.edit_original_response(content="Search post sent successfully on all servers <a:verifyblack:1216302923441504287>")
    
    

# The Commands
class findTeams(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

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


async def setup(bot):
  await bot.add_cog(findTeams(bot))