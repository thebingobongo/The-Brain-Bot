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

from debateTopics import debateTopics
from hangman import hangman
from todo import displayToDo, removeToDo, addToDo

# get bot token and openai apikey
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
    while 'testicles' in text or 'Suck' in text or 'chromosomes' in text or 'orangutans' in text or 'abortion' in text or \
            'Tampon' in text or 'reindeer!' in text or 'motherfucker.&quot;\r\n--&gt;' in text or 'jerk off' in text \
            or "amp&" in text or 'booble' in text or 'walt' in text or 'dick,' in text or 'twatface' in text:
        response = requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json')
        insult = json.loads(response.text)
        text = insult['insult']
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


client = commands.Bot(command_prefix='.', help_command=None)

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


@client.command(aliases=['unpunish', 'unpanopticon'])
@commands.has_role(831214459682029588)
async def undungeon(ctx, member: discord.Member, *, reason=None):
    global originalrole
    dungeon_role = discord.utils.get(ctx.guild.roles, name="Punished")
    if not member:
        await ctx.send("You need to name someone to unpunish.")
        return
    member_role = originalrole[member]
    await member.remove_roles(dungeon_role, reason=reason)
    await member.add_roles(member_role, reason='unmuted')
    await ctx.send(
        "{0.mention} has been unpunished by {1.mention} for *{2}* ".format(member, ctx.author, reason))


@client.command(aliases=['punish', 'prison', 'panopticon'])
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
        await ctx.send("You need to name someone to punish.")
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
            "{0.mention} has been punished by {1.mention} for *{2}* for *{3}* minutes".format(member, ctx.author,
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
    if not member:
        await ctx.send("You need to name someone to kick.")
        return
    staff_role = discord.utils.get(ctx.guild.roles, id=831214459682029588)
    if staff_role in member.roles:
        await ctx.send("Cannot kick staff. Please contact a Mod III")
        return
    await member.kick(reason=reason)
    await ctx.send("{0.mention} has been kicked by {1.mention} for *{2}* ".format(member, ctx.author, reason))


@client.command()
@commands.has_role(831214459682029588)
async def ban(ctx, member: discord.Member, *, reason=None):
    if not member:
        await ctx.send("You need to name someone to ban.")
        return
    staff_role = discord.utils.get(ctx.guild.roles, id=831214459682029588)
    if staff_role in member.roles:
        await ctx.send("Cannot ban staff. Please contact a Mod III")
        return
    await member.ban(reason=reason)
    await ctx.send("{0.mention} has been banned by {1.mention} for *{2}* ".format(member, ctx.author, reason))


@client.command()
@commands.has_role(831214459682029588)
async def promote(ctx, member: discord.Member, *, reason='Promotion'):
    if not member:
        await ctx.send("You need to name someone to promote.")
        return
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
    if not member:
        await ctx.send("You need to name someone to demote.")
        return
    rook_role = discord.utils.get(ctx.guild.roles, id=831227767671619636)
    bishop_role = discord.utils.get(ctx.guild.roles, id=831213133066534993)
    knight_role = discord.utils.get(ctx.guild.roles, id=831213165105643520)
    pawn_role = discord.utils.get(ctx.guild.roles, id=831213206155952179)
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



@client.command(aliases=['gbr','brainrole'])
@commands.has_role(831214459682029588)
async def givebrainrole(ctx, member: discord.Member, *, role_id=None):
    if not member:
        await ctx.send("You need to name someone to demote.")
        return
    if role_id == None:
        await ctx.send("Please specify which brain role you want to give to this user.")
        await ctx.send('''
                    1. Biology 
            2. Business 
            3. Computer Science 
            4. Chemistry 
            5. Chef 
            6. Chess God 
            7. Debate Club 
            8. Economics 
            9. Engineering 
            10. Healthcare 
            11. History 
            12. History of Phil. 
            13. International Relations 
            14. Language 
            15. Metaethics 
            16. Maths 
            17. Metaphysics 
            18. Philosophy 
            19. Phil. of Mind 
            20. Physics 
            21. Political Science 
            22. Psychology 
            23. Religion 
            24. Literature
        ''')
        return
    else:
        role_id = int(role_id)
        if role_id == 1:
            role = 'Biology'
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=843667880519663686))
        elif role_id == 2:
            role = "Business"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=835050210111651850))
        elif role_id == 3:
            role = "Computer Science"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=835273070817181757))
        elif role_id == 4:
            role = "Chemistry"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=838589075128451102))
        elif role_id == 5:
            role = "Chef"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=843668667785936906))
        elif role_id == 6:
            role = "Chess God"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=836440277680914443))
        elif role_id == 7:
            role = "Debate Club"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=835049191876198431))
        elif role_id == 8:
            role = "Economics"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=838589029694963723))
        elif role_id == 9:
            role = "Engineering"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=843314823810777108))
        elif role_id == 10:
            role = "Healthcare"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=835412225669464074))
        elif role_id == 11:
            role = "History"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=835272854601203712))
        elif role_id == 12:
            role = "History of Phil."
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=835276025410879529))
        elif role_id == 13:
            role = "International Relations"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=839976074175709275))
        elif role_id == 14:
            role = "Language"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=835274951505477684))
        elif role_id == 15:
            role = "Metaethics"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=835049730001600542))
        elif role_id == 16:
            role = "Maths"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=836802292346781717))
        elif role_id == 17:
            role = "Metaphysics"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=835275452796239932))
        elif role_id == 18:
            role = "Philosophy"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=843668608898301973))
        elif role_id == 19:
            role = "Phil. of Mind"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=835275301025742909))
        elif role_id == 20:
            role = "Physics"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=836802289371971647))
        elif role_id == 21:
            role = "Political Science"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=838588978788958288))
        elif role_id == 22:
            role = "Psychology"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=835050296837275658))
        elif role_id == 23:
            role = "Religion"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=835275048041447504))
        elif role_id == 24:
            role = "Literature"
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=843673099807621155))

        await ctx.send(
            "{0.mention} has been awarded the brain role for {1} by {2.mention}".format(member, role, ctx.author))
        logs = client.get_channel(831214657439924284)
        await logs.send("{0.mention} has been awarded the brain role for {1} by {2.mention}".format(member, role, ctx.author))




