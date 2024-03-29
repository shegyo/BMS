from discord.ext import commands, tasks
import discord
from discord import app_commands


# The Commands
class findTeams(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(description="Creates a Support Ticket")
  @app_commands.checks.cooldown(1, 60*5, key=lambda i: (i.guild_id, i.user.id))
  async def find_mates(self, interaction: discord.Interaction, your_total_trophies: int, trophy_minimum: int, game_mode: str, team_code: str):
    
    await interaction.response.send_message("Search posted on all servers!")

  @find_mates.error
  async def ticket_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)




async def setup(bot):
  await bot.add_cog(findTeams(bot))