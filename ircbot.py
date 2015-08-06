#!/usr/bin/env python3
import socket

def enc(text):
    return text.encode('utf-8')

class IrcBot:
    """A class for creating IRC Bots"""
    connected = False

    def __init__(self, host, port, nick, chan):
        self.host = host
        self.port = port
        self.nick = nick
        self.chan = chan
        self.private_key = ".pm"
        self.greeting = "yawns"

    def connect(self):
        self.socket = socket.socket()
        self.socket.connect((self.host, self.port))
        self.socket.send(enc("NICK %s\r\n" % self.nick))
        self.socket.send(enc("USER %s 8 i :%s\r\n" % (self.nick, self.nick)))

        while True:
            ctx = self.get_ctx()
            try:
                self.target = ctx['target']
                msg = ctx['msg']
                self.sender = ctx['sender']
                if self.nick in msg:
                    self.targeted_response(ctx)
                elif self.private_key in msg:
                    self.private_message(ctx)
                else:
                    self.response(ctx)
            except KeyError as e:
                print("E>",e)



    def get_ctx(self):
        buf = self.socket.recv(4096)
        lines = buf.decode('utf-8').split('\n')
        for data in lines:
            data = data.strip()
            if data == '':
                continue
            print("D<", data)
            if data.find('PING') != -1:
                n = data.split(':')[1]
                self.socket.send(enc("PONG :%s\r\n" % n))
                if self.connected == False:
                    self.reconnect()
            args = data.split(None, 3)
            self.args = args
            #if len(args) != 4:
            #    continue
            ctx = {}
            try:
                ctx['sender'] = args[0][1:].split("!")[0]
                ctx['type'] = args[1]
                ctx['target'] = args[2]
                ctx['msg'] = args[3][1:]
            except IndexError as e:
                print("E>",e)
        return ctx

    def reconnect(self):
        for chan in self.chan:
            self.socket.send(enc("JOIN %s\r\n" % chan))
        self.connected == True


    # Ways to respond
    def creply(self, msg):
        print("C>", msg, "->", self.target)
        self.socket.send(enc("PRIVMSG %s :%s\r\n" % (self.target, msg)))

    def reply(self, ctx):
        msg = ctx['msg']
        print("R>", msg, "->", self.sender)
        self.socket.send(enc("PRIVMSG %s :%s\r\n" %(self.sender, msg)))

    def send(self, to, ctx):
        msg = ctx['msg']
        print("S>", msg, "->", to)
        self.socket.send(enc("PRIVMSG %s :%s\r\n" % (to, msg)))

    def thinks(self, to, ctx):
        msg = ctx['msg']
        print("T>", msg, "->", to)
        self.socket.send(enc("PRIVMSG %s :%s\r\n" % (to, chr(1) + "ACTION " + msg + chr(1))))


    # what to respond to and how
    def private_message(self, ctx):
        msg = ctx['msg']
        self.reply(msg)

    def targeted_response(self, msg):
        if "target" in msg:
            self.send(self.target, msg)

    def response(self, msg):
        if "respond" in msg:
            self.creply(self.target, msg)

if __name__ == "__main__":

    bot = IrcBot("irc.freenode.net", 6667, "Half-Panic", "#andybots").connect()