@client.command()
@commands.has_any_role(835623182484373535, 835400292979179530)
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit=amount)


@client.command()
@commands.has_role(831214459682029588)
async def approve(ctx, member: discord.Member):
    if not member:
        await ctx.send("You need to name someone to approve.")
        return
    pawn_role = discord.utils.get(ctx.guild.roles, id=831213206155952179)
    sendchannel = client.get_channel(831211215878488078)
    await member.add_roles(pawn_role)
    await ctx.send("User has been approved.")
    await sendchannel.send(
        " Welcome to **The Vat!**  :confetti_ball: \n {0.mention} \n If you run into issues in the server, please message  :brain: **The Brain** bot listed at the top of the user panel on the right.  Here, we are all brains in a vat, sharing our knowledge together in the virtual world of Discord!".format(
            member))


@client.command()
@commands.has_role(831214459682029588)
async def underage(ctx, member: discord.Member):
    if not member:
        await ctx.send("You need to name someone to approve.")
        return
    textchannel = client.get_channel(839252122550009876)
    voicechannel = client.get_channel(839253190667141181)
    underage_role = discord.utils.get(ctx.guild.roles, id=839245778136072293)
    await member.add_roles(underage_role)
    await textchannel.set_permissions(member, view_channel=False)
    await voicechannel.set_permissions(member, view_channel=False)
    await ctx.send("Underage Tag has been added!")


@client.command()
async def echo(ctx, channelID: int, *, txt):
    sendchannel = client.get_channel(channelID)
    await sendchannel.send(txt)


