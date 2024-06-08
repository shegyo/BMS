from discord.ext import commands
import discord, requests, tempfile, json
from discord import app_commands
from cogs.Utility import View, LinkButton
import mongodb

# ENV Daten laden
with open("data/env.json", "r", encoding="UTF-8") as f:
  envData = json.load(f)

with open("languages/generalTexts.json", "r", encoding="UTF-8") as f:
   generalTexts = json.load(f)

def getPlayerNameForId(bs_id):
  bs_id = bs_id.upper().replace(" ", "").replace("#", "")
  url = f"https://api.brawlstars.com/v1/players/%23{bs_id}"
  headers = {
      "Authorization": f"Bearer {envData['BsApi']}"
  }
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
      return response.json()["name"], bs_id
  else:
      return "", bs_id


# Funktion zum laden der Profilbilder mit Brawlerranks
def getBsProfile(bs_id, source):
  # Check player exists
  player_name, bs_id = getPlayerNameForId(bs_id)

  if player_name:
    response = requests.get(f"{source}{bs_id}")
    if response.status_code == 200:
        # Speichern der binären Daten in einer temporären Datei
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(response.content)
            temp_filename = temp_file.name
            return temp_filename, bs_id, player_name
    else:
      return None, bs_id, player_name
  else:
    return None, bs_id, player_name
  

class brawlProfiles(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    
  # Get your Profile Image
  @app_commands.command(description="get your bs profile's meta info")
  async def brawl_profile(self, interaction: discord.Interaction, bs_id: str=None):
      # Ausgewählte Sprache fetchen
      options = mongodb.findGuildOptions(interaction.guild.id)
      language = options["language"]

      # Nutzer Id fetchen
      user_options = mongodb.findUserOptions(interaction.user.id)
      bs_id = user_options["bs_id"]

      if not bs_id:
        return await interaction.response.send_message(generalTexts["noIdGiven"][language], ephemeral=True, delete_after=60)


      await interaction.response.defer()
      profileImg, bs_id, player_name = getBsProfile(bs_id, "https://share.brawlify.com/player/")
      if not (profileImg and player_name):
        embed = discord.Embed(title=player_name, description=f"### <:info:1216306156222287894> ID: #{bs_id}", color=int("000000", 16))
        await interaction.edit_original_response(content="", attachments=[discord.File("playerNotFound.webp", filename="playerNotFound.webp")], embed=embed)
      else:
        viewItems = [LinkButton("Brawlify", "https://brawlify.com/stats/profile/"+bs_id, "<:brawlify:1226211333540941844>")]
        embed = discord.Embed(title=player_name, description=f"### <:info:1216306156222287894> ID: #{bs_id}", color=int("000000", 16))
        await interaction.edit_original_response(content="", attachments=[discord.File(profileImg, filename="profile_image.png")], embed=embed, view=View(viewItems))

  @brawl_profile.error
  async def brawl_profile_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.NoPrivateMessage):
      return await interaction.response.send_message("Command can't be run in Private Messages.", delete_after=5, ephemeral=True)
    else:
      return await interaction.response.send_message(f"Unknown error: {error}", delete_after=5, ephemeral=True)
    
    
  # Get your Profile Ranks Image
  @app_commands.command(description="get your bs profile's brawler ranks")
  async def brawl_ranks(self, interaction: discord.Interaction, bs_id: str=None):
      # Ausgewählte Sprache fetchen
      options = mongodb.findGuildOptions(interaction.guild.id)
      language = options["language"]

      # Nutzer Id fetchen
      user_options = mongodb.findUserOptions(interaction.user.id)
      bs_id = user_options["bs_id"]

      if not bs_id:
        return await interaction.response.send_message(generalTexts["noIdGiven"][language], ephemeral=True, delete_after=60)


      await interaction.response.defer()
      profileImg, bs_id, player_name = getBsProfile(bs_id, "https://brawlbot.xyz/api/image/rank/")
      if not (profileImg and player_name):
        embed = discord.Embed(title=player_name, description=f"### <:info:1216306156222287894> ID: #{bs_id}", color=int("000000", 16))
        await interaction.edit_original_response(content="", attachments=[discord.File("playerNotFound.webp", filename="playerNotFound.webp")], embed=embed)
      else:
        viewItems = [LinkButton("Brawlify", "https://brawlify.com/stats/profile/"+bs_id, "<:brawlify:1226211333540941844>")]
        embed = discord.Embed(title=player_name, description=f"### <:info:1216306156222287894> ID: #{bs_id}", color=int("000000", 16))
        await interaction.edit_original_response(content="", attachments=[discord.File(profileImg, filename="profile_image.png")], embed=embed, view=View(viewItems))

  @brawl_ranks.error
  async def brawl_ranks_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.NoPrivateMessage):
      return await interaction.response.send_message("Command can't be run in Private Messages.", delete_after=5, ephemeral=True)
    else:
      return await interaction.response.send_message(f"Unknown error: {error}", delete_after=5, ephemeral=True)
    

  # Save your Id
  @app_commands.command(description="save your id and never type it again")
  async def save_id(self, interaction: discord.Interaction, bs_id: str):
    # Ausgewählte Sprache fetchen
    options = mongodb.findGuildOptions(interaction.guild.id)
    language = options["language"]

    await interaction.response.defer(ephemeral=True)
    player_name, bs_id = getPlayerNameForId(bs_id)
    if not player_name:
      await interaction.edit_original_response(content=generalTexts["invalidId"][language].format(bs_id=bs_id))
    else:
      user_options = mongodb.findUserOptions(interaction.user.id)
      user_options["bs_id"] = bs_id 
      mongodb.saveUser(user_options)
      await interaction.edit_original_response(content=generalTexts["idSaved"][language].format(bs_id=bs_id))

  @save_id.error
  async def save_id_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.NoPrivateMessage):
      return await interaction.response.send_message("Command can't be run in Private Messages.", delete_after=5, ephemeral=True)
    else:
      return await interaction.response.send_message(f"Unknown error: {error}", delete_after=5, ephemeral=True)
    
async def setup(bot):
  await bot.add_cog(brawlProfiles(bot))