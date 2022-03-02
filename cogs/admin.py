import discord
from discord.ext import commands
import asyncio
from databaselayer import *
import datetime

def predicate(ctx):
    admin_role1 = discord.utils.get(ctx.guild.roles, id=835623182484373535)
    admin_role2 = discord.utils.get(ctx.guild.roles, id=835400292979179530)
    return admin_role1 in ctx.author.roles or admin_role2 in ctx.author.roles or ctx.author.id == 339070790987284491
    # test = discord.utils.get(ctx.guild.roles, id=858614845363322881)
    # return test in ctx.author.roles


has_roles = commands.check(predicate)


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @has_roles
    async def award(self, ctx, member:discord.Member, ammount:int):
        if member == None:
            await ctx.send("Who do you want to give brain cells.")
            return
        if ammount == None:
            await ctx.send(f"How much do you want to give {member.name}?")
            return
        addBal(member.id, ammount)
        await ctx.send(f"{member.name} has been awarded {ammount} Brain Cells!")

    @commands.command()
    @has_roles
    async def awardvc(self,ctx, ammount = 200):
        voice_channel = ctx.message.author.voice.channel
        for mem in voice_channel.members:
            addBal(mem.id,ammount)
        await ctx.send(f"All members in this VC have been awarded {ammount} Brain Cells!")

    @commands.command(name="raidban")
    @has_roles
    async def raidban(self, ctx, minutes: int):
        log_channel = self.bot.get_channel(934867511273476177)
        for member in ctx.guild.members:
            check_time = datetime.datetime.now(member.joined_at.tzinfo) - datetime.timedelta(minutes=minutes)
            if member.joined_at > check_time:
                await member.ban(reason="raid")
                await log_channel.send(f"Banned: {member.name} for raiding")

    @commands.command()
    @has_roles
    async def slowban(self, ctx, member: discord.Member, time_to_ban: int, *, reason=None):
        await ctx.send(
            f" <a:vibing:847619864738267217> <a:vibing:847619864738267217> {member.mention} is gonna get banned in {time_to_ban} seconds!!!! <a:vibing:847619864738267217> <a:vibing:847619864738267217>")
        for i in range(time_to_ban):
            await ctx.send(f"{member.mention} is gone in {time_to_ban - i} seconds <a:vibing:847619864738267217>")
            await asyncio.sleep(1)
        await member.ban(reason=reason)
        await ctx.send(
            f"<a:vibing:847619864738267217><a:vibing:847619864738267217><a:vibing:847619864738267217> {member.display_name} IS GONE NOW! <a:vibing:847619864738267217><a:vibing:847619864738267217><a:vibing:847619864738267217>")

    @commands.command()
    @has_roles
    async def slowestban(self, ctx, member: discord.Member, time_to_ban: int, *, reason=None):
        await ctx.send(
            f" <a:vibing:847619864738267217> <a:vibing:847619864738267217> {member.mention} is gonna get banned in {time_to_ban} seconds!!!! <a:vibing:847619864738267217> <a:vibing:847619864738267217>")
        for i in range(time_to_ban):
            await ctx.send(f"{member.mention} is gone in {time_to_ban - i} seconds <a:vibing:847619864738267217>")
            await asyncio.sleep(1)
        await ctx.send(
            f"<a:vibing:847619864738267217><a:vibing:847619864738267217><a:vibing:847619864738267217> {member.display_name} IS GONE NOW! <a:vibing:847619864738267217><a:vibing:847619864738267217><a:vibing:847619864738267217>")

    @commands.command()
    @has_roles
    async def clear(self, ctx, amount=5):
        panopticon = self.client.get_channel(835630845996826676)
        await panopticon.purge(limit=amount)

    @commands.command()
    @has_roles
    async def echo(self, ctx, channelID: int, *, txt):
        sendchannel = self.client.get_channel(channelID)
        await sendchannel.send(txt)

    @commands.command()
    @has_roles
    async def doomsday(self, ctx, ntime):
        await ctx.send(
            f"<a:vibing:847619864738267217><a:vibing:847619864738267217> **Doomsday initiated for {ntime} seconds.** \n Commencing Doomsday <a:vibing:847619864738267217><a:vibing:847619864738267217>")
        ntime = int(ntime)
        for i in range(ntime):
            await ctx.send(
                f"<a:vibing:847619864738267217><a:vibing:847619864738267217> T - {ntime - i} <a:vibing:847619864738267217><a:vibing:847619864738267217>")
            await asyncio.sleep(1)
        await ctx.send("Sike motherfuckers. Get a life.")
        await ctx.send(
            " <a:vibing:847619864738267217><a:vibing:847619864738267217><a:vibing:847619864738267217><a:vibing:847619864738267217>")

    @commands.command()
    @has_roles
    async def gclr(self, ctx, number: int):
        await ctx.channel.purge(limit=(number+1))

def setup(client):
    client.add_cog(Admin(client))