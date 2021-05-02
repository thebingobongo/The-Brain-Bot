import requests
import discord
from discord.ext import commands
import json
import random
import openai
from dotenv import load_dotenv
import os
from datetime import date
import pickle
import asyncio
import typing

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
    if 'testicles' in text or 'Suck' in text or 'chromosomes' in text or 'orangutans' in text or 'abortion' in text or\
            'Tampon' in text or 'reindeer!' in text or 'motherfucker.&quot;\r\n--&gt;' in text or 'jerk off' in text\
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
with open('todo.pkl', 'rb') as f:
    todolist = pickle.load(f)


def displayToDo():
    global todolist
    with open('todo.pkl', 'rb') as f:
        todolist = pickle.load(f)
    returntext = '**To Do list:**\n'
    for i in range(len(todolist)):
        returntext = returntext + (str(i + 1) + '. ' + todolist[i] + '\n')

    returntext = returntext + '\n To remove a task: .delete [task number] \n To add a new task: .add [task]'
    return returntext


def removeToDo(index):
    if index > len(todolist):
        return 'Index does not exist, try again.'
    else:
        todolist.pop(index - 1)
        with open('todo.pkl', 'wb') as f:
            pickle.dump(todolist, f)
        return ' Task at index ' + str(index) + ' has been successfully removed.'


def addToDo(task):
    todolist.append(task)
    with open('todo.pkl', 'wb') as f:
        pickle.dump(todolist, f)
    return "Task has been successfully added!"


client = commands.Bot(command_prefix='-')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('with ideas'))
    print("I am alive.")


@client.command()
@commands.has_role(831214459682029588)
async def mute(ctx, members: commands.Greedy[discord.Member],
                   mute_minutes: typing.Optional[int] = 0,
                   *, reason: str = "None"):
    """Mass mute members with an optional mute_minutes parameter to time it"""


    if not members:
        await ctx.send("You need to name someone to mute")
        return

    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

    for member in members:
        await member.add_roles(muted_role, reason = reason)
        await ctx.send("{0.mention} has been muted by {1.mention} for *{2}* for *{3}* minutes".format(member, ctx.author, reason, mute_minutes))

    if mute_minutes > 0:
        await asyncio.sleep(mute_minutes * 60)
        for member in members:
            await member.remove_roles(muted_role, reason = "time's up ")


@client.command()
@commands.has_role(831214459682029588)
async def unmute(ctx, member: discord.Member, *, reason=None):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not member:
        await ctx.send("You need to name someone to unmute.")
        return
    await member.remove_roles(muted_role, reason=reason)
    await ctx.send(
        "{0.mention} has been unmuted by {1.mention} for *{2}* ".format(member, ctx.author, reason))


@client.command()
@commands.has_role(831214459682029588)
async def undungeon(ctx, member: discord.Member, *, reason=None):
    dungeon_role = discord.utils.get(ctx.guild.roles, name="Punished")
    if not member:
        await ctx.send("You need to name someone to undungeon.")
        return
    await member.remove_roles(dungeon_role, reason=reason)
    await ctx.send(
        "{0.mention} has been undungeoned by {1.mention} for *{2}* ".format(member, ctx.author, reason))


