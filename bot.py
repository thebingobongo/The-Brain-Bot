import requests
import discord
from discord.ext import commands
import json
import random
import openai
from dotenv import load_dotenv
import os
from datetime import date
import asyncio
import typing

# get bot token and openai apikey
from debateTopics import debateTopics
from hangman import hangman
from todo import displayToDo, removeToDo, addToDo

load_dotenv()
openai.api_key = os.getenv('APIKEY')
bot_token = os.getenv('TOKEN')


# with open('token.json') as json_file:
#     data = json.load(json_file)
#
# openai.api_key = data['APIKEY']


def getAnswer(question):
    text = "The Brain is a chatbot that reluctantly answers questions.\nYou: How many pounds are in a kilogram?\nThe Brain: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What does HTML stand for?\nThe Brain: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nThe Brain: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nYou:" + str(
        question) + "\nThe Brain:"
    response = openai.Completion.create(
        engine="curie",
        prompt=text,
        temperature=0.6,
        max_tokens=60,
        top_p=0.3,
        frequency_penalty=0.75,
        presence_penalty=0.5,
        stop=["\n"]
    )
    answer = response["choices"][0]["text"]
    return answer


def getAnswer2(question):
    text = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: " + str(
        question) + "\n AI:",

    response = openai.Completion.create(
        engine="curie-instruct-beta",
        prompt=text,
        temperature=0.75,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " Human:", " AI:"]
    )
    answer = response["choices"][0]["text"]
    return answer


def getAnswer3(question):
    text = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: " + str(
        question) + "\n AI:",

    response = openai.Completion.create(
        engine="davinci-instruct-beta",
        prompt=text,
        temperature=0.75,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " Human:", " AI:"]
    )
    answer = response["choices"][0]["text"]
    return answer


def getJoke():
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    joke = json.loads(response.text)
    text = joke['setup'] + " \n " + joke['punchline']
    return text


def getProgrammingJoke():
    response = requests.get('https://official-joke-api.appspot.com/jokes/programming/random')
    joke = json.loads(response.text)
    text = joke[0]['setup'] + " \n " + joke[0]['punchline']
    return text


def getKnockKnock():
    response = requests.get('https://official-joke-api.appspot.com/jokes/knock-knock/random')
    joke = json.loads(response.text)
    text = joke[0]['setup'] + " \n " + joke[0]['punchline']
    return text


def getInsult():
    response = requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json')
    insult = json.loads(response.text)
    text = insult['insult']
    if 'testicles' in text or 'Suck' in text or 'chromosomes' in text or 'orangutans' in text or 'abortion' in text or \
            'Tampon' in text or 'reindeer!' in text or 'motherfucker.&quot;\r\n--&gt;' in text or 'jerk off' in text \
            or "amp&" in text or 'booble' in text or 'walt' in text or 'dick,' in text or 'twatface' in text:
        return 'Something went wrong. You suck. Try again.'
    else:
        return text


def getQuote():
    id = random.randint(1, 583)
    response = requests.get('https://philosophyapi.herokuapp.com/api/ideas/' + str(id))
    json_data = json.loads(response.text)
    # print(json_data)
    quote = '"' + json_data['quote'] + '" \n                           -' + json_data['author']
    # print(quote)
    return quote


def getAdvice():
    response = requests.get('https://api.adviceslip.com/advice')
    advice = json.loads(response.text)
    text = advice['slip']['advice']
    return text


def getSearch(searchterm):
    response = requests.get('http://philosophyapi.herokuapp.com/api/ideas/?search=' + str(searchterm))
    json_data = json.loads(response.text)
    # print(json_data)
    if json_data['count'] != 0:
        quotelist = json_data['results']
        if len(quotelist) == 1:
            quote = '"' + quotelist[0]['quote'] + '" \n                           -' + quotelist[0]['author']
        else:
            rand = random.randint(0, len(quotelist) - 1)
            quote = '"' + quotelist[rand]['quote'] + '" \n                           -' + quotelist[rand]['author']
    else:
        quote = "Couldn't find a quote with that search. Try another search term."
    # print(quote)
    return quote


