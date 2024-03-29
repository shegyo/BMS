import os, discord, json
from discord.ext import commands

class BMates(commands.Bot):
  
  def __init__(self, intents):
    super().__init__(command_prefix="-------", intents=intents, activity=discord.Activity(type=discord.ActivityType.listening, name="team searches"))
    

  async def on_ready(self):
    print("Bot rasiert alles")
    for f in os.listdir('./cogs'):
      if f.endswith('.py'):
        await bot.load_extension(f'cogs.{f[:-3]}')
    await self.tree.sync()    


intents = discord.Intents.all()
bot = BMates(intents=intents)
with open("jsons/env.json", "r") as f:
  env = json.load(f)
bot.run(env['TOKEN'])

