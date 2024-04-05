import os, discord, json
from discord.ext import commands
from cogs.Utility import View, LinkButton
import mongodb
import asyncio

class BMates(commands.Bot):
  
  def __init__(self, intents):
    super().__init__(command_prefix="-------", intents=intents, activity=discord.Activity(type=discord.ActivityType.playing, name="with good mates"))
    

  async def on_ready(self):
    print("Bot rasiert alles")
    for f in os.listdir('./cogs'):
      if f.endswith('.py'):
        await bot.load_extension(f'cogs.{f[:-3]}')
    await self.tree.sync()


  async def on_guild_join(self, guild: discord.guild):
    options = mongodb.findGuildOptions(guild.id)
    language = options["language"]
    
    # Only Read permission definieren
    onlyRead = {
      guild.default_role: discord.PermissionOverwrite(send_messages=False),
    }
    
    await asyncio.sleep(5)

    # Map Rota Kanäle erstellen 
    try:
      # Kategorie suchen
      mapRotaCategory = None
      i = 0
      while not mapRotaCategory and i < len(guild.categories):
        if "maprotation" in guild.categories[i].name.lower().replace(" ", ""):
          mapRotaCategory = guild.categories[i]
        i += 1

      # Kategorie erstellen falls nicht da
      if not mapRotaCategory:
        mapRotaCategory = await guild.create_category_channel("Map Rotation")
            
      # Kanäle suchen
      currentMapsChannel = None
      nextMapsChannel = None
      i = 0
      while (not currentMapsChannel or not nextMapsChannel) and i < len(mapRotaCategory.text_channels):
        if "current-maps" in mapRotaCategory.text_channels[i].name.lower():
          currentMapsChannel = mapRotaCategory.text_channels[i]
        elif "next-maps" in mapRotaCategory.text_channels[i].name.lower():
          nextMapsChannel = mapRotaCategory.text_channels[i]
        i += 1

      # Erstellen und eine Nachricht senden falls nicht vorhanden
      if not currentMapsChannel:
        currentMapsChannel = await mapRotaCategory.create_text_channel("current-maps", overwrites=onlyRead, topic="Active Maps!")
        await currentMapsChannel.send("<:info:1216306156222287894> Current maps will be here soon!")
      if not nextMapsChannel:
        nextMapsChannel = await mapRotaCategory.create_text_channel("next-maps", overwrites=onlyRead, topic="Predicted Upcoming Maps!")
        await nextMapsChannel.send("<:info:1216306156222287894> Predicted upcoming maps will be here soon!")
      

      # Find Mates Kanäle erstellen
      
      # Kategorie erstmal finden
      findMatesCategory = None
      i = 0
      while not findMatesCategory and i < len(guild.categories):
        if "findmates" in guild.categories[i].name.lower().replace(" ", ""):
          findMatesCategory = guild.categories[i]
        i += 1

      # Erstellen falls nicht da
      if not findMatesCategory:
        findMatesCategory = await guild.create_category_channel("Find Mates")

      # Kanäle erstmal finden
      findMatesChannel = None
      teamInquiriesChannel = None
      findEsportChannel = None
      i = 0
      while (not findMatesChannel or not teamInquiriesChannel or not findEsportChannel) and i < len(findMatesCategory.text_channels):
        if "find-mates" in findMatesCategory.text_channels[i].name.lower():
          findMatesChannel = findMatesCategory.text_channels[i]
        elif "team-inquiries" in findMatesCategory.text_channels[i].name.lower():
          teamInquiriesChannel = findMatesCategory.text_channels[i]
        elif "find-esport" in findMatesCategory.text_channels[i].name.lower():
          findEsportChannel = findMatesCategory.text_channels[i]
        i += 1

      if not findMatesChannel:
        findMatesChannel = await findMatesCategory.create_text_channel("find-mates", overwrites=onlyRead, topic="find a team to join here")
      if not findEsportChannel:
        findEsportChannel = await findMatesCategory.create_text_channel("find-esport", overwrites=onlyRead, topic="find an esport team or players here")
      if not teamInquiriesChannel:
        teamInquiriesChannel = await findMatesCategory.create_text_channel("team-inquiries", topic="run /find_mates to post your search!")

        await teamInquiriesChannel.send("<a:Announcement:1216306085565042710> Type `/find_mates` to search for teammates.\n"
                          +f"<:info:1216306156222287894> You can find all current search queries in {findMatesChannel.mention}\n\n"

                          +"I hope you find good mates and wish you a lot of fun and good luck! <a:pikacool:1216303417119735808>")

      systemChannel = guild.system_channel
      if systemChannel:
        await systemChannel.send("<:Hi:1216304655861284974> I am the **Brawl Mates System!** <:BMSlogo:1223389796450308197>\n\n"
                                +"I'm glad you've decided to use my service!\n"
                                +"I have already freed up your work and created all the channels for you and activated the system directly\n" 
                                +"If you still need help, please use the `/help` command <:settings:1223374255232651476>\n\n"

                                +"To support me, check out our Social Media in the Linktree <:Linktree:1218980236260278292>\n"
                                +"<:thx:1216304741949374504> for your support! You are the best",
                                view=View([LinkButton("Linktree", "https://linktr.ee/bsystems")]))
    except discord.errors.Forbidden:
      if systemChannel:
        await systemChannel.send("<:Hi:1216304655861284974> I am the **Brawl Mates System!** <:BMSlogo:1223389796450308197>\n\n"
                                +"Seems like I am missing permissions!\n"
                                +"To get started, create the category `find mates` with the channels `#find-mates` and `#find-esport`\n"
                                +"As well as the category `map rotation` with the channels `#current-maps` and `#next-maps`\nAlternatively, you could just ensure I have admin permission and reinvite me.\n" 
                                +"If you still need help, please use the `/help` command <:settings:1223374255232651476>\n\n"

                                +"To support me, check out our Social Media in the Linktree <:Linktree:1218980236260278292>\n"
                                +"<:thx:1216304741949374504> for your support! You are the best",
                                view=View([LinkButton("Linktree", "https://linktr.ee/bsystems")]))
      

intents = discord.Intents.all()
bot = BMates(intents=intents)
with open("jsons/env.json", "r") as f:
  env = json.load(f)
bot.run(env['TOKEN'])

