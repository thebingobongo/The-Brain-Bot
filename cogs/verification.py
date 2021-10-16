import discord
from discord.ext import commands
import asyncio
from databaselayer import createUser, updateUserRole

class Verification(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def verify(self, ctx):

        aboveage_role = discord.utils.get(ctx.guild.roles,  id=897665019913842768)
        underage_role = discord.utils.get(ctx.guild.roles, id=839245778136072293)

        if aboveage_role not in ctx.author.roles and underage_role not in ctx.author.roles:
            m = await ctx.send("Please react to the age message.")
            await ctx.message.delete()
            await asyncio.sleep(30)
            await m.delete()
            return

        member_role = discord.utils.get(ctx.guild.roles, id=835286042176127027)
        sendchannel = self.client.get_channel(831211215878488078)
        try:
            createUser(ctx.author.id)
        except:
            updateUserRole(ctx.author.id, 831213206155952179)
        await ctx.author.add_roles(member_role)
        await ctx.message.delete()
        await sendchannel.send(
            " Welcome to **The Vat!**  :confetti_ball: \n {0.mention} \n If you run into issues in the server, please message  :brain: **The Brain** bot listed at the top of the user panel on the right. Make sure to grab some roles from <#831215253076574219>! Here, we are all brains in a vat, sharing our knowledge together in the virtual world of Discord!".format(
                ctx.author))



def setup(client):
    client.add_cog(Verification(client))