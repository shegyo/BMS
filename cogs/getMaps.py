from discord.ext import commands, tasks
import discord, requests, datetime, json
import mongodb

icons = requests.get("https://api.brawlapi.com/v1/icons").json()

format = "%d.%m.%Y, %H:%M"

with open("jsons/mapsTexts.json", "r", encoding="UTF-8") as f:
   mapsTexts = json.load(f)

class getMaps(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    self.mapRota.start()


  @tasks.loop(seconds=120)
  async def mapRota(self):
    mapRota = requests.get("https://api.brawlapi.com/v1/events").json()
    
    languageEmbeds = {"german" : [], "english" : [], "french" : [], "spanish" : [], "russian" : []}
    embeds = {"active" : languageEmbeds, "upcoming" : languageEmbeds}

    for language in languageEmbeds:
      for event in mapRota["active"]:
        if event["slot"]["name"] == "Challenge":
          continue
        if event["map"]["gameMode"]["name"] == "Solo Showdown":
          continue
        if event["map"]["gameMode"]["name"] == "Duo Showdown":
          eventName = "Showdown"
        else:
          eventName = event["map"]["gameMode"]["name"]
        embed=discord.Embed(title=event["map"]["name"], description=eventName)
        endDate = datetime.datetime.fromisoformat(event["endTime"].replace("Z", "+00:00"))
        embed.description += f"\n{mapsTexts["ends"][language]}: {endDate.strftime(format)} UTC"
        embed.set_image(url=event["map"]["imageUrl"])
        embed.set_thumbnail(url=event["map"]["gameMode"]["imageUrl"])
        embeds["active"][language].append(embed)
        if len(embeds["active"][language]) == 10:
          break
      
      embed.set_footer(text=mapsTexts["footer"][language].format(lastUpdate=datetime.datetime.now().strftime(format)))


    for language in languageEmbeds:
      for event in mapRota["upcoming"]:
        if event["slot"]["name"] == "Challenge":
          continue
        if event["map"]["gameMode"]["name"] == "Solo Showdown":
          continue
        if event["map"]["gameMode"]["name"] == "Duo Showdown":
          eventName = "Showdown"
        else:
          eventName = event["map"]["gameMode"]["name"]
        embed=discord.Embed(title=event["map"]["name"], description=eventName)
        startDate = datetime.datetime.fromisoformat(event["startTime"].replace("Z", "+00:00"))
        embed.description += f"\n{mapsTexts["starts"][language]}: {startDate.strftime(format)} UTC"
        embed.set_image(url=event["map"]["imageUrl"])
        embed.set_thumbnail(url=event["map"]["gameMode"]["imageUrl"])
        embeds["upcoming"][language].append(embed)
        if len(embeds["upcoming"][language]) == 10:
          break

    embed.set_footer(text=mapsTexts["footer"][language].format(lastUpdate=datetime.datetime.now().strftime(format)))


    for guild in self.bot.guilds:
      # Sprache suchen
      options = mongodb.findGuildOptions(guild.id)
      language = options["language"]

      # Kategorie suchen
      mapRotaCategory = None
      i = 0
      while not mapRotaCategory and i < len(guild.categories):
        if "maprotation" in guild.categories[i].name.lower().replace(" ", ""):
          mapRotaCategory = guild.categories[i]
        i += 1

      if not mapRotaCategory:
        continue
            
      # Kanal suchen
      currentMapsChannel = None
      nextMapsChannel = None
      i = 0
      while (not currentMapsChannel or not nextMapsChannel) and i < len(mapRotaCategory.text_channels):
        if "current-maps" in mapRotaCategory.text_channels[i].name.lower():
          currentMapsChannel = mapRotaCategory.text_channels[i]
        elif "next-maps" in mapRotaCategory.text_channels[i].name.lower():
          nextMapsChannel = mapRotaCategory.text_channels[i]
        i += 1
      if not currentMapsChannel or not nextMapsChannel:
          continue
    
      messages = [message async for message in currentMapsChannel.history()]
      if not messages:
         await currentMapsChannel.send(f'# {mapsTexts["activeMapsTitle"][language]}', embeds=embeds["active"][language])
      for msg in messages:
          if msg.author != self.bot.user:
              await msg.delete()
          else:
              await msg.edit(content=f'# {mapsTexts["activeMapsTitle"][language]}', embeds=embeds["active"][language])
              break

      messages = [message async for message in nextMapsChannel.history()]
      if not messages:
         await nextMapsChannel.send(f'# {mapsTexts["upcomingMapsTitle"][language]}', embeds=embeds["upcoming"][language])
      for msg in messages:
          if msg.author != self.bot.user:
              await msg.delete()
          else:
              await msg.edit(content=f'# {mapsTexts["upcomingMapsTitle"][language]}', embeds=embeds["upcoming"][language])
              break


async def setup(bot):
  await bot.add_cog(getMaps(bot))
