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

# Formular zum Ausfüllen, erstellt den Suchbeitrag
class FindMatesModalGerman(discord.ui.Modal):
  def __init__(self, bot, trophies, language):
    super().__init__(title="Neue Team Suche erstellen")
    self.bot = bot
    self.trophies = trophies
    self.language = language

  gameMode = discord.ui.TextInput(label="Spielmodus", placeholder="z.B. Knockout", style=discord.TextStyle.short, min_length=2, max_length=25)
  teamCode = discord.ui.TextInput(label="Team-Code", placeholder="X??????", style=discord.TextStyle.short, min_length=4, max_length=25)
  trophyRange = discord.ui.TextInput(label="Gewünschter Trophäenbereich", placeholder="z.B. 600-750", style=discord.TextStyle.short, max_length=11, required=False)
  region = discord.ui.TextInput(label="Region", placeholder="EMEA/NA/SA/APAC", style=discord.TextStyle.short, max_length=5, required=False)
  note = discord.ui.TextInput(label="Zusätzliche Informationen", placeholder="nur Leute mit Verstand bitte. Ich bin um 12:00 Uhr offline", style=discord.TextStyle.long, max_length=999, required=False)

  async def on_submit(self, interaction: discord.Interaction):
    await handleFindMatesSubmit(interaction, self.bot, self.gameMode.value, self.teamCode.value, self.trophyRange.value, self.region.value, self.note.value, self.trophies, self.language)

# Formulario para completar, crea la publicación de búsqueda
class FindMatesModalSpanish(discord.ui.Modal):
  def __init__(self, bot, trophies, language):
    super().__init__(title="Publicar nueva consulta")
    self.bot = bot
    self.trophies = trophies
    self.language = language

  gameMode = discord.ui.TextInput(label="Modo de juego", placeholder="p. ej. Knockout", style=discord.TextStyle.short, min_length=2, max_length=25)
  teamCode = discord.ui.TextInput(label="Código de equipo", placeholder="X??????", style=discord.TextStyle.short, min_length=4, max_length=25)
  trophyRange = discord.ui.TextInput(label="Rango de trofeos deseado", placeholder="p. ej. 600-750", style=discord.TextStyle.short, max_length=11, required=False)
  region = discord.ui.TextInput(label="Región", placeholder="EMEA/NA/SA/APAC", style=discord.TextStyle.short, max_length=5, required=False)
  note = discord.ui.TextInput(label="Información adicional", placeholder="solo personas con cerebro por favor. Estaré fuera de línea a las 12:00", style=discord.TextStyle.long, max_length=999, required=False)

  async def on_submit(self, interaction: discord.Interaction):
    await handleFindMatesSubmit(interaction, self.bot, self.gameMode.value, self.teamCode.value, self.trophyRange.value, self.region.value, self.note.value, self.trophies, self.language)

# Formulaire à remplir, crée la publication de recherche
class FindMatesModalFrench(discord.ui.Modal):
  def __init__(self, bot, trophies, language):
    super().__init__(title="Poster une nouvelle demande")
    self.bot = bot
    self.trophies = trophies
    self.language = language

  gameMode = discord.ui.TextInput(label="Mode de jeu", placeholder="par exemple, Knockout", style=discord.TextStyle.short, min_length=2, max_length=25)
  teamCode = discord.ui.TextInput(label="Code d'équipe", placeholder="X??????", style=discord.TextStyle.short, min_length=4, max_length=25)
  trophyRange = discord.ui.TextInput(label="Plage de trophées souhaitée", placeholder="par exemple, 600-750", style=discord.TextStyle.short, max_length=11, required=False)
  region = discord.ui.TextInput(label="Région", placeholder="EMEA/NA/SA/APAC", style=discord.TextStyle.short, max_length=5, required=False)
  note = discord.ui.TextInput(label="Informations supplémentaires", placeholder="seulement les personnes ayant un cerveau s'il vous plaît. Je serai hors ligne à 12h00", style=discord.TextStyle.long, max_length=999, required=False)

  async def on_submit(self, interaction: discord.Interaction):
    await handleFindMatesSubmit(interaction, self.bot, self.gameMode.value, self.teamCode.value, self.trophyRange.value, self.region.value, self.note.value, self.trophies, self.language)

