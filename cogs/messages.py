import discord
from discord.ext import commands
import json
import requests
import random
import asyncio
from debateTopics import debateTopics
from databaselayer import addBal, getUserRole
from cogs.library import *
from timezones import *







class Messages(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['timezone','times','clock','time'])
    async def timezones(self, ctx):
        await ctx.send(embed=getTimeZones(ctx))

    @commands.command()
    async def joke(self, ctx):
        await ctx.send(embed=getJoke())

    @commands.command()
    async def programming(self, ctx):
        await ctx.send(embed=getProgrammingJoke())

    @commands.command()
    async def knockknock(self, ctx):
        await ctx.send(embed=getKnockKnock())

    @commands.command()
    async def zodiac(self, ctx, sign):
        if sign.lower() not in ["aries", 'capricorn', 'sagittarius', 'aquarius', 'taurus', 'virgo', 'libra', 'gemini',
                                'scorpio', 'pisces', 'leo', 'cancer']:
            await ctx.send("That is not a valid Zodiac sign.")
            return
        await ctx.send(embed=getZodiac(ctx, sign))

    @commands.command()
    async def debatetopic(self,ctx):
        rand = random.randint(1, len(debateTopics))
        # await ctx.send(debateTopics[rand])
        while len(debateTopics[rand]) > 256:
            rand = random.randint(1, len(debateTopics))

        embed = discord.Embed(title=debateTopics[rand], color=0xc203fc)
        embed.add_field(name="It's .debatetopic for more!", value="** **")
        embed.set_footer(
            text="For more info check the Rules and Info channel. \nIf you encouter any issues, DM me or any of the mods!")
        await ctx.send(embed=embed)

    @commands.command()
    async def quote(self, ctx, *, searchterm = None):
        if searchterm == None:
            await ctx.send(embed=getQuote())
        else:
            await ctx.send(embed=getSearch(searchterm))

    @commands.command()
    async def search(self,ctx, *, searchterm):
        await ctx.send(embed=getSearchPhilosopher(searchterm))

    @commands.command()
    async def ask2(self,ctx, *, question: str):
        # if '@everyone' in question or '@here' in question or '@Member':
        answer = getAnswer2(question)
        if '@' in question or '@' in answer:
            await ctx.send("No.")
            return
        await ctx.send(answer)

    @commands.command()
    async def ask(self,ctx, *, question):
        # if '@everyone' in question or '@here' in question:
        answer = getAnswer(question)
        if '@' in question or '@' in answer:
            await ctx.send("No.")
            return
        await ctx.send(answer)

    @commands.command(aliases=['pl'])
    async def poll(self, ctx, *, msg):
        if '@' in msg:
            await ctx.send("No.")
            return
        await ctx.message.delete()
        title = ctx.author.display_name + " asks: " + msg
        if len(title) >= 255:
            await ctx.send("Please use a shorter prompt for your poll.")
            return
        embed = discord.Embed(title=title, color=ctx.author.color)
        message = await ctx.send(embed=embed)
        await message.add_reaction("<:upvote:837763222513778759>")
        await message.add_reaction("<:downvote:837763222886547486>")

    @commands.command()
    async def makepoll(self, ctx, options: int, messagelink):
        if options > 9:
            await ctx.send("Can only add up to 9 options. Try again with less.")
            return
        try:
            messagelink = messagelink.strip()
            if len(messagelink) == 18:
                try:
                    message = await ctx.fetch_message(int(messagelink))
                except:
                    await ctx.send("Either the message ID is invalid, or you are not in the channel of the message.")
                    return
            else:
                links = messagelink.split('/')
                messageid = int(links[-1])
                channelid = int(links[-2])
                guildid = int(links[-3])

                server = self.client.get_guild(guildid)
                channel = server.get_channel(channelid)
                message = await channel.fetch_message(messageid)
        except:
            await ctx.send("Invalid message link, try again.")
            return

        reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

        for i in range(options):
            await message.add_reaction(reactions[i])
        await ctx.message.delete()


    @commands.command(aliases=['remind','remindme'])
    async def reminder(self,ctx,time=None,unit=None,*,reminder=None):
        if time == None or unit == None or reminder == None or unit.lower() not in ['minute','second','minutes', 'seconds','hours','hour','day','days','sec','min','secs','mins','hr','hrs'] or time.isdigit() == False:
            await ctx.send("The way to use this command is with .reminder [time with unit like 1 second or 2 minutes] [what you want to be reminded of]")
            return
        if unit in ['days', 'day']:
            await ctx.send("Days are not currently supported. Please ping bingobongo if you really want it")
            return
        await ctx.send("Reminder has been set.")
        time = int(time)
        if unit in ['seconds','second','sec','secs']:
            await asyncio.sleep(time)
        elif unit in ['minute','minute','min','mins']:
            time = time * 60
            await asyncio.sleep(time)
        elif unit in ['hour','hours','hr','hrs']:
            time = time * 60 * 60
            await asyncio.sleep(time)
        await ctx.send(f"Hello {ctx.author.mention}, reminding you to {reminder}.")


    @commands.command()
    async def advice(self,ctx):
        await ctx.send(embed=getAdvice())

    @commands.command()
    async def insult(self,ctx):
        await ctx.send(embed=getInsult())

    @commands.command()
    async def mathfact(self,ctx):
        await ctx.send(embed=getMathFact())

    @commands.command()
    async def today(self,ctx):
        await ctx.send(embed=getDateFact())

    @commands.command()
    async def define(self,ctx, *, search):
        result = getDefinition(search)
        if len(result) > 1:
            embedVar = discord.Embed(title=result[0], color=0x000000)
            for i in result[1]:
                embedVar.add_field(name=i[0], value=i[1], inline=False)
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(result[0])


    @commands.command(aliases=['urban','urbandict','urbandefine','udefine'])
    async def urbandictionary(self,ctx,*,word):
        embed = getUrbanDefinition(word)
        if embed == None:
            await ctx.send("Word not found.")
        elif type(embed) == str:
            await ctx.send(embed)
        else:
            await ctx.send(embed=embed)

    @commands.command()
    async def sep(self,ctx, *, text):
        text = text.strip()
        text = text.replace(" ", "-")
        if '@' in text:
            await ctx.send("No.")
            return
        link = 'https://plato.stanford.edu/entries/' + text
        response = requests.get(link)
        if response.status_code == 404:
            link = " https://plato.stanford.edu/search/searcher.py?query=" + text
        await ctx.send(link)

    @commands.command()
    async def wiki(self,ctx, *, text):
        text = text.strip()
        text = text.replace(" ", "_")
        if '@' in text:
            await ctx.send("No.")
            return
        link = 'https://en.wikipedia.org/wiki/' + text
        response = requests.get(link)
        if response.status_code == 404:
            link = 'https://en.wikipedia.org/w/index.php?search=' + text
        await ctx.send(link)

    @commands.command()
    async def google(self,ctx, *, text):
        text = text.strip()
        text = text.replace(' ', '+')
        if '@' in text:
            await ctx.send("No.")
            return
        text = 'https://www.google.com/search?q=' + text
        await ctx.send(text)

    @commands.command()
    async def ob(self, ctx, *, emotename=None):
        if not emotename == None:
            emotename = emotename.strip()
            observer = self.client.get_guild(737104128777650217)
            if emotename == "list":
                c = 0
                returnt = ''
                line = ''
                for emote in observer.emojis:
                    line = line + " " + emote.name
                    c += 1
                    if c == 3:
                        returnt = returnt + "`" + line + "` \n"
                        line = ''
                        c = 0
                await ctx.send(returnt)
            else:
                for emote in observer.emojis:
                    if emotename == emote.name[3:].lower():
                        await ctx.message.delete()
                        await ctx.send(str(emote))
                        break
        else:
            await ctx.send("Try .ob [emote name] or .ob [list]")





def setup(client):
    client.add_cog(Messages(client))