#!/usr/bin/env python3


##
# Dear Andy,
# Good job going through your code today!
# However, whatever you were thinking when
# you made me must have been some sort of
# insanity.  Please don't do most of what
# you thought you were doing here again.
# -- Note from Self.
##

from ircbot import IrcBot
from bog import Boggle
import random
import re

SERVER = "irc.freenode.net"
PORT = 6667
NICK = "Sleepzies"
CHANS = ("#andybots","#botdever", )

class ExampleBot(IrcBot):
    def response(self, ctx):
        """Clean this up and don't ever do it again"""
        msg = ctx['msg']
        if "testing" in msg:
            self.creply("Loud and clear")
        if ".game" in msg:
            gametypes = ["help","boggle","guess"]
            self.gameinit = False
            if len(msg.split()) > 2:
                _, game_type, *players = msg.split()
                print(players)
                if game_type in gametypes:
                    if players and "help" not in game_type:
                        self.gameinit = True
                        game = game_type
                        self.creply("So we have " + ", ".join(players[:(len(players) - 1)]) + " and " + players[-1] + " who want to play " + game_type + ".  Lets get started!")
                        if "guess" in game:
                            self.guess(players)

                        if "boggle" in game:
                            self.boggle(players)

                    elif "help" in game_type and players:
                        self.help_message(players)
                    else:
                        self.help_message()
                else:
                    self.creply("I'm not sure how you play that game.")
                    self.list_games(gametypes)
            else:
                self.help_message()
                self.list_games(gametypes)

        if ".boggle" in msg:
            self.boggle = Boggle(4)
            for line in self.boggle.board.split("\n"):
                self.creply(line)

        if ".answers" in msg:
            self.answers = self.boggle.answers
            self.creply("Total Possible: " + str(len(self.answers.split(", "))))
            self.creply("Answers were any of: " + self.answers)

        if ".guess" in msg:
            self.guess(ctx['sender'])
    def help_message(self, games=None):
        """Based on what I see here, I should be using a dict"""
        if games is None:
            self.creply("You do the .game [game or help] [*players or *games] and I'll figure out what you want.  :D")
        else:
            for game in games:
                if "guess" in game:
                    self.creply("Guess is a multiplayer number guessing game.")
                if "boggle" in game:
                    self.creply("Boggle is a classic.  Seriously, look it up.")
                if "help" in game:
                    self.creply("I don't know how much more I can help ya...")

    def list_games(self, game_list):
        games = ", ".join(game_list[1:len(game_list) -1]) + " and " + game_list[-1]
        self.creply("I know how to play " + games + ". But that's it at the moment.")

    def guess(self, players):
        """ Don't put the games in the bot... clean this too!"""
        self.creply("I'm thinking of a number between 1 and 255.  First player to guess it wins! :D")
        answer = int(random.choice(range(255))) + 1
        print("A>>>", answer)
        number = re.compile("(^|\W*)\d+(\W*)")
        numtype = type(re.compile("(^|\W*)\d+(\W*)"))
        correct_answer = re.compile("(^|\W*)" + str(answer) + "(\W*)")
        over = False
        while not over:
            ctx = self.get_ctx()
            msg = ctx['msg']
            sender = ctx['sender']
            found = correct_answer.match(ctx['msg'])
            try:
                num = int(number.match(ctx['msg']).group())
            except AttributeError as e:
                print("E<",e)
                num = ""

            if sender in players:
                if found:
                    self.creply("You win " + sender + "! :D")
                    self.creply("The answer was: " + str(num))
                    over = True
                if num and not found:
                    self.creply("Good try, but no")
                    print("N>>>",num)
                    if num > answer:
                        self.creply("too high..." + sender)
                    if num < answer:
                        self.creply("too low..." + sender)
                elif msg and not num:
                    if ".end" in msg:
                        self.creply("I guess that means I win.  Game over!")
                        over = True
                    else:
                        self.creply("Try numbers, those generally work " + sender)

    def boggle(self, players):
        self.creply("Sorry " + ", ".join(players) + "... I'm not fully able to play boggle yet.  Bug dont-panic and maybe he can fix it?")

if __name__ == "__main__":
    bot = ExampleBot(SERVER, PORT, NICK, CHANS).connect()

