import discord
from discord.ext import commands
import random
# import requests

# Create intents
intents = discord.Intents.all()
intents.messages = True  # Enable message intents

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Event listener for when the bot is ready
@bot.event
async def on_ready():
    print(f'Bot is ready: {bot.user}')
    # Load the Quotes cog when the bot is ready
    bot.load_extension('cogs.quotes')  # Awaiting the load_extension

# Command to send a simple ping response
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')
    
# Event listener for when a new member joins the server
@bot.event
async def on_member_join(member):
    # Get the channel to send the greeting
    channel = discord.utils.get(member.guild.text_channels, name='general')  # Change 'general' to your desired channel name
    if channel:
        await channel.send(f"eassalim ealaykum, {member.mention}!")

# Event listener for when a member leaves the server
@bot.event
async def on_member_remove(member):
    # Get the channel to send the goodbye message
    channel = discord.utils.get(member.guild.text_channels, name='general')  # Change 'general' to your desired channel name
    if channel:
        # Generate a random number between 1 and 100
        if random.randint(1, 100) <= 20:  # 20% chance
            await channel.send(f"{member} has been ejected. They were an Impostor.")
        else:
            await channel.send(f"{member} has been ejected. They were not an Impostor.")

# Command to delete messages in a channel (requires 'Manage Messages' permission) 
@bot.command()
async def delete(ctx, amount: int):
    # Check if the user has the required permissions
    if ctx.author.guild_permissions.manage_messages:
        if amount < 1:
            await ctx.send("Please specify a number greater than 0.")
            return
        
        # Delete the specified number of messages
        deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to also delete the command message
        await ctx.send(f'Deleted {len(deleted) - 1} messages.', delete_after=5)  # Adjust message to delete after 5 seconds
    else:
        await ctx.send("You do not have permission to delete messages.")
        


# Run the bot with your token
bot.run('MTI5NTA4NDA5MjExNDczMTAyOA.G3tOLS.5KYgekMFMGNmDX2OcEaCJxx-hytv-qJ3h8LPlg')  