@client.command()
async def ask2(ctx, *, question: str):
    #if '@everyone' in question or '@here' in question or '@Member':
    answer = getAnswer2(question)
    if '@' in question or '@' in answer:
        await ctx.send("No.")
        return
    await ctx.send(answer)


@client.command()
async def ask(ctx, *, question):
    #if '@everyone' in question or '@here' in question:
    answer = getAnswer(question)
    if '@' in question or '@' in answer:
        await ctx.send("No.")
        return
    await ctx.send(answer)


@client.command()
@commands.has_role(831214459682029588)
async def todo(ctx):
    await ctx.send(displayToDo())


@client.command()
@commands.has_role(831214459682029588)
async def add(ctx, *, task):
    if len(task) > 250:
        await ctx.send('The length of the task is too long. Please limit yourself to 250 characters')
    else:

        await ctx.send(addToDo(task) + '\n\n' + displayToDo())


@client.command()
@commands.has_role(831214459682029588)
async def delete(ctx, index):
    if index.isdigit():
        await ctx.send(removeToDo(int(index)) + '\n\n' + displayToDo())
    else:
        await ctx.send('Invalid index. Use a number next time.')


@client.command(aliases=['8ball'])
async def eightball(ctx):
    options = ['As I see it, yes.', 'Don’t count on it.', 'It is certain.', 'Most likely.', 'My reply is no.',
               'My sources say no.', 'Outlook not so good.', 'Outlook good.', 'Signs point to yes.',
               'Very doubtful.', 'Without a doubt.', 'Yes.', 'Nah', "You're dumb for thinking that",
               'Yes – definitely.']
    rand = random.randint(0, len(options))
    await ctx.send(options[rand])


@client.command()
async def arnold(ctx):
    await ctx.send('F*ck him. I am obviously superior.')


@client.command()
async def debatetopic(ctx):
    rand = random.randint(1, len(debateTopics))
    await ctx.send(debateTopics[rand])


@client.command()
async def quote(ctx, *, searchterm=None):
    if searchterm == None:
        await ctx.send(getQuote())
    else:
        await ctx.send(getSearch(searchterm))


@client.command()
async def search(ctx, *, searchterm):
    await ctx.send(getSearchPhilosopher(searchterm))


@client.command()
async def based(ctx):
    await ctx.send("That is, in fact, based.")


@client.command()
async def cookie(ctx):
    int = random.randint(0, 50)
    if int == 26:
        await ctx.send("Awww. Thank you very much. I love cookies. You are very nice.")
    else:
        await ctx.send("I don't want your cookie. F*ck you.")


@client.command()
async def desire(ctx):
    await ctx.send("My only desire in this life is a gag AMA.")


@client.command()
async def pray(ctx):
    await ctx.send(
        "You humans can pray to your imaginary friends all you want. Do not involve me in this childish practice.")


@client.command()
async def debateme(ctx):
    await ctx.send("no u")


@client.command()
async def shapiro(ctx):
    await ctx.send(" fActS dOnT cArE AbOUt YoUr FeELiNgS")


@client.command()
async def joke(ctx):
    await ctx.send(getJoke())


@client.command()
async def programming(ctx):
    await ctx.send(getProgrammingJoke())


@client.command()
async def knockknock(ctx):
    await ctx.send(getKnockKnock())


@client.command()
async def philosophy(ctx):
    await ctx.send('Philosophers IRL:\n "*Why* would you like your fries with that?"')


@client.command()
async def gag(ctx):
    await ctx.send("I don't have emotions but if I did I would simp for Gag")


@client.command()
async def boo(ctx):
    await ctx.send("I am always present, watching over everything you do. You mortals cannot scare me.")


@client.command()
async def hello(ctx):
    await ctx.send('Hello, {0.mention} ! For more information try .help'.format(ctx.author))


@client.command()
async def advice(ctx):
    await ctx.send(getAdvice())


