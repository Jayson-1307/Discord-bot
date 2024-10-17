from datetime import datetime, timedelta
import discord
from discord.ext import commands
import random
import requests  # Make sure requests is imported
import certifi  # Ensure certifi is imported for SSL verification
import ssl

print(ssl.OPENSSL_VERSION)

# In-memory storage for user currencies (for demonstration; consider using a database for persistent storage)
user_currency = {}

# In-memory storage for user last work time
user_last_work = {}

# In-memory storage for user last crime time
user_last_crime = {}

# Create intents
intents = discord.Intents.all()
intents.messages = True  # Enable message intents

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready: {bot.user}')

# Command to check user balance
@bot.command()
async def balance(ctx):
    user_id = ctx.author.id
    balance = user_currency.get(user_id, 100)  # Default balance is 100 if not found
    await ctx.send(f'Your balance is: {balance} coins.')

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
    response = requests.get(api_url, headers={'X-Api-Key': ''})
    
    if response.status_code == requests.codes.ok:
        quote_data = response.json()
        quote = quote_data[0]  # Get the first quote from the list
        await ctx.send(f'"{quote["quote"]}" - {quote["author"]}')
    else:
        await ctx.send(f"Error fetching quote: {response.status_code} - {response.text}")

# Code for joke command ----------------------------    
@bot.command()
async def joke(ctx):
    api_url = 'https://api.api-ninjas.com/v1/jokes'  # Removed the limit parameter
    
    # Replace with your actual API key
    response = requests.get(api_url, headers={'X-Api-Key': ''})
    
    if response.status_code == requests.codes.ok:
        joke_data = response.json()
        if joke_data:  # Check if the joke_data list is not empty
            joke = joke_data[0]  # Get the first joke from the list
            await ctx.send(f'{joke["joke"]}')  # Adjusted to just send the joke
        else:
            await ctx.send("No jokes found.")
    else:
        await ctx.send(f"Error fetching joke: {response.status_code} - {response.text}")

# Code for riddle command ----------------------------
current_riddle = None  # Variable to store the current riddle

@bot.command()
async def riddle(ctx):
    global current_riddle  # Use the global variable
    api_url = 'https://api.api-ninjas.com/v1/riddles'

    # Replace with your actual API key
    response = requests.get(api_url, headers={'X-Api-Key': ''})

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

# Code for the kick command ----------------------------
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await ctx.send(f'{member} has been kicked.')
    else:
        await ctx.send("You do not have permission to kick members.")

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

# Code for the ban command ----------------------------
@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await ctx.send(f'{member} has been banned.')
    else:
        await ctx.send("You do not have permission to ban members.")





# Code for roll the dice command ----------------------------
@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

# code for work command ----------------------------
@bot.command()
async def work(ctx):
    user_id = ctx.author.id
    current_time = datetime.now()

    # Check if the user has worked today
    if user_id in user_last_work:
        last_work_time = user_last_work[user_id]
        if last_work_time.date() == current_time.date():
            await ctx.send("You can only work once a day! Please try again tomorrow.")
            return

    # Give user 100 coins
    user_currency[user_id] = user_currency.get(user_id, 100) + 100  # Default balance is 100 if not found
    user_last_work[user_id] = current_time  # Update last work time

    await ctx.send(f"You worked hard today and earned 100 coins! Your new balance is: {user_currency[user_id]} coins.")

#code for crime command ----------------------------
@bot.command()
async def crime(ctx):
    user_id = ctx.author.id
    current_time = datetime.now()

    # Check if the user has committed a crime today
    if user_id in user_last_crime:
        last_crime_time = user_last_crime[user_id]
        if last_crime_time.date() == current_time.date():
            await ctx.send("You can only commit a crime once a day! Please try again tomorrow.")
            return
        
     # 50% chance of success
    success = random.choice([True, False])
    if success:
        # Give user 200 coins
        user_currency[user_id] = user_currency.get(user_id, 100) + 200
        user_last_crime[user_id] = current_time  # Update last crime time
        await ctx.send(f"You successfully committed a crime and earned 200 coins! Your new balance is: {user_currency[user_id]} coins.")
    else:
        # Deduct 100 coins from user
        user_currency[user_id] = user_currency.get(user_id, 100) - 100
        user_last_crime[user_id] = current_time  # Update last crime time

        if user_currency[user_id] < 0:
            user_currency[user_id] = 0

        await ctx.send(f"You were caught committing a crime and lost 100 coins! Your new balance is: {user_currency[user_id]} coins.")



