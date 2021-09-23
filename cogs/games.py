import discord
from discord.ext import commands
import random
import requests
import json
from databaselayer import addBal, subBal, hasEnough, getUserBal
import asyncio


def hangman(word, guessedletters, game_in_progress):
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
        return [(hangmanpics[0] + '\n' + text), game_in_progress]
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
        return [(hangmanpics[errors] + "\n" + ' It was ' + word + '\n' + text + "\n\n YOU LOSE!"), game_in_progress]
    elif not ' - ' in printletter:
        game_in_progress = False
        return [(hangmanpics[errors] + "\n" + text + "\n\n YOU WIN!!!"), game_in_progress]
    else:
        return [(hangmanpics[errors] + "\n" + guessedletters + '\n' + text), game_in_progress]


# Python3 program to Split string into characters
def split(word):
    return [char for char in word]

people_list = ['alan turing', 'albert camus', 'aristotle', 'socrates', 'elon musk', 'albert einstein',
               'marie curie',
               'stephen hawking', 'isaac newton', 'confucius', 'napoleon bonaparte', 'karl marx', 'julius caesar',
               'nikola tesla', 'adolf hitler', 'george washington', 'william shakespeare', 'plato',
               'charles darwin',
       'galileo galilei', 'bingo bongo', 'leonardo da vinci']

place_list = ['paris', 'toronto', 'canada', 'america', 'france', 'europe', 'england', 'new york', 'los angeles',
              'las vegas', 'kansas', 'london', 'boston', 'pakistan', 'germany', 'new jersey', 'russia', 'china',
              'india', 'poland',
              'mexico', 'ottawa', 'berlin', 'alaska', 'serbia', 'japan', 'africa', 'australia', 'asia']

easy_list = ['wolf', 'deer', 'dangerous', ' fire station', 'surgeon', 'building', 'astrophysics', 'philosophy',
             'telekinetic',
             'genuine', 'nuclear', 'animal', 'greenhouse', 'firetruck', 'finger', 'palace', 'military',
             'commercial',
             'chemistry',
             'mathematics', 'rhino', 'jazz', 'music', 'dancing', 'alexa', 'siri']

hard_list = ['anomaly', 'equivocal', 'precipitate', 'assuage', 'erudite', 'opaque', 'prodigal', 'enigma', 'fervid',
             'placate',
             'desiccate', 'audacious', 'gullible', 'laudable', 'adulterate', 'jazz music', 'capricious',
             'homogenous',
             'loquacious', 'misanthrope', 'corroborate', 'paradox', 'philanthropic', 'epistemology', 'replicate',
             'jupiter',
             'alpha centauri']

guessedletters = ''
word = ''
game_in_progress = False


def getCard(deck):
    rand = random.randint(0, len(deck) - 1)
    # print(f"card index {rand} in {len(deck)}")
    card = deck.pop(rand)
    # diamonds -> spades -> clubs -> hearts
    if card <= 13:
        suit = '♢'
        value = card
    elif card <= 26:
        suit = "♤"
        value = card - 13
    elif card <= 39:
        suit = '♧'
        value = card - 26
    else:
        suit = '♡'
        value = card - 39

    return (suit, value)


def printCard(card):
    suit = card[0]
    value = card[1]
    if value == 1:
        value = "A"
    elif value == 11:
        value = "J"
    elif value == 12:
        value = "Q"
    elif value == 13:
        value = 'K'
    return f"`{value}{suit}` "


def getValue(hand):
    sum = 0
    for card in hand:
        value = card[1]
        if value >= 10:
            value = 10
        sum = sum + value
    return sum


def printHand(hand):
    rts = ''
    for card in hand:
        rts = rts + printCard(card)
    return rts


def predicate(ctx):
    admin_role1 = discord.utils.get(ctx.guild.roles, id=835623182484373535)
    admin_role2 = discord.utils.get(ctx.guild.roles, id=835400292979179530)
    return admin_role1 in ctx.author.roles or admin_role2 in ctx.author.roles or ctx.author.id == 339070790987284491
    # test = discord.utils.get(ctx.guild.roles, id=858614845363322881)
    # return test in ctx.author.roles