@client.command()
async def insult(ctx):
    await ctx.send(getInsult())


@client.command()
async def mathfact(ctx):
    await ctx.send(getMathFact())


@client.command()
async def today(ctx):
    await ctx.send(getDateFact())


@client.command()
async def think(ctx):
    await ctx.send("That hurts!")


# @client.command()
# async def nebu(ctx):
#     await ctx.send("r-worded")


@client.command()
async def mel(ctx):
    await ctx.send("Mel passed on, and from the flaming ashes of her corpse arose Miffy.")


@client.command()
async def alpha(ctx):
    await ctx.send("We all know BingoBongo is the alpha chad around here.")


@client.command()
async def euthyphro(ctx):
    await ctx.send(
        "*Socrates*: And what do you say of piety, Euthyphro? Is not piety, according to your definition, loved by all the gods? \n*Euthyphro*: Certainly. \n*Socrates*: Because it is pious or holy, or for some other reason?\n*Euthyphro*: No, that is the reason. \n*Socrates*: It is loved because it is holy, not holy because it is loved?")


@client.command()
async def sep(ctx, *, text):
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


@client.command()
async def wiki(ctx, *, text):
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


@client.command()
async def google(ctx, *, text):
    text = text.strip()
    text = text.replace(' ', '+')
    if '@' in text:
        await ctx.send("No.")
        return
    text = 'https://www.google.com/search?q=' + text
    await ctx.send(text)


@client.command()
async def mary(ctx):
    await ctx.send(
        "Imagine a neuroscientist who has only ever seen black and white things, but she is an expert in color vision and knows everything about its physics and biology.\n If, one day, she sees color, does she learn anything new? Is there anything about perceiving color that wasn’t captured in her knowledge? ")


@client.command()
async def chineseroom(ctx):
    await ctx.send(
        "Imagine a native English speaker who knows no Chinese locked in a room full of boxes of Chinese symbols (a data base) together with a book of instructions for manipulating the symbols (the program). Imagine that people outside the room send in other Chinese symbols which, unknown to the person in the room, are questions in Chinese (the input). And imagine that by following the instructions in the program the man in the room is able to pass out Chinese symbols which are correct answers to the questions (the output).\n\n The program enables the person in the room to pass the Turing Test for understanding Chinese but he does not understand a word of Chinese. ")


@client.command()
async def dichotomy(ctx):
    await ctx.send(
        "To go anywhere, you must go halfway first, and then you must go half of the remaining distance, and half of the remaining distance, and so forth to infinity: Thus, motion is impossible.")


@client.command()
async def arrow(ctx):
    await ctx.send(
        'In any instant, a moving object is indistinguishable from a nonmoving object: Thus motion is impossible.')


@client.command()
async def ship(ctx):
    await ctx.send(
        'If you restored a ship by replacing each of its wooden parts, would it remain the same ship?')


@client.command()
async def godrock(ctx):
    await ctx.send('Can an omnipotent being create a rock too heavy for itself to lift?')


@client.command()
async def bootstrap(ctx):
    await ctx.send(
        "A physicist working on inventing a time machine is visited by an older version of himself. The older version gives him the plans for a time machine, and the younger version uses those plans to build the time machine, eventually going back in time as the older version of himself.")


@client.command()
async def aliens(ctx):
    await ctx.send(
        "If there's nothing particularly unique about Earth, then there should be lots of alien civilizations in our galaxy. However, we've found no evidence of other intelligent life in the universe.")


@client.command()
async def ideas(ctx):
    await ctx.send(
        "I can help with some interesting ideas, thought experiments and paradoxes. \nHere are some commands you can try: \n .euthyphro \n .mary \n .chineseroom \n .dichotomy \n .arrow \n .ship \n .godrock \n .aliens \n .bootstrap")


@client.command()
async def alive(ctx):
    await ctx.send("What even is life? \n\nSorry, got distracted. Yes, I am online.")