# Форма для заполнения, создающая поиск
class FindMatesModalRussian(discord.ui.Modal):
  def __init__(self, bot, trophies, language):
    super().__init__(title="Опубликовать новый запрос")
    self.bot = bot
    self.trophies = trophies
    self.language = language

  gameMode = discord.ui.TextInput(label="Режим игры", placeholder="например, Knockout", style=discord.TextStyle.short, min_length=2, max_length=25)
  teamCode = discord.ui.TextInput(label="Код команды", placeholder="X??????", style=discord.TextStyle.short, min_length=4, max_length=25)
  trophyRange = discord.ui.TextInput(label="Желаемый диапазон трофеев", placeholder="например, 600-750", style=discord.TextStyle.short, max_length=11, required=False)
  region = discord.ui.TextInput(label="Регион", placeholder="EMEA/NA/SA/APAC", style=discord.TextStyle.short, max_length=5, required=False)
  note = discord.ui.TextInput(label="Дополнительная информация", placeholder="только люди с умом, пожалуйста. Я буду оффлайн в 12:00", style=discord.TextStyle.long, max_length=999, required=False)

  async def on_submit(self, interaction: discord.Interaction):
    await handleFindMatesSubmit(interaction, self.bot, self.gameMode.value, self.teamCode.value, self.trophyRange.value, self.region.value, self.note.value, self.trophies, self.language)

# Formular to fill out, creates the Search post
class FindMatesModalEnglish(discord.ui.Modal):
  def __init__(self, bot, trophies, language):
    super().__init__(title="Post New Inquiry")
    self.bot = bot
    self.trophies = trophies
    self.language = language

  gameMode = discord.ui.TextInput(label="Game Mode", placeholder="e.g. knockout", style=discord.TextStyle.short, min_length=2, max_length=25)
  teamCode = discord.ui.TextInput(label="Team Code", placeholder="X??????", style=discord.TextStyle.short, min_length=4, max_length=25)
  trophyRange = discord.ui.TextInput(label="Desired trophy range", placeholder="e.g. 600-750", style=discord.TextStyle.short, max_length=11, required=False)
  region = discord.ui.TextInput(label="Region", placeholder="EMEA/NA/SA/APAC", style=discord.TextStyle.short, max_length=5, required=False)
  note = discord.ui.TextInput(label="Additional Info", placeholder="only people with brain pls. Ill be offline at 12:00", style=discord.TextStyle.long, max_length=999, required=False)

  async def on_submit(self, interaction: discord.Interaction):
    await handleFindMatesSubmit(interaction, self.bot, self.gameMode.value, self.teamCode.value, self.trophyRange.value, self.region.value, self.note.value, self.trophies, self.language)

async def handleFindMatesSubmit(interaction, bot, gameMode, teamCode, trophyRange, region, note, trophies, language):
    desiredMode = None
    if gameMode.lower().replace(" ", "") in ["friendlyfight", "friendlymatch", "testmatch", "friendlybattle"]:
      desiredMode = "Friendly Battle"
    elif gameMode.lower().replace(" ", "") in ["duoshowdown", "duos", "sd", "duosd", "duo"]:
      desiredMode = "Duo Showdown"
    else:
      for mode in gamemodes:
        if mode["name"].lower().replace(" ", "") == gameMode.lower().replace(" ", ""):
          desiredMode = mode["name"]
    
    if not desiredMode:
      return await interaction.response.send_message(findTeamsTexts["gameModeNotFound"][language])
    
    
    await interaction.response.send_message(findTeamsTexts["sendingPosts"][language], ephemeral=True, delete_after=10)
    
    embeds = {"german" : [], "english" : [], "french" : [], "spanish" : [], "russian" : []}
    
    for language in embeds:
      # Titel mit user name darunter die trophäen des users
      searchPost = f"## <a:Announcement:1216306085565042710> `{interaction.user}`\n"
      searchPost += f"<:Trophy:1223277455821902046> **{trophies}**\n"
      # Gamemode anheften
      searchPost += f"{modeEmojis[desiredMode]} **{desiredMode}**\n"
      # Trophy Range anheften
      if trophyRange:
        searchPost += f"<:list:1216305645083689111> **{trophyRange}**\n"
      # Region anheften
      if region:
        searchPost += f"<a:Global:1223361709729779896> **{region.upper()}**\n"
      # Team Code anheften
      searchPost += f"<:right_arrow:1216305900961271859> **{teamCode.upper()}**\n"
      # Notiz anheften
      if note:
        searchPost += f"<:info:1216306156222287894> `{note}`"

      # Embed erstellen
      embed = discord.Embed(title="", description=searchPost, color=int("ffffff", 16))
      embed.set_author(name=findTeamsTexts["newInquiry"][language], icon_url=interaction.user.display_avatar.url)
      embed.set_footer(text=findTeamsTexts["sentFrom"][language].format(guild=interaction.guild), icon_url=interaction.guild.icon.url)

      embeds[language].append(embed)

    JoinButton = LinkButton(findTeamsTexts["joinTeam"][language], f"https://link.brawlstars.com/invite/gameroom/en?tag={teamCode}")

    for guild in bot.guilds:
      # Sprache suchen
      options = mongodb.findGuildOptions(guild.id)
      guildLanguage = options["language"]

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
        await findMatesChannel.send(embeds=embeds[guildLanguage], view=View([JoinButton]))

    await interaction.edit_original_response(content=findTeamsTexts["postSent"][language])
    
    