@client.command()
@commands.has_role(831214459682029588)
async def dungeon(ctx, members: commands.Greedy[discord.Member],
                   dungeon_minutes: typing.Optional[int] = 0,
                   *, reason: str = "None"):
    """Mass mute members with an optional mute_minutes parameter to time it"""


    if not members:
        await ctx.send("You need to name someone to dungeon.")
        return

    dungeon_role = discord.utils.get(ctx.guild.roles, name="Punished")

    for member in members:
        await member.add_roles(dungeon_role, reason = reason)
        await ctx.send("{0.mention} has been dungeoned by {1.mention} for *{2}* for *{3}* minutes".format(member, ctx.author, reason, dungeon_minutes))

    if dungeon_minutes > 0:
        await asyncio.sleep(dungeon_minutes * 60)
        for member in members:
            await member.remove_roles(dungeon_role, reason = "time's up ")


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
    global debateTopics

    if msg.startswith(".ask2"):
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
        options = ['As I see it, yes.', 'Don’t count on it.','It is certain.','Most likely.','My reply is no.','My sources say no.','Outlook not so good.','Outlook good.','Signs point to yes.','Very doubtful.','Without a doubt.','Yes.', 'Nah', "You're dumb for thinking that",'Yes – definitely.']
        rand = random.randint(0,len(options))
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
            await message.channel.send(removeToDo(int(index))+ '\n\n' + displayToDo())
        else:
            await message.channel.send('Invalid index. Use a number next time.')

    elif msg.startswith('.arnold'):
        await message.channel.send('F*ck him. I am obviously superior.')

    elif msg.startswith('.debatetopic'):
        rand = random.randint(1,len(debateTopics))
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

    elif msg.startswith('.echo'):
        sendchannel = client.get_channel(int(msg[6:24]))
        text = msg[25:]
        await sendchannel.send(text)

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
        await message.channel.send("*bang bang*")

    elif msg.startswith(".end "):
        await message.channel.send("*look towards " + msg[5:] + "* . *bang bang*")

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
        if len(result)> 1:
            embedVar = discord.Embed(title=result[0],color=0x000000)
            for i in result[1]:
                embedVar.add_field(name=i[0], value=i[1], inline=False)
            await message.channel.send(embed=embedVar)
        else:
            await message.channel.send(result[0])
    # elif msg.startswith('.test'):
    #     embedVar = discord.Embed(title="Title",  color=0x00ff00)
    #     embedVar.add_field(name="Field1", value="hi", inline=False)
    #     await message.channel.send(embed=embedVar)

    elif msg.startswith('.fact'):
        await message.channel.send("I can confirm that this is perhaps the only objective truth in this universe.")

    elif msg.startswith('.about'):
        await message.channel.send("Common to many science fiction stories, it outlines a scenario in which a mad scientist, machine, or other entity might remove a person's brain from the body, suspend it in a vat of life-sustaining liquid, and connect its neurons by wires to a supercomputer which would provide it with electrical impulses identical to those the brain normally receives. According to such stories, the computer would then be simulating reality (including appropriate responses to the brain's own output) and the 'disembodied' brain would continue to have perfectly normal conscious experiences, such as those of a person with an embodied brain, without these being related to objects or events in the real world.")

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
            await message.channel.send(hangman(word, guessedletters))

    elif msg.startswith('.hangman places'):
        if game_in_progress:
            await message.channel.send("A game is in progress. Try .guess")
        else:
            game_in_progress = True
            rand = random.randint(0, len(place_list))
            word = place_list[rand]
            guessedletters = ''
            await message.channel.send(hangman(word, guessedletters))

    elif msg.startswith('.hangman easy'):
        if game_in_progress:
            await message.channel.send("A game is in progress. Try .guess")
        else:
            game_in_progress = True
            rand = random.randint(0, len(easy_list))
            word = easy_list[rand]
            guessedletters = ''
            await message.channel.send(hangman(word, guessedletters))

    elif msg.startswith('.hangman hard'):
        if game_in_progress:
            await message.channel.send("A game is in progress. Try .guess")
        else:
            game_in_progress = True
            rand = random.randint(0, len(hard_list))
            word = hard_list[rand]
            guessedletters = ''
            await message.channel.send(hangman(word, guessedletters))

    elif msg.startswith('.guess'):
        guess = msg[7:]
        guess = guess.strip()
        guess = guess.lower()
        if guess == word:
            await message.channel.send(hangman(word, guess))
        elif len(guess) > 1:
            await message.channel.send("Only one letter per guess")
        elif guess in guessedletters:
            await message.channel.send("This letter has already been guessed.")
        else:
            guessedletters = guessedletters + guess
            returntext = hangman(word, guessedletters)
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
             'loquacious', 'misanthrope', 'corroborate', 'paradox', 'philanthropic', 'epistemology', 'replicate', 'jupiter',
             'alpha centauri']