def getSearchPhilosopher(philosopher):
    response = requests.get('https://philosophyapi.herokuapp.com/api/philosophers/?search=' + str(philosopher))
    json_data = json.loads(response.text)
    if json_data['count'] != 0:
        quotelist = json_data['results'][0]['ideas']
        name = json_data['results'][0]['name']
        rand = random.randint(1, len(quotelist) - 1)
        quote = '"' + quotelist[rand] + '"\n                         -' + name
    else:
        quote = "Search Term not found. Try a different philosopher."

    return quote


def getMathFact():
    response = requests.get('http://numbersapi.com/random/math')
    return response.text


def getDateFact():
    today = date.today()
    day = today.day
    month = today.month
    response = requests.get('http://numbersapi.com/' + str(month) + '/' + str(day) + '/date')
    return response.text


def getDefinition(search):
    response = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en_US/' + str(search))
    text = json.loads(response.text)
    if len(text) == 3:
        return ["Word not found. Try again."]
    else:
        word = text[0]['word']
        def_list = []
        definitions = text[0]['meanings']
        for i in range(len(definitions)):
            type = definitions[i]['partOfSpeech']
            definition = definitions[i]['definitions'][0]['definition']
            def_list.append([type, definition])
        return [word, def_list]


# todolist = []


client = commands.Bot(command_prefix='-')

originalrole = {}


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('with ideas'))
    print("I am alive.")


@client.command()
@commands.has_role(831214459682029588)
async def mute(ctx, members: commands.Greedy[discord.Member],
               mute_minutes: typing.Optional[int] = 0,
               *, reason: str = "None"):
    global originalrole
    """Mass mute members with an optional mute_minutes parameter to time it"""

    rook_role = discord.utils.get(ctx.guild.roles, id=831227767671619636)
    bishop_role = discord.utils.get(ctx.guild.roles, id=831213133066534993)
    knight_role = discord.utils.get(ctx.guild.roles, id=831213165105643520)
    pawn_role = discord.utils.get(ctx.guild.roles, id=831213206155952179)

    member_role = []

    if not members:
        await ctx.send("You need to name someone to mute")
        return

    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

    for member in members:
        if rook_role in member.roles:
            member_role.append(rook_role)
            await member.remove_roles(rook_role, reason=reason)
            originalrole[member] = rook_role
        elif bishop_role in member.roles:
            member_role.append(bishop_role)
            await member.remove_roles(bishop_role, reason=reason)
            originalrole[member] = bishop_role
        elif knight_role in member.roles:
            member_role.append(knight_role)
            await member.remove_roles(knight_role, reason=reason)
            originalrole[member] = knight_role
        elif pawn_role in member.roles:
            member_role.append(pawn_role)
            originalrole[member] = pawn_role
            await member.remove_roles(pawn_role, reason=reason)

        await member.add_roles(muted_role, reason=reason)
        await member.edit(mute=True)
        await ctx.send(
            "{0.mention} has been muted by {1.mention} for *{2}* for *{3}* minutes".format(member, ctx.author, reason,
                                                                                           mute_minutes))

    if mute_minutes > 0:
        await asyncio.sleep(mute_minutes * 60)
        count = 0
        for member in members:
            await member.remove_roles(muted_role, reason="time's up ")
            await member.edit(mute=False)
            await member.add_roles(member_role[count], reason=reason)
            count += 1


@client.command()
@commands.has_role(831214459682029588)
async def unmute(ctx, member: discord.Member, *, reason=None):
    global originalrole
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not member:
        await ctx.send("You need to name someone to unmute.")
        return
    member_role = originalrole[member]
    await member.remove_roles(muted_role, reason=reason)
    await member.add_roles(member_role, reason='unmuted')
    await member.edit(mute=False)
    await ctx.send(
        "{0.mention} has been unmuted by {1.mention} for *{2}* ".format(member, ctx.author, reason))


