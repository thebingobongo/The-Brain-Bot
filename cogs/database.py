import discord
from discord.ext import commands
import random

from databaselayer import *

def predicate(ctx):
    staff_role = discord.utils.get(ctx.guild.roles, id=831214459682029588)
    return staff_role in ctx.author.roles
    # test = discord.utils.get(ctx.guild.roles, id=858614845363322881)
    # return test in ctx.author.roles

has_roles = commands.check(predicate)

class Database(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        rand = random.randint(1,2)
        if rand == 2:
            addBal(message.author.id, 1)



    @commands.command(aliases=["bal"])
    async def balance(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        res = getUserBal(member.id)
        await ctx.send(f"{member.display_name} has {res} Brain cells!")

    @commands.command()
    async def give(self, ctx, member: discord.Member = None, ammount: int = None):
        if member == None:
            await ctx.send("Who do you want to give brain cells.")
            return
        if ammount == None:
            await ctx.send(f"How much do you want to give {member.name}?")
            return
        elif ammount < 0:
            await ctx.send("Can't do that.")
            return
        elif not isinstance(ammount, int):
            await ctx.send("Can't do that.")
            return
        if hasEnough(ctx.author.id, ammount):
            await ctx.send("Need more brain cells for that buddy.")
            return
        addBal(member.id, ammount)
        subBal(ctx.author.id, ammount)
        # userbal = getUserBal(ctx.author.id)
        # recbal = getUserBal(member.id)
        # newrecbal = recbal + ammount
        # newuserbal = userbal - ammount
        # updateUserBal(member.id, newrecbal)
        # updateUserBal(ctx.author.id, newuserbal)
        await ctx.send(f"You have given {ammount} brain cells to {member.display_name}!")


    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def coinflip(self, ctx,ammount:int = 10, options:str = None):
        if options == None:
            await ctx.send("Heads or Tails? Try again.")
            return
        if ammount < 0:
            await ctx.send("Can't do that buddy.")
            return
        if hasEnough(ctx.author.id, ammount):
            await ctx.send("You don't have enough Brain Cells for that.")
            return
        options = options.strip().lower()
        result = random.randint(0,1)
        if options not in ["heads", 'head', 'tails', "tail"]:
            await ctx.send("Enter a valid option.")
            return
        if result == 1 and (options == "heads" or options == "head"):
            await ctx.send(f"It was Heads! You win {ammount} Brain cells!")
            addBal(ctx.author.id, ammount)
            return
        elif result == 0 and (options == "tails" or options == "tail"):
            await ctx.send(f"It was Tails! You win {ammount} Brain cells!")
            addBal(ctx.author.id, ammount)
            return
        elif result == 1:
            await ctx.send(f"It was Heads, you lose {ammount} Brain Cells!")
            subBal(ctx.author.id, ammount)
        elif result == 0:
            await ctx.send(f"It was Tails, you lose {ammount} Brain Cells!")
            subBal(ctx.author.id, ammount)


    @commands.command(aliases=["think", "earn"])
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        earned = random.randint(5, 50)
        addBal(ctx.author.id, earned)
        await ctx.send(f"You just earned {earned} Brain Cells!")


    @commands.command(aliases=["addwarn"])
    @has_roles
    async def warn(self, ctx, member:discord.Member = None, warn:str=None):
        if member == None:
            await ctx.send("Name a member.")
            return
        if warn == None:
            await ctx.send("What are you warning them for?")
            return
        if len(warn) > 300:
            await ctx.send("Please limit the length of the 'warn' to 300 characters.")
            return
        addWarn(member.id, warn, ctx.author.id)
        await ctx.send(f"{member.mention} has been warned.")


    # @commands.command()
    # async def showWarns(self,ctx,target:discord.Member=None):
    #     res = getWarns(target.id)
    #     await ctx.send(res)


    @commands.command(aliases=["addnote"])
    @has_roles
    async def note(self, ctx, member:discord.Member = None, note:str=None):
        if member == None:
            await ctx.send("Name a member.")
            return
        if note == None:
            await ctx.send("What did you want to note?")
            return
        if len(note) > 300:
            await ctx.send("Please limit the length of the 'note' to 300 characters.")
            return
        addNote(member.id, note, ctx.author.id)
        await ctx.send("Note has been added.")

    # @commands.command()
    # async def showNotes(self,ctx,target:discord.Member=None):
    #     res = getNotes(target.id)
    #     await ctx.send(res)

def setup(client):
    client.add_cog(Database(client))