# Formulaire à remplir, crée la publication de recherche esport
class FindEsportModalFrench(discord.ui.Modal):
  def __init__(self, bot, language):
    super().__init__(title="Poster une nouvelle demande esport")
    self.bot = bot
    self.language = language

  position = discord.ui.TextInput(label="Recherche", placeholder="player/team/scrim/manager/analyst/coach", style=discord.TextStyle.short, min_length=4, max_length=10)
  region = discord.ui.TextInput(label="Région", placeholder="EMEA/NA/SA/APAC", style=discord.TextStyle.short, min_length=2, max_length=5, required=False)
  tier = discord.ui.TextInput(label="Niveau", placeholder="D/C/B/A/S/SS+", style=discord.TextStyle.short, min_length=1, max_length=3, required=False)
  note = discord.ui.TextInput(label="Informations supplémentaires", placeholder="doit parler anglais/devrait avoir x revenus", style=discord.TextStyle.paragraph, max_length=999, required=False)

  async def on_submit(self, interaction: discord.Interaction):
    await handleFindEsportSubmit(interaction, self.bot, self.position.value, self.region.value, self.tier.value, self.note.value, self.language)

# Форма для заполнения, создающая пост поиска электронного спорта
class FindEsportModalRussian(discord.ui.Modal):
  def __init__(self, bot, language):
    super().__init__(title="Создать новый запрос по электронному спорту")
    self.bot = bot
    self.language = language

  position = discord.ui.TextInput(label="Ищу", placeholder="player/team/scrim/manager/analyst/coach", style=discord.TextStyle.short, min_length=4, max_length=10)
  region = discord.ui.TextInput(label="Регион", placeholder="EMEA/NA/SA/APAC", style=discord.TextStyle.short, min_length=2, max_length=5, required=False)
  tier = discord.ui.TextInput(label="Уровень", placeholder="D/C/B/A/S/SS+", style=discord.TextStyle.short, min_length=1, max_length=3, required=False)
  note = discord.ui.TextInput(label="Дополнительная информация", placeholder="должен говорить по-английски/должен иметь доход x", style=discord.TextStyle.paragraph, max_length=999, required=False)

  async def on_submit(self, interaction: discord.Interaction):
    await handleFindEsportSubmit(interaction, self.bot, self.position.value, self.region.value, self.tier.value, self.note.value, self.language)

# Formulario para completar, crea la publicación de búsqueda de Esport
class FindEsportModalSpanish(discord.ui.Modal):
  def __init__(self, bot, language):
    super().__init__(title="Publicar nueva consulta de Esport")
    self.bot = bot
    self.language = language

  position = discord.ui.TextInput(label="Buscando", placeholder="player/scrim/team/manager/analyst/coach", style=discord.TextStyle.short, min_length=4, max_length=10)
  region = discord.ui.TextInput(label="Región", placeholder="EMEA/NA/SA/APAC", style=discord.TextStyle.short, min_length=2, max_length=5, required=False)
  tier = discord.ui.TextInput(label="Nivel", placeholder="D/C/B/A/S/SS+", style=discord.TextStyle.short, min_length=1, max_length=3, required=False)
  note = discord.ui.TextInput(label="Información adicional", placeholder="debe hablar inglés/debería tener x ingresos", style=discord.TextStyle.paragraph, max_length=999, required=False)

  async def on_submit(self, interaction: discord.Interaction):
    await handleFindEsportSubmit(interaction, self.bot, self.position.value, self.region.value, self.tier.value, self.note.value, self.language)

# Formular zum Ausfüllen, erstellt den Suchbeitrag für Esport
class FindEsportModalGerman(discord.ui.Modal):
  def __init__(self, bot, language):
    super().__init__(title="Neue Esport-Suche veröffentlichen")
    self.bot = bot
    self.language = language

  position = discord.ui.TextInput(label="Suche nach", placeholder="player/scrim/team/manager/analyst/coach", style=discord.TextStyle.short, min_length=4, max_length=10)
  region = discord.ui.TextInput(label="Region", placeholder="EMEA/NA/SA/APAC", style=discord.TextStyle.short, min_length=2, max_length=5, required=False)
  tier = discord.ui.TextInput(label="Tier", placeholder="D/C/B/A/S/SS+", style=discord.TextStyle.short, min_length=1, max_length=3, required=False)
  note = discord.ui.TextInput(label="Zusätzliche Informationen", placeholder="muss Englisch sprechen/sollte x Einnahmen haben", style=discord.TextStyle.paragraph, max_length=999, required=False)

  async def on_submit(self, interaction: discord.Interaction):
    await handleFindEsportSubmit(interaction, self.bot, self.position.value, self.region.value, self.tier.value, self.note.value, self.language)

