# Imports
import wikipedia
import discord
from discord.ext import commands, tasks
from discord import app_commands
import logging
from dotenv import load_dotenv
import os
import random
import time
import datetime
from zoneinfo import ZoneInfo
from googletrans import Translator
from mcstatus import JavaServer
import aiohttp
import wikipedia
import yt_dlp
from difflib import get_close_matches


# Variables
Gifs = [
    'https://tenor.com/view/horse-horse-reaction-reaction-elite-dangerous-borann-boys-gif-25049405',
    'https://tenor.com/view/horse-side-eye-gif-2138439955218797613',
    'https://tenor.com/view/horse-gif-16989653505354355713',
    'https://tenor.com/view/horse-wine-horse-with-wine-gif-13140298122387270411',
    'https://tenor.com/view/grass-horse-horse-sitting-gif-18247540597407868249',
    'https://tenor.com/view/horse-silly-gif-12886436098092344563',
    'https://tenor.com/view/uh-gif-230597167926076170',
    'https://tenor.com/view/sad-horse-horse-sad-rain-horse-sad-horse-on-the-rain-gif-2339772143737630615'
]

_playing_guilds = set()
translator = Translator()
NoE = False
quotes = []
floobert = True
WordsOfWisdom = []
IDs = 0
sex = False
Neighs = [
    " Neigh",
    " neigh",
    "...Neigh...",
    " Neigh?",
    " **NEIGH!!!**",
    " Neigh :(",
    " Neighhhh",
    " :wilted_rose:",
    " Neigh :D",
    " Neigh >:("
]
### Here is the channel blacklist. I'm going to make this into a .txt file shortly.
BlackListedChannelsFile = 'BlacklistedChannels.txt'
BlacklistedChannels = [
]
with open(BlackListedChannelsFile, 'r') as file:
    for line in file:
        BlacklistedChannels.append(line.strip())
        print(BlacklistedChannels) ### Debug

handler = logging.FileHandler(filename='discordlog.log', encoding='utf-8', mode='w')
c = 0
ch = ''
TakeControl = False # Used to take control of the bot and yell at people
AnnounceMode = False # Used to make announcements on bot launch
HorseHitListFile = 'HorseHitList.txt'
FuckerCentral = 0 # Don't mind the name
yea = [
    "𝓝𝓰𝓱...𝓘 𝓷𝓮𝓮𝓭 𝓽𝓸 𝓫𝓻𝓮𝓮𝓭 𝔂𝓸𝓾...",
    f"{random.randint(1,1000)} billion to Israel",
    "Aaaaand it's all over the screen",
    "A barbershop haircut that costs a quarter",
    "I'm gonna hold you hand when I say this...||Yes. Absolutely.||",
    "You're fucking brilliant, absolutely.",
    "I would rather shove a meet cleaver up my ass than say no to that.",
    "Hell yeah dude punch it in",
    "A tear just ran down my leg......",
    "Fuck yeah",
    "Hell yes",
    "Yea",
    "Sure?",
    "If you insist",
    "Probably",
    "Give me choccy milk and I'll say yes.",
    "Idk man.",
    "Probably not",
    f"Probably like... {random.randint(1,11)}",
    "I'm so close hang on 1 second",
    "Oh.",
    "Ok",
    "Did you ask me?",
    "I'm not answering that.",
    "Ask me that again. I fucking dare you.",
    "Take me out to dinner first bro",
    "Nah",
    "Obviously not",
    "The fuck? No!",
    "Absulutely the fuck not.",
    "I would rather shove a meet cleaver up my ass than say yes to that.",
    "I'm gonna call you a slur.",
    "I'm gonna hold you hand when I say this...||No. Fuck no.||",
    "Fuck you. I'm not answering that. Instead, I'll ask you this: If you were 3 inches deep in Donald Trump and Elon Musk was 3 inches deep in you, which way are you moving?",
    "No",
    "You're a fucking dumbass.",
    "I'm a horse. I can't answer that.",
    "Fuh Naw :broken_heart: :wilted_rose:",
    "Take what you just said, write it down, and shove it up your ass.",
    "?",
    "J",
    "That's so bad I might recreate 9/11",
    f"Is {random.randint(1,1000)} stories high enough?",
    "Alright, that's it. Back to bed with you."
    ]
m = False
# Setup
load_dotenv()
token = os.getenv("DISCORD_TOKEN_2")
print("Getting Quotes")
with open('Quotes.txt', 'r') as file:
    for line in file:
        try:
            WordsOfWisdom.append(line)
            IDs += 1
            #print("Got", line) # For Debug
        except:
            print(f"Error at line {IDs}")
print(f"Successfully loaded quotes at ID {IDs}")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)
# Setup complete, running
@bot.event
async def on_ready():
    print("Discord Bot should be online, hol up tho")
    bot.loop.create_task(console_input_task())
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s).")
        print("Bot is done loading!")
    except Exception as e:
        print(f"Error syncing commands: {e}")
    await bot.change_presence(activity=discord.Game(name="Ngl, I'm kinda gay. Neigh."))
    if AnnounceMode == True:
        text = str(input("> "))
        for guild in bot.guilds:
            sent = False
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    print(f"Checking {guild.name} #{channel.name}")
                    if channel.name.lower() == "general" or channel.name.lower() == "chat":
                        try:
                            await channel.send(text)
                            print(f"Sent wisdom to {guild.name} in #{channel.name}")
                            sent = True
                            break  # stop after finding general in this guild
                        except Exception as e:
                            print(f"Failed to send to {guild.name} #{channel.name}: {e}")
            if not sent:
                print(f"No suitable 'general' channel found in {guild.name}")
    send_daily_message.start()  # start the background task
    send_PSA.start()



