import discord
from discord.ext import commands
from databaselayer import *
from cogs.library import Library

class ApprovalButton(discord.ui.View):
    @discord.ui.button(label="✅", style=discord.ButtonStyle.green)
    async def checkmark(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        self.stop()
        embed = interaction.message.embeds[0]
        embed.title = f"APPROVED by {interaction.user}"
        embed.color = 0x00ff00
        await interaction.message.edit(embed=embed)
        return

    @discord.ui.button(label="❌", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        self.stop()
        embed = interaction.message.embeds[0]
        embed.title = f"DECLINED by {interaction.user}"
        embed.color = 0xff0000
        await interaction.message.edit(embed=embed)
        return

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="confess")
    async def confess(self, ctx, *, message):
        try:
            await ctx.message.delete()
        except:
            pass
        confession_channel = self.client.get_channel(917916158940823563)
        embed = discord.Embed(title="Confession", description=message, color=0xc93eb0)
        lb = Library(self.client)
        if await lb.get_approval("Confession", ctx.author, message):
            await confession_channel.send(embed=embed)


def setup(client):
    client.add_cog(Events(client))