import discord
from discord.ext import commands
import random
import requests  # Make sure requests is imported
import certifi  # Ensure certifi is imported for SSL verification

import ssl
print(ssl.OPENSSL_VERSION)

# Create intents
intents = discord.Intents.all()
intents.messages = True  # Enable message intents

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Code for the on_ready event ----------------------------
@bot.event
async def on_ready():
    print(f'Bot is ready: {bot.user}')

# Code for the ping pong command ----------------------------
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Code for the quote command ----------------------------
@bot.command()
async def quote(ctx):
    category = 'funny'
    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    
    # Replace with your actual API key
    response = requests.get(api_url, headers={'X-Api-Key': 'DhyVol8N8ZLOYP1Vld/s+w==y7pPbG1yixm1L41M'})
    
    if response.status_code == requests.codes.ok:
        quote_data = response.json()
        # Assuming the response contains a 'quote' field and an 'author' field
        quote = quote_data[0]  # Get the first quote from the list
        await ctx.send(f'"{quote["quote"]}" - {quote["author"]}')
    else:
        await ctx.send(f"Error fetching quote: {response.status_code} - {response.text}")
    
# Code for joke command ----------------------------    
@bot.command()
async def joke(ctx):
    api_url = 'https://api.api-ninjas.com/v1/jokes'  # Removed the limit parameter
    
    # Replace with your actual API key
    response = requests.get(api_url, headers={'X-Api-Key': 'DhyVol8N8ZLOYP1Vld/s+w==y7pPbG1yixm1L41M'})
    
    if response.status_code == requests.codes.ok:
        joke_data = response.json()
        # Assuming the response contains a 'joke' field
        if joke_data:  # Check if the joke_data list is not empty
            joke = joke_data[0]  # Get the first joke from the list
            await ctx.send(f'{joke["joke"]}')  # Adjusted to just send the joke
        else:
            await ctx.send("No jokes found.")
    else:
        await ctx.send(f"Error fetching joke: {response.status_code} - {response.text}")
        
#Code for riddle command ----------------------------
current_riddle = None  # Variable to store the current riddle

@bot.command()
async def riddle(ctx):
    global current_riddle  # Use the global variable
    api_url = 'https://api.api-ninjas.com/v1/riddles'

    # Replace with your actual API key
    response = requests.get(api_url, headers={'X-Api-Key': 'DhyVol8N8ZLOYP1Vld/s+w==y7pPbG1yixm1L41M'})

    if response.status_code == requests.codes.ok:
        riddle_data = response.json()
        if riddle_data:  # Check if the riddle_data list is not empty
            current_riddle = riddle_data[0]  # Get the first riddle
            await ctx.send(f'**Riddle**: {current_riddle["question"]}')  # Display the riddle question
            await ctx.send(f'**Type `!answer` to reveal the answer.**')  # Prompt for the answer
        else:
            await ctx.send("No riddles found.")
    else:
        await ctx.send(f"Error fetching riddle: {response.status_code} - {response.text}")

@bot.command()
async def answer(ctx):
    if current_riddle:  # Check if there's a current riddle
        await ctx.send(f'The answer is: {current_riddle["answer"]}')
    else:
        await ctx.send("No riddle available to answer.")
        
# Code for the on_member_join and on_member_remove events ----------------------------
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='general')  # Change 'general' to your desired channel name
    if channel:
        await channel.send(f"eassalim ealaykum, {member.mention}!")

# Code for the on_member_remove event ----------------------------
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name='general')  # Change 'general' to your desired channel name
    if channel:
        if random.randint(1, 100) <= 20:  # 20% chance
            await channel.send(f"{member} has been ejected. They were an Impostor.")
        else:
            await channel.send(f"{member} has been ejected. They were not an Impostor.")

# Code for the delete command ----------------------------
@bot.command()
async def delete(ctx, amount: int):
    if ctx.author.guild_permissions.manage_messages:
        if amount < 1:
            await ctx.send("Please specify a number greater than 0.")
            return
        
        deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to also delete the command message
        await ctx.send(f'Deleted {len(deleted) - 1} messages.', delete_after=5)  # Adjust message to delete after 5 seconds
    else:
        await ctx.send("You do not have permission to delete messages.")

# Run the bot with the token from environment variable
bot.run('your token here')  # Fetch the token from environment variable
