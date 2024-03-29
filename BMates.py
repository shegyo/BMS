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
    # Find Mates Kanäle erstellen
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

    systemChannel = guild.system_channel
    if systemChannel:
      await systemChannel.send("<:Hi:1216304655861284974> I am the **Brawl Mates System!** <:BMSlogo:1223389796450308197>\n\n"
                                +"I'm glad you've decided to use my service!\n"
                                +"I have already freed up your work and created all the channels for you and activated the system directly\n" 
                                +"If you still need help, please use the `/help` command <:settings:1223374255232651476>\n\n"

                                +"To support me, check out our Social Media in the Linktree <:Linktree:1218980236260278292>\n"
                                +"<:thx:1216304741949374504> for your support! You are the best",
                                view=View[LinkButton("Linktree", "https://linktr.ee/bsystems")])

intents = discord.Intents.all()
bot = BMates(intents=intents)
with open("jsons/env.json", "r") as f:
  env = json.load(f)
bot.run(env['TOKEN'])