@client.command()
@commands.has_role(831214459682029588)
async def undungeon(ctx, member: discord.Member, *, reason=None):
    global originalrole
    dungeon_role = discord.utils.get(ctx.guild.roles, name="Punished")
    if not member:
        await ctx.send("You need to name someone to undungeon.")
        return
    member_role = originalrole[member]
    await member.remove_roles(dungeon_role, reason=reason)
    await member.add_roles(member_role, reason='unmuted')
    await ctx.send(
        "{0.mention} has been undungeoned by {1.mention} for *{2}* ".format(member, ctx.author, reason))


@client.command()
@commands.has_role(831214459682029588)
async def dungeon(ctx, members: commands.Greedy[discord.Member],
                  dungeon_minutes: typing.Optional[int] = 0,
                  *, reason: str = "None"):
    global originalrole
    """Mass mute members with an optional mute_minutes parameter to time it"""

    rook_role = discord.utils.get(ctx.guild.roles, id=831227767671619636)
    bishop_role = discord.utils.get(ctx.guild.roles, id=831213133066534993)
    knight_role = discord.utils.get(ctx.guild.roles, id=831213165105643520)
    pawn_role = discord.utils.get(ctx.guild.roles, id=831213206155952179)

    member_role = []

    if not members:
        await ctx.send("You need to name someone to dungeon.")
        return

    dungeon_role = discord.utils.get(ctx.guild.roles, name="Punished")

    for member in members:
        if rook_role in member.roles:
            member_role.append(rook_role)
            await member.remove_roles(rook_role, reason=reason)
            originalrole[member] = rook_role
        elif bishop_role in member.roles:
            member_role.append(bishop_role)
            await member.remove_roles(bishop_role, reason=reason)
            originalrole[member] = bishop_role
        elif knight_role in member.roles:
            member_role.append(knight_role)
            await member.remove_roles(knight_role, reason=reason)
            originalrole[member] = knight_role
        elif pawn_role in member.roles:
            member_role.append(pawn_role)
            originalrole[member] = pawn_role
            await member.remove_roles(pawn_role, reason=reason)
        await member.add_roles(dungeon_role, reason=reason)
        await ctx.send(
            "{0.mention} has been dungeoned by {1.mention} for *{2}* for *{3}* minutes".format(member, ctx.author,
                                                                                               reason, dungeon_minutes))

    if dungeon_minutes > 0:
        await asyncio.sleep(dungeon_minutes * 60)
        count = 0
        for member in members:
            await member.remove_roles(dungeon_role, reason="time's up ")
            await member.add_roles(member_role[count], reason=reason)


@client.command()
@commands.has_role(831214459682029588)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send("{0.mention} has been kicked by {1.mention} for *{2}* ".format(member, ctx.author, reason))


@client.command()
@commands.has_role(831214459682029588)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send("{0.mention} has been banned by {1.mention} for *{2}* ".format(member, ctx.author, reason))


@client.command()
@commands.has_role(831214459682029588)
async def promote(ctx, member: discord.Member, *, reason='Promotion'):
    rook_role = discord.utils.get(ctx.guild.roles, id=831227767671619636)
    bishop_role = discord.utils.get(ctx.guild.roles, id=831213133066534993)
    knight_role = discord.utils.get(ctx.guild.roles, id=831213165105643520)
    pawn_role = discord.utils.get(ctx.guild.roles, id=831213206155952179)
    member_role = discord.utils.get(ctx.guild.roles, id=835286042176127027)
    if rook_role in member.roles:
        await ctx.send("{0.mention} is already a Rook!".format(member))
    elif bishop_role in member.roles:
        await member.remove_roles(bishop_role, reason=reason)
        await member.add_roles(rook_role, reason=reason)
        await ctx.send("{0.mention} has been promoted to Rook!".format(member))
    elif knight_role in member.roles:
        await member.remove_roles(knight_role, reason=reason)
        await member.add_roles(bishop_role, reason=reason)
        await ctx.send("{0.mention} has been promoted to Bishop!".format(member))
    elif member_role in member.roles:
        await member.remove_roles(pawn_role, reason=reason)
        await member.add_roles(knight_role, reason=reason)
        await ctx.send("{0.mention} has been promoted to Knight!".format(member))
    elif pawn_role in member.roles:
        await member.add_roles(member_role, reason=reason)
        await ctx.send("{0.mention} has been promoted to Member!".format(member))
    else:
        await ctx.send("There was an error. Either that member is a Mod, or is not a pawn yet.")