# Code for slot machine command ----------------------------
@bot.command()
async def slot(ctx):
    user_id = ctx.author.id
    # Deduct cost from user's balance
    cost = 2
    user_balance = user_currency.get(user_id, 100)  # Default balance is 100 if not found

    if user_balance < cost:
        await ctx.send("You don't have enough coins to play the slot machine!")
        return
    
    user_currency[user_id] = user_balance - cost  # Deduct the cost from user's balance

    emojis = [':apple:', ':banana:', ':watermelon:', ':tangerine:', ':grapes:']
    slot1 = random.choice(emojis)
    slot2 = random.choice(emojis)
    slot3 = random.choice(emojis)

    await ctx.send(f'{slot1} | {slot2} | {slot3}')

    # Determine winnings based on slot results
    if slot1 == slot2 == slot3:
        winnings = 20  # Jackpot
        user_currency[user_id] += winnings  # Add winnings to user's balance
        await ctx.send(f'Congratulations! You won the jackpot! Your new balance is: {user_currency[user_id]} coins.')
    elif slot1 == slot2 or slot1 == slot3 or slot2 == slot3:
        winnings = 5  # Partial win
        user_currency[user_id] += winnings  # Add winnings to user's balance
        await ctx.send(f'Congratulations! You won! Your new balance is: {user_currency[user_id]} coins.')
    else:
        await ctx.send(f'Sorry, you lost. Your new balance is: {user_currency[user_id]} coins. Try again!')

# Code for the blackjack command ----------------------------
player_hand = []
dealer_hand = []

@bot.command()
async def blackjack(ctx):
    global player_hand, dealer_hand  # Declare global variables
    user_id = ctx.author.id
    balance = user_currency.get(user_id, 100)  # Get user's balance

    if balance <= 0:
        await ctx.send("You don't have enough coins to play Blackjack!")
        return

    # Start a new game
    player_hand = [random.randint(1, 11), random.randint(1, 11)]
    dealer_hand = [random.randint(1, 11), random.randint(1, 11)]

    await ctx.send(f'**Your Hand**: {player_hand[0]} | {player_hand[1]}')
    await ctx.send(f'**Dealer Hand**: {dealer_hand[0]} | ?')

    player_total = sum(player_hand)

    if player_total == 21:
        await ctx.send('Congratulations! You got a Blackjack!')
    else:
        await ctx.send('Type `!hit` to draw another card or `!stand` to keep your hand.')

@bot.command()
async def hit(ctx):
    global player_hand  # Declare the global variable

    player_hand.append(random.randint(1, 11))  # Draw another card

    await ctx.send(f'**Your Hand**: {", ".join(map(str, player_hand))}')  # Display updated hand
    player_total = sum(player_hand)

    if player_total > 21:
        await ctx.send('Bust! You lost. Type `!blackjack` to start a new game.')
    elif player_total == 21:
        await ctx.send('Congratulations! You got a Blackjack! Type `!blackjack` to start a new game.')
    else:
        await ctx.send('Type `!hit` to draw another card or `!stand` to keep your hand.')

@bot.command()
async def stand(ctx):
    global player_hand, dealer_hand  # Declare global variables

    player_total = sum(player_hand)

    # Dealer logic
    dealer_total = sum(dealer_hand)
    while dealer_total < 17:
        dealer_hand.append(random.randint(1, 11))  # Dealer draws one card if total is less than 17
        dealer_total = sum(dealer_hand)

    await ctx.send(f'**Your Hand**: {", ".join(map(str, player_hand))} (Total: {player_total})')
    await ctx.send(f'**Dealer Hand**: {", ".join(map(str, dealer_hand))} (Total: {dealer_total})')

    # Update user currency based on the outcome
    user_id = ctx.author.id
    if player_total > 21:
        await ctx.send('You busted! You lost.')
        user_currency[user_id] = user_currency.get(user_id, 100) - 10  # Deduct 10 coins on loss
    elif dealer_total > 21:
        await ctx.send('Dealer busted! You win!')
        user_currency[user_id] = user_currency.get(user_id, 100) + 10  # Add 10 coins on win
    elif player_total > dealer_total:
        await ctx.send('You win!')
        user_currency[user_id] = user_currency.get(user_id, 100) + 10  # Add 10 coins on win
    elif player_total < dealer_total:
        await ctx.send('You lost.')
        user_currency[user_id] = user_currency.get(user_id, 100) - 10  # Deduct 10 coins on loss
    else:
        await ctx.send('It\'s a tie!')


# Run the bot with the token from environment variable
bot.run('')  # Fetch the token from environment variable
