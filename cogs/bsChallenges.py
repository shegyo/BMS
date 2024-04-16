from discord.ext import commands
import discord, json
from discord import app_commands
import mongodb
import random

# ENV Daten laden
with open("data/challenges.json", "r", encoding="UTF-8") as f:
  bsChallenges = json.load(f)
  

class bsChallenges(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    
  # Get your Random Challenge
  @app_commands.command(description="get a random bs challenge (soon)")
  async def challenge(self, interaction: discord.Interaction, bs_id: str=None):
    return await interaction.response.send_message("coming soon...")
    # Ausgewählte Sprache fetchen
    options = mongodb.findGuildOptions(interaction.guild.id)
    language = options["language"]

    challenge = random.choice(bsChallenges)
    description = ""
    for text in challenge["content"][language]:
      description += text
    embed = discord.Embed(title=challenge["title"][language], description=description, color=int("000000", 16))
    await interaction.edit_original_response(content="", attachments=[discord.File("playerNotFound.webp", filename="playerNotFound.webp")], embed=embed)
      
  @challenge.error
  async def challenge_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.NoPrivateMessage):
      return await interaction.response.send_message("Command can't be run in Private Messages.", delete_after=5, ephemeral=True)
    else:
      return await interaction.response.send_message(f"Unknown error: {error}", delete_after=5, ephemeral=True)
    
    
async def setup(bot):
  await bot.add_cog(bsChallenges(bot))