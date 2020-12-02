# importing discord bot tools
import discord
from discord.ext import commands

# importing other functionalities
import os
import random
import json
import asyncio
from dotenv import load_dotenv

# initializing environment variables (sensitive information)
# env variables taken from either a .env file or from github/heroku secret keys
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PRIVATE_COMMAND_1 = os.getenv('PRIVATE_ONE')
PRIVATE_COMMAND_2 = os.getenv('PRIVATE_TWO')

# declaring first char needed to call a command (from user input)
client = commands.Bot(command_prefix='/')


# displays a message on command line confirming bot startup
@client.event
async def on_ready():
    print("bot is active")

# removing built-in help command
client.remove_command('help')


# creating custom help command
@client.command(name='help')
async def help(ctx):
    response = discord.Embed(title='BOT HELP')
    response.add_field(name="help", value="shows this message", inline=False)
    response.add_field(name="ping", value="returns the bot's delay with server", inline=False)
    response.add_field(name="test", value="shows sample embedded message", inline=False)
    response.add_field(name="8ball", value="ask a question and it will answer", inline=False)
    response.add_field(name="burrito", value="sends gif of a burrito", inline=False)
    response.add_field(name="gacha", value="summons random creature", inline=False)
    response.add_field(name="gacha_info", value="shows stats about the gacha command", inline=False)
    response.add_field(name="doot", value="dispenses doots (HALLOWEEN SEASON ONLY)")
    response.add_field(name="jingle", value="dispenses holiday cheer (CHRISTMAS SEASON ONLY)")
    response.set_footer(text='''
    --------------------------------------------------------------------------\n
    if you have ideas/pics to add, just let me know!
    ''')
    await ctx.send(embed=response)


# checks to see if discord user has the following IDs
def is_it_me(ctx):
    if ctx.author.id == 128236709715378176:
        return True
    if ctx.author.id == 694024881330716722:
        return True


# secret command: certain users can clear the specified amount of messages
@client.command()
@commands.check(is_it_me)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)


# returns bot's delay from discord server
@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)} ms')


# opens the json used for testing embedded messages
with open('data/Test_Pics.json') as file:
    testdict = json.load(file)


# tests sending discord embedded messages
@client.command(name='test')
async def test(ctx):
    response = discord.Embed(color=discord.Color.orange(), title='Testing')
    response.set_image(url=random.choice(list(testdict.values())))
    response.set_footer(text="This is the footer")
    response.set_author(name="By: Me")
    await ctx.send(embed=response)


# user asks a question; returns a classic magic8ball answer
@client.command(aliases=['8ball', 'eightball'])
async def magic8ball(ctx, *, question):

    responses = ['it is certain',
                 'it is decidedly so',
                 'without a doubt',
                 'yes - definitely',
                 'you may rely on it',
                 'as I see it, yes',
                 'most likely',
                 'outlook good',
                 'signs point to yes',
                 'reply hazy, try again',
                 'ask again later',
                 "better not tell you now",
                 'cannot predict now',
                 'concentrate and ask again',
                 "don't count on it",
                 'my reply is no',
                 'my sources say no.',
                 'outlook not so good',
                 'very doubtful']

    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


# tests sending discord gifs
@client.command(name='burrito')
async def response(ctx):
    await ctx.send("BURRITO IS COOKING...")
    await asyncio.sleep(3)

    await ctx.send(file=discord.File('data/image0.gif'))


# opens the library for the gacha game
with open('data/gacha.json') as file:
    gacha_dict = json.load(file)


# gacha game: draws one card/summon/collectible from the deck
@client.command(name='gacha')
async def gacha(ctx):
    # units are taken from the library and sorted by rarity
    units = gacha_dict.keys()
    specials = []
    one_stars = []
    two_stars = []
    three_stars = []
    four_stars = []
    five_stars = []
    ten_stars = []

    for unit in units:
        if gacha_dict[unit][1] == 1:
            one_stars.append(unit)
        elif gacha_dict[unit][1] == 2:
            two_stars.append(unit)
        elif gacha_dict[unit][1] == 3:
            three_stars.append(unit)
        elif gacha_dict[unit][1] == 4:
            four_stars.append(unit)
        elif gacha_dict[unit][1] == 5:
            five_stars.append(unit)
        elif gacha_dict[unit][1] == 10:
            ten_stars.append(unit)
        else:
            specials.append(unit)

    # the number returned by the selector determines what rarity will be pulled
    selector = random.randint(1, 100)

    # 1 percent chance
    if selector == 100:
        pool = ten_stars
    # 3 percent chance
    elif selector >= 97:
        pool = five_stars
    # 8 percent chance
    elif selector >= 89:
        pool = four_stars
    # 20 percent chance
    elif selector >= 69:
        pool = three_stars
    # 25 percent chance
    elif selector >= 44:
        pool = two_stars
    # 34 percent chance
    elif selector >= 11:
        pool = one_stars
    # 10 percent chance
    else:
        pool = specials

    unit = random.choice(pool)
    await ctx.send("YOU GOT... ")

    # depending on the rarity, a different color is assigned to the embedded message
    if gacha_dict[unit][1] == 1:
        rarity_color = discord.Color.lighter_gray()
    elif gacha_dict[unit][1] == 2:
        rarity_color = discord.Color.blue()
    elif gacha_dict[unit][1] == 3:
        rarity_color = discord.Color.green()
    elif gacha_dict[unit][1] == 4:
        rarity_color = discord.Color.gold()
    elif gacha_dict[unit][1] == 5:
        rarity_color = discord.Color.magenta()
    elif gacha_dict[unit][1] == 10:
        rarity_color = discord.Color.purple()
    else:
        rarity_color = discord.Color.dark_grey()

    response = discord.Embed(color=rarity_color, title=gacha_dict[unit][0])

    # from the specific unit drawn, their information from the library is formatted into an embedded message
    response.set_image(url=gacha_dict[unit][4])
    response.set_author(name="RARITY: " + "★" * gacha_dict[unit][1])
    if gacha_dict[unit][1] == 0:
        response.set_author(name="SPECIAL EFFECT:")
    response.set_footer(text="Copyright This Bot Inc.")
    response.add_field(name='Description: ', value=gacha_dict[unit][2], inline=False)
    response.add_field(name='Special Ability: ', value=gacha_dict[unit][3], inline=False)
    await ctx.send(embed=response)


# provides information on the library of units in the gacha dictionary
# info includes number of units of each rarity and the probability of drawing a certain rarity
@client.command(name='gacha_info')
async def gacha_info(ctx):
    all_units = list(gacha_dict.keys())
    zero_stars = []
    one_stars = []
    two_stars = []
    three_stars = []
    four_stars = []
    five_stars = []
    legends = []

    for unit in all_units:
        if gacha_dict[unit][1] == 0:
            zero_stars.append(unit)
        elif gacha_dict[unit][1] == 1:
            one_stars.append(unit)
        elif gacha_dict[unit][1] == 2:
            two_stars.append(unit)
        elif gacha_dict[unit][1] == 3:
            three_stars.append(unit)
        elif gacha_dict[unit][1] == 4:
            four_stars.append(unit)
        elif gacha_dict[unit][1] == 5:
            five_stars.append(unit)
        elif gacha_dict[unit][1] == 10:
            legends.append(unit)

    response = discord.Embed(title="Gacha Information and Stats")
    response.add_field(name='number of all units:', value=len(all_units), inline=False)
    response.add_field(name='number of effect summons (pull chance: 10%):', value=len(zero_stars), inline=False)
    response.add_field(name='number of one star units (pull chance: 34%):', value=len(one_stars), inline=False)
    response.add_field(name='number of two star units (pull chance: 25%):', value=len(two_stars), inline=False)
    response.add_field(name='number of three star units (pull chance: 20%):', value=len(three_stars), inline=False)
    response.add_field(name='number of four star units (pull chance: 8%):', value=len(four_stars), inline=False)
    response.add_field(name='number of five star units (pull chance: 3%):', value=len(five_stars), inline=False)
    response.add_field(name='number of LEGENDARY units (pull chance: 1%):', value=len(legends), inline=False)
    await ctx.send(embed=response)


# loads data from the couple and couple_quotes libraries
with open('data/couple.json') as file:
    pictures_dict = json.load(file)

with open('data/couple_quotes.json') as file:
    quotes_dict = json.load(file)


# if the user knows the private command and has the proper ID, they can access this commands
# returns a picture of a couple and a quote that describes the picture
@client.command(name=PRIVATE_COMMAND_1)
@commands.check(is_it_me)
async def oh(ctx):
    picture = random.choice(list(pictures_dict.keys()))
    quote = random.choice(list(quotes_dict.keys()))

    response = discord.Embed(color=discord.Color.red(), title=pictures_dict[picture][0])
    response.set_image(url=pictures_dict[picture][1])
    response.add_field(name=quotes_dict[quote][0] + ":", value=quotes_dict[quote][1])
    await ctx.send(embed=response)


# returns a halloween themed picture
# removed: halloween is over
"""
with open('data/spook.json') as file:
    dootlist = json.load(file)


@client.command(name='doot')
async def doot(ctx):
    picture = random.choice(dootlist)
    await ctx.send(picture)
"""


# very similar to PRIVATE_COMMAND_1 but instead utilizes .txt files instead of .json
@client.command(name=PRIVATE_COMMAND_2)
@commands.check(is_it_me)
async def nom(ctx):
    pics = []
    quotes = []

    with open('data/pictures.txt', 'r') as file:
        for line in file:
            strip_line = line.strip()
            if strip_line not in pics:
                pics.append(strip_line)

    with open('data/picture_captions.txt', 'r') as file:
        for line in file:
            quotes.append(line.strip())

    pic = random.choice(pics)
    quote = random.choice(quotes)

    await ctx.send(pic)
    await ctx.send(quote)

# runs the bot using the bot specific token
client.run(TOKEN)