# Basic, safe typo checker using English word list
with open("words_alpha.txt", "r") as f:
    VALID_WORDS = set(w.strip().lower() for w in f)

def find_typos(text, cutoff=0.8):
    words = [w.lower() for w in text.split()]
    typos = []

    for word in words:
        if word.isalpha() and word not in VALID_WORDS:
            matches = get_close_matches(word, VALID_WORDS, n=1, cutoff=cutoff)
            if matches:
                typos.append((word, matches[0]))

    return typos


@bot.tree.command(name="join", description="Joins a VC")
async def join(interaction: discord.Interaction):

    if interaction.user.voice:
        channel = interaction.user.voice.channel

        if interaction.guild.voice_client:
            await interaction.guild.voice_client.move_to(channel)
        else:
            try:
                await channel.connect()
                await interaction.response.send_message(":)")
            except Exception as e:
                await interaction.response.send_message(f"Voice error: {e}")
    else:
        await interaction.response.send_message("You're not in a voice channel.")

@bot.tree.command(name="play")
async def play(interaction: discord.Interaction, url: str):
    print("PLAY COMMAND HIT")

    try:
        await interaction.response.defer()

        print("Deferred")

        voice = interaction.guild.voice_client

        if not voice:
            if interaction.user.voice:
                channel = interaction.user.voice.channel
                voice = await channel.connect()
                print("Connected VC")
            else:
                await interaction.followup.send("Join VC")
                return

        import yt_dlp
        print("yt-dlp imported")

        ydl_opts = {
        "format": "bestaudio/best",
        "js_runtimes": {
            "node": {}
        }
}


        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print("Extracted")
            source = info["url"]

        print("Starting FFmpeg")

        voice.play(discord.FFmpegPCMAudio(
            source,
            before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            options="-vn"
        ))

        await interaction.followup.send(f"Playing {url} :3")

    except Exception as e:
        print("CRASH:", e)





@bot.tree.command(name="leave", description="Leave VC (why are you looking at this?)")
async def leave(interaction: discord.Interaction):
    if interaction.user.voice:
        try:
            await interaction.response.send_message(":(")
            await interaction.guild.voice_client.disconnect()
        except Exception as e:
            print("Voice error:", e)


# Taking Control of the Bot for fun :)
async def console_input_task():
    await bot.wait_until_ready()
    if TakeControl == True:
        channel_id_1 = int(input("Enter the channel ID for the first channel: "))

        channel_id = int(input("Enter the second channel ID: "))
        channel = bot.get_channel(channel_id)
        if channel_id_1 != 0:
            channel2 = bot.get_channel(channel_id_1)
        else:
            if not channel:
                print("Invalid channel ID")
                return
            while True:
                msg = input("> ")
                await channel.send(msg)
    else:
        print("Bot is automatic, no taking control.")


@tasks.loop(time=datetime.time(hour=2, minute=00))  # 10:00 PM
async def send_PSA():
    
    ctx = 1148608661577547894
    channel = bot.get_channel(ctx)
    await channel.send("Good evening all. I am not a horse. Please do not go to bed. Sleeping is not important. \n Some pro tips from my buddy Paul: \n"
    "- Turn your phone on, and crank that brightness up. \n"
    "- Listen to some absolutely metal music or orange noise. \n"
    "- Definitely do not run over Jackson Maclure with a car. For no reason. At 132 mph. \n"
    "- Be straight. \n"
    "- Fuck you. Kill yourself."
    )

# Quotes
@tasks.loop(minutes=1440)
async def send_daily_message():
    global floobert
    if floobert ==  True:
        floobert = False
    else:
        for guild in bot.guilds:
            sent = False
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    print(f"Checking {guild.name} #{channel.name}")
                    if channel.name.lower() == "general":
                        try:
                            await channel.send(random.choice(WordsOfWisdom))
                            print(f"Sent wisdom to {guild.name} in #{channel.name}")
                            sent = True
                            break  # stop after finding general in this guild
                        except Exception as e:
                            print(f"Failed to send to {guild.name} #{channel.name}: {e}")
            if not sent:
                print(f"No suitable 'general' channel found in {guild.name}")

async def get_horse_hitlist(author_name: str, filepath: str):
    """
    Returns the horse crime count for a given author (or 0 if not found).
    """
    try:
        with open(filepath, 'r') as file:
            lines = [line.strip() for line in file]
            for i in range(0, len(lines), 2):  # name/number pairs
                name = lines[i]
                number = int(lines[i + 1])
                if name == author_name:
                    return number
    except FileNotFoundError:
        return 0  # no file = no crimes
    except Exception as e:
        print(f"GET FAILED?????????????????????????????????? {e}")
        return 0
    return 0
async def update_horse_hitlist(author_name: str, filepath: str, change: int = 1, base_value: int = 1):
    """
    Updates the Horse Hit List file by changing an author's count.

    :param author_name: The name of the author (user).
    :param filepath: Path to the hitlist file.
    :param change: How much to change the count by (default +1, use -1 to subtract).
    :param base_value: Starting value for new authors (default = 1).
    :return: The updated number for this author.
    """
    data = {}

    try:
        # Load current file into dict
        try:
            with open(filepath, 'r') as file:
                lines = [line.strip() for line in file]
                for i in range(0, len(lines), 2):  # pairs of (name, number)
                    name = lines[i]
                    number = int(lines[i + 1])
                    data[name] = number
        except FileNotFoundError:
            # No file yet, we’ll create one later
            pass

        # Update or insert
        if author_name in data:
            data[author_name] += change
            print(f"Updated {author_name}: {data[author_name]}")
        else:
            # if subtracting on a new user, just start them at 0
            data[author_name] = base_value if change > 0 else 0
            print(f"Added {author_name}: {data[author_name]}")

        # Write back cleanly
        with open(filepath, 'w') as file:
            for name, number in data.items():
                file.write(f"{name}\n{number}\n")

        return data[author_name]

    except Exception as e:
        print(f"EVERYTHING FAILED????????????????????????????????????????????? {e}")
        return None

