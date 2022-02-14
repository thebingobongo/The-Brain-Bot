import asyncio

import discord
from discord.ext import commands
from databaselayer import *
import random
from cogs.moderation import Moderation


class Shop(commands.Cog):

    def __init__(self, client):
        self.client = client

    minute_mute = {'name': '1 Minute Mute', 'cost': 17500, 'effect': "You can mute anyone in the server in a VC for 1 minute."}
    dj_role = {'name': 'DJ Role', 'cost': 25000, 'effect': 'You gain the DJ role for the music bot.'}
    book = {'name': 'Book', 'cost': 6000, 'effect': 'Gives you access to the .study command.'}
    items = {'DJ Role':  dj_role, 'Book': book, "1 Minute Mute":minute_mute}

    @commands.command()
    async def shop(self, ctx):
        if ctx.channel.id == 831211215878488078:
            await ctx.send("Use <#835370412161630270> you stupid fuck")
            return
        embed = discord.Embed(title="The Vat's Shop", color=0x00ffff)
        for item in self.items:
            embed.add_field(name=self.items[item]['name'], value=f"Cost = {self.items[item]['cost']} \n {self.items[item]['effect']}")
        embed.set_footer(text="Suggest an item to add to the shop to bingobongo")
        await ctx.send(embed=embed)

    @commands.command(aliases=['inventory'])
    async def inv(self, ctx, member:discord.Member=None):
        if ctx.channel.id == 831211215878488078:
            await ctx.send("Use <#835370412161630270> you stupid fuck")
            return
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
        if ctx.channel.id == 831211215878488078:
            await ctx.send("Use <#835370412161630270> you stupid fuck")
            return
        if not hasItem(ctx.author.id, "Book"):
            await ctx.send("You need a book for that command.")
            self.study.reset_cooldown(ctx)
            return
        else:
            bookburn = random.randint(0,9)
            # await ctx.send(bookburn)
            if bookburn in [0,1,2]:
                await ctx.send("Your book spontaneously combusted. Get another book if you'd like to keep studying.")
                removeItem(ctx.author.id, "Book")
                return
            elif bookburn in [4, 5]:
                earned = random.randint(7500, 10000)
                sendstring = f"You learned a lot from your book! You got {earned} Brain Cells!"
            elif bookburn in [3, 6, 7, 8, 9]:
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
        if ctx.channel.id == 831211215878488078:
            await ctx.send("Use <#835370412161630270> you stupid fuck")
            return
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
    @commands.cooldown(1,7200,commands.BucketType.user)
    async def use(self, ctx,*, item=None):
        if item == None:
            await ctx.send("What would you like to use?")
            self.use.reset_cooldown(ctx)
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
            self.use.reset_cooldown(ctx)


        elif item in ['mute', 'minute mute', '1 minute mute', '1mm']:
            if not hasItem(ctx.author.id, "1 Minute Mute"):
                await ctx.send("You do not have that item.")
                self.use.reset_cooldown(ctx)
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
                self.use.reset_cooldown(ctx)
                return
            member = reply.mentions[0]
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

            if muted_role in member.roles:
                await ctx.send("That member has already been muted.")
                return

            member_role = discord.utils.get(ctx.guild.roles, id=835286042176127027)

            if member == self.client.user:
                await ctx.send("You cannot do that to me, young one.")
                self.use.reset_cooldown(ctx)
                return

            await member.remove_roles(member_role, reason='use item')

            await member.add_roles(muted_role, reason='use item')
            voice_state = member.voice

            if voice_state is not None:
                await member.edit(mute=True)
            await ctx.send(
                "{0.mention} has been muted by {1.mention} with the item.".format(member, ctx.author))
            logs = self.client.get_channel(934867511273476177)
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
            await member.add_roles(member_role, reason="time's up")

            await ctx.send(f"{member.mention} has been unmuted.")


        else:
            await ctx.send("That item could not be found. Try again.")
            self.use.reset_cooldown(ctx)



def setup(client):
    client.add_cog(Shop(client))