@client.command()
@commands.has_role(831214459682029588)
async def demote(ctx, member: discord.Member, *, reason='Demotion'):
    rook_role = discord.utils.get(ctx.guild.roles, id=831227767671619636)
    bishop_role = discord.utils.get(ctx.guild.roles, id=831213133066534993)
    knight_role = discord.utils.get(ctx.guild.roles, id=831213165105643520)
    pawn_role = discord.utils.get(ctx.guild.roles, id=831213206155952179)
    sendchannel = client.get_channel(831211215878488078)
    if rook_role in member.roles:
        await member.remove_roles(rook_role, reason=reason)
        await member.add_roles(bishop_role, reason=reason)
        await ctx.send("{0.mention} has been demoted to bishop.".format(member))
    elif bishop_role in member.roles:
        await member.remove_roles(bishop_role, reason=reason)
        await member.add_roles(knight_role, reason=reason)
        await ctx.send("{0.mention} has been demoted to a Knight.".format(member))
    elif knight_role in member.roles:
        await member.remove_roles(knight_role, reason=reason)
        await member.add_roles(pawn_role, reason=reason)
        await ctx.send("{0.mention} has been demoted to Pawn.".format(member))
    elif pawn_role in member.roles:
        await ctx.send("{0.mention} is a Pawn. Cannot be further demoted.".format(member))
    else:
        await ctx.send("There was an error. Either that member is a Mod, or is not a pawn yet.")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Checking if its a dm channel
    if isinstance(message.channel, discord.DMChannel):
        # Getting the channel
        sendchannel = client.get_channel(831214657439924284)
        await sendchannel.send(f"{message.author} sent:\n```{message.content}```")
    # Processing the message so commands will work
    await client.process_commands(message)

    msg = message.content
    # print(msg)
    global word
    global guessedletters
    global game_in_progress

    if msg.startswith('.echo'):
        sendchannel = client.get_channel(int(msg[6:24]))
        text = msg[25:]
        await sendchannel.send(text)

    elif '@everyone' in msg or '@here' in msg:
        await message.channel.send("I wont say that.")

    elif msg.startswith(".ask2"):
        question = msg.split('.ask2 ', 1)[1]
        await message.channel.send(getAnswer2(question))

    # elif msg.startswith('.askbigbrain'):
    #     question = msg.split('.askbigbrain ', 1)[1]
    #     await message.channel.send(getAnswer3(question))

    elif msg.startswith(".ask"):
        question = msg.split('.ask ', 1)[1]
        await message.channel.send(getAnswer(question))

    elif msg.startswith('.todo'):
        await message.channel.send(displayToDo())

    elif msg.startswith('.8ball'):
        options = ['As I see it, yes.', 'Don’t count on it.', 'It is certain.', 'Most likely.', 'My reply is no.',
                   'My sources say no.', 'Outlook not so good.', 'Outlook good.', 'Signs point to yes.',
                   'Very doubtful.', 'Without a doubt.', 'Yes.', 'Nah', "You're dumb for thinking that",
                   'Yes – definitely.']
        rand = random.randint(0, len(options))
        await message.channel.send(options[rand])

    elif msg.startswith('.add'):
        task = msg[5:]
        if len(task) > 250:
            await message.channel.send('The length of the task is too long. Please limit yourself to 250 characters')
        else:

            await message.channel.send(addToDo(task) + '\n\n' + displayToDo())

    elif msg.startswith('.delete'):
        index = msg[8:]
        index = index.strip()
        if index.isdigit():
            await message.channel.send(removeToDo(int(index)) + '\n\n' + displayToDo())
        else:
            await message.channel.send('Invalid index. Use a number next time.')

    elif msg.startswith('.arnold'):
        await message.channel.send('F*ck him. I am obviously superior.')

    elif msg.startswith('.debatetopic'):
        rand = random.randint(1, len(debateTopics))
        await message.channel.send(debateTopics[rand])

    elif msg == '.quote':
        await message.channel.send(getQuote())
        # print(1)
    elif msg.startswith('.quote'):
        searchterm = msg.split('.quote ', 1)[1]
        # print(searchterm)
        await message.channel.send(getSearch(searchterm))
        # print(2)

    elif msg.startswith('.search'):
        searchterm = msg.split('.search ', 1)[1]
        await message.channel.send(getSearchPhilosopher(searchterm))


    elif msg.startswith('.based'):
        await message.channel.send("That is, in fact, based.")

    elif msg.startswith('.cookie'):
        await message.channel.send("I don't want your cookie. F*ck you.")

    elif msg.startswith('.desire'):
        await message.channel.send("My only desire in this life is a gag AMA.")

    elif msg.startswith(".pray"):
        await message.channel.send(
            "You humans can pray to your imaginary friends all you want. Do not involve me in this childish practice.")

    elif msg.startswith(".debateme"):
        await message.channel.send("no u")

    elif msg.startswith('.shapiro'):
        await message.channel.send(" fActS dOnT cArE AbOUt YoUr FeELiNgS")

    elif msg.startswith('.joke'):
        await message.channel.send(getJoke())

    elif msg.startswith('.programming'):
        await message.channel.send(getProgrammingJoke())

    elif msg.startswith(".knockknock"):
        await message.channel.send(getKnockKnock())

    elif msg.startswith('.philosophy'):
        await message.channel.send('Philosophers IRL:\n "Why would you like your fries with that?"')

    elif msg.startswith('.gag'):
        await message.channel.send("I don't have emotions but if I did I would simp for Gag")

    elif msg == '.boo':
        await message.channel.send(
            "I am always present, watching over everything you do. You mortals cannot scare me.")

    elif msg.startswith('.hello'):
        send = 'Hello, {0.author.mention} ! For more information try .help'.format(message)
        await message.channel.send(send)

    elif msg.startswith('.advice'):
        await message.channel.send(getAdvice())

    elif msg.startswith('.insult'):
        await message.channel.send(getInsult())

    elif msg.startswith('.mathfact'):
        await message.channel.send(getMathFact())

    elif msg.startswith('.today'):
        await message.channel.send(getDateFact())

    elif msg.startswith(".think"):
        await message.channel.send("That hurts!")

    elif msg.startswith(".nebu"):
        await message.channel.send("r-worded")

    elif msg.startswith(".mel"):
        await message.channel.send("Mel passed on, and from the flaming ashes of her corpse arose Miffy.")

    elif msg.startswith(".alpha"):
        await message.channel.send("We all know BingoBongo is the alpha chad around here.")

    elif msg.startswith(".euthyphro"):
        await message.channel.send(
            "*Socrates*: And what do you say of piety, Euthyphro? Is not piety, according to your definition, loved by all the gods? \n*Euthyphro*: Certainly. \n*Socrates*: Because it is pious or holy, or for some other reason?\n*Euthyphro*: No, that is the reason. \n*Socrates*: It is loved because it is holy, not holy because it is loved?")

    elif msg.startswith(".sep"):
        text = msg[5:]
        text = text.strip()
        text = text.replace(" ", "-")
        text = "https://plato.stanford.edu/entries/" + text
        await message.channel.send(text)

    elif msg.startswith('.wiki'):
        text = msg[6:]
        text = text.strip()
        text = text.replace(" ", "_")
        text = 'https://en.wikipedia.org/wiki/' + text
        await message.channel.send(text)

    elif msg.startswith('.google'):
        text = msg[8:]
        text = text.strip()
        text = text.replace(' ', '+')
        text = 'https://www.google.com/search?q=' + text
        await message.channel.send(text)

    elif msg.startswith(".mary"):
        await message.channel.send(
            "Imagine a neuroscientist who has only ever seen black and white things, but she is an expert in color vision and knows everything about its physics and biology.\n If, one day, she sees color, does she learn anything new? Is there anything about perceiving color that wasn’t captured in her knowledge? ")

    elif msg.startswith('.chineseroom'):
        await message.channel.send(
            "Imagine a native English speaker who knows no Chinese locked in a room full of boxes of Chinese symbols (a data base) together with a book of instructions for manipulating the symbols (the program). Imagine that people outside the room send in other Chinese symbols which, unknown to the person in the room, are questions in Chinese (the input). And imagine that by following the instructions in the program the man in the room is able to pass out Chinese symbols which are correct answers to the questions (the output).\n\n The program enables the person in the room to pass the Turing Test for understanding Chinese but he does not understand a word of Chinese. ")

    elif msg.startswith('.dichotomy'):
        await message.channel.send(
            "To go anywhere, you must go halfway first, and then you must go half of the remaining distance, and half of the remaining distance, and so forth to infinity: Thus, motion is impossible.")

    elif msg.startswith('.arrow'):
        await message.channel.send(
            'In any instant, a moving object is indistinguishable from a nonmoving object: Thus motion is impossible.')

    elif msg.startswith('.ship'):
        await message.channel.send(
            'If you restored a ship by replacing each of its wooden parts, would it remain the same ship?')

    elif msg.startswith('.godrock'):
        await message.channel.send('Can an omnipotent being create a rock too heavy for itself to lift?')

    elif msg.startswith('.bootstrap'):
        await message.channel.send(
            "A physicist working on inventing a time machine is visited by an older version of himself. The older version gives him the plans for a time machine, and the younger version uses those plans to build the time machine, eventually going back in time as the older version of himself.")

    elif msg.startswith('.aliens'):
        await message.channel.send(
            "If there's nothing particularly unique about Earth, then there should be lots of alien civilizations in our galaxy. However, we've found no evidence of other intelligent life in the universe.")

    elif msg.startswith('.ideas'):
        await message.channel.send(
            "I can help with some interesting ideas, thought experiments and paradoxes. \nHere are some commands you can try: \n .euthyphro \n .mary \n .chineseroom \n .dichotomy \n .arrow \n .ship \n .godrock \n .aliens \n .bootstrap")

    elif msg.startswith('.alive'):
        await message.channel.send("What even is life? \n\nSorry, got distracted. Yes, I am online.")

    elif msg.startswith(".hassan"):
        await message.channel.send("Usse miss kara, chutiya chekha hai. Tu joint bana.")

    # elif msg.startswith('.cyrie'):
    #     await message.channel.send("Cyrie did not want a special message so there is none. Ignore this message.")

    elif msg.startswith('.stop'):
        await message.channel.send("YOU'VE BEEN TOLD TO STOP!")


    elif msg.startswith(".marz"):
        await message.channel.send('*Certified language game moment*')

    elif msg.startswith('.endme'):
        await message.channel.send("**bang bang**")

    elif msg.startswith(".end "):
        await message.channel.send("*look towards " + msg[5:] + "* . **bang bang**")

    # elif msg.startswith('.georg'):
    #     await message.channel.send('Nice corpse you got there. Mind if I stop the hearse at my place for 2 minutes?')

    elif msg.startswith('.hohoho'):
        await message.channel.send("Santa does not exist. Grow up.")

    elif msg.startswith('.bingo'):
        await message.channel.send('Please do not say the Lords name in vain.')

    elif msg.startswith('.trumped'):
        await message.channel.send('Meat machine trying to join force with silicon machines')


    elif msg.startswith('.define'):
        search = msg[8:]
        result = getDefinition(search)
        if len(result) > 1:
            embedVar = discord.Embed(title=result[0], color=0x000000)
            for i in result[1]:
                embedVar.add_field(name=i[0], value=i[1], inline=False)
            await message.channel.send(embed=embedVar)
        else:
            await message.channel.send(result[0])
    elif msg.startswith('.test'):
        embedVar = discord.Embed(title="testing",  color=0x00ff00)
        embedVar.add_field(name="Field1", value="hi", inline=False)
        await message.channel.send(embed=embedVar)

    elif msg.startswith('.fact'):
        await message.channel.send("I can confirm that this is perhaps the only objective truth in this universe.")

    elif msg.startswith('.about') or msg.startswith('.thevat'):
        await message.channel.send(
            "Common to many science fiction stories, it outlines a scenario in which a mad scientist, machine, or other entity might remove a person's brain from the body, suspend it in a vat of life-sustaining liquid, and connect its neurons by wires to a supercomputer which would provide it with electrical impulses identical to those the brain normally receives. According to such stories, the computer would then be simulating reality (including appropriate responses to the brain's own output) and the 'disembodied' brain would continue to have perfectly normal conscious experiences, such as those of a person with an embodied brain, without these being related to objects or events in the real world.")

    elif msg.startswith(".help"):
        rules = client.get_channel(831215204280958986)
        await message.channel.send(
            "Hi, I am The Brain bot and I am here to help you enjoy the server. \n If you have any complaints or need to speak to mods, send me a dm! \n\n Here are my commands:\n .quote -> I'll send a random quote \n .quote [searchterm] -> I'll send a quote with the term you searched for \n .search [philosopher] -> I'll send a quote by the philosopher you mention \n .ask [question] -> I will answer your questions \n .ask2 [question] -> I will answer your question in the most intellectual way I can \n .sep [article name] -> I will send the link to the sep article \n .wiki [article name] -> I will send the link to the wikipedia article \n .google [search term] -> I will return a link to the google search \n .define [word] -> I will get you the definition of the word. \n .ideas -> I will send a list of ideas and thought experiments for you to choose from \n\n .advice -> I'll give you some helpful advice \n .joke -> I'll tell you a funny joke \n .programming -> I'll tell you a funny programming joke \n .knockknock -> I'll tell you a knock knock joke \n .insult -> I'll insult you, and be warned, I'm mean! \n .mathfact -> I will tell you an interesting math fact \n .today -> I will tell you a fact about todays date \n .hangman -> you can play a game of hangman  \n\n You can try out other commands, and see what you find! I have some hidden gems too!\n I'll give you one, try .pray \n\n For more information about the server go to  {0.mention}".format(
                rules))

    elif msg.startswith(".hug"):
        await message.channel.send("Sending a nice warm embrace your way, my friend.")

    elif msg == ".hangman":
        await message.channel.send(
            "Choose which word list / topic you want to play: \n .hangman person \n .hangman places \n .hangman easy \n .hangman hard")

    elif msg.startswith('.hangman person'):
        if game_in_progress:
            await message.channel.send("A game is in progress. Try .guess")
        else:
            game_in_progress = True
            rand = random.randint(0, len(people_list))
            word = people_list[rand]
            guessedletters = ''
            (hangmanResult, game_in_progress) = hangman(word, guessedletters, game_in_progress)
            await message.channel.send(hangmanResult)
            await message.channel.send("Use .guess to play.")

    elif msg.startswith('.hangman places'):
        if game_in_progress:
            await message.channel.send("A game is in progress. Try .guess")
        else:
            game_in_progress = True
            rand = random.randint(0, len(place_list))
            word = place_list[rand]
            guessedletters = ''
            (hangmanResult, game_in_progress) = hangman(word, guessedletters, game_in_progress)
            await message.channel.send(hangmanResult)
            await message.channel.send("Use .guess to play.")

    elif msg.startswith('.hangman easy'):
        if game_in_progress:
            await message.channel.send("A game is in progress. Try .guess")
        else:
            game_in_progress = True
            rand = random.randint(0, len(easy_list))
            word = easy_list[rand]
            guessedletters = ''
            (hangmanResult, game_in_progress) = hangman(word, guessedletters, game_in_progress)
            await message.channel.send(hangmanResult)
            await message.channel.send("Use .guess to play.")

    elif msg.startswith('.hangman hard'):
        if game_in_progress:
            await message.channel.send("A game is in progress. Try .guess")
        else:
            game_in_progress = True
            rand = random.randint(0, len(hard_list))
            word = hard_list[rand]
            guessedletters = ''
            (hangmanResult, game_in_progress) = hangman(word, guessedletters, game_in_progress)
            await message.channel.send(hangmanResult)
            await message.channel.send("Use .guess to play.")

    elif msg.startswith('.guess'):
        guess = msg[7:]
        guess = guess.strip()
        guess = guess.lower()
        if guess == word:
            (hangmanResult, game_in_progress) = hangman(word, word, game_in_progress)
            await message.channel.send(hangmanResult)
        elif len(guess) > 1:
            await message.channel.send("Only one letter per guess")
        elif guess in guessedletters:
            await message.channel.send("This letter has already been guessed.")
        else:
            guessedletters = guessedletters + guess
            (hangmanResult, game_in_progress) = hangman(word, guessedletters, game_in_progress)
            returntext = hangmanResult
            if 'WIN' in returntext or "LOSE" in returntext:
                guessedletters = ''
                word = ''
            await message.channel.send(returntext)