# Formular to fill out, creates the Search post
class findEsportModalEnglish(discord.ui.Modal):
  def __init__(self, bot, language):
    super().__init__(title="Post New Esport Inquiry")
    self.bot = bot
    self.language = language

  position = discord.ui.TextInput(label="Searching for", placeholder="player/scrim/team/manager/analyst/coach", style=discord.TextStyle.short, min_length=4, max_length=10)
  region = discord.ui.TextInput(label="Region", placeholder="EMEA/NA/SA/APAC", style=discord.TextStyle.short, min_length=2, max_length=5, required=False)
  tier = discord.ui.TextInput(label="Tier", placeholder="D/C/B/A/S/SS+", style=discord.TextStyle.short, min_length=1, max_length=3, required=False)
  note = discord.ui.TextInput(label="Additional Info", placeholder="must speak english/should have x earnings", style=discord.TextStyle.paragraph, max_length=999, required=False)

  async def on_submit(self, interaction: discord.Interaction):
    await handleFindEsportSubmit(interaction, self.bot, self.position.value, self.region.value, self.tier.value, self.note.value, self.language)

async def handleFindEsportSubmit(interaction, bot, position, region, tier, note, language):
    # Positions Validität prüfen
    if not position.lower() in ["manager", "coach", "analyst" ,"player", "team", "scrim"]:
      return await interaction.response.send_message(findTeamsTexts["unknownPosition"][language].format(pos=position.capitalize()), ephemeral=True, delete_after=3)
      
    await interaction.response.send_message(findTeamsTexts["sendingPosts"][language], ephemeral=True, delete_after=10)

    embeds = {"german" : [], "english" : [], "french" : [], "spanish" : [], "russian" : []}

    for language in embeds:
      # Titel mit user name
      searchPost = f"## <a:Announcement:1216306085565042710> `{interaction.user}`\n"
      
      # Gesuchtes Position anheften
      searchPost += f"🔎 **{position.upper()}** {esportEmojis[position.lower()]}\n"
      
      # Region anheften
      if region:
        searchPost += f"<a:Global:1223361709729779896> **{region.upper()}**\n"
      # Tier anheften
      tier = tier.upper()
      if tier:
        if tier in ["D", "C", "B", "A", "S", "SS+"]:
          searchPost += f"{esportEmojis[tier]} **TIER**\n"
      # Notiz anheften
      if note:
        searchPost += f"<:info:1216306156222287894> `{note}`"

      # Embed bauen
      embed = discord.Embed(title="", description=searchPost, color=int("ffffff", 16))
      embed.set_author(name=findTeamsTexts["newEsportInquiry"][language], icon_url=interaction.user.display_avatar.url)
      embed.set_footer(text=findTeamsTexts["sentFrom"][language].format(guild=interaction.guild), icon_url=interaction.guild.icon.url)

      embeds[language].append(embed)


    for guild in bot.guilds:
      # Sprache suchen
      options = mongodb.findGuildOptions(guild.id)
      guildLanguage = options["language"]

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
        await findEsportChannel.send(embeds=embeds[guildLanguage])

    await interaction.edit_original_response(content=findTeamsTexts["postSent"][language])



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
      if language == "german":
        await interaction.response.send_modal(FindMatesModalGerman(self.bot, profileData["trophies"], language))
      elif language == "english":
        await interaction.response.send_modal(FindMatesModalEnglish(self.bot, profileData["trophies"], language))
      elif language == "spanish":
        await interaction.response.send_modal(FindMatesModalSpanish(self.bot, profileData["trophies"], language))
      elif language == "russian":
        await interaction.response.send_modal(FindMatesModalRussian(self.bot, profileData["trophies"], language))
      else:
        await interaction.response.send_modal(FindMatesModalFrench(self.bot, profileData["trophies"], language))
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
    if language == "german":
      await interaction.response.send_modal(FindEsportModalGerman(self.bot, language))
    elif language == "english":
      await interaction.response.send_modal(findEsportModalEnglish(self.bot, language))
    elif language == "spanish":
      await interaction.response.send_modal(FindEsportModalSpanish(self.bot, language))
    elif language == "russian":
      await interaction.response.send_modal(FindEsportModalRussian(self.bot, language))
    else:
      await interaction.response.send_modal(FindEsportModalFrench(self.bot, language))

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
