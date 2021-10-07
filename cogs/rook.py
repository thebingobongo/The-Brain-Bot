import discord
from discord.ext import commands


def predicate(ctx):
    rook_role = discord.utils.get(ctx.guild.roles, id=831227767671619636)
    staff_role = discord.utils.get(ctx.guild.roles, id=831214459682029588)
    monarch_role = discord.utils.get(ctx.guild.roles, id=886454608774459403)
    return rook_role in ctx.author.roles or staff_role in ctx.author.roles or monarch_role in ctx.author.roles
    # test = discord.utils.get(ctx.guild.roles, id=858614845363322881)
    # return test in ctx.author.roles


has_roles = commands.check(predicate)


class Rook(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['gameping', 'pg', 'pinggames', 'pingames', 'pingame'])
    @has_roles
    async def pinggame(self, ctx, *, game=None):
        if game is None:
            await ctx.send(
                f"Hey <@&843707687643643924>, {ctx.author.mention} invites you all to come play a game with him!")
        else:
            await ctx.send(
                f"Hey <@&843707687643643924>, {ctx.author.mention} invites you to come play {game} with them!")

    @commands.command(aliases=['vcping', 'pingvoice', 'pingvoicechat', 'voiceping', 'voicechatping'])
    @has_roles
    async def pingvc(self, ctx, *, topic=None):
        if topic is None:
            await ctx.send(
                f"Hey <@&843707891265306624>, {ctx.author.mention} thinks there is an interesting discussion that you would like to hear!")
        else:
            await ctx.send(
                f"Hey <@&843707891265306624>, {ctx.author.mention} is talking about {topic}, and thought you would like to join!")

    @commands.command(aliases=['movieping', 'pingM', 'pingmovie', 'moviesvoice'])
    @has_roles
    async def pingmovies(self, ctx, *, movie=None):
        if movie is None:
            await ctx.send(
                f"Hey <@&846967076634624010>, {ctx.author.mention} invites you to come watch a movie with them!")
        else:
            await ctx.send(
                f"Hey <@&846967076634624010>, {ctx.author.mention} invites you to come watch {movie} with them!")


def setup(client):
    client.add_cog(Rook(client))
