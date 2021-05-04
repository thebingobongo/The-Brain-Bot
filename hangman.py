

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