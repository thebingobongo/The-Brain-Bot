import discord
from discord.ext import commands
import random

from databaselayer import *


def predicate(ctx):
    staff_role = discord.utils.get(ctx.guild.roles, id=831214459682029588)
    return staff_role in ctx.author.roles


has_roles = commands.check(predicate)


class Database(commands.Cog):

    def __init__(self, client):
        self.client = client

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #
    @commands.command(aliases=["bal"])
    async def balance(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        res = getUserBal(member.id)
        embed = discord.Embed(title=f"{member.display_name} has {res} Brain cells!",colour=member.colour)
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/861788174249754634/863326727018905640/happybrain.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def give(self, ctx, member: discord.Member = None, ammount: str = None):
        if ctx.channel.id == 831211215878488078:
            await ctx.send("Use <#835370412161630270> you stupid fuck")
            return
        if 'all' in ammount.strip().lower():
        # if ammount == "all":
            ammount = getUserBal(ctx.author.id)
        try:
            ammount = int(ammount)
        except:
            await ctx.send("There was an error, try again.")
            return
        if member == None:
            await ctx.send("Who do you want to give brain cells.")
            return
        if ctx.author == member:
            await ctx.send("Can't give yourself brain cells, dummy.")
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
        if not hasEnough(ctx.author.id, ammount):
            await ctx.send("Need more brain cells for that buddy.")
            return
        addBal(member.id, ammount)
        subBal(ctx.author.id, ammount)
        embed = discord.Embed(title=f"You have given {ammount} brain cells to {member.display_name}!", colour=member.colour)
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/861788174249754634/863326727018905640/happybrain.png")
        await ctx.send(embed=embed)

    @commands.command(aliases=["think", "earn"])
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        if ctx.channel.id == 831211215878488078:
            await ctx.send("Use <#835370412161630270> you stupid fuck")
            return
        earned = random.randint(200, 1000)
        addBal(ctx.author.id, earned)
        embed = discord.Embed(title=f"You just earned {earned} Brain Cells!",
                              colour=ctx.author.colour)
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/861788174249754634/863326727018905640/happybrain.png")
        await ctx.send(embed=embed)

    @commands.command(aliases=["addwarn"])
    @has_roles
    async def warn(self, ctx, member:discord.Member = None, *, warn:str=None):
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

    @commands.command(aliases=['showwarns','swarns','warns'])
    async def showWarns(self,ctx,target:discord.Member=None):
        if target == None:
            target = ctx.author
        res = getWarns(target.id)
        embed = discord.Embed(title=f"Warns for {target.display_name}", colour=target.colour)
        count = 1
        for warn in res:
            submitter = self.client.get_user(int(warn[2]))
            embed.add_field(name=f"{count}. {warn[1]}", value=f"Submitted by {submitter.name}, on {warn[3]}")
            count += 1
        embed.set_footer(text="It's .deletewarn to delete a warning, or .warn to add a warning.")
        await ctx.send(embed=embed)

    @commands.command(aliases=['delwarn','deletewarn'])
    @has_roles
    async def deleteWarn(self,ctx,member:discord.Member=None, index:int=None):
        if index == None:
            await ctx.send("Please specify which warning to delete by its index.")
            return
        if member == None:
            await ctx.send("Please mention which members warning you would like to delete.")
            return
        res = getWarns(member.id)
        index = index - 1
        warns = res[index]
        # cur.execute(f"DELETE FROM warns WHERE discordid = {member.id} AND warnmessage = '{warns[1]}'")
        # con.commit()
        deleteWarn(member.id, warns[1])
        await ctx.send("Warn has been deleted.")

    @commands.command(aliases=["addnote"])
    @has_roles
    async def note(self, ctx, member:discord.Member = None, *, note:str=None):
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

    @commands.command(aliases=['shownotes','snotes','notes'])
    @has_roles
    async def showNotes(self,ctx,target:discord.Member=None):
        if target == None:
            target = ctx.author
        res = getNotes(target.id)
        embed = discord.Embed(title=f"Notes for {target.display_name}",colour=target.colour)
        count = 1
        for note in res:
            submitter = self.client.get_user(int(note[2]))
            embed.add_field(name=f"{count}. {note[1]}",value=f"Submitted by {submitter.name}, on {note[3]}")
            count += 1
        embed.set_footer(text="It's .deletenote to delete a note, or .addnote to add a note.")
        await ctx.send(embed=embed)

    @commands.command(aliases = ['deletenote','delnote'])
    @has_roles
    async def deleteNote(self,ctx,member:discord.Member=None, index:int=None):
        if index == None:
            await ctx.send("Please specify which note to delete by its index.")
            return
        if member == None:
            await ctx.send("Please mention which members note you would like to delete.")
            return
        res = getNotes(member.id)
        notes = res[index-1]
        # cur.execute(f"DELETE FROM notes WHERE discordid = {member.id} AND note = '{notes[1]}'")
        # con.commit()
        deleteNote(member.id, notes[1])
        await ctx.send("Note has been deleted.")

    @commands.command(aliases=['leaderboard','top','rich','smart'])
    async def smartest(self, ctx):
        if ctx.channel.id == 831211215878488078:
            await ctx.send("Use <#835370412161630270> you stupid fuck")
            return
        res = getLeaderBoard()
        count = 1
        embed = discord.Embed(title="The Smartest",colour=ctx.author.color)
        for member in res:
            try:
                user = self.client.get_user(int(member[0]))
                name = user.display_name
            except:
                name = "Unknown User"
            embed.add_field(name=f"{count}. {name}",value=f"{member[1]} Brain Cells",inline=False)
            count += 1
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Database(client))