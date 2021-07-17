import discord
from discord.ext import commands
from databaselayer import *
import random


class Shop(commands.Cog):

    def __init__(self, client):
        self.client = client

    minute_mute = {'name': '1 Minute Mute', 'cost': 10000, 'effect': "You can mute anyone in the server for 1 minute."}
    dj_role = {'name': 'DJ Role', 'cost': 10000, 'effect': 'You gain the DJ role for the music bot.'}
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
    async def inv(self, ctx):
        res= getInventory(ctx.author.id)
        embed=discord.Embed(title=f"{ctx.author.name}'s Inventory",color=ctx.author.color)
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
            return
        else:
            bookburn = random.randint(0,9)
            await ctx.send(bookburn)
            if bookburn in [0,1,2,3]:
                await ctx.send("Your book spontaneously combusted. Get another book if you'd like to keep studying.")
                removeItem(ctx.author.id, "Book")
                return
            elif bookburn in [4, 5]:
                earned = random.randint(7500, 10000)
                sendstring = f"You learned a lot from your book! You got {earned} Brain Cells!"
            elif bookburn in [6, 7,8,9]:
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
            await ctx.send("That part is still under construction.")





def setup(client):
    client.add_cog(Shop(client))
