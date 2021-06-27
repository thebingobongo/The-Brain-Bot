import discord
from discord.ext import commands,tasks
import random
from cogs.messages import getDateFact, getQuote, getAdvice
from debateTopics import debateTopics
import asyncio

class Taskloops(commands.Cog):

    def __init__(self, client):
        self.client = client

    @tasks.loop(minutes=60)
    async def waterreminder(self):
        await self.client.wait_until_ready()
        general = self.client.get_channel(831211215878488078)
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

    @tasks.loop(minutes=60)
    async def debatetopicloop(self):
        await self.client.wait_until_ready()
        general = self.client.get_channel(831211215878488078)
        rand = random.randint(1, len(debateTopics))
        while len(debateTopics[rand]) > 250:
            rand = random.randint(1, len(debateTopics))

        embed = discord.Embed(title=debateTopics[rand], color=0xc203fc)
        embed.add_field(name="It's .debatetopic for more!", value="** **")

        embed.set_footer(
            text="For more info check the Rules and Info channel. \nIf you encouter any issues, DM me or any of the mods!")
        await general.send(embed=embed)

    @tasks.loop(minutes=3)
    async def keepalive(self):
        await self.client.wait_until_ready()
        channel = self.client.get_channel(856065317524733954)
        await channel.send("keeping shit alive ")

    @commands.Cog.listener()
    async def on_ready(self):
        self.keepalive.start()
        self.waterreminder.start()
        await asyncio.sleep(1800)
        self.debatetopicloop.start()
#

def setup(client):
    client.add_cog(Taskloops(client))