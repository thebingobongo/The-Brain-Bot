import asyncpg
import discord
from discord.ext import commands, tasks
from cogs.messages import getDateFact, getQuote, getAdvice
from databaselayer import *


class Taskloops(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.data = []
        self.vccheck.add_exception_type(asyncpg.PostgresConnectionError)
        self.vccheck.start()
        self.waterreminder.add_exception_type(asyncpg.PostgresConnectionError)
        self.waterreminder.start()

    def cog_unload(self):
        self.vccheck.cancel()
        self.waterreminder.cancel()

    @tasks.loop(minutes=1)
    async def vccheck(self):
        await self.client.wait_until_ready()
        vat = self.client.get_guild(831211215375433728)
        vc_channels = vat.voice_channels
        for channel in vc_channels:
            if channel.id == 835061032073297920:
                continue
            for member in channel.members:
                ammount = 20
                if member.voice.self_deaf:
                    ammount = 5
                addBal(member.id, ammount)

    @tasks.loop(minutes=120)
    async def waterreminder(self):
        # thevat = self.client.get_guild(id=831211215375433728)
        # thevat = discord.utils.get(self.client.guilds, id=831211215375433728)
        await self.client.wait_until_ready()
        general = self.client.get_channel(831211215878488078)
        embed = getDateFact()
        embed.add_field(name="This is your reminder to go drink some water!", value="** **")
        embed.set_footer(
            text="For more info check the Rules and Info channel. \nIf you encounter any issues, DM me or any of the mods!")
        await general.send(embed=embed)


def setup(client):
    client.add_cog(Taskloops(client))