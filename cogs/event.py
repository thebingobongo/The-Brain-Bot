import discord
from discord.ext import commands
import asyncio
import random

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def vibecheck(self, ctx, member:discord.Member=None):
        if member == None:
            await ctx.send("Whos vibe would you like to check?")
            return
        redteam = discord.utils.get(ctx.guild.roles, id=903488654364778556)
        blueteam = discord.utils.get(ctx.guild.roles, id=903489166237634570)
        strin = f"Looking through {member.mention}'s messages\n Commencing analysis:"
        await ctx.send(strin)
        await asyncio.sleep(20)
        await ctx.send("100% completed")
        results = random.randint(1, 100)
        if redteam in member.roles:
            await ctx.send(f"{member} has been assigned to Red team")
            await member.add_roles(redteam)
        elif blueteam in member.roles:
            await ctx.send(f"{member} has been assigned to Blue team")
            await member.add_roles(blueteam)
        elif results <= 50:
            await ctx.send(f"{member} has been assigned to Red team")
            await member.add_roles(redteam)
        elif results <= 100:
            await ctx.send(f"{member} has been assigned to Blue team")
            await member.add_roles(blueteam)
        await ctx.send("-------------------------------------------------")


    @commands.command()
    async def answer(self,ctx,*, answer=None):
        if answer == None:
            await ctx.send("Please enter an answer.")
            return
        redteam = discord.utils.get(ctx.guild.roles, id=903488654364778556)
        blueteam = discord.utils.get(ctx.guild.roles, id=903489166237634570)
        answer = answer.strip()
        if answer in ["wbfrcu", "WBFRCU"]:
            c = self.client.get_channel(903883933635182592)
            await ctx.send("Congratulations for finishing the first trial. Your team has advanced to the next trial.")
            if redteam in ctx.author.roles:
                await ctx.send("Red team has unlocked Trial 2.")
                overwrite = discord.PermissionOverwrite()
                overwrite.view_channel = True
                overwrite.read_messages = True
                overwrite.read_message_history = True
                overwrite.send_messages = False
                await c.set_permissions(blueteam, overwrite=overwrite)
                await ctx.message.delete()
            elif blueteam in ctx.author.roles:
                await ctx.send("Blue team has unlocked Trial 2.")
                overwrite = discord.PermissionOverwrite()
                overwrite.view_channel = True
                overwrite.read_messages = True
                overwrite.read_message_history = True
                overwrite.send_messages = False
                await c.set_permissions(blueteam, overwrite=overwrite)
                await ctx.message.delete()
        elif answer in ["grapevine", "GRAPEVINE"]:
            c = self.client.get_channel(903885767280058398)
            await ctx.send("Congratulations for finishing the second trial. Your team has advanced to the next trial.")
            if redteam in ctx.author.roles:
                await ctx.send("Red team has unlocked Trial 3.")
                overwrite = discord.PermissionOverwrite()
                overwrite.view_channel = True
                overwrite.read_messages = True
                overwrite.read_message_history = True
                overwrite.send_messages = False
                await c.set_permissions(blueteam, overwrite=overwrite)
                await ctx.message.delete()
            elif blueteam in ctx.author.roles:
                await ctx.send("Blue team has unlocked Trial 3.")
                overwrite = discord.PermissionOverwrite()
                overwrite.view_channel = True
                overwrite.read_messages = True
                overwrite.read_message_history = True
                overwrite.send_messages = False
                await c.set_permissions(blueteam, overwrite=overwrite)
                await ctx.message.delete()
        elif answer.lower() in ["gmt+10", "gmt+11", "gmt +10", "gmt +11", "utc+10", "utc+11", "utc +10", "utc +11"]:
            c = self.client.get_channel(904227909005344818)
            await ctx.send("Congratulations for finishing the second trial. Your team has advanced to the next trial.")
            if redteam in ctx.author.roles:
                await ctx.send("Red team has unlocked Trial 3.")
                overwrite = discord.PermissionOverwrite()
                overwrite.view_channel = True
                overwrite.read_messages = True
                overwrite.read_message_history = True
                overwrite.send_messages = False
                await c.set_permissions(blueteam, overwrite=overwrite)
                await ctx.message.delete()
            elif blueteam in ctx.author.roles:
                await ctx.send("Blue team has unlocked Trial 3.")
                overwrite = discord.PermissionOverwrite()
                overwrite.view_channel = True
                overwrite.read_messages = True
                overwrite.read_message_history = True
                overwrite.send_messages = False
                await c.set_permissions(blueteam, overwrite=overwrite)
                await ctx.message.delete()
        else:
            await ctx.send("That is incorrect.")
            return




def setup(client):
    client.add_cog(Events(client))