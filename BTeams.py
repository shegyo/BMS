import os, discord, asyncio, json
from discord.ext import commands

class BTeams(commands.Bot):
  
  def __init__(self, intents):
    super().__init__(command_prefix="-------", intents=intents, activity=discord.Activity(type=discord.ActivityType.listening, name="team searches"))
    

  async def on_ready(self):
    print("Bot rasiert alles")
    for f in os.listdir('./cogs'):
      if f.endswith('.py'):
        await bot.load_extension(f'cogs.{f[:-3]}')
    await self.tree.sync()

  async def on_member_join(self, member: discord.Member):
    # Wenn der bot selbst gejoint ist
    if member.id == 1223344546260193280:
      # Kategorie erstmal finden
      findMatesCategory = discord.utils.find(member.guild.categories, name="FIND MATES")
      # Erstellen falls nicht da
      if not findMatesCategory:
        findMatesCategory = await member.guild.create_category_channel("FIND MATES")
        # Kanäle erstellen
        onlyRead = {
          member.guild.default_role: discord.PermissionOverwrite(send_messages=False),
        }
        await findMatesCategory.create_text_channel("find-mates", overwrites=onlyRead, topic="find a team to join in this channel")
        await findMatesCategory.create_text_channel("search-mates", topic="run /find_mates to post your search!")


intents = discord.Intents.all()
bot = BTeams(intents=intents)
with open("jsons/env.json", "r") as f:
  env = json.load(f)
bot.run(env['TOKEN'])