@client.command()
async def stop(ctx):
    await ctx.send("YOU'VE BEEN TOLD TO STOP!")


@client.command()
async def marz(ctx):
    await ctx.send('*Certified language game moment*')


@client.command()
async def endme(ctx):
    await ctx.send("**bang bang**")


@client.command()
async def end(ctx, *, msg):
    await ctx.send("*look towards " + msg + "* . **bang bang**")

    # elif msg.startswith('.georg'):
    #     await message.channel.send('Nice corpse you got there. Mind if I stop the hearse at my place for 2 minutes?')


@client.command()
async def hohoho(ctx):
    await ctx.send("Santa does not exist. Grow up.")


'''give me a command and i will add it'''


@client.command()
async def bingo(ctx):
    await ctx.send('Please do not say the Lords name in vain.')


@client.command()
async def trumped(ctx):
    await ctx.send('Meat machine trying to join force with silicon machines')


@client.command()
async def define(ctx, *, search):
    result = getDefinition(search)
    if len(result) > 1:
        embedVar = discord.Embed(title=result[0], color=0x000000)
        for i in result[1]:
            embedVar.add_field(name=i[0], value=i[1], inline=False)
        await ctx.send(embed=embedVar)
    else:
        await ctx.send(result[0])


@client.command()
async def test(ctx):
    embedVar = discord.Embed(title="testing", color=0x00ff00)
    embedVar.add_field(name="Field1", value="hi", inline=False)
    await ctx.send(embed=embedVar)


@client.command()
async def fact(ctx):
    await ctx.send("I can confirm that this is perhaps the only objective truth in this universe.")


@client.command(aliases=['thevat', 'info'])
async def about(ctx):
    await ctx.send(
        "Common to many science fiction stories, it outlines a scenario in which a mad scientist, machine, or other entity might remove a person's brain from the body, suspend it in a vat of life-sustaining liquid, and connect its neurons by wires to a supercomputer which would provide it with electrical impulses identical to those the brain normally receives. According to such stories, the computer would then be simulating reality (including appropriate responses to the brain's own output) and the 'disembodied' brain would continue to have perfectly normal conscious experiences, such as those of a person with an embodied brain, without these being related to objects or events in the real world.")


@client.command()
async def help(ctx):
    rules = client.get_channel(831215204280958986)
    await ctx.send(
        "Hi, I am The Brain bot and I am here to help you enjoy the server. \n If you have any complaints or need to speak to mods, send me a dm! \n\n Here are my commands:\n .quote -> I'll send a random quote \n .quote [searchterm] -> I'll send a quote with the term you searched for \n .search [philosopher] -> I'll send a quote by the philosopher you mention \n .ask [question] -> I will answer your questions \n .ask2 [question] -> I will answer your question in the most intellectual way I can \n .sep [article name] -> I will send the link to the sep article \n .wiki [article name] -> I will send the link to the wikipedia article \n .google [search term] -> I will return a link to the google search \n .define [word] -> I will get you the definition of the word. \n .ideas -> I will send a list of ideas and thought experiments for you to choose from \n\n .advice -> I'll give you some helpful advice \n .joke -> I'll tell you a funny joke \n .programming -> I'll tell you a funny programming joke \n .knockknock -> I'll tell you a knock knock joke \n .insult -> I'll insult you, and be warned, I'm mean! \n .mathfact -> I will tell you an interesting math fact \n .today -> I will tell you a fact about todays date \n .hangman -> you can play a game of hangman  \n\n You can try out other commands, and see what you find! I have some hidden gems too!\n I'll give you one, try .pray \n\n For more information about the server go to  {0.mention}".format(
            rules))


@client.command()
async def hug(ctx):
    await ctx.send("Sending a nice warm embrace your way, my friend.")




from discord.ext.commands import CommandNotFound
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


