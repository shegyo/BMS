from discord.ext import commands, tasks
import discord, requests, datetime, json, pytz

icons = requests.get("https://api.brawlapi.com/v1/icons").json()

format = "%d.%m.%Y, %H:%M"

class getMaps(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    self.mapRota.start()


  @tasks.loop(seconds=120)
  async def mapRota(self):
    mapRota = requests.get("https://api.brawlapi.com/v1/events").json()
    
    ActiveEmbeds = []
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
      embed.description += f"\nEnds: {endDate.strftime(format)} UTC"
      embed.set_image(url=event["map"]["imageUrl"])
      embed.set_thumbnail(url=event["map"]["gameMode"]["imageUrl"])
      ActiveEmbeds.append(embed)
      if len(ActiveEmbeds) == 10:
        break
    
    embed.set_footer(text=f'Last Update: {datetime.datetime.now().strftime(format)} UTC\nCredits to: Brawlify.com')

    UpcomingEmbeds = []
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
      embed.description += f"\nStart: {startDate.strftime(format)} UTC"
      embed.set_image(url=event["map"]["imageUrl"])
      embed.set_thumbnail(url=event["map"]["gameMode"]["imageUrl"])
      UpcomingEmbeds.append(embed)
      if len(UpcomingEmbeds) == 10:
        break

    embed.set_footer(text=f'Last Update: {datetime.datetime.now().strftime(format)}  UTC\nCredits to: Brawlify.com')


    for guild in self.bot.guilds:
      currentMapsChannel = discord.utils.get(guild.channels, name="current-maps")
      nextMapsChannel = discord.utils.get(guild.channels, name="next-maps")
      if not currentMapsChannel or not nextMapsChannel:
          continue
    
      messages = [message async for message in currentMapsChannel.history()]
      for msg in messages:
          if msg.author != self.bot.user:
              await msg.delete()
          else:
              await msg.edit(content="# Active Maps", embeds=ActiveEmbeds)
              break

      messages = [message async for message in nextMapsChannel.history()]
      for msg in messages:
          print(msg.author)
          print(self.bot.user)
          if msg.author != self.bot.user:
              await msg.delete()
          else:
              await msg.edit(content="# Upcoming Maps", embeds=UpcomingEmbeds)
              break


async def setup(bot):
  await bot.add_cog(getMaps(bot))
