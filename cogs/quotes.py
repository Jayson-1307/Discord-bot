import discord
from discord.ext import commands
import requests

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def quote(self, ctx):
        response = requests.get("https://api.quotable.io/random")
        if response.status_code == 200:
            quote_data = response.json()
            await ctx.send(f'"{quote_data["content"]}" - {quote_data["author"]}')
        else:
            await ctx.send("Could not fetch a quote at this time.")

# Setup function to add the Quotes cog to the bot
def setup(bot):
    bot.add_cog(Quotes(bot))  # No need to await this line
