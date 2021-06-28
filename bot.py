import discord
from discord.ext import commands, tasks
import random
import openai
from dotenv import load_dotenv
import os
import asyncio

from cogs.messages import getDateFact, getQuote, getAdvice
from debateTopics import debateTopics


# get bot token and openai apikey
load_dotenv()
openai.api_key = os.getenv('APIKEY')
bot_token = os.getenv('TOKEN')


# with open('token.json') as json_file:
#     data = json.load(json_file)
#
# openai.api_key = data['APIKEY']



# todolist = []


client = commands.Bot(command_prefix='.', help_command=None)

originalrole = {}


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('with ideas'))
    print("I am alive.")
    keepalive.start()
    waterreminder.start()
    # await asyncio.sleep(1800)
    # debatetopicloop.start()


@tasks.loop(minutes=60)
async def waterreminder():
    general = client.get_channel(831211215878488078)
    rand = random.randint(1, 3)
    if rand == 1:
        embed = getDateFact()
        embed.add_field(name="This is your hourly reminder to go drink some water!", value="** **")
    elif rand == 2:
        embed = getQuote()
        embed.add_field(name="This is your hourly reminder to go drink some water!", value="** **")
    elif rand == 3:
        embed = getAdvice()
        embed.add_field(name="This is your hourly reminder to go drink some water!", value="** **")

    embed.set_footer(
        text="For more info check the Rules and Info channel. \nIf you encouter any issues, DM me or any of the mods!")
    await general.send(embed=embed)

# @tasks.loop(minutes=60)
# async def debatetopicloop():
#     await client.wait_until_ready()
#     general = client.get_channel(831211215878488078)
#     rand = random.randint(1, len(debateTopics))
#     while len(debateTopics[rand]) > 250:
#         rand = random.randint(1, len(debateTopics))
#
#     embed = discord.Embed(title=debateTopics[rand], color=0xc203fc)
#     embed.add_field(name="It's .debatetopic for more!", value="** **")
#
#     embed.set_footer(
#         text="For more info check the Rules and Info channel. \nIf you encouter any issues, DM me or any of the mods!")
#     await general.send(embed=embed)

@tasks.loop(minutes=3)
async def keepalive():
    await client.wait_until_ready()
    channel = client.get_channel(856065317524733954)
    await channel.send("keeping shit alive ")


@client.command()
@commands.has_any_role(835623182484373535,835400292979179530)
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send("done")


@client.command()
@commands.has_any_role(835623182484373535,835400292979179530)
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send("done")


@client.command()
@commands.has_any_role(835623182484373535,835400292979179530)
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send("done")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error,commands.MissingPermissions):
        await ctx.send("You do not have the permissions to use that command.")
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("You are missing a required argument, please try again.")
    elif isinstance(error,commands.MemberNotFound):
        await ctx.send("Member was not found, please try again.")
    elif isinstance(error,commands.ChannelNotFound):
        await ctx.send("The channel could not be found or does not exist, please try again.")
    elif isinstance(error,commands.BadArgument):
        await ctx.send("One of the arguments failed. Please try again.\n P.S. If a member is a required argument, you must **mention** them with @.")
    elif isinstance(error,commands.TooManyArguments):
        await ctx.send("You have added too many arguments, please try again.")
    elif isinstance(error,commands.MissingRole):
        return
    elif isinstance(error,commands.CommandInvokeError):
        if "(error code: 40032)" in str(error.original):
            await ctx.send("User was not connected to voice.")
        else:
            await ctx.send(f"Command raised an exception: {error.original}")



@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    # Processing the message so commands will work
    await client.process_commands(message)



for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
        print(f"{filename} has been loaded.")


# data['TOKEN']
client.run(bot_token)