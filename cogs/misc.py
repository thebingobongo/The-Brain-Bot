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
    async def think(self, ctx):
        await ctx.send("That hurts!")


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
    async def mary(self, ctx):
        embedVar = discord.Embed(title="Marys Room", color=0x00ffff)
        embedVar.add_field(
            value="Imagine a neuroscientist who has only ever seen black and white things, but she is an expert in color vision and knows everything about its physics and biology.\n If, one day, she sees color, does she learn anything new? Is there anything about perceiving color that wasn’t captured in her knowledge?",
            name="** **")
        embedVar.set_footer(text=".ideas for more")
        await ctx.send(embed=embedVar)

    @commands.command()
    async def chineseroom(self, ctx):
        embedVar = discord.Embed(title="The Chinese Room", color=0x00ffff)
        embedVar.add_field(
            value="Imagine a native English speaker who knows no Chinese locked in a room full of boxes of Chinese symbols (a data base) together with a book of instructions for manipulating the symbols (the program). Imagine that people outside the room send in other Chinese symbols which, unknown to the person in the room, are questions in Chinese (the input). And imagine that by following the instructions in the program the man in the room is able to pass out Chinese symbols which are correct answers to the questions (the output).\n\n The program enables the person in the room to pass the Turing Test for understanding Chinese but he does not understand a word of Chinese. ",
            name="** **")
        embedVar.set_footer(text=".ideas for more")
        await ctx.send(embed=embedVar)

    # color=0x00ffff

    @commands.command()
    async def dichotomy(self, ctx):
        embedVar = discord.Embed(title="Zeno's Dichotomy", color=0x00ffff)
        embedVar.add_field(
            name="To go anywhere, you must go halfway first, and then you must go half of the remaining distance, and half of the remaining distance, and so forth to infinity: Thus, motion is impossible.",
            value="** **")
        embedVar.set_footer(text=".ideas for more")
        await ctx.send(embed=embedVar)

    @commands.command()
    async def arrow(self, ctx):
        embedVar = discord.Embed(title="The Fletchers Paradox", color=0x00ffff)
        embedVar.add_field(
            name='In any instant, a moving object is indistinguishable from a nonmoving object: Thus motion is impossible.',
            value="** **")
        embedVar.set_footer(text=".ideas for more")
        await ctx.send(embed=embedVar)

    @commands.command()
    async def ship(self, ctx):
        embed = discord.Embed(title="The ship of Theseus", color=0x00ffff)
        embed.add_field(
            name='If you restored a ship by replacing each of its wooden parts, would it remain the same ship?',
            value="** **")
        embed.set_footer(text=".ideas for more")
        await ctx.send(embed=embed)

    @commands.command()
    async def euthyphro(self, ctx):
        embed = discord.Embed(title="Euthypros Dilemma", color=0x00ffff)
        embed.add_field(
            value="*Socrates*: And what do you say of piety, Euthyphro? Is not piety, according to your definition, loved by all the gods? \n*Euthyphro*: Certainly. \n*Socrates*: Because it is pious or holy, or for some other reason?\n*Euthyphro*: No, that is the reason. \n*Socrates*: It is loved because it is holy, not holy because it is loved?",
            name="** **")
        embed.set_footer(text=".ideas for more")
        await ctx.send(embed=embed)

    @commands.command()
    async def godrock(self, ctx):
        embed = discord.Embed(
            title="The God Rock Paradox",
            color=0x00ffff)
        embed.add_field(name='Can an omnipotent being create a rock too heavy for itself to lift?', value="** **")
        embed.set_footer(text=".ideas for more")
        await ctx.send(embed=embed)

    @commands.command()
    async def bootstrap(self, ctx):
        embed = discord.Embed(
            title="The Boot Strap Paradox", color=0x00ffff)
        embed.add_field(
            value="A physicist working on inventing a time machine is visited by an older version of himself. The older version gives him the plans for a time machine, and the younger version uses those plans to build the time machine, eventually going back in time as the older version of himself.",
            name="** **")
        embed.set_footer(text=".ideas for more")
        await ctx.send(embed=embed)

    @commands.command()
    async def aliens(self, ctx):
        embed = discord.Embed(
            title="The Alien Paradox", color=0x00ffff)
        embed.add_field(
            name="If there's nothing particularly unique about Earth, then there should be lots of alien civilizations in our galaxy. However, we've found no evidence of other intelligent life in the universe.",
            value="** **")
        embed.set_footer(text=".ideas for more")
        await ctx.send(embed=embed)

    @commands.command(aliases=["thoughtexperiments", 'te', 'paradoxes'])
    async def ideas(self, ctx):

        embedVar = discord.Embed(
            title="I can help you with some interesting ideas, thought experiments and paradoxes!\n here are some commands you can try",
            color=0x00ffff)
        embedVar.add_field(name=".euthyphro", value="** **", inline=True)
        embedVar.add_field(name=".mary", value="** **", inline=True)
        embedVar.add_field(name=".chineseroom", value="** **", inline=True)
        embedVar.add_field(name=".dichotomy", value="** **", inline=True)
        embedVar.add_field(name=".arrow", value="** **", inline=True)
        embedVar.add_field(name=".ship", value="** **", inline=True)
        embedVar.add_field(name=".godrock", value="** **", inline=True)
        embedVar.add_field(name=".aliens", value="** **", inline=True)
        embedVar.add_field(name=".bootstrap", value="** **", inline=True)
        await ctx.send(embed=embedVar)

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

    @commands.command(aliases=['thevat', 'info'])
    async def about(self, ctx):
        await ctx.send(
            "Common to many science fiction stories, it outlines a scenario in which a mad scientist, machine, or other entity might remove a person's brain from the body, suspend it in a vat of life-sustaining liquid, and connect its neurons by wires to a supercomputer which would provide it with electrical impulses identical to those the brain normally receives. According to such stories, the computer would then be simulating reality (including appropriate responses to the brain's own output) and the 'disembodied' brain would continue to have perfectly normal conscious experiences, such as those of a person with an embodied brain, without these being related to objects or events in the real world.")

    @commands.command()
    async def help(self, ctx, *, type=None):
        if type == None:
            embedVar = discord.Embed(title="I'm here to help", color=0x00ff00)
            embedVar.add_field(name="Hi, I am The Brain bot and I am here to help you enjoy the server.",
                               value="If you have any complaints or need to speak to mods, send me a dm!\n To learn more about any category, type .help [category name]",
                               inline=False)
            embedVar.add_field(name="Moderation",
                               value="For moderators", inline=False)
            embedVar.add_field(name="Message",
                               value="For the chat bot commands", inline=False)
            embedVar.add_field(name="Utility",
                               value="For the utility commands", inline=False)
            embedVar.add_field(name="Rook",
                               value="For the commands only rook and up can use", inline=False)

        elif type.lower() == "moderation":
            staff_role = discord.utils.get(ctx.guild.roles, id=831214459682029588)
            if staff_role in ctx.author.roles:
                embedVar = discord.Embed(title="Moderation commands:", color=0x00ff00)
                embedVar.add_field(name=".approve [@user]", value="This approves a user in the verification page.")
                embedVar.add_field(name='.underage [@user]', value="This gives the user the underage tag.")
                embedVar.add_field(name=".todo", value="Displays the staff todo list.")
                embedVar.add_field(name=".mute [@user] [time] [reason]",
                                   value="This will mute the user for the specified time, and if time isn't specified, indefinitely.")
                embedVar.add_field(name=".unmute [@user] [reason]", value="This will unmute the user.")
                embedVar.add_field(name=".kick [@user]", value="Will kick the user from the server.")
                embedVar.add_field(name=".panopticon or .prison [@user] [time] [reason]",
                                   value="This will send the user to the panopticon for the specified time, and if time isn't specified, indefinitely.")
                embedVar.add_field(name=".unprison or .unpanopticon [@user]", value="Will free the user.")
                embedVar.add_field(name=".ban [@user]", value="Will ban the user from the server.")
            else:
                embedVar = discord.Embed(title="You dont have access to those commands.", color=0xff0000)

        elif type.lower() == "message" or type.lower() == 'messages':
            embedVar = discord.Embed(title="Message commands:", color=0x00ff00)
            embedVar.add_field(name=".ask [question]", value="I will answer your question.")
            embedVar.add_field(name=".ask2 [question]", value="I will answer your question in a more intellectual way.")
            embedVar.add_field(name=".invite", value="I will send you an invite to The Vat!")
            embedVar.add_field(name=".search [philosopher]",
                               value="I will send a random quote by your chosen philosopher from my database.")
            embedVar.add_field(name=".quote [optional search term]",
                               value="I will send a quote from my database with your search term, otherwise, I'll just send a random quote.")
            embedVar.add_field(name=".ideas",
                               value="I will send a list of ideas and thought experiments for you to choose from ")
            embedVar.add_field(name=".advice", value="I will offer some random advice.")
            embedVar.add_field(name=".joke", value="I will send you a joke!")
            embedVar.add_field(name=".knockknock", value="I will send you a knock knock joke")
            embedVar.add_field(name=".programming", value="I will send you a programming joke.")
            embedVar.add_field(name=".insult", value="I will insult you. Be careful, I can be mean!")
            embedVar.add_field(name=".today", value="I will tell you a random fact about todays date in history.")
            embedVar.add_field(name=".mathfact", value="I will send a math fact for the nerds among you!")

        elif type.lower() == "utillity" or type.lower() == "utility":
            embedVar = discord.Embed(title="Utility commands:", color=0x00ff00)
            embedVar.add_field(name=".sep [article name]", value="I will send a link to the sep article.")
            embedVar.add_field(name=".wiki [article name]", value="I will send a link to the wikipedia article.")
            embedVar.add_field(name=".google [search]", value="I will send a link to the google search.")
            embedVar.add_field(name=".define [word]", value="I will define that word!")
            embedVar.add_field(name=".poll [poll question]", value="I will create a poll for you.")
            embedVar.add_field(name=".hangman", value="I will start a game of hangman")

        elif type.lower() == "rook":
            embedVar = discord.Embed(title="Rook commands:", color=0x00ff00)
            embedVar.add_field(name=".pingvc", value="I will ping all members with the Ping for VC role.", inline=False)
            embedVar.add_field(name=".pinggame", value="I will ping all members with the Ping for Games role.",
                               inline=False)
            embedVar.add_field(name=".pingmovie [optional movie name]",
                               value="I will ping members with the Ping for Movies role.", inline=False)
        else:
            await ctx.send("Invalid category. Try again")
            return
        embedVar.set_footer(
            text="For more info check the Rules and Info channel. \nIf you encouter any issues, DM me or any of the mods!")
        await ctx.send(embed=embedVar)

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