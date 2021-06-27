import discord
from discord.ext import commands
import random


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

easy_list = ['wolf', 'deer', 'dangerous', ' fire station', 'surgeon', 'building', 'astrophysics', 'phiilosophy',
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

class Hangman(commands.Cog):


    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_message(self, message):

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
                    guessedletters = ''
                    word = ''
                await message.channel.send(returntext)
        #




def setup(client):
    client.add_cog(Hangman(client))