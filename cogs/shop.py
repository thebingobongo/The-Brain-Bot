import asyncio

import discord
from discord.ext import commands
from databaselayer import *
import random
from cogs.moderation import Moderation


class Shop(commands.Cog):

    def __init__(self, client):
        self.client = client

    minute_mute = {'name': '1 Minute Mute', 'cost': 15000, 'effect': "You can mute anyone in the server in a VC for 1 minute."}
    dj_role = {'name': 'DJ Role', 'cost': 20000, 'effect': 'You gain the DJ role for the music bot.'}
    book = {'name': 'Book', 'cost': 5000, 'effect': 'Gives you access to the .study command.'}
    items = {"1 Minute Mute":minute_mute, 'DJ Role':  dj_role, 'Book': book}

    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(title="The Vat's Shop", color=0x00ffff)
        for item in self.items:
            embed.add_field(name=self.items[item]['name'], value=f"Cost = {self.items[item]['cost']} \n {self.items[item]['effect']}")
        embed.set_footer(text="Suggest an item to add to the shop to bingobongo")
        await ctx.send(embed=embed)


    @commands.command(aliases=['inventory'])
    async def inv(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        res= getInventory(member.id)
        embed=discord.Embed(title=f"{member.name}'s Inventory",color=member.color)
        for item in res:
            embed.add_field(name=item[1],value="** **")
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/861788174249754634/863326727018905640/happybrain.png")
        await ctx.send(embed=embed)


    @commands.command(aliases=['read'])
    @commands.cooldown(1,3600,commands.BucketType.user)
    async def study(self,ctx):
        if not hasItem(ctx.author.id, "Book"):
            await ctx.send("You need a book for that command.")
            self.study.reset_cooldown(ctx)
            return
        else:
            bookburn = random.randint(0,9)
            # await ctx.send(bookburn)
            if bookburn in [0,1,2,3]:
                await ctx.send("Your book spontaneously combusted. Get another book if you'd like to keep studying.")
                removeItem(ctx.author.id, "Book")
                return
            elif bookburn in [4, 5]:
                earned = random.randint(7500, 10000)
                sendstring = f"You learned a lot from your book! You got {earned} Brain Cells!"
            elif bookburn in [6, 7, 8, 9]:
                earned = random.randint(2000, 4000)
                sendstring = f"Studying has earned you {earned} Brain Cells!"

            embed = discord.Embed(title=sendstring,
                                  colour=ctx.author.colour)
            addBal(ctx.author.id, earned)
            embed.set_thumbnail(
                url="https://media.discordapp.net/attachments/861788174249754634/863326727018905640/happybrain.png")
            await ctx.send(embed=embed)




    @commands.command()
    async def buy(self,ctx,*, item = None):
        if item == None:
            await ctx.send("Which item would you like to buy?")
            return
        item = item.lower().strip()
        if item in ['book']:
            name = 'Book'
        elif item in ['mute', 'minute mute', '1 minute mute', '1mm']:
            name = '1 Minute Mute'
        elif item in ['dj', 'djrole', 'dj role']:
            name = 'DJ Role'
        else:
            await ctx.send("Item not found.")
            return
        cost = self.items[name]['cost']
        if hasItem(ctx.author.id, name):
            await ctx.send("You already have that item.")
            return
        elif not hasEnough(ctx.author.id, cost):
            await ctx.send("You do not have enough brain cells for that item.")
            return
        else:
            subBal(ctx.author.id, cost)
            addItem(ctx.author.id, name)
            await ctx.send(f"You successfully bought a {name}")



    @commands.command()
    async def use(self, ctx,*, item=None):
        if item == None:
            await ctx.send("What would you like to use?")
            return
        item = item.lower().strip()
        # if item in ['mute', 'minute mute', '1 minute mute', '1mm']:
        #     await ctx.invoke(self.client.get_command('mute'), )
        if item in ['dj', 'djrole', 'dj role']:
            if not hasItem(ctx.author.id, "DJ Role"):
                await ctx.send("You do not have that item.")
                return
            dj_role = discord.utils.get(ctx.guild.roles, id=865858719480807464)
            await ctx.author.add_roles(dj_role, reason="Bought dj role")
            removeItem(ctx.author.id, "DJ Role")
            await ctx.send("The DJ Role has been applied to you.")


        elif item in ['mute', 'minute mute', '1 minute mute', '1mm']:
            if not hasItem(ctx.author.id, "1 Minute Mute"):
                await ctx.send("You do not have that item.")
                return
            # if member == None or not isinstance(member, discord.Member):
            #     await ctx.send("Try .use mute @(whoever)")
            #     return
            await ctx.send("Who do you want to mute?")
            def check(m):
                return m.author == ctx.author and len(m.mentions) == 1 and m.channel == ctx.channel

            try:
                reply = await self.client.wait_for('message', check=check, timeout = 30.0)
            except asyncio.TimeoutError:
                await ctx.send("Timed out, try again.")
                return
            member = reply.mentions[0]

            rook_role = discord.utils.get(ctx.guild.roles, id=831227767671619636)
            bishop_role = discord.utils.get(ctx.guild.roles, id=831213133066534993)
            knight_role = discord.utils.get(ctx.guild.roles, id=831213165105643520)
            pawn_role = discord.utils.get(ctx.guild.roles, id=831213206155952179)
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

            if member == self.client.user:
                await ctx.send("You cannot do that to me, young one.")
                return
            if rook_role in member.roles:
                await member.remove_roles(rook_role, reason='use item')
            elif bishop_role in member.roles:
                await member.remove_roles(bishop_role, reason='use item')
            elif knight_role in member.roles:
                await member.remove_roles(knight_role, reason='use item')
            elif pawn_role in member.roles:
                await member.remove_roles(pawn_role, reason='use item')

            await member.add_roles(muted_role, reason='use item')
            voice_state = member.voice

            if voice_state is not None:
                await member.edit(mute=True)
            await ctx.send(
                "{0.mention} has been muted by {1.mention} with the item.".format(member, ctx.author))
            logs = self.client.get_channel(831214657439924284)
            await logs.send(
                "{0.mention} has been muted by {1.mention} with the item.".format(member, ctx.author))

            try:
                removeItem(ctx.author.id, "1 Minute Mute")
            except:
                await ctx.send("You got really lucky! You can use 1 minute mute again!")
            await asyncio.sleep(60)

            await member.remove_roles(muted_role, reason="time's up ")
            voice_state = member.voice
            if voice_state is not None:
                await member.edit(mute=False)
            roleid = int(getUserRole(member.id))
            memberrole = discord.utils.get(ctx.guild.roles, id=roleid)
            await member.add_roles(memberrole, reason="time's up")

            await ctx.send(f"{member.mention} has been unmuted.")


        else:
            await ctx.send("That item could not be found. Try again.")

            # mute = self.client.get_command("mute")
            # print(mute, type(mute))
            # print('got mute')
            # m = Moderation(self.client)
            # await m.mute(ctx=ctx, members=member,mute_minutes= 1, reason='use item')
            # #await self.client.invoke(mute, members=member,mute_minutes= 1, reason='use item')
            # print('muted')

            # if member.voice is not None:
            #     await member.edit(mute=True)
            #     await ctx.send(f"{member.mention} has been muted for a minute by {ctx.author.mention}")
            #     logs = self.client.get_channel(831214657439924284)
            #     await logs.send(
            #         "{0.mention} has been muted by {1.mention} using the item.".format(member, ctx.author))
            #     await asyncio.sleep(60)
            #     await member.edit(mute=False)
            #     removeItem(ctx.author.id, "1 Minute Mute")
            # else:
            #     await ctx.send("The member isn't connected to a VC.")
                    # await ctx.send("That part is still under construction.")
            # await ctx.invoke(self.client.get_command('mute'), members = member, mute_minutes = 1)
            # await ctx.Moderation.mute(member, 1, 'use item')
            # await Moderation.mute(self.client, ctx, member, 1, 'use item')
            # mute = self.client.get_command('mute')
            # await ctx.invoke(mute,members = member, mute_minutes = 1 )


    # @commands.command()
    # @commands.cooldown(1,42200,commands.BucketType.user)
    # async def steal(self,ctx, member:discord.Member):
    #     stealbal = getUserBal(member.id)
    #     chances = random.randint(0,2)
    #     success = False
    #     if chances == 0:
    #         success = True
    #         newbal = int(stealbal * 0.15)
    #     elif chances == 1:
    #         success = True
    #         newbal = int(stealbal * 0.35)
    #     else:
    #         userbal = getUserBal(ctx.author.id)
    #         newuserbal = int(userbal * 0.80)
    #         subBal(ctx.author.id, newuserbal)
    #         addBal(member.id, newuserbal)
    #         await ctx.send("You got caught, stupid. You lost 20% of your brain cells.")
    #         return
    #     if success == True:
    #         addBal(ctx.author.id, newbal)
    #         subBal(member.id, newbal)
    #         await ctx.send(f"You stole {newbal} Brain Cells from {member.display_name}!")


def setup(client):
    client.add_cog(Shop(client))