def hangman(word, guessedletters):
    global game_in_progress
    hangmanpics = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']
    printletter = []
    for i in range(len(word)):
        if word[i] != " ":
            printletter.append(' - ')
        else:
            printletter.append("  ")
    if guessedletters == '':
        text = ''
        # text = ''.join(printletter)
        for i in printletter:
            text = text + i
        return (hangmanpics[0] + '\n' + text)
    wordlist = split(word)
    guesslist = split(guessedletters)
    matchcount = 0
    matchfound = False
    foundcount = 0
    for i in guesslist:
        for j in range(len(word)):
            if i == word[j]:
                printletter[j] = i
                matchcount += 1
                matchfound = True
        if matchfound == True:
            foundcount += 1
        matchfound = False

    text = ''.join(printletter)
    errors = len(guesslist) - foundcount

    if errors == 6:
        game_in_progress = False
        return (hangmanpics[errors] + "\n" + ' It was ' + word + '\n' + text + "\n\n YOU LOSE!")
    elif not ' - ' in printletter:
        game_in_progress = False
        return (hangmanpics[errors] + "\n" + text + "\n\n YOU WIN!!!")
    else:
        return (hangmanpics[errors] + "\n" + guessedletters + '\n' + text)


debateTopics = {
    1 : 'Should abortion be legal?',
    2: 'All people should have the right to own guns.',
    3:'Human cloning should be legalized.',
    4: 'Does life require a purpose and a goal?',
    5: 'Do acts of kindness have a motive?',
    6: 'Is having a big ego a negative trait of positive trait?',
    7: 'Are humans obligated to better themselves and will that make them happier?',
    8: 'Have we become less happy in this age of technology?',
    9: 'Is love simply physical desire or something more?',
    10: 'Does evil come from within, and if so why?',
    11: 'Can achieving nothing make a person happy?',
    12: 'If everyone spoke their mind would this world be a better place?',
    13: 'Is there a perfect life?',
    14: 'Does money truly buy happiness?',
    15: 'Are highly intelligent people less happy than individuals with average intelligence?',
    16: 'Do knowledge and understanding make you content and happy as a person?',
    17: 'Does an ideal government exist?',
    18: 'Are there limitations on free speech?',
    19: 'Does free will exist, or is every action predetermined?',
    20: 'What is human consciousness?',
    21: 'Do atheists make their own gods?',
    22: 'Can artificial intelligence be creative?',
    23: 'Can religious beliefs affect scientific thinking?',
    24: 'Will a world without reliance on modern technology make any progress?',
    25: 'Does belief make God exist?',
    26: 'Will robots take over the world in the future?',
    27: 'Are beliefs and superstitions the same?',
    28: 'How does one find purpose in life?',
    29: 'Will racism cease to exist?',
    30: 'Will the world be a better place if caste and religion cease to exist?',
    31: 'Is humanity doomed to head in a destructive direction?',
    32: 'Should full access to the internet be a fundamental right?',
    33: 'Is true beauty subjective or objective?',
    34: 'What is the extent of freedom human beings should have?',
    35: 'Will technological advances wipe out humanity?',
    36: 'Does understanding philosophy lead to progress?',
    37: 'Will concepts and theories in regard to religion becoming obsolete come true?',
    38: 'If death is inevitable, why bother doing anything?',
    39: 'Is there such a thing as a good death?',
    40: 'How do you properly say goodbye to someone that has died?',
    41: 'How can you convince a non-believer that God exists?',
    42: 'All drugs should be legalized.',
    43: 'All people should have Universal Basic Income.',
    44: 'Every citizen should be mandated to perform national public service.',
    45: 'Standardized testing in education should be abolished.',
    46: 'Sexual education should be mandatory in schools.',
    47: 'Healthcare should be universal.',
    48: 'All people should be vegetarians.',
    49: 'Euthanasia should be legal.',
    50: 'Smoking should be banned in all public places.',
    51: 'Obesity should be labeled a disease.',
    52: 'The sale of human organs should be legalized.',
    53: 'Social media has improved human communication.',
    54: 'The development of artificial intelligence will help humanity.',
    55: 'The universal basic income should be everyone’s right.',
    56: 'Death penalty has no place in the modern world.',
    57: 'Animals should enjoy the same rights as humans.',
    58: ' Where is the line between art and not art?',
    59: 'What should be the goal of humanity?',
    60: 'What does it mean to live a good life?',
    61: 'Is it possible to live a normal life and not ever tell a lie?',
    62: 'Is the meaning of life the same for animals and humans? ',
    63: 'If someone you loved was killed in front of you, but someone created a copy of them that was perfect right down to the atomic level, would they be the same person and would you love them just as much?',
    64: 'If you could become immortal on the condition you would NEVER be able to die or kill yourself, would you choose immortality?',
    65: 'If a child somehow survived and grew up in the wilderness without any human contact, how “human” would they be without the influence of society and culture?',
    66: 'How would humanity change if all humans’ life expectancy was significantly increased (let’s say to around 500 years)?',
    67: 'What do you think would be humanity’s reaction to the discovery of extraterrestrial life?',
    68: 'Will religion ever become obsolete?',
    69: 'If you could teach everyone in the world one concept, what concept would have the biggest positive impact on humanity?',
    70: 'Is suffering a necessary part of the human condition? What would people who never suffered be like?',
    71: 'What benefits does art provide society? Does art hurt society in any way?',
    72: 'How likely do you think it will be that humans will last another 1,000 years without killing ourselves off?',
    73: 'If freedom is simply being able to do what you want, are animals freer than humans?',
    74: 'Would you want to know you are going to die before hand or die suddenly without warning?',
    75: 'Does the study of philosophy ever lead to answers or simply more questions?',
    76: 'Is it better for a person to have a broad knowledge base or a deep knowledge base?',
    77: 'Is it more important to help yourself, help your family, help your society, or help the world?',
    78: 'What life-altering things should every human ideally get to experience at least once in their lives?',
    79: 'Is it better to be a big fish in a small pond or a small fish in a big pond?',
    80: 'Some people believe that if life has no purpose, then there is no reason for living. While others think that if life has no purpose, that frees a person to find/create and follow their own personal purpose. Which is a more valid point of view or are they both equally valid?',
    81: 'Does knowledge have intrinsic value or does it need to have a practical use to have value?',
    82: 'Where do you think is the most worthwhile place to find meaning in life? Work, family, hobby, religion, philosophy, helping others, all the small miracles, or something else entirely?',
    83: 'Is a life that focuses on avoiding pain and seeking out pleasure a good and worthwhile life? Why or why not?',
    84: 'Is math something that humans created or something we discovered? Is looking at reality mathematically an accurate representation of how things work?',
    85: 'Is it possible for a human to fathom the true depths of reality and existence?',
    86: 'What is the best path to find truth; science, math, art, philosophy, or something else?',
    87: 'As more and more is being discovered about quantum physics, we become less and less able to comprehend the nature of reality. Is this something temporary and our minds will adapt and begin to understand this new reality or is it possible that the human mind will soon reach its limits of comprehension? If it’s only temporary, is there is a limit to what the human mind can comprehend? If we are reaching our limits, how do we continue to study our reality?',
    88: 'Is there inherent order in nature or is it all chaos and chance?',
    89: 'What in life is truly objective and not subjective?',
    90: 'Is happiness just chemicals flowing through your brain or something more?',
    91: 'If every neuron in a human was accurately simulated in a computer, would it result in human consciousness?',
    92: 'Is it possible that some animals are self-aware and think about their ability to think?',
    93: 'How do you define consciousness?',
    94: 'Is it possible to prove that other people besides yourself have consciousness?',
    95: 'How conscious do you think animals are?',
    96: 'Assuming evolution is correct, do you think that if humans went extinct another species as intelligent as humans would evolve? If life exists long enough on a planet, is intelligence and consciousness inevitable?',
    97: 'Would it be more frightening to discover that humans are the most advanced species in the universe or that we are far from being the most advanced species in the universe?',
    98: 'Why do humans have such a strong urge to distract ourselves from the real world?',
    99: 'Is the concept of “you” continuous or does past “you” continually fade into present and future “you”? In other words, what part of “you” sticks around over time considering that the atoms that make up your body are constantly being replaced and your memories are always changing?',
    100: ' Is it possible that someone’s genes might affect their political leanings? If no, why not? If so, what would be the ramifications?',
    101: 'Would selectively breeding an animal such as a dog based on intelligence, increase its intelligence over time? If so, how intelligent could dogs become? If not, how does intelligence emerge in a species?',
    102: 'If there existed a perfect clone of you, would it also be you? Would it act in exactly the same manner as you (like a mirror) or would it act differently? If it acted differently then would it still be you? At what point would it not be you?',
    103: ' Are intelligence and happiness tied together in any way? If you are highly intelligent, is it more likely that you’ll be more, or less happy?',
    104: 'When, if ever, is taking a human life justified?',
    105: 'Without religion would people become more, less, or be equally morally corrupt?',
    106: 'If humanity was put on trial by an advanced race of aliens, how would you defend humanity and argue for its continued existence?',
    107: 'What rights does every human have? Do those rights change based on age?',
    108: 'Do animals have rights and do those rights extend to all animals or do the rights change based on the complexity of the animal?',
    109: 'Is justice a human construct or is it independent of humans?',
    110: 'Why do people expect a universe full of randomness to be fair?',
    111: 'With no laws or rules to influence your behavior, how do you think you would behave?',
    112: 'What’s the difference between justice and revenge?',
    113: 'If it was discovered that personality traits were partly genetic and could be removed with gene therapy, would it be ethical to edit out negative character traits that harm others like extreme aggression, compulsive lying, or cruelty?',
    114: 'If you could press a button and receive a million dollars, but one stranger would die, would you press the button? And if so, how many times?',
    115: 'At what point is overthrowing a government ethical, considering all the violence a revolution usually entails?',
    116: 'Can morality ever be objective or is it always subjective? If it can be objective, in what instances? If it’s always subjective, how do we decide whose concept of morality is correct?',
    117: 'Are intentions or outcomes more important when judging whether actions are moral?',
    118: 'Should there be limitations on the right to free speech?',
    119: 'Should euthanasia be legal? Why or why not?',
    120: 'If scientists could accurately predict who was more likely to commit crimes, what should society do with that information?',
    121: 'If you can save another’s life and don’t because doing so would break the law, are you ethically justified in your decision?',
    122: 'Are all individuals morally obligated to save another person’s life if they are able? What if that person lives in another country?',
    123: 'Should we terraform planets if it means that we may be destroying undiscovered microscopic alien life?',
    124: 'Does anonymity encourage people to misbehave or does it reveal how people would choose to act all the time if they could?',
    125: 'If doing something good for others makes us feel good, can there ever be such a thing as pure altruism?',
    126: 'Do all people have equal value regardless of their actions or is a person’s value based on their actions?',
    127: 'How much effort should an individual put into not offending others?',
    128: 'Would a government run with algorithms, A.I., and statistics be better or worse than the government we have now?',
    129: 'Would the world be a better or worse place if everyone looked the same?',
    130: 'Do people in wealthier countries have a moral obligation to help those in poorer countries?',
    131: 'What should the role of a government be, what boundaries and limitations should it have?',
    132: 'Do you think there will ever be a global government? If a world government did come to power, assuming it wasn’t particularly cruel or evil, would it be a good or bad thing?',
    133: 'What would happen to a society in which no one had to work, and everyone was provided enough food/water/shelter/healthcare for free?',
    134: 'Has social media been a net positive or a net negative for our society? Why?',
    135: 'Is it right or wrong that everyone seems to be accustomed to the fact that all of humanity and most of the life on Earth could be wiped out at the whim of a handful of people?',
    136: 'At what point is a technologically enhanced human not a human anymore?',
    137: 'Is true artificial intelligence possible with our current technology and methods of programming?',
    138: 'What scientific breakthrough would have the biggest effect on humanity?',
    139: 'Will we keep leaping to even greater technological and scientific breakthroughs that radically change society, or will the rate of progress slow and humanity’s progress be limited to incremental improvements?',
    140: 'If a robust and cheap genetic engineering industry existed, would you have your genes edited? If so, what genetic changes would you choose to make? If not, why not?',
    141: 'Assume that in the future there will be huge leaps in human augmentation. Given a scale from completely human to completely machine, how far would you choose to augment yourself with robotics? What parts would you augment and why?',
    142: 'If the transporters in Star Trek existed and you used it, your particles would be disassembled and then reassembled, do you die every single time? Are you ever alive at two places at once? Are you ever completely dead?',
    143: 'Should full access to the internet be a fundamental human right?',
    144: 'Has the invention of the atomic bomb made the world a more peaceful place?',
    145: 'If emotions are the product of biochemical reactions, then in the future we will be theoretically able to control them. If we could control emotions through technology, should we?',
    146: 'Is there a limit to what humans can create through technology and science?',
    147: 'Is cancel culture a good thing?',
    148: 'Is cancel culture a bad thing?',
    149: 'How can we differentiate between a valid use of "Cancel Culture" vs an instance of mob delirium?',
    150: 'Will the advent of "Designer Babies" via genetic modifications be ethical?'
}


# data['TOKEN']
client.run(bot_token)