has_roles = commands.check(predicate)


class Games(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['bj'])
    async def blackjack(self, ctx, ammount:str = None):
        if ammount == None:
            await ctx.send("How much do you want to bet? Try again.")
            return
        if 'all' in ammount.strip().lower():
        # if ammount == "all":
            ammount = getUserBal(ctx.author.id)
        try:
            ammount = int(ammount)
        except:
            await ctx.send("There was an error, try again.")
            return

        if ammount <= 0:
            await ctx.send("Can't do negative numbers.")
            return
        elif ammount < 50:
            await ctx.send("Need to bet at least 50 Brain Cells.")
            return
        elif not hasEnough(ctx.author.id, ammount):
            await ctx.send("You do not have enough Brain Cells.")
            return

        subBal(ctx.author.id, ammount)
        deck = []
        for i in range(1, 52):
            deck.append(i)
        game_state = True
        player_hand = []
        bot_hand = []
        player_hand.append(getCard(deck))
        player_hand.append(getCard(deck))
        bot_hand.append(getCard(deck))
        bot_hand.append(getCard(deck))

        # bot_hand_to_print = f"
        lost = False

        while game_state:
            embed = discord.Embed(title=f"{ctx.author.display_name}'s blackjack game", color=ctx.author.color)
            embed.add_field(name=f"Your hand: {printHand(player_hand)}", value=f"Value = `{getValue(player_hand)}`",
                            inline=True)
            embed.add_field(name=f"My hand: {printCard(bot_hand[0])} `?`", value="Value = `?`")
            embed.add_field(name='H for Hit, S for Stand.', value="** **", inline=False)
            # {printHand(bot_hand)}, value = {getValue(bot_hand)}")
            if getValue(player_hand) > 21:
                embed.add_field(name="**You lose.**", value="** **", inline=False)
                embed.color = 0xff0000
                #await ctx.send(embed=embed)
                lost = True
                break
                # subBal(ctx.author.id, ammount)
                # return

            embed.set_footer(text="A = 1, | J, Q, K = 10")
            await ctx.send(embed=embed)

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.lower().strip() in ["h", 'H', 'S', 's']

            try:
                reply = await self.client.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send("Since you didn't answer within a minute, I'm assuming you Stand..")
                game_state = False
                break

            msg = reply.content
            msg = msg.strip().lower()
            if msg == 'h':
                player_card = getCard(deck)
                player_hand.append(player_card)
            elif msg == 's':
                game_state = False
            else:
                await ctx.send("Since you didn't give me a valid response, I'm assuming you Stand.")
                game_state = False

        # game_state = True
        while not getValue(bot_hand) >= 17:
            bot_card = getCard(deck)
            bot_hand.append(bot_card)

            # await ctx.send(printCard(card))
        embed = discord.Embed(title=f"{ctx.author.display_name}'s blackjack game")
        embed.add_field(name=f"Your hand: {printHand(player_hand)}", value=f"Value = {getValue(player_hand)}",
                        inline=True)
        embed.add_field(name=f"My hand: {printHand(bot_hand)}", value=f"Value = {getValue(bot_hand)}")
        # await ctx.send(embed=embed)
        if lost:
            embed.add_field(name="**You lose.**", value="** **", inline=False)
            embed.color = 0xff0000
            # subBal(ctx.author.id, ammount)
        elif getValue(player_hand) == 21 and getValue(bot_hand) == 21:
            embed.add_field(name="**It's a draw.**", value="** **", inline=False)
            addBal(ctx.author.id, ammount)
        elif getValue(bot_hand) > 21:
            embed.add_field(name="**You win.**", value="** **", inline=False)
            embed.color = 0x00ff00
            addBal(ctx.author.id, (ammount*2))

        elif getValue(player_hand) == getValue(bot_hand):
            embed.add_field(name="**You draw.**", value="** **", inline=False)
            addBal(ctx.author.id, ammount)

        elif getValue(player_hand) > getValue(bot_hand):
            embed.add_field(name="**You win**.", value="** **", inline=False)
            embed.color = 0x00ff00
            addBal(ctx.author.id, (ammount*2))

        else:
            embed.add_field(name="**You lose.**", value="** **", inline=False)
            embed.color = 0xff0000
            # subBal(ctx.author.id, ammount)

        embed.set_footer(text="A = 1 | J, Q, K = 10")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,15,commands.BucketType.guild)
    async def trivia(self, ctx):
        res = requests.get("https://opentdb.com/api.php?amount=1&type=multiple")
        result = json.loads(res.text)
        ans = result['results'][0]
        question = ans['question'].replace('&quot;', '"')
        question = question.replace('&#039;', "'")
        question = question.replace('&amp;', "&")
        embed = discord.Embed(title="Trivia Time", colour=0x03fcdf)
        if ans['type'] == "multiple":
            answerlist = ans['incorrect_answers']
            index = random.randint(0, 3)
            answerlist.insert(index, ans['correct_answer'])
            answers = f"1️⃣: {answerlist[0]}\n2️⃣: {answerlist[1]}\n3️⃣: {answerlist[2]}\n4️⃣: {answerlist[3]} "
            # msg = await ctx.send(ans['question'])
            embed.add_field(name=question, value=answers)
            # await msg.add_reaction("✅")

            embed.set_footer(text=f"Category: {ans['category']}  Difficulty: {ans['difficulty']}")
            embed.set_thumbnail(
                url="https://media.discordapp.net/attachments/861788174249754634/863326727018905640/happybrain.png")
            msg = await ctx.send(embed=embed)
            emotelist = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
            for emote in emotelist:
                await msg.add_reaction(emote)

        # await ctx.send(f"Winning option is {index + 1}")

        if ans['difficulty'] == 'easy':
            award = 100
        elif ans['difficulty'] == 'medium':
            award = 200
        elif ans['difficulty'] == 'hard':
            award = 300
        await asyncio.sleep(15)
        cache_msg = discord.utils.get(self.client.cached_messages, id=msg.id)
        cache_reaction = cache_msg.reactions
        users = await cache_reaction[index].users().flatten()
        users.remove(self.client.user)
        cache_reaction.remove(cache_reaction[index])

        removelist = []
        for user in users:

            for reaction in cache_reaction:
                temp = await reaction.users().flatten()
                # print(f"{user} reacted {reaction}")
                # print(temp)
                if user in temp:
                    # print(f"User was in temp")
                    try:
                        removelist.append(user)
                        # users.remove(user)
                    except:
                        print("something")
                        # pass
                    # print('removed user')

        for user in removelist:
            try:
                users.remove(user)
            except:
                pass

        if len(users) == 0:
            sendmsg = f"No one got it right. The correct answer was: {index + 1}. {answerlist[index]}"
        else:
            sendmsg = "Congrats to "
            for user in users:
                if user == self.client.user:
                    pass
                else:
                    sendmsg = sendmsg + f"{user.mention} "
                    addBal(user.id, award)
                # addbal
                # print(f"Added bal to {user.display_name}")
                # await ctx.send(user.display_name)
            sendmsg = sendmsg + f" for getting it right! They win {award} Brain Cells. "

            sendmsg = sendmsg + f"The correct answer was: {index + 1}. {answerlist[index]}"
        await ctx.send(sendmsg)

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def coinflip(self, ctx, ammount: str = '10', options: str = None):
        if 'all' in ammount.strip().lower():
            # if ammount == "all":
            ammount = getUserBal(ctx.author.id)
        try:
            ammount = int(ammount)
        except:
            await ctx.send("There was an error, try again.")
            return
        if options == None:
            await ctx.send("Heads or Tails? Try again.")
            return
        elif ammount < 0:
            await ctx.send("Can't do that buddy.")
            return
        elif not hasEnough(ctx.author.id, ammount):
            await ctx.send("You don't have enough Brain Cells for that.")
            return
        options = options.strip().lower()

        result = random.randint(0, 1)
        if options not in ["heads", 'head', 'tails', "tail"]:
            await ctx.send("Enter a valid option.")
            return
        if result == 1 and (options == "heads" or options == "head"):
            st = f"It was Heads! You win {ammount} Brain cells!"
            addBal(ctx.author.id, ammount)
        elif result == 0 and (options == "tails" or options == "tail"):
            st = f"It was Tails! You win {ammount} Brain cells!"
            addBal(ctx.author.id, ammount)
        elif result == 1 and (options == "tails" or options == "tail"):
            st = f"It was Heads, you lose {ammount} Brain Cells!"
            subBal(ctx.author.id, ammount)
        elif result == 0 and (options == "heads" or options == "head"):
            st = f"It was Tails, you lose {ammount} Brain Cells!"
            subBal(ctx.author.id, ammount)
        else:
            st = "There was an error."
        embed = discord.Embed(title=st,
                              colour=ctx.author.colour)
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/861788174249754634/863326727018905640/happybrain.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def dice(self, ctx, number:int, ammount:str):
        if 'all' in ammount.strip().lower():
        # if ammount == "all":
            ammount = getUserBal(ctx.author.id)
        try:
            ammount = int(ammount)
        except:
            await ctx.send("There was an error, try again.")
            return
        if number > 6 or number <= 0:
            await ctx.send("A die only has 6 sides dummy.")
            return
        if not hasEnough(ctx.author.id, ammount):
            await ctx.send("You don't have enough.")
            return
        if ammount <= 0:
            await ctx.send("Can't do negative numbers.")
            return
        rand = random.randint(1,6)
        subBal(ctx.author.id, ammount)
        if number == rand:
            embed = discord.Embed(title=f"You win! The number was {rand}! You got {ammount*6} Brain Cells!", colour=ctx.author.colour)
            embed.set_thumbnail(
                url="https://media.discordapp.net/attachments/861788174249754634/863326727018905640/happybrain.png")
            await ctx.send(embed=embed)
            addBal(ctx.author.id, ammount*6)
        else:
            embed = discord.Embed(title=f"You lose! The number was {rand}.",
                                  colour=ctx.author.colour)
            embed.set_thumbnail(
                url="https://media.discordapp.net/attachments/861788174249754634/863326727018905640/happybrain.png")
            await ctx.send(embed=embed)



    async def getJackpot(self, channel, recipient):
        amount = random.randint(2500, 6000)
        s = ""
        if random.randint(1, 15) == 13:
            s = "**YOU HIT THE JACKPOT**"
            amount = 42069
        if random.randint(1, 50) == 25:
            s = "**YOU HIT THE JACKPOT**"
            amount = 500000
        if random.randint(1, 100) == 81:
            s = "**YOU HIT THE JACKPOT**"
            amount = 1000000
        addBal(recipient.id, amount)
        s += f"Thanks for bumping the server! We really appreciate the support!\n Here's {amount} Brain Cells for the effort! \n Keep bumping and you may get **really** lucky ; )"
        await channel.send(s)


    @commands.command()
    @has_roles
    async def calculate(self,ctx, recipient:discord.Member):
        await self.getJackpot(ctx.channel, recipient)


    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content == "!d bump":
            def check(m):
                # thevat = self.client.get_guild(831211215375433728)
                return m.author == self.client.get_user(302050872383242240) # and message.guild == thevat

            reply = await self.client.wait_for('message', check=check, timeout=2.0)
            embed = reply.embeds[0]
            if "Bump done" in embed.description:
                await self.getJackpot(message.channel, message.author)
                await asyncio.sleep(7200)
                await message.channel.send("Time for a bump!")

        global word
        global guessedletters
        global game_in_progress
        global people_list
        global easy_list
        global hard_list
        global place_list

        msg = message.content

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
                    if "WIN" in returntext:
                        addBal(message.author.id, 250)
                    guessedletters = ''
                    word = ''
                await message.channel.send(returntext)
        #


def setup(client):
    client.add_cog(Games(client))