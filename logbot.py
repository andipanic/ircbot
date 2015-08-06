#!/usr/bin/env python3

from ircbot import IrcBot

SERVER = "irc.freenode.net"
PORT = 6667
NICK = "Sleepzies"
CHANS = ("#ubuntu","#debian", )

if __name__ == '__main__':
    bot = IrcBot(SERVER,PORT,NICK,CHANS).connect()
