import os, discord, json
from discord.ext import commands
from cogs.Utility import View, LinkButton

class BMates(commands.Bot):
  
  def __init__(self, intents):
    super().__init__(command_prefix="-------", intents=intents, activity=discord.Activity(type=discord.ActivityType.listening, name="team searches"))
    

  async def on_ready(self):
    print("Bot rasiert alles")
    for f in os.listdir('./cogs'):
      if f.endswith('.py'):
        await bot.load_extension(f'cogs.{f[:-3]}')
    await self.tree.sync()


  async def on_guild_join(self, guild: discord.guild):
    # Maps Kanäle erstellen
    for guild in self.guilds:
      # Kategorie erstmal finden
      mapsCategory = discord.utils.get(guild.categories, name="Map Rotation")
      # Erstellen falls nicht da
      if not mapsCategory:
        mapsCategory = await guild.create_category_channel("Map Rotation", position = 0)

      # Kanäle erstmal finden
      currentMaps = discord.utils.get(mapsCategory.text_channels, name="current-maps")
      nextMaps = discord.utils.get(mapsCategory.text_channels, name="next-maps")
      onlyRead = {
        guild.default_role: discord.PermissionOverwrite(send_messages=False),
      }
      if not currentMaps:
        currentMaps = await mapsCategory.create_text_channel("current-maps", overwrites=onlyRead, topic="Active Maps!")
      if not nextMaps:
        nextMaps = await mapsCategory.create_text_channel("next-maps", topic="Predicted Upcoming Maps!")

      await currentMaps.send("<:info:1216306156222287894> Current maps will be here soon!")
      await nextMaps.send("<:info:1216306156222287894> Predicted upcoming maps will be here soon!")

    # Find Mates Kanäle erstellen
    for guild in self.guilds:
      # Kategorie erstmal finden
      findMatesCategory = discord.utils.get(guild.categories, name="FIND MATES")
      # Erstellen falls nicht da
      if not findMatesCategory:
        findMatesCategory = await guild.create_category_channel("FIND MATES")

      # Kanäle erstmal finden
      teamInquiriesChannel = discord.utils.get(findMatesCategory.text_channels, name="team-inquiries")
      findMatesChannel = discord.utils.get(findMatesCategory.text_channels, name="find-mates")
      onlyRead = {
        guild.default_role: discord.PermissionOverwrite(send_messages=False),
      }
      if not findMatesChannel:
        await findMatesCategory.create_text_channel("find-mates", overwrites=onlyRead, topic="find a team to join in this channel")
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
      

intents = discord.Intents.all()
bot = BMates(intents=intents)
with open("jsons/env.json", "r") as f:
  env = json.load(f)
bot.run(env['TOKEN'])

