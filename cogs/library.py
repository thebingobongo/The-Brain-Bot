
import discord
from discord.ext import commands
from databaselayer import hasEnough


class ApprovalButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
     
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


class Library(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def get_approval(self, type, author, text):
        def check(m):
            print(m.component, m.components)

        approval_channel = self.client.get_channel(908283306599145475)
        view = ApprovalButton()
        embed = discord.Embed(title=f"APPROVAL REQUEST", colour=0x03fce3)
        embed.add_field(name=type, value=text)
        embed.set_footer(text=f"Sent by {author}")
        msg = await approval_channel.send(embed=embed, view=view)
        await view.wait()
        await msg.edit(view=None)
        return view.value

async def check_input(channel, amount):
    try:
        amount = int(amount)
    except:
        await channel.send("There was an error, try again.")
        return False
    if amount <= 0:
        await channel.send("Can't do negative numbers.")
        return False
    elif amount < 50:
        await channel.send("Need to bet at least 50 Brain Cells.")
        return False
    elif not hasEnough(channel.author.id, amount):
        await channel.send("You do not have enough Brain Cells.")
        return False
    return True


def setup(client):
    client.add_cog(Library(client))