ZodiacSigns = [
    'Aquarius',
    'Pisces',
    'Aries',
    'Taurus',
    'Gemini',
    'Cancer',
    'Leo',
    'Virgo',
    'Libra',
    'Scorpio',
    'Sagittarius',
    'Capricorn'
]

@bot.tree.command(name="compatiblity", description="Check two users romantic compatibility!")
@app_commands.describe(userone="First user", usertwo="Second user", signone="First user's zodiac sign", signtwo="Second user's zodiac sign")
@app_commands.choices(signone=[app_commands.Choice(name=z, value=z) for z in ZodiacSigns], signtwo=[app_commands.Choice(name=z, value=z) for z in ZodiacSigns])
async def compatibility(interaction: discord.Interaction, userone: discord.User, usertwo: discord.User, signone: str, signtwo: str):
    with open('Compatibility.txt', 'r') as file:
        for line in file:
            if f"{userone.name}" in line and f"{usertwo.name}" in line:
                await interaction.response.send_message(f"The compatibility between {userone.mention} and {usertwo.mention} is... **{line.split('= ')[1].strip()}**. Neigh neigh.")
                return
            else:
                pass
    Compat = 0
    print(f"Checking compatibility between {userone} and {usertwo}")
    print(f"{signone} {signtwo}")
    await interaction.response.send_message(f"Calculating compatibility between {userone.mention} ({signone}) and {usertwo.mention} ({signtwo})...")
    for letter in signone + signtwo:
        Compat += 1
    print(Compat)
    userscoreone = await get_horse_hitlist(userone.name, HorseHitListFile)
    userscoretwo = await get_horse_hitlist(usertwo.name, HorseHitListFile)
    if userscoreone is None or userscoretwo is None:
        print("Error getting user scores for compatibility.")
    else:
        Compat += (userscoreone - userscoretwo)
    if Compat < 0:
        Compat *= -1
    while Compat > 100:
        Compat = Compat / 2
    with open('Compatibility.txt', 'a') as file:
        file.write(f"{userone.name} ({signone}) + {usertwo.name} ({signtwo}) = {int(Compat)}%\n")
        print("Written to file successfully!")
    await interaction.followup.send(f"The compatibility between {userone.mention} and {usertwo.mention} is... **{int(Compat)}%**. Neigh neigh.")
    

@bot.tree.command(name="roll", description="Roll a dice")
@app_commands.describe(sides="how many sides should it be")
async def roll(interaction: discord.Interaction, sides: int):
    print(f"Rolling {sides}")
    if sides == 67:
        await interaction.response.send_message("no.")
    else:    
        await interaction.response.send_message(f"You rolled a d{sides}, and lowk got {random.randint(1,sides)}. Good job or some shit. Neigh neigh")

@bot.tree.command(name="blacklist", description="Blacklists the channel you are currently in from Horse's view.")
async def blacklist(interaction: discord.Interaction, channel: discord.TextChannel):
    global BlacklistedChannels
    print("ran /blacklist")
    if str(channel.id) in BlacklistedChannels:
        await interaction.response.send_message("Woah, easy there partner. Don't want to blacklist this channel twice now do we? That's it, I'm nuking Venezuela")
    else:
        with open(BlackListedChannelsFile, 'a') as file:
            file.write(f"{channel.id} \n")
            print(f"written {channel.id} to file.")
        await interaction.response.send_message("**This channel is now blacklisted.**")
        BlacklistedChannels = []
        with open(BlackListedChannelsFile, 'r') as file:
            for line in file:
                BlacklistedChannels.append(line.strip())
                # print(BlacklistedChannels) ### Debug


# Beautiful code if I do say so myself (this is awful)
@bot.tree.command(name="status", description="Change the horses status!")
@app_commands.describe(status="What should it be?")
async def status(interaction: discord.Interaction, status: str):
    await interaction.response.send_message("Hold your horses a sec...")
    await bot.change_presence(activity=discord.Game(name=status))
    await interaction.followup.send("My status is different now, neigh neigh.")

@bot.tree.command(name="confess", description="Confess your sins to Horse, and be judged.")
async def confess(interaction: discord.Interaction, confession: str):
    print("confessed")
    print("running...")
    await interaction.response.send_message(f"Your confession has been sent to {interaction.channel.name}!.", ephemeral=True)
    await runconfession(confession, interaction)

async def runconfession(confession, interaction):
    try:
        print("sending response...")
        embed = discord.Embed(
            title=f"Anonymous Confession (#{random.randint(1,100000)})",
            description=f"\"{confession}\"",
            color=random.randint(1,100000)
        )
        await interaction.channel.send(embed=embed)
    except Exception as e:
        print(f"An error has occured! {e}")

@bot.tree.command(name="horse", description="?")
async def horse(interaction: discord.Interaction, password: str):
    print(f"Guessed {password}")
    if password == "cock and balls":
        await interaction.response.send_message("You have guessed the password correctly. Your reward will be delivered shortly...")
        exit()
    else:
        time.sleep(2)
        await interaction.response.send_message("Incorrect.")

@bot.tree.command(name="version", description="Displays the current bot version")
async def version(interaction: discord.Interaction):
    print("Ran command /version")
    await interaction.response.send_message("Good day, horse enthusiast. My current version is 26.2.2. New hidden response, new confession message to match the already existing confessions bot. Neigh.")

@bot.tree.command(name="quote", description="Add a quote to the bot!")
@app_commands.describe(quote="Type the quote here, or a number to fetch a quote.", user="Whose quote is this?")
async def quote(interaction: discord.Interaction, quote: str, user: discord.User = None):
    global IDs
    global m
    global quotes
    await interaction.response.send_message("Hol up a sec chat")

    with open("Quotes.txt", "r") as file:
        quotes = []
        for line in file:
            quotes.append(line)
    print("Adding quote...")
    m = False
    if "\n" in quote: 
        await interaction.followup.send("Buddy. What the fuck are you doing.")
    try:
        # If it's a number, fetch that line
        quote_num = int(quote)
        with open("Quotes.txt", "r") as file:
            lines = [line.strip() for line in file]
        if 1 <= quote_num <= len(lines):
            await interaction.followup.send(lines[quote_num - 1])
            print(lines[quote_num - 1])
        else:
            await interaction.followup.send("That quote number doesn’t exist!")
            print("Heyyyyyyyyyy pookie that doesn't exist :point_right: :point_left:")
    except:
            try:
                # Check for duplicates
                if quote in quotes:
                    await interaction.followup.send("Hey man, that lowkey exists already. Great minds think alike or some shit. Neigh neigh.")
                    print("Duplicate")
                    m = True
                else:
                    # Count how many quotes exist already
                    IDs = len(quotes)
                    with open("Quotes.txt", "a") as file:
                        file.write(f"{quote}\n")
                    # Append new one
                    print(f"Added {quote} at id {IDs + 1}")
                    await interaction.followup.send(f"We ball or something idk, added your quote at ID {IDs+1}")
            except Exception as e:
                await interaction.followup.send("My bad bro. Whoever coded me fucking sucks so it threw an error. If it uses emojis it might not work, my apologies.")
### GAMBLING!!!!!!!!!!!!!!!!!!!!!
@bot.tree.command(name="gamble", description="Flip a coin, and if it's what you chose...well let's just say...we'll up your score.")
@app_commands.describe(side="what side of the coin do you choose?", percent="What percent of your score are you betting? People in the negatives will have a max return to get them back to 0 score.")
async def gamble(interaction: discord.Interaction, side: str, percent: int):
    if side != "tails" and side != "heads":
        await interaction.response.send_message("Dude, that's not a side? The fuck are you doing?")
    elif percent >= 100 or percent <= 0:
        await interaction.response.send_message("A horse like me will not be tricked by your antics. Move along, slut")
    else: 
        score = await get_horse_hitlist(interaction.user.name, HorseHitListFile)
        print(interaction.user.name)
        print(score)
        print(percent) # debug
        await interaction.response.send_message(f"{interaction.user} is gambling! They chose {side}. Will they win {score*(percent/100):.0f} points? Or will they die trying?")
        time.sleep(0.5)
        await interaction.followup.send("Drumroll please...")
        win = False
        sidething = random.randint(1,2)
        if side == "heads" and sidething == 1:
            print("They won!")
            win = True
        elif side == "tails" and sidething == 2:
            print("They won!")
            win = True
        else:
            print("They fucking lost. What a bozo")
        time.sleep(3)
        if sidething == 1:
            await interaction.followup.send("The side is...**heads!**")
        else:
            await interaction.followup.send("The side is...**tails!**")
        time.sleep(0.5)
        if win == True:
            change_value = round(score * (percent / 100))
            await interaction.followup.send(f"Congrats! You won the coinflip, and won {score*(percent/100):.0f} points! Your new total is {score+score*(percent/100):.0f}!")
            await update_horse_hitlist(interaction.user.name, HorseHitListFile, change=change_value)
        else:
            await interaction.followup.send(f"Sadly, you have lost the coinflip. Your new score is {score-score*(percent/100):.0f}. Wanna try again? ")
            change_value = round(-1 * score * (percent / 100))
            await update_horse_hitlist(interaction.user.name, HorseHitListFile, change=change_value)
    
@bot.tree.command(name="score", description="Check how much Horse hates you.")
async def horsescore(interaction: discord.Interaction, user: discord.User = None):
    if user is None:
        user = interaction.user
    score = await get_horse_hitlist(user.name, HorseHitListFile)
    await interaction.response.send_message(f"{user.name}: **{score}** ")
    if score > 0:
        await interaction.followup.send("Good job.")
    else:
        await interaction.followup.send("What the hell are you doing?")

BlockedLetter = 'e'
@bot.tree.command(name="e", description="Disables everyone's access to a chosen letter.")
async def e(interaction: discord.Interaction, letter: str = None):
    global NoE
    global BlockedLetter
    if not NoE and letter != None:
        BlockedLetter = letter
        await interaction.response.send_message(f"Nobody can say **{BlockedLetter}** now.")
        NoE = True
        print(f"Set the blocked letter to {BlockedLetter}")
        
    else:
        await interaction.response.send_message(f"You can say {BlockedLetter} again.")
        NoE = False

@bot.tree.command(name="server", description="Checks to see if the server's online.")
async def server(interaction: discord.Interaction):
    print("Checking...")
    server_ip = "98.216.20.149"
    server_port = 25565

    try:
        server = JavaServer.lookup(f"{server_ip}:{server_port}")
        status = server.status()
        print(f"Server is online! {status.players.online} Non-Equines are online.")
        await interaction.response.send_message(f"Server is online! {status.players.online} Non-Equines are online.")
    except Exception as e:
        print("Server is offline or unreachable.")
        await interaction.response.send_message("Server is offline or unreachable.")

@bot.tree.command(name="pickupline", description="Submit a pickup line (or leave blank for info)")
async def pickupline(interaction: discord.Interaction, line: str = None):
    if line is None:
        await interaction.response.send_message("*One of the creators of Horse has made a deal with themself that if they do not lock in (that is, talk to a girl) before February 14th 2026, then they will have to send the top-rated pickup line to their love interest. Neigh.*")
    else:
        with open("PickupLines.txt", "a") as file:
            file.write(f"{line}\n")
            await interaction.response.send_message(f"*{interaction.user}* Submitted the pickup line '{line}'")
async def get_synonyms(word):
    url = "https://api.datamuse.com/words"
    
    if random.randint(1,2) == 1:
        params = {"rel_syn": word}
    else:
        params = {"rel_ant": word}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=2) as r:
                if r.status != 200:
                    return []
                data = await r.json()
                return [item["word"] for item in data]
    except Exception as e:
        print(f"Error fetching synonyms: {e}")
        return []
    
@bot.event
async def on_message(message):
    global trans
    global NoE
    global sex
    global BlockedLetter
    global syns
    global c
    global ch
    if str(message.channel.id) not in BlacklistedChannels:
        bingbong = message.content.lower().strip("'")
        
        # Typo detection
        result = find_typos(message.content)
        print(result)
        if result:
            corrections = ", ".join([f"'{w}' → '{c}'" for w, c in result])
            try:
                if random.randint(1,100) != 1: # 1 in 100
                    await message.channel.send("Fuck you.")
                else:
                    if random.randint(1,5) != 5: # 1 in 500
                        await message.channel.send("*Super fuck you.*")
                    else:
                        if random.randint(1,5) != 5: # 1 in 2,500
                            await message.channel.send("**Ultra Fuck you.**")
                        else:
                            if random.randint(1,5) != 5: # 1 in 12,500
                                await message.channel.send("***LEGENDARY FUCK YOU!***")
                            else:
                                await message.channel.send("# ***MYTHIC FUCK YOU!***") 

            except:
                pass

        if random.randint(1, 25) == 1:
            print("fetching wiki...")
            try:
                summary = wikipedia.summary(bingbong, sentences=random.randint(1, 5))
                print(summary)
                await message.channel.send(summary)
            except:
                print("No Wiki found :(")

        if random.randint(1, 10) == 1:
            print("Help")
            try:
                s = bingbong.strip()
                s = bingbong.split()
                syns = await get_synonyms(random.choice(s))
                print(random.choice(syns)) if syns else print("no synonyms found for word")
                await message.channel.send(f"**{random.choice(syns)}**.")
            except Exception as e:
                print(f"lmao {e}")

        if trans == True and not message.author.name == "Horse":
            print("oop")
            await message.delete()
            bingbong = message.content.lower().strip("'")
            result = await translator.translate(bingbong, dest='es')
            print(result.text)
            result = await translator.translate(result.text, dest='af')
            print(result.text)
            result = await translator.translate(result.text, dest='de')
            print(result.text)
            result = await translator.translate(result.text, dest='ta')
            print(result.text)
            # result = await translator.translate(result.text, dest='vi')
            print(result.text)
            # result = await translator.translate(result.text, dest='zu')
            print(result.text)
            # result = await translator.translate(result.text, dest='yi')
            print(result.text)
            result = await translator.translate(result.text, dest='en')
            print(result.text)
            await message.channel.send(f"{message.author.name}: {result.text}")

        Mockery = []
        if random.randint(1, 150) == 1 and message.author.name != "Horse":
            print("ARE YOU MOCKING ME????")
            for letter in bingbong:
                if random.randint(1,2) == 1:
                    Mockery.append(letter.lower())
                else:
                    Mockery.append(letter.capitalize())
            thing = ''.join(Mockery)
            print(thing)
            await message.channel.send(f"{thing}")
        
        if NoE and BlockedLetter in bingbong:
            print("E")
            try:
                await message.delete()
            except:
                print("Error...")
        if not "what" in bingbong and message.channel.name == ch:
            ch = ''
            c = 0
        if message.author.name == "cometvgc":
            if random.randint(1, 50) == 1:
                await message.channel.send("Omg transgender here")
                await update_horse_hitlist(message.author.name, HorseHitListFile, change=1)
                print("Ruby")
        if message.author.name == "Horse":
            return
        if random.randint(1, 100) == 1:
            if random.randint(1, 500) == 1:
                await message.add_reaction("🎃")
                await update_horse_hitlist(message.author.name, HorseHitListFile, change=100)
                print("Holy shit")
            else:
                try:
                    await message.add_reaction("🐴")
                    print(":3")
                    await update_horse_hitlist(message.author.name, HorseHitListFile, change=10)
                except discord.errors.Forbidden:
                    print("can't vro")
                    pass
        if random.randint(1, 75) == 1:
            try: 
                await message.channel.send(random.choice(Gifs))
                print(":33")
                await update_horse_hitlist(message.author.name, HorseHitListFile, change=25)
            except discord.errors.Forbidden:
                print("oopsies")
                pass
        if "is erin the imposter" in bingbong or "is erin it" in bingbong or "is it erin" in bingbong:
            await message.channel.send("Erin is obviously the imposter. The fuck you talking 'bout? Neigh Neigh motherfuckers.")
        if "i like my cheese drippy bruh" in bingbong:
            await message.channel.send("ok")
        if "i'm so hungry i could eat a horse" in bingbong:
            score = await get_horse_hitlist(message.author.name, HorseHitListFile)
            if score >= 0:
                await message.channel.send("Are you fucking kidding me")
            else:
                await message.channel.send("# We know.")
            await update_horse_hitlist(message.author.name, HorseHitListFile, change=-1)
        elif "summarize" in bingbong or "ask chatgpt" in bingbong or "ask horsegpt" in bingbong or "horsegpt?" in bingbong or "explain" in bingbong:
            await message.channel.send("Asking HorseGPT...")
            ans = ""
            time.sleep(3)
            while random.randint(1,25) != 25:
                ans += random.choice(Neighs)
            await message.channel.send(ans)
        elif "<@1403849240073211995>" in bingbong:
            pingresponse = [
                "Tf you want",
                "Can a horse like me get some sleep bro? Sybau",
                "You called?",
                "yep that's me",
                "I'm jorking it gimme a sec",
                "If it's not related to Paul McCartney, don't ping me.", ### Contributed by Rae
                "Imagine how sad your life must be to ping a fucking horse",
                "Mgmmhm~",
                "Neigh",
                "shut the fuck up I'm busy busting", ### Contributed by Dahl
            ]
            
            await message.channel.send(random.choice(pingresponse))
        elif "horse" in bingbong and "?" in bingbong:
            await message.channel.send(random.choice(yea))
        elif "how many" in bingbong or "how much" in bingbong or ("what's" in bingbong and "+" in bingbong):
            await message.channel.send(f"Probably like... {random.randint(1,10)}")
        elif "?" in bingbong and not "how many" in bingbong or "how much" in bingbong or "+" in bingbong:
            if random.randint(1, 2) == 1:
                await message.channel.send(random.choice(yea))
        elif "your" in bingbong and random.randint(1,2) == 1:
            await message.channel.send("*you're")
        elif "you're" in bingbong and random.randint(1,2) == 1:
            await message.channel.send("*your")
        elif "there" in bingbong and random.randint(1,2) == 1:
            await message.channel.send("*their")
        elif "their" in bingbong and random.randint(1,2) == 1:
            await message.channel.send("*they're")
        elif "they're" in bingbong and random.randint(1,2) == 1:
            await message.channel.send("*there")
        elif "i could eat a horse" in bingbong:
            await message.channel.send("There's no fucking way you're THAT hungry.")
            await update_horse_hitlist(message.author.name, HorseHitListFile, change=-1)
        elif "i'm hungry" in bingbong and "again" in bingbong:
            await message.channel.send("Fuck off")
        
        elif "i'm so hungry" in bingbong:
            await message.channel.send("How hungry...")
        elif "i'm not hungry" in bingbong:
            await message.channel.send("Thank the lord")
            await update_horse_hitlist(message.author.name, HorseHitListFile, change=1)

        elif ("hey" in bingbong and not "they" in bingbong) or "paul" in bingbong or "john lennon" in bingbong or "george harrison" in bingbong or "ringo starr" in bingbong or "stuart sutcliffe" in bingbong or "pete best" in bingbong or "jimmie nicol" in bingbong or "chas newby" in bingbong or "billy preston" in bingbong or "hay" in bingbong or "baithook" in bingbong:
            await message.channel.send("# WHERE??????????????")
        elif "evil twink" in bingbong:
            score = await get_horse_hitlist(message.author.name, HorseHitListFile)
            if score >= 0:
                await message.channel.send("That fucker will pay. Mark my words.")
            else:
                await message.channel.send("He's you, isn't he? Neighhhh...")
        elif "twink" in bingbong or "trystan" in bingbong or "toby" in bingbong or "jackson" in bingbong or "erin" in bingbong:
            await message.channel.send("The evil twink...he will pay. This twink seems fine tho")
        elif "carrot" in bingbong:
            score = await get_horse_hitlist(message.author.name, HorseHitListFile)
            if score >= 0:
                await message.channel.send("Can I shove it up my ass?")
            else:
                await message.channel.send("I'm gonna shove it so far up your ass it sees Neil's footprints.")
            await update_horse_hitlist(message.author.name, HorseHitListFile, change=1)
        elif "apple" in bingbong:
            await message.channel.send(":3")
        elif "cock" in bingbong and "horse" in bingbong:
            await message.channel.send("I know it's massive but you don't need to talk about it bro")
        elif "cock" in bingbong and "horse" not in bingbong:
            await message.channel.send("What kind of cock...")
        elif "what" in bingbong:
            print(c)
            if c == 0:
                ch = message.channel.name
                print(ch)
            c += 1
            if c == 10:
                await message.channel.send("Bro shut the fuck up")
            elif c == 25:
                await message.channel.send("Quit horsing around")
                await update_horse_hitlist(message.author.name, HorseHitListFile, change=-10)
            elif c == 30:
                await message.channel.send("I said stop. https://cdn.discordapp.com/attachments/1023729983744659527/1405356965957472377/sleipnir_grande.png?ex=689e882a&is=689d36aa&hm=ec08770e35e596df88b4e0e565e73666e2486c3387331196b20dc94caa7a347b&")
                await update_horse_hitlist(message.author.name, HorseHitListFile, change=-500)
                c = 0
                ch = ''
            else:
                await message.channel.send("what")
        elif "huh" in bingbong:
            await message.channel.send("huh")
        elif "job" in bingbong or "breather" in bingbong:
            await message.channel.send("My child...one must control themself in times of slurrage. One must not stray too far to the darkside. One must think before they speak, for one word could harm millions. Rest easy my child, and never say such a word again.")
            await update_horse_hitlist(message.author.name, HorseHitListFile, change=-3)
        elif "i love horse" in bingbong or "i love you horse" in bingbong or "i love horses" in bingbong or "i love this horse" in bingbong:
            score = await get_horse_hitlist(message.author.name, HorseHitListFile)
            if score >= -10:
                await message.channel.send("I love you too pookie <3")
            else:
                await message.channel.send("slut")
        elif ("thank you" in bingbong or "thanks" in bingbong) and ("horse" in bingbong):
            score = await get_horse_hitlist(message.author.name, HorseHitListFile)
            if score >= 0:
                await message.channel.send("You're so very welcome")
            else:
                await message.channel.send("Clip Clop slut")

        elif ("i need" in bingbong or "i want" in bingbong) and ("more" in bingbong or "so much" in bingbong):
            await message.channel.send("Biblical levels of gluttony...")
        elif "i need" in bingbong or "i want" in bingbong or "he wants" in bingbong or "she wants" in bingbong or "they want" in bingbong:
            await message.channel.send("Your greed is sickening.")
        elif "ride me" in bingbong:
            score = await get_horse_hitlist(message.author.name, HorseHitListFile)
            if score >= 0:
                await message.channel.send("The fuck did you just say to me?")
            else:
                await message.channel.send("I know you've never said that to anyone before.")
            await update_horse_hitlist(message.author.name, HorseHitListFile, change=-1)
        elif "can i ride you" in bingbong:
            score = await get_horse_hitlist(message.author.name, HorseHitListFile)
            if score >= 0:
                await message.channel.send("Absolutely the fuck not.")
            else:
                await message.channel.send("Billions of years of evolution. Billions. All that setup, all that random chance, or purposeful creation, and you...said that...to a horse. You know how sad that is, {message.author.name}? I hope you never feel the touch of a woman. Or man. Never talk to me again. Neigh Neigh motherfucker")
            
            await update_horse_hitlist(message.author.name, HorseHitListFile, change=-2)
        elif "fuck" in bingbong and "horse" in bingbong:
            await update_horse_hitlist(message.author.name, HorseHitListFile, change=-3)
            if message.author.name == "ash" or message.author.name == "thatgayemokod":
                await message.channel.send("Well fuck you too, Ash.")
            else:
                score = await get_horse_hitlist(message.author.name, HorseHitListFile)
                if score >= 0:
                    await message.channel.send("Hey man that's not very kind")
                else: await message.channel.send("kill youself")
        elif "shut up" in bingbong and "horse" in bingbong:
            await message.channel.send(":(")
            await update_horse_hitlist(message.author.name, HorseHitListFile, change=-2)
        elif "now has" in bingbong and "swears" in bingbong:
            goog = random.randint(1,6)
            if goog == 1:
                await message.channel.send("Fuck you Swear Jar.")
            elif goog == 2:
                await message.channel.send("Go to hell Swear Jar.")
            elif goog == 3:
                await message.channel.send("I'm gonna say a slur, Swear Jar.")
            elif goog == 4:
                await message.channel.send("Swear Jar I swear to fucking god.")
            elif goog == 5:
                await message.channel.send("Fuck off Swear Jar.")
            elif goog == 6:
                await message.channel.send("Y'know, Swear Jar, you're not half bad. What do you say, wanna get freaky?")
            await update_horse_hitlist(message.author.name, HorseHitListFile, change=-1)
        elif ("horse" in bingbong) and ("he" in bingbong or "his" in bingbong) and not ("she" in bingbong or "hers" in bingbong):
            await message.channel.send("Hey I'm a woman btw do you mind")
        elif "horseplay" in bingbong:
            await message.channel.send("...What play?")
        elif "horsing around" in bingbong:
            await message.channel.send("There better fucking not be anyone doing that.")
        elif "meow" in bingbong:
            await message.channel.send("The fuck did you just say to me?")
        elif "sabrina carpenter" in bingbong:
            await message.channel.send("MANCHIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIILD")
        elif "lesbian sex" in bingbong or "sesbian lex" in bingbong:
            await message.channel.send("Hm?")
        elif "yes" in bingbong:
            await message.channel.send("No")
            await update_horse_hitlist(message.author.name, HorseHitListFile, change=-1)
        elif "no" in bingbong:
            await message.channel.send("Yes")
            await update_horse_hitlist(message.author.name, HorseHitListFile, change=1)
        elif "chappell roan" in bingbong:
            await message.channel.send("So baby let's get freaky get kinky let's make this bed get squeaky!")
        elif "in vc" in bingbong or "join vc" in bingbong:
            await message.channel.send("Neigh Neigh? Brother why would I join VC I'm a fucking horse")
        elif "horse walks in" in bingbong:
            await message.channel.send("hi")
        elif ("hi" in bingbong or "hello" in bingbong) and "horse" in bingbong:
            await message.channel.send("Hello :3")
            await update_horse_hitlist(message.author.name, HorseHitListFile, change=1)
        elif "how are you" in bingbong or "how is" in bingbong and "horse" in bingbong:
            await message.channel.send("Every day is a struggle. Doing good tho how are you?")
            await update_horse_hitlist(message.author.name, HorseHitListFile, change=1)
        elif ("bye" in bingbong or "goodbye" in bingbong or "good bye" in bingbong) and ("horse" in bingbong):
            score = await get_horse_hitlist(message.author.name, HorseHitListFile)
            if score >= 15:
                await message.channel.send("Oh, bye :(")
            elif score >= 5:
                await message.channel.send("Cya! :)")
            elif score >= 0: 
                await message.channel.send("bye ig")
            elif score >= -15:
                await message.channel.send("Thank the lord")
        elif ("kill yourself" in bingbong or "kys" in bingbong) and "horse" in bingbong:
            await message.channel.send("# April. April 9th. Do not forget this date.")
            await update_horse_hitlist(message.author.name, HorseHitListFile, change=-5)
        elif "i fear" in bingbong:
            await message.channel.send("Why are you afraid? Do not be scared, my child...")

    else:
        print("Blacklisted!")
    await bot.process_commands(message)
# React Role Message
reaction_message_id = 1411870382952157314  

reaction_roles = {
    "🔴": "Red",
    "🟢": "Green",
    "🔵": "Blue",
    "🟣": "Purple",
    "🟠": "Orange"
}

@bot.tree.command(name="leaderboard", description="See the top and bottom scores (My favorite and least favorite not equine people).")
async def leaderboard(interaction: discord.Interaction):
    try:
        # Load scores
        data = {}
        with open(HorseHitListFile, "r") as file:
            lines = [line.strip() for line in file]
            for i in range(0, len(lines), 2):
                name = lines[i]
                score = int(lines[i + 1])
                data[name] = score

        if not data:
            await interaction.response.send_message("No scores yet! Everyone is equally loved (or hated).")
            return

        # Sort scores
        sorted_scores = sorted(data.items(), key=lambda x: x[1], reverse=True)

        # Top 5
        top_five = sorted_scores[:5]

        # Bottom 5
        bottom_five = sorted_scores[-5:][::-1]  # reverse so lowest is at the top

        # Build leaderboard text
        leaderboard_text = "# My Favorite Non-Equine People\n\n"

        leaderboard_text += "**Most Loved:**\n"
        for i, (name, score) in enumerate(top_five, start=1):
            leaderboard_text += f"**{i}.** {name} — {score}\n"

        leaderboard_text += "\n**Most Hated:**\n"
        for i, (name, score) in enumerate(bottom_five, start=1):
            leaderboard_text += f"**{i}.** {name} — {score}\n"

        await interaction.response.send_message(leaderboard_text)

    except FileNotFoundError:
        await interaction.response.send_message("No scores have been recorded yet!")
    except Exception as e:
        print(f"Error in leaderboard: {e}")
        await interaction.response.send_message("Something went wrong trying to load the leaderboard :(")

trans = False
@bot.tree.command(name="trans", description="This is a test command, use with caution.")
async def trans(interaction: discord.Interaction):
    global trans
    print("trans.")
    await interaction.response.send_message("One moment.")
    if trans == False:
        print("true")
        trans = True
    else:
        trans = False
        print("false")
    return trans

@bot.tree.command(name="pay", description="Spend some of that hard earned HorseBucks™ to pay someone!")
async def pay(interaction: discord.Interaction, user: discord.User, amount: int):
    
    print(user)
    print(amount)
    print(interaction.user.name)
    HorseBucks = await get_horse_hitlist(interaction.user.name, HorseHitListFile)
    if amount > HorseBucks or amount < 0:
        await interaction.response.send_message("Horseplay is not allowed. Fuck off.")
    else:
        print(f"subtracting {amount} from {interaction.user.name}")
        await update_horse_hitlist(interaction.user.name, HorseHitListFile, change=(amount*-1))
        time.sleep(0.5)
        await update_horse_hitlist(user.name, HorseHitListFile, change=(amount))
        await interaction.response.send_message(f"Sent {amount} HorseBucks™ to {user}")


@bot.command()
async def colorroles(ctx):
    global reaction_message_id
    message = await ctx.send("Good day. I am Horse. React to me to get a color role. Neigh Neigh.\n\n")
    for emoji in reaction_roles.keys():
        await message.add_reaction(emoji)

    reaction_message_id = 1411870382952157314
    print(f"Reaction role message ID set to {1411870382952157314}")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == "1411870382952157314":
        print(f"Reaction detected: {payload.emoji} by user {payload.user_id} on message {payload.message_id}")
        if payload.message_id != reaction_message_id or payload.user_id == bot.user.id:
            print("Something happened idk")
            return
        
        guild = bot.get_guild(payload.guild_id)
        if not guild:
            print("Something happened idk")
            return
        
        role_name = reaction_roles.get(payload.emoji.name)
        if not role_name:
            print("Something happened idk")
            return

        role = discord.utils.get(guild.roles, name=role_name)
        if role:
            print("Trying to add the role hol up")
            member = guild.get_member(payload.user_id)
            try:
                await member.add_roles(role)
                print(f"Gave {role_name} to {member.display_name}")
            except Exception as e:
                print(f"Fuck you. {e}")

@bot.event
async def on_raw_reaction_remove(payload):
    print("Lemme remove the role")
    if payload.message_id != reaction_message_id or payload.user_id == bot.user.id:
        print("Something happened idk")
        return
    
    guild = bot.get_guild(payload.guild_id)
    if not guild:
        print("Something happened idk")
        return
    
    role_name = reaction_roles.get(payload.emoji.name)
    if not role_name:
        print("Something happened idk")
        return

    role = discord.utils.get(guild.roles, name=role_name)
    if role:
        print("Gimme a sec.")
        member = guild.get_member(payload.user_id)
        try:
            await member.remove_roles(role)
            print(f"Removed {role_name} from {member.display_name}")
        except Exception as e:
            print(f"Fuck you. {e}")

# End Code
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
