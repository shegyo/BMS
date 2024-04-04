from discord.ext import commands, tasks
import discord, requests, datetime, pytz

format = "%d.%m.%Y, %H:%M"
germanTimeZone = pytz.timezone("Europe/Berlin")

class serverList(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    self.serverList.start()


  @tasks.loop(seconds=120)
  async def serverList(self):
    description = ""
    for guild in self.bot.guilds:
        inviteLink = ""
        try:
            invites = await guild.invites()
            if not invites:
                inviteLink = guild.id
        except:
            inviteLink = guild.id
        else:
            inviteLink = invites[0].url
        description += f"{guild.name} - {inviteLink}\n"
    serverListEmbed = discord.Embed(title="Server List", description=description, color=int("ffffff", 16))
    serverListEmbed.add_field(name="Server Count", value=len(self.bot.guilds))
    serverListEmbed.set_footer(text=f"Last Update: {datetime.datetime.now(germanTimeZone).strftime(format)}")

    serverListChannel = await self.bot.fetch_channel(1223417217727856661)
    if not serverListChannel:
        return
    
    messages = [message async for message in serverListChannel.history()]
    if not messages:
            return await serverListChannel.send(embed=serverListEmbed)
    for msg in messages:
        if msg.author == self.bot.user:
            await msg.edit(embed=serverListEmbed)
            return
    
    await serverListChannel.send(embed=serverListEmbed)

async def setup(bot):
  await bot.add_cog(serverList(bot))
