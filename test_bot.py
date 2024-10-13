import discord
from discord.ext import commands

# Create intents
intents = discord.Intents.all()
intents.messages = True  # Enable message intents

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready: {bot.user}')

@bot.command()
async def ping(ctx):
    print("Ping command invoked!")  # Log when command is invoked
    await ctx.send('Pong!')

# Run the bot with the new token
bot.run('MTI5NTA5MjQ3NzI0OTk4MjQ2NA.G28DYv.H0cAOBIS5oZLjjAv9zhQt51FZglStKZ6oDRDHo')  