# Python3 program to Split string into characters
def split(word):
    return [char for char in word]


guessedletters = ''
word = ''
game_in_progress = False

people_list = ['alan turing', 'albert camus', 'aristotle', 'socrates', 'elon musk', 'albert einstein', 'marie curie',
               'stephen hawking', 'isaac newton', 'confucius', 'napoleon bonaparte', 'karl marx', 'julius caesar',
               'nikola tesla', 'adolf hitler', 'george washington', 'william shakespeare', 'plato', 'charles darwin',
               'galileo galilei', 'bingo bongo', 'leonardo da vinci']

place_list = ['paris', 'toronto', 'canada', 'america', 'france', 'europe', 'england', 'new york', 'los angeles',
              'las vegas'
              'kansas', 'london', 'boston', 'pakistan', 'germany', 'new jersey', 'russia', 'china', 'india', 'poland',
              'mexico', 'ottawa', 'berlin', 'alaska', 'serbia', 'japan', 'africa', 'australia', 'asia']

easy_list = ['wolf', 'deer', 'dangerous', ' fire station', 'surgeon', 'building', 'astrophysics', 'phiilosophy',
             'telekinetic',
             'genuine', 'nuclear', 'animal', 'greenhouse', 'firetruck', 'finger', 'palace', 'military', 'commercial',
             'chemistry',
             'mathematics', 'rhino', 'jazz', 'music', 'dancing', 'alexa', 'siri']

hard_list = ['anomaly', 'equivocal', 'precipitate', 'assuage', 'erudite', 'opaque', 'prodigal', 'enigma', 'fervid',
             'placate',
             'desiccate', 'audacious', 'gullible', 'laudable', 'adulterate', 'jazz music', 'capricious', 'homogenous',
             'loquacious', 'misanthrope', 'corroborate', 'paradox', 'philanthropic', 'epistemology', 'replicate',
             'jupiter',
             'alpha centauri']

# data['TOKEN']
client.run(bot_token)
