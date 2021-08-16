# Brain bot

The Brain

A multi-purpose open-source Discord Bot written in Python. It uses multiple API's, the GPT-3 AI, as well as a MySQL DB for the Brain Cell economy and other things.

Features

 - Moderation (Mute, Dungeon, Ban, warnings, and notes)
 - Games (Coinflip, Blackjack, Trivia, Dice and Hangman)
 - Token Economy called Brain Cells (Shop, Working, Studying, Leaderboard)
 - Productivity commands (Studymode and ToDo List for Mods)
 - Fun (.ask to ask The Brain a question, Quotes, Jokes, Insults, Facts about Today, advice, and a list of thought experiments)
 - Utillity Commands (Instantly search the SEP, Google, and Wikipedia, Defines words, and makes Polls)
 - High Rank commands (Pings special roles)
 - Owner (Purge Channels, Award Brain Cells)
 - Other (server leaderboards for balance/score/pomodoros, search wikipedia articles, make suggestions to owner, ebook library)

## Setup

To install necesarry libraries run

python -m pip install -r requirements.txt

You will need to add your tokens (discord, openai, db credentials) to the .env file.

Next run

python bot.py

To start the bot