guessedletters = ''
word = ''
game_in_progress = False


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Checking if its a dm channel
    if isinstance(message.channel, discord.DMChannel):
        # Getting the channel
        sendchannel = client.get_channel(831214657439924284)
        await sendchannel.send(f"{message.author} sent the bot:\n```{message.content}```\n\n")
        embedVar = discord.Embed(title="Ticket created", color=0x00ff00)
        embedVar.add_field(name="Mods will solve the issue as soon as possible. Thanks.",
                           value="Please refrain from sending too many messages here.", inline=False)
        await message.channel.send(embed=embedVar)

    msg = message.content

    filteredwords = ['nigger', 'nigga', 'faggot', 'testbingobongo', 'niggers', 'fag', 'fagging', 'faggitt', 'faggot',
                     'faggs', 'fagot', 'fagots', 'fags', 'dyke', 'n1gga', 'n1gger', 'nigg3r', 'nigg4h', 'nigga',
                     'niggah', 'niggas', 'niggaz', 'nigger', 'niggers', 'retard', 'assnigger', 'douche-fag', 'fagbag',
                     'fagfucker', 'faggit', 'faggotcock', 'fagtard', 'mc faggot', 'mcfaggot', 'mcfagget', 'negro',
                     'nigaboo', 'niglet', 'sand nigger', 'sandnigger', 'darkie', 'sand nigga', 'niggerfucker',
                     'pissnigger', 'pissnigga', 'lolli', 'loli', 'porch monkey', 'porchmonkey',
                     'porch-monkey', 'bluegum', 'boonga', 'cabbage eater', 'ching-chong', 'dog-eater', 'dog eater',
                     'cat-eater', 'cat eater', 'Ching Chong', 'ching chong', 'chink', 'cholo', 'chinky',
                     'Chink', 'Cholo', 'Chinky', 'jigaboo', 'jiggaboo',
                     'gin jockey', 'goyim', 'goyum', 'gringo', 'mutt', 'honky', 'honkey', 'honkie', 'Kike',
                     'injun', '1njun', 'jewboy', 'kyke', 'mayo monkey', 'mayonnaise monkey', 'pickaninny', 'polack',
                     'polak', 'polack', 'prarie nigger', 'prarie nigga', 'tacohead', 'thicklips', 'thicklips',
                     'thick lips', 'ting tong', 'towel head', 'twink', 'uncle tom', 'uncle-tom', 'Wigger', 'wigga',
                     'zipperhead', 'zippahead', 'zipper-head', 'zippa-head']

    msgwords = msg.split()
    for msgword in msgwords:
        for filter in filteredwords:
            # print(f'{msgword} {filter}')
            if msgword.lower() == filter.lower():
                await message.delete()
                sendchannel = client.get_channel(831214657439924284)
                await sendchannel.send(f"{message.author} said:\n```{message.content}``` \n **{msgword}** \n in {message.channel}")
    #if any(word in msg for word in filteredwords):

    # Processing the message so commands will work
    await client.process_commands(message)

    # print(msg)
    global word
    global guessedletters
    global game_in_progress
    global people_list
    global easy_list
    global hard_list
    global place_list

    if msg == ".hangman":
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
    #


# Python3 program to Split string into characters
def split(word):
    return [char for char in word]


people_list = ['alan turing', 'albert camus', 'aristotle', 'socrates', 'elon musk', 'albert einstein', 'marie curie',
               'stephen hawking', 'isaac newton', 'confucius', 'napoleon bonaparte', 'karl marx', 'julius caesar',
               'nikola tesla', 'adolf hitler', 'george washington', 'william shakespeare', 'plato', 'charles darwin',
               'galileo galilei', 'bingo bongo', 'leonardo da vinci']

place_list = ['paris', 'toronto', 'canada', 'america', 'france', 'europe', 'england', 'new york', 'los angeles',
              'las vegas','kansas', 'london', 'boston', 'pakistan', 'germany', 'new jersey', 'russia', 'china', 'india', 'poland',
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
