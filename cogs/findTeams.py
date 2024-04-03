from discord.ext import commands
import discord, requests, json
from discord import app_commands
from cogs.Utility import View, LinkButton
import mongodb

gamemodes = requests.get("https://api.brawlapi.com/v1/gamemodes").json()["list"]
gamemodes.append({"name" : "Ranked"})
gamemodes.append({"name" : "Showdown"})
gamemodes.append({"name" : "Present Plunder"})
gamemodes.append({"name" : "Pumpkin Plunder"})

# EnvData laden
with open("jsons/env.json", "r", encoding="UTF-8") as f:
  envData = json.load(f)

# Emoji Listen laden
with open("jsons/modeEmojis.json", "r", encoding="UTF-8") as f:
  modeEmojis = json.load(f)

with open("jsons/esportEmojis.json", "r", encoding="UTF-8") as f:
  esportEmojis = json.load(f)

# Texte laden
with open("jsons/findTeamsTexts.json", "r", encoding="UTF-8") as f:
  findTeamsTexts = json.load(f)

# Formular to fill out, creates the Search post
class findMatesModal(discord.ui.Modal):
  def __init__(self, bot, trophies, language):
    super().__init__(title="Post New Inquiry")
    self.bot = bot
    self.trophies = trophies
    self.language = language

  gameMode = discord.ui.TextInput(label="Game Mode", placeholder="e.g. knockout", style=discord.TextStyle.short, min_length=4, max_length=25)
  teamCode = discord.ui.TextInput(label="Team Code", placeholder="X??????", style=discord.TextStyle.short, min_length=4, max_length=25)
  trophyRange = discord.ui.TextInput(label="Desired trophy range", placeholder="e.g. 600-750", style=discord.TextStyle.short, max_length=11, required=False)
  region = discord.ui.TextInput(label="Region", placeholder="EMEA/NA/SA/APAC", style=discord.TextStyle.short, max_length=5, required=False)
  note = discord.ui.TextInput(label="Add whatever info", placeholder="only people with brain pls. Ill be offline at 12:00", style=discord.TextStyle.long, max_length=200, required=False)

  async def on_submit(self, interaction: discord.Interaction):
    desiredMode = None
    if self.gameMode.value.lower().replace(" ", "") in ["friendlyfight", "friendlymatch", "testmatch", "friendlybattle"]:
      desiredMode = "Friendly Battle"
    elif self.gameMode.value.lower().replace(" ", "") in ["duoshowdown", "duos", "sd", "duosd", "duo"]:
      desiredMode = "Duo Showdown"
    else:
      for mode in gamemodes:
        if mode["name"].lower().replace(" ", "") == self.gameMode.value.lower().replace(" ", ""):
          desiredMode = mode["name"]
    
    if not desiredMode:
      return await interaction.response.send_message("Could not find desired gamemode.")
    
    
    # Titel mit user name darunter die trophäen des users
    searchPost = f"## <a:Announcement:1216306085565042710> `{interaction.user}`\n"
    searchPost += f"<:Trophy:1223277455821902046> **{self.trophies}**\n"
    # Gamemode anheften
    searchPost += f"{modeEmojis[desiredMode]} **{desiredMode}**\n"
    # Trophy Range anheften
    if self.trophyRange.value:
      searchPost += f"<:list:1216305645083689111> **{self.trophyRange.value}**\n"
    # Region anheften
    if self.region.value:
      searchPost += f"<a:Global:1223361709729779896> **{self.region.value.upper()}**\n"
    # Team Code anheften
    searchPost += f"<:right_arrow:1216305900961271859> **{self.teamCode.value.upper()}**\n"
    # Notiz anheften
    if self.note.value:
      searchPost += f"<:info:1216306156222287894> `{self.note.value}`"

    # Embed erstellen
    embed = discord.Embed(title="", description=searchPost, color=int("ffffff", 16))
    embed.set_author(name="new inquiry",icon_url=interaction.user.display_avatar.url)
    embed.set_footer(text=f"sent from: {interaction.guild}", icon_url=interaction.guild.icon.url)

    JoinButton = LinkButton("Join Team", f"https://link.brawlstars.com/invite/gameroom/en?tag={self.teamCode.value}")

    await interaction.response.send_message("sending Search post on all servers...", ephemeral=True, delete_after=5)

    for guild in self.bot.guilds:
      # Kategorie suchen
      findMatesCategory = None
      i = 0
      while not findMatesCategory and i < len(guild.categories):
        if "FINDMATES" in guild.categories[i].name.upper().replace(" ", ""):
          findMatesCategory = guild.categories[i]
        i += 1

      if not findMatesCategory:
        continue
            
      # Kanal suchen
      findMatesChannel = None
      i = 0
      while not findMatesChannel and i < len(findMatesCategory.text_channels):
        if "find-mates" in findMatesCategory.text_channels[i].name.lower():
          findMatesChannel = findMatesCategory.text_channels[i]
        i += 1

      
      # Nachricht posten wenn Kanal gefunden wurde
      if findMatesChannel:
        await findMatesChannel.send(embed=embed, view=View([JoinButton]))

    await interaction.edit_original_response(content="Search post sent successfully on all servers <a:verifyblack:1216302923441504287>")
    
    
# Formular to fill out, creates the Search post
class findEsportModal(discord.ui.Modal):
  def __init__(self, bot, language):
    super().__init__(title="Post New Esport Inquiry")
    self.bot = bot
    self.language = language

  position = discord.ui.TextInput(label="Position looked for", placeholder="player/team/manager/analyst", style=discord.TextStyle.short, min_length=4, max_length=10)
  region = discord.ui.TextInput(label="Region", placeholder="EMEA/NA/SA/APAC", style=discord.TextStyle.short, min_length=2, max_length=5, required=False)
  tier = discord.ui.TextInput(label="Tier", placeholder="D/C/B/A/S/SS+", style=discord.TextStyle.short, min_length=1, max_length=3, required=False)
  note = discord.ui.TextInput(label="Additional Info", placeholder="must speak english/should have x earnings", style=discord.TextStyle.paragraph, max_length=200, required=False)

  async def on_submit(self, interaction: discord.Interaction):
    # Titel mit user name
    searchPost = f"## <a:Announcement:1216306085565042710> `{interaction.user}`\n"

    # Positions Validität prüfen
    if not self.position.value.lower() in ["manager", "coach", "analyst" ,"player"]:
      return await interaction.response.send_message(f"Unknown position: {self.position.value.lower().capitalize()}", ephemeral=True, delete_after=3)
    
    # Gesuchtes Position anheften
    searchPost += f"🔎 **{self.position.value.upper()}**\n"
    
    # Region anheften
    if self.region.value:
      searchPost += f"<a:Global:1223361709729779896> **{self.region.value.upper()}**\n"
    # Tier anheften
    tier = self.tier.value.upper()
    if tier:
      if tier in ["D", "C", "B", "A", "S", "SS+"]:
        searchPost += f"{esportEmojis[tier]} **TIER**\n"
    # Notiz anheften
    if self.note.value:
      searchPost += f"<:info:1216306156222287894> `{self.note.value}`"

    # Embed bauen
    embed = discord.Embed(title="", description=searchPost, color=int("ffffff", 16))
    embed.set_author(name="new esport inquiry",icon_url=interaction.user.display_avatar.url)
    embed.set_footer(text=f"sent from: {interaction.guild}", icon_url=interaction.guild.icon.url)

    await interaction.response.send_message("sending Search post on all servers...", ephemeral=True, delete_after=5)

    for guild in self.bot.guilds:
      # Kategorie suchen
      findMatesCategory = None
      i = 0
      while not findMatesCategory and i < len(guild.categories):
        if "FINDMATES" in guild.categories[i].name.upper().replace(" ", ""):
          findMatesCategory = guild.categories[i]
        i += 1

      if not findMatesCategory:
        continue
            
      # Kanal suchen
      findEsportChannel = None
      i = 0
      while not findEsportChannel and i < len(findMatesCategory.text_channels):
        if "find-esport" in findMatesCategory.text_channels[i].name.lower():
          findEsportChannel = findMatesCategory.text_channels[i]
        i += 1

      
      # Nachricht posten wenn Kanal gefunden wurde
      if findEsportChannel:
        await findEsportChannel.send(embed=embed)

    await interaction.edit_original_response(content="Search post sent successfully on all servers <a:verifyblack:1216302923441504287>")


# The Commands
class findTeams(commands.Cog):

  def __init__(self, bot):
    self.bot = bot


  # allgemeine Team Suche
  @app_commands.command(description="post a new inquiry")
  @app_commands.checks.cooldown(1, 60*5, key=lambda i: (i.user.id))
  async def find_mates(self, interaction: discord.Interaction, bs_id: str):
    # Ausgewählte Sprache fetchen
    options = mongodb.findGuildOptions(interaction.guild.id)
    language = options["language"]

    bs_id = bs_id.upper().replace(" ", "").replace("#", "")
    url = f"https://api.brawlstars.com/v1/players/%23{bs_id}"
    headers = {
        "Authorization": f"Bearer {envData['BsApi']}"
    }
    profileData = requests.get(url, headers=headers).json()
    if "trophies" in profileData:
        await interaction.response.send_modal(findMatesModal(self.bot, profileData["trophies"], language))
    else:
      await interaction.response.send_message(findTeamsTexts["noProfileFound"][language].format(bs_id = bs_id), ephemeral=True, delete_after=3)

  @find_mates.error
  async def ticket_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)


  # Esport Team Suche Command
  @app_commands.command(description="post a new inquiry")
  @app_commands.checks.cooldown(1, 60*5, key=lambda i: (i.user.id))
  async def find_esport(self, interaction: discord.Interaction):
    # Ausgewählte Sprache fetchen
    options = mongodb.findGuildOptions(interaction.guild.id)
    language = options["language"]

    await interaction.response.send_modal(findEsportModal(self.bot, language))

  @find_esport.error
  async def find_esport_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)


  # Esport Team Suche Command
  @app_commands.command(description="remove all your search posts")
  @app_commands.checks.cooldown(1, 60*5, key=lambda i: (i.user.id))
  async def cancel_search(self, interaction: discord.Interaction):
    # Ausgewählte Sprache fetchen
    options = mongodb.findGuildOptions(interaction.guild.id)
    language = options["language"]

    await interaction.response.send_message(findTeamsTexts["cancelStart"][language], ephemeral=True, delete_after=30)
    for guild in self.bot.guilds:
      # Kategorie suchen
      findMatesCategory = None
      i = 0
      while not findMatesCategory and i < len(guild.categories):
        if "FINDMATES" in guild.categories[i].name.upper().replace(" ", ""):
          findMatesCategory = guild.categories[i]
        i += 1

      if not findMatesCategory:
        continue
            
      # Kanäle erstmal finden
      findMatesChannel = None
      findEsportChannel = None
      i = 0
      while (not findMatesChannel or not findEsportChannel) and i < len(findMatesCategory.text_channels):
        if "find-mates" in findMatesCategory.text_channels[i].name.lower():
          findMatesChannel = findMatesCategory.text_channels[i]
        elif "find-esport" in findMatesCategory.text_channels[i].name.lower():
          findEsportChannel = findMatesCategory.text_channels[i]
        i += 1

      for channel in [findMatesChannel, findEsportChannel]:
        if channel:
          messages = [message async for message in channel.history(limit=25)]
          # Iteriere über letzte 25 Nachrichten und suche User Post
          msgdeleted = False
          i = 0
          while i < len(messages) and not msgdeleted:
            if messages[i].embeds[0].author.icon_url == interaction.user.display_avatar.url:
              await messages[i].delete()
            i += 1


    await interaction.edit_original_response(content=findTeamsTexts["cancelSuccessful"][language])

  @find_esport.error
  async def find_esport_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)

async def setup(bot):
  await bot.add_cog(findTeams(bot))
