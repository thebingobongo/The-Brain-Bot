import discord
from discord.ext import commands
import random

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def arnold(self, ctx):
        await ctx.send('F*ck him. I am obviously superior.')


    @commands.command()
    async def based(self, ctx):
        await ctx.send("That is, in fact, based.")


    @commands.command()
    async def cookie(self, ctx):
        int = random.randint(0, 50)
        if int == 26:
            await ctx.send("Awww. Thank you very much. I love cookies. You are very nice.")
        else:
            await ctx.send("I don't want your cookie. F*ck you.")


    @commands.command()
    async def desire(self, ctx):
        await ctx.send("My only desire in this life is a gag AMA.")


    @commands.command()
    async def pray(self, ctx):
        await ctx.send(
            "You humans can pray to your imaginary friends all you want. Do not involve me in this childish practice.")


    @commands.command()
    async def vibing(self, ctx):
        await ctx.send("<a:vibing:847619864738267217><a:vibing:847619864738267217><a:vibing:847619864738267217><a:vibing:847619864738267217>")


    @commands.command()
    async def debateme(self, ctx):
        await ctx.send("no u")


    @commands.command()
    async def shapiro(self, ctx):
        await ctx.send(" fActS dOnT cArE AbOUt YoUr FeELiNgS")


    @commands.command()
    async def philosophy(self, ctx):
        await ctx.send('Philosophers IRL:\n "*Why* would you like your fries with that?"')


    @commands.command()
    async def gag(self, ctx):
        await ctx.send("I don't have emotions but if I did I would simp for Gag")


    @commands.command()
    async def boo(self, ctx):
        await ctx.send("I am always present, watching over everything you do. You mortals cannot scare me.")


    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello, {0.mention} ! For more information try .help'.format(ctx.author))



    @commands.command()
    async def mel(self, ctx):
        await ctx.send("Mel passed on, and from the flaming ashes of her corpse arose Miffy.")


    @commands.command()
    async def alpha(self,ctx):
        await ctx.send("We all know BingoBongo is the alpha around here.")

    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx):
        options = ['As I see it, yes.', 'Don’t count on it.', 'It is certain.', 'Most likely.', 'My reply is no.',
                   'My sources say no.', 'Outlook not so good.', 'Outlook good.', 'Signs point to yes.',
                   'Very doubtful.', 'Without a doubt.', 'Yes.', 'Nah', "You're dumb for thinking that",
                   'Yes – definitely.']
        rand = random.randint(0, len(options))
        await ctx.send(options[rand])


    @commands.command()
    async def alive(self, ctx):
        await ctx.send("What even is life? \n\nSorry, got distracted. Yes, I am online.")

    @commands.command()
    async def stop(self, ctx):
        await ctx.send("YOU'VE BEEN TOLD TO STOP!")

    @commands.command()
    async def marz(self, ctx):
        await ctx.send('*Certified language game moment*')

    @commands.command()
    async def endme(self, ctx):
        await ctx.send("**bang bang**")

    @commands.command()
    async def end(self, ctx, *, msg):
        await ctx.send("*look towards " + msg + "* . **bang bang**")

        # elif msg.startswith('.georg'):
        #     await message.channel.send('Nice corpse you got there. Mind if I stop the hearse at my place for 2 minutes?')

    @commands.command()
    async def georg(self, ctx):
        await ctx.send("The milf magnet.")

    @commands.command()
    async def hohoho(self, ctx):
        await ctx.send("Santa does not exist. Grow up.")


    @commands.command()
    async def bingo(self, ctx):
        await ctx.send('Please do not say the Lords name in vain.')

    @commands.command()
    async def trumped(self, ctx):
        await ctx.send('Meat machine trying to join force with silicon machines')

    @commands.command()
    async def test(self, ctx):
        embedVar = discord.Embed(title="testing", color=0x00ff00)
        embedVar.add_field(name="Field1", value="hi", inline=False)
        await ctx.send(embed=embedVar)

    @commands.command()
    async def fact(self, ctx):
        await ctx.send("I can confirm that this is perhaps the only objective truth in this universe.")



        # rules = client.get_channel(831215204280958986)
        # await ctx.send(
        #     "Hi, I am The Brain bot and I am here to help you enjoy the server. \n If you have any complaints or need to speak to mods, send me a dm! \n\n Here are my commands:\n .quote -> I'll send a random quote \n .quote [searchterm] -> I'll send a quote with the term you searched for \n .search [philosopher] -> I'll send a quote by the philosopher you mention \n .ask [question] -> I will answer your questions \n .ask2 [question] -> I will answer your question in the most intellectual way I can \n .sep [article name] -> I will send the link to the sep article \n .wiki [article name] -> I will send the link to the wikipedia article \n .google [search term] -> I will return a link to the google search \n .define [word] -> I will get you the definition of the word. \n .ideas -> I will send a list of ideas and thought experiments for you to choose from \n\n .advice -> I'll give you some helpful advice \n .joke -> I'll tell you a funny joke \n .programming -> I'll tell you a funny programming joke \n .knockknock -> I'll tell you a knock knock joke \n .insult -> I'll insult you, and be warned, I'm mean! \n .mathfact -> I will tell you an interesting math fact \n .today -> I will tell you a fact about todays date \n .hangman -> you can play a game of hangman  \n\n You can try out other commands, and see what you find! I have some hidden gems too!\n I'll give you one, try .pray \n\n For more information about the server go to  {0.mention}".format(
        #         rules))

    @commands.command()
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_uses=5, reason=f"{ctx.author} wanted an invite.")
        await ctx.send("Here is an instant invite to The Vat:\n\n " + str(link))

    @commands.command()
    async def hug(self, ctx):
        await ctx.send("Sending a nice warm embrace your way, my friend.")

    @commands.command()
    async def kill(self, ctx):
        await ctx.send("***bang bang***")



def setup(client):
    client.add_cog(Misc(client))