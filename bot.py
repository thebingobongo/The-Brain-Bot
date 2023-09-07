import discord
from discord.ext import commands, tasks
import random
import openai
from dotenv import load_dotenv
import os
import asyncio

from databaselayer import *


# get bot token and openai apikey
load_dotenv()
openai.api_key = os.getenv('APIKEY')
bot_token = os.getenv('TOKEN')


intents = discord.Intents().default()
intents.members = True
client = commands.Bot(command_prefix='.', help_command=None, intents=intents)



def predicate(ctx):
    admin_role1 = discord.utils.get(ctx.guild.roles, id=835623182484373535)
    admin_role2 = discord.utils.get(ctx.guild.roles, id=835400292979179530)
    return admin_role1 in ctx.author.roles or admin_role2 in ctx.author.roles or ctx.author.id == 339070790987284491



has_roles = commands.check(predicate)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('with ideas'))
    print("I am alive.")


@client.command()
@has_roles
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send("done")


@client.command()
@has_roles
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send("Done")


@client.command()
@has_roles
async def rename(ctx,* ,name):
    thevat = ctx.message.guild
    await ctx.send("COMMENCING")
    x = 0
    for member in thevat.members:
        try:
            await member.edit(nick=name)
            print(f"Doing it {x}")
        except:
            print(f"not doing it {x}")
        x += 1
    await ctx.send("DONE")


@client.command()
@has_roles
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Done")


@client.command()
@has_roles
async def loadall(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                client.load_extension(f"cogs.{filename[:-3]}")
                print(f"{filename} has been loaded.")
            except:
                print(f"{filename} has already been loaded.")
    await ctx.send("Done.")


@client.command()
@has_roles
async def unloadall(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                client.unload_extension(f"cogs.{filename[:-3]}")
                print(f"{filename} has been unloaded.")
            except:
                print(f"{filename} is already unloaded")
    await ctx.send("Done.")


@client.command()
@has_roles
async def cogstatus(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                client.load_extension(f"cogs.{filename[:-3]}")
            except commands.ExtensionAlreadyLoaded:
                await ctx.send(f"{filename} is loaded")
            except commands.ExtensionNotFound:
                await ctx.send(f"{filename} not found")
            else:
                await ctx.send(f"{filename} is unloaded")
                client.unload_extension(f"cogs.{filename[:-3]}")

    await ctx.send("Done.")


@client.command(aliases=["cogslist"])
@has_roles
async def coglist(ctx):
    embed = discord.Embed(title="List of Cogs",color=0x00ffff)
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            embed.add_field(name=filename, value="** **", inline=True)
    await ctx.send(embed=embed)


@client.command()
@commands.is_owner()
async def init(ctx, member:discord.Member=None):
    if member == None:
        for member in ctx.guild.members:
            print(f'{member.name} is being attempted')
            try:
                exists = getUserBal(member.id)
                print(f'{member.name} is already in the db')
            except:
                print(f'{member.name} has been added to the db')
                createUser(member.id)
        await ctx.send("All members have been initialized.")
    else:
        createUser(member.id)
        print(f'{member.name} has been added to the db')
        await ctx.send(f"{member.name} has been initialized.")



@client.command()
@commands.is_owner()
async def resetdatabase(ctx):
    resetBalance()
    await ctx.send("The brain cell table has been reset.")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.CommandOnCooldown):
        if error.retry_after < 60:
            await ctx.send(f'This command is on cooldown, you can use it in {round(error.retry_after, 1)} seconds')
        elif error.retry_after > 3600:
            timeleft = (error.retry_after / 60) / 60
            await ctx.send(f'This command is on cooldown, you can use it in {round(timeleft, 1)} hour(s).')
        else:
            timeleft = error.retry_after / 60
            await ctx.send(f'This command is on cooldown, you can use it in {round(timeleft, 1)} minute(s)')

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
        await ctx.send("You do not have the roles required for that command, please try again.")

    elif isinstance(error,commands.CommandInvokeError):
        if "(error code: 40032)" in str(error.original):
            await ctx.send("User was not connected to voice.")
        else:
            await ctx.send(f"Command raised an exception: {error.original}")




@client.event
async def on_message(message):

    if message.author == client.user:
        return


    try:
        rand = random.randint(1, 2)
        if rand == 2:
            addBal(message.author.id, 1)
    except:
        pass

    # Processing the message so commands will work
    await client.process_commands(message)

#
# @client.event
# async def on_member_remove(member):
#     deleteUser(member.id)

# @client.event
# async def on_member_join(member):
#     createUser(member.id)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
        print(f"{filename} has been loaded.")


# data['TOKEN']
client.run(bot_token)
