#! /usr/bin/env python2
# This file is part of the anontwi project, http://anontwi.03c8.net
# Copyright (c) 2012/2013/2014/2015 by psy <epsylon@riseup.net>
# AnonTwiIRCBot v0.1 - 2012 - GPLv3.0
# pancake <nopcode.org>
# psy <nopcode.org>
import os
import sys
import socket
import string
import time
import HTMLParser
from core.wrapper import WrapperAnontwi

def getuser(user):
    return user.split('!')[0][1:]
HELPMSG = """
-----------------------
AnonTwiIRCbot commands: 
    !home [num]             : view account 'home' timeline
    !public [user] [num]    : view public timeline of a user
    !private [num]          : view private timeline
-----------------------
    !gen                    : generate secret
    !pin [secret]           : active encryption
    !nopin                  : deactive encryption
    !dec [pin] [msg]        : decrypt a message
-----------------------
    !m [msg]                : send a public message
    !d [user] [msg]         : send a private message
    !rt [ID]                : retweet a message
    !tt                     : view trending topics
    !search [term]          : search a term
-----------------------
    !kill                   : kill bot!
-----------------------
"""
HELLO = """Hello, I am an AnonTwi-IRCbot (http://anontwi.03c8.net). Use: !help for options."""
class AnonTwiIrcBot():
    def runcmd(self, who, args):
        a = args[0].lower ()

        if (a=="!gen\r"):
            print "Generating secret!"
            self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
            try:
                key = self.wrapper.generate_key()
                self.s.send ( 'PRIVMSG ' + who + " :" + "Secret(PIN): " + key + "\n")
            except:
                self.s.send ( 'PRIVMSG ' + who + " :" + "Random secret generation failed :( " + "\n")
            self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")

        if (a=="!pin"):
             print "Encryption: ON"
             key = string.join(args[1:2]," ") + "\n"
             key = key.rstrip("\n\r") 
             enc = { 'enc' : True,
                     'pin' : key, }
             self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
             self.s.send ( 'PRIVMSG ' + who + " :" + "Encryption is ON using secret: " + key + "\n")
             self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
             self.enc = enc

        if (a=="!nopin\r"):
             print "Encryption: OFF"
             enc = { 'enc' : False,
                     'pin' : None, }
             key = None
             self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
             self.s.send ( 'PRIVMSG ' + who + " :" + "Encryption is OFF! (secret removed!)" + "\n")
             self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
             self.enc = enc

        if (a=="!dec"):
            print "Decrypting message"
            h = HTMLParser.HTMLParser()
            key = string.join(args[1:2]," ") + "\n"
            messages = string.join(args[2:]," ") + "\n"
            self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
            if not key:
                self.s.send ( 'PRIVMSG ' + who + " :" + "Error: Pin is empty!" + "\n")
            elif not messages:
                self.s.send ( 'PRIVMSG ' + who + " :" + "Error: Message is empty!" + "\n")
            self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
            try:
                msg = self.wrapper.decrypt(messages, key)
                m = h.unescape(msg)
                self.s.send ( 'PRIVMSG ' + who + " :" + "Message(Decrypted): " + m + "\n")
            except:
                self.s.send ( 'PRIVMSG ' + who + " :" + "Descryption failed :( " + "\n")
            self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")

#        if (a=="!proxy"):
#             print "Proxy: ON"
#             proxy_irc = string.join(args[1:2]," ") + "\n"
#             proxy_irc = proxy_irc.rstrip("\n\r")
#             if proxy_irc.startswith("http://"): # better parse required
#                 proxy_prefix = "http://"
#                 proxy_irc = proxy_irc.strip("http://")
#             if proxy_irc.startswith("https://"):
#                 proxy_prefix = "https://"
#                 proxy_irc = proxy_irc.strip("https://")
#             [host, port] = proxy_irc.rsplit(':')
#             proxy = { 'proxy' : True,
#                       'ip_address' : host,
#                       'port' : proxy_prefix + port, }
#             self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
#             self.s.send ( 'PRIVMSG ' + who + " :" + "Proxy is ON!" + "\n")
#             self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
#             self.proxy = proxy

#        if (a=="!noproxy\r"):
#             print "Proxy: OFF"
#             proxy = { 'proxy' : False,
#                       'ip_address' : None,
#                       'port' : None }
#             self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
#             self.s.send ( 'PRIVMSG ' + who + " :" + "Proxy is OFF!" + "\n")
#             self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
#             self.proxy = proxy

        if (a=="!m"):
            print "Sending public message!"
            self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
            tweet = string.join(args[1:]," ")+"\n"
            pm = { 'pm' : False,
                   'user' : None, }
            try:
                if self.enc["enc"] is True: # encryption activated
                    self.wrapper.send_tweet (tweet, pm, True, None, self.enc) #msg, fake GPS, enc
                else:      
                    self.wrapper.send_tweet (tweet, pm, True, True, None) #msg, fake GPS, waves
                self.s.send ( 'PRIVMSG ' + who + " :" + "Public message sent!" + "\n")
            except:
                self.s.send ( 'PRIVMSG ' + who + " :" + "Public message failed :(" + "\n")
            self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")

        if (a=="!d"):
            print "Sending private message"
            self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
            user = string.join(args[1:2]," ") + "\n"
            tweet = string.join(args[2:]," ") + "\n"
            pm = { 'pm' : True,
                   'user' : user, }
            try:
                if self.enc["enc"] is True: # encryption activated
                    self.wrapper.send_tweet (tweet, pm, None, None, self.enc, None) #msg, private, enc
                else:
                    self.wrapper.send_tweet (tweet, pm, None, None, None, None) #msg, private
                self.s.send ( 'PRIVMSG ' + who + " :" + "Private message sent!" + "\n")
            except:
                self.s.send ( 'PRIVMSG ' + who + " :" + "Private message failed :(" + "\n")
            self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")

        if (a=="!rt"):
            print "Retweeting message"
            self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
            ID = string.join(args[1:]," ") + "\n"
            if not ID:
                self.s.send ( 'PRIVMSG ' + who + " :" + "You must enter a correct ID to Retweet this message " + "\n")
            try:
                self.wrapper.retweet_tweet(ID)
                self.s.send ( 'PRIVMSG ' + who + " :" + "Retweet sent! " + "\n")
            except:
                self.s.send ( 'PRIVMSG ' + who + " :" + "Retweet failed :( " + "\n")
            self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")

#        if (a=="!reply"):
#            print "Replying message"
#            self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
#            ID = string.join(args[1:2]," ") + "\n"
#            msg = string.join(args[2:]," ") + "\n"
#            print ID
#            print msg
#            if not ID:
#                self.s.send ( 'PRIVMSG ' + who + " :" + "You must enter a correct ID to Replying this message " + "\n")
#            try:
#                replies = self.wrapper.reply(ID, msg, None, None)
#                self.s.send ( 'PRIVMSG ' + who + " :" + "Reply sent! " + "\n")
#            except:
#                self.s.send ( 'PRIVMSG ' + who + " :" + "Reply failed :( " + "\n")
#            self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")

        if (a=="!tt\r"):
            print "Showing Trending Topics"
            h = HTMLParser.HTMLParser()
            self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
            try:
                trendingtopics = self.wrapper.search_topics()
                if len(trendingtopics) <= 0:
                    print "Not trending topics.\n"
                    self.s.send ( 'PRIVMSG ' + who + " :" + "Not trending topics. " + "\n")
                else:
                    for line in trendingtopics.split("\n"):
                        line = line.encode("utf-8")
                        self.s.send ( 'PRIVMSG ' + who + " :" + str(line) + "\n")
                self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")

            except:
                print "Something wrong getting trending topics... Aborting!\n"

        if (a=="!search"):
            print "Searching..."
            h = HTMLParser.HTMLParser()
            try:
                textsearch = string.join(args[1:]," ") + "\n"
                num_ocurrences = "4" # fix this to provide a num of results
                searches = self.wrapper.search_messages(textsearch, num_ocurrences)
                self.s.send ( 'PRIVMSG ' + who + " :" + "===================" + "\n")
                self.s.send ( 'PRIVMSG ' + who + " :" + "Results for: " + textsearch + "\n")
                self.s.send ( 'PRIVMSG ' + who + " :" + "===================" + "\n")
                if len(searches) <= 0:
                    print "Not searching results.\n"
                    self.s.send ( 'PRIVMSG  ' + who + " :" + "Not searching results. " + "\n")
                    self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
                else:
                    for s in searches:
                        t = h.unescape(s.user.screen_name)
                        self.s.send ( 'PRIVMSG ' + who + " :" + "Nick: " + str(t) + "\n")
                        try:
                            t =  h.unescape(s.user.screen_name)
                            self.s.send ( 'PRIVMSG ' + who + " :" + "Nick: " + str(t) + "\n")
                        except:
                            try:
                                t = t.encode("utf-8")
                                self.s.send ( 'PRIVMSG ' + who + " :" + "Nick: " + str(t) + "\n")
                            except:
                                self.s.send ( 'PRIVMSG ' + who + " :" + "ERROR: This nickname contains invalid parameters. Sorry!" + "\n")
                        self.s.send ( 'PRIVMSG ' + who + " :" + "ID: " + str(s.id) + "\n")
                        self.s.send ( 'PRIVMSG ' + who + " :" + str(s.created_at) + "\n")
                        try:
                            m =  h.unescape(s.text)
                            self.s.send ( 'PRIVMSG ' + who + " :" + str(m) + "\n")
                        except:
                            try:
                                m = m.encode("utf-8")
                                self.s.send ( 'PRIVMSG ' + who + " :" + str(m) + "\n")
                            except:
                                self.s.send ( 'PRIVMSG ' + who + " :" + "ERROR: This message contains invalid parameters. Sorry!" + "\n")
                        if s.place:
                            self.s.send ( 'PRIVMSG ' + who + " :" + "Location " + str(s.place["full_name"]) + "\n")
                        else:
                            pass
                        time.sleep(5) #irc breathing
                        self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
            except:
                print "Something wrong searching... Aborting!\n"

        if (a=="!home") or (a=="!home\r"):
            print "Showing Home Timeline..."
            try:
                num_ocurrences = int(string.join(args[1:]," ").replace("[","").replace("]","").replace("\r","")) 
            except:
                num_ocurrences = 2        
            h = HTMLParser.HTMLParser()
            try:
                if num_ocurrences is None or num_ocurrences <=0:
                    num_ocurrences = 2
                (timelines, num) = self.wrapper.show_public(num_ocurrences, None)
                self.s.send ( 'PRIVMSG ' + who + " :" + "===================" + "\n")
                self.s.send ( 'PRIVMSG ' + who + " :" + "Home Timeline: " + "\n")
                self.s.send ( 'PRIVMSG ' + who + " :" + "===================" + "\n")
                if len(timelines) <= 0:
                    self.s.send ( 'PRIVMSG ' + who + " :" + "You haven't any message, yet." + "\n")
                    self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
                    return
                else:
                    if int(len(timelines)) < int(num):
                        num = int(len(timelines))
                    for i in range(int(num)):
                        try:
                            t = h.unescape(timelines[i].user.screen_name)
                            self.s.send ( 'PRIVMSG ' + who + " :" + str(t) + "\n")
                        except:
                            try:
                                t = t.encode("utf-8")
                                self.s.send ( 'PRIVMSG ' + who + " :" + str(t) + "\n")
                            except:
                                self.s.send ( 'PRIVMSG ' + who + " :" + "ERROR: This nickname contains invalid parameters. Sorry!" + "\n")
                        self.s.send ( 'PRIVMSG ' + who + " :" + "ID: " + str(timelines[i].id) + "\n")
                        self.s.send ( 'PRIVMSG ' + who + " :" + str(timelines[i].created_at) + "\n")
                        try:
                            m =  h.unescape(timelines[i].text)
                            self.s.send ( 'PRIVMSG ' + who + " :" + str(m) + "\n")
                        except:
                            try:
                                m = m.encode("utf-8")
                                self.s.send ( 'PRIVMSG ' + who + " :" + str(m) + "\n")
                            except:
                                self.s.send ( 'PRIVMSG ' + who + " :" + "ERROR: This message contains invalid parameters. Sorry!" + "\n")
                        if timelines[i].place is not None:
                            self.s.send ( 'PRIVMSG ' + who + " :" + "Location: " + str(timelines[i].place["full_name"]) + "\n")
                        else:
                            pass
                        self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
                        time.sleep(5) #irc breathing
            except:
                print "Something wrong showing 'Home' Timeline... Aborting!\n"

        if (a=="!public") or (a=="!public\r"):
            print "Showing Public Timeline..."
            h = HTMLParser.HTMLParser()
            try:
                params =  string.join(args[1:]).replace("[","").replace("]","").replace("\r","").split(" ")
                
                user = params[0]
                num_ocurrences = params[1]
                
                try:
                    num_ocurrences = int(num_ocurrences)
                    if num_ocurrences < 1:
                        num_ocurrences = 4
                except:
                    num_ocurrences = 4
                
                ps = self.wrapper.home_timeline(user, num_ocurrences)
                self.s.send ( 'PRIVMSG ' + who + " :" + "===================" + "\n")
                self.s.send ( 'PRIVMSG ' + who + " :" + "Public Timeline of: " + user + "\n")
                self.s.send ( 'PRIVMSG ' + who + " :" + "===================" + "\n")
                for p in ps[0]:
                    try:
                        u = h.unescape(p.user.screen_name)
                        self.s.send ( 'PRIVMSG ' + who + " :" + "Nick: " + str(u) + "\n")
                    except:
                        try:
                            u = u.encode("utf-8")
                            self.s.send ( 'PRIVMSG ' + who + " :" + str(u) + "\n")
                        except:
                            self.s.send ( 'PRIVMSG ' + who + " :" + "ERROR: This nickname contains invalid parameters. Sorry!" + "\n")
                    self.s.send ( 'PRIVMSG ' + who + " :" + "ID: " + str(p.id) + "\n")
                    self.s.send ( 'PRIVMSG ' + who + " :" + str(p.created_at) + "\n")
                    try:
                        #TODO Fix ExcessFlood by waving?
                        m =  h.unescape(p.text)
                        self.s.send ( 'PRIVMSG ' + who + " :" + str(m) + "\n")
                    except:
                        try:
                            m = m.encode("utf-8")
                            self.s.send ( 'PRIVMSG ' + who + " :" + str(m) + "\n")      
                        except:
                            self.s.send ( 'PRIVMSG ' + who + " :" + "ERROR: This message contains invalid parameters. Sorry!" + "\n")
                    if p.place is not None:
                        self.s.send ( 'PRIVMSG ' + who + " :" + "Location: " + str(p.place["full_name"]) + "\n")
                    else:
                        pass
                    self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
                    time.sleep(5) #irc breathing
            except:
                print "Something wrong showing Public Timeline... Aborting!\n"

        if (a=="!private") or (a=="!private\r"):
            print "Showing Private Timeline..."
            try:
                params =  string.join(args[1:]).replace("[","").replace("]","").replace("\r","").split(" ")                

                num_ocurrences = params[0]
                num_ocurrences = int(num_ocurrences)
                if num_ocurrences < 1:
                    num_ocurrences = 4
            except:
                num_ocurrences = 2     

            h = HTMLParser.HTMLParser()
            try:
                (privates, num) = self.wrapper.show_private(str(num_ocurrences))
                self.s.send ( 'PRIVMSG ' + who + " :" + "===================" + "\n")
                self.s.send ( 'PRIVMSG ' + who + " :" + "Private Timeline: " + "\n")
                self.s.send ( 'PRIVMSG ' + who + " :" + "===================" + "\n")
                if len(privates) <= 0:
                    self.s.send ( 'PRIVMSG ' + who + " :" + "You haven't any private, yet." + "\n")
                    self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
                    return
                else:
                    if int(len(privates)) < int(num):
                        num = int(len(privates))
                    for i in range(int(num)):
                        self.s.send ( 'PRIVMSG ' + who + " :" + "ID: " + str(privates[i].id) + "\n")
                        self.s.send ( 'PRIVMSG ' + who + " :" + str(privates[i].created_at) + "\n")
                        u = h.unescape(privates[i].sender_screen_name)
                        self.s.send ( 'PRIVMSG ' + who + " :" + "From: " + str(u) + "\n")                       
                        try:
                            s = h.unescape(privates[i].text)
                            self.s.send ( 'PRIVMSG ' + who + " :" + str(s) + "\n")
                        except:
                            try:
                                s = s.encode("utf-8")
                                self.s.send ( 'PRIVMSG ' + who + " :" + str(s) + "\n")
                            except:
                                self.s.send ( 'PRIVMSG ' + who + " :" + "ERROR: This message contains invalid parameters. Sorry!" + "\n")

                        self.s.send ( 'PRIVMSG ' + who + " :" + "------------------------------" + "\n")
                        time.sleep(5) #irc breathing
            except:
                print "Something wrong showing Public Timeline... Aborting!\n"

        if (a=="!help\r"):
            for line in HELPMSG.split("\n"):
                time.sleep(1) #irc breathing
                self.s.send ( 'PRIVMSG ' + who + " :" + str(line) + "\n")
        
        if (a=="!kill\r"):
            print "Killing bot"
            self.s.send ( 'PRIVMSG ' + who + " :" + "===================" + "\n")
            self.s.send ( 'PRIVMSG ' + who + " :" + "Bot killed!" + "\n")
            self.s.send ( 'PRIVMSG ' + who + " :" + "===================" + "\n")
            self.s.send ( 'QUIT\r\n' )
            sys.exit()

    def __init__(self):
        self.wrapper = WrapperAnontwi()
       # checking if 'temp' tokens are on correct position
        if os.getenv("ANONTWI_TOKEN_KEY") is None and os.getenv("ANONTWI_TOKEN_SECRET") is None: 
            print "\nWarning: AnonTwi cannot authenticate you correctly!", "There is a problem with your tokens.\n\n You must provide a correct 'ANONTWI_TOKEN_KEY' and 'ANONTWI_TOKEN_SECRET' environment variables to the shell that launchs this GTK interface.\n\n - On Unix: \n export ANONTWI_TOKEN_KEY=Value\n export ANONTWI_TOKEN_SECRET=Value \n\n - On Win32: \n set ANONTWI_TOKEN_KEY=Value\n set ANONTWI_TOKEN_SECRET=Value\n\nTry: anontwi --tokens on shell mode, if you don't understand this error.\n"
            sys.exit()
        if os.getenv("ANONTWI_TOKEN_KEY") is None:
            print("\nWarning: AnonTwi cannot authenticate you correctly!", "There is a problem with tokens. You must provide a correct 'ANONTWI_TOKEN_KEY' environment variable to the shell that launchs this GTK interface.\n\n - On Unix: \n export ANONTWI_TOKEN_KEY=Value \n\n - On Win32: \n set ANONTWI_TOKEN_KEY=Value\n\nTry: anontwi --tokens on shell mode, if you don't understand this error.\n")
            sys.exit()
        elif os.getenv("ANONTWI_TOKEN_SECRET") is None:          
            GuiUtils.Warning("\nWarning: AnonTwi cannot authenticate you correctly!", "There is a problem with tokens. You must provide a correct 'ANONTWI_TOKEN_SECRET' environment variable to the shell that launchs this GTK interface.\n\n - On Unix: \n export ANONTWI_TOKEN_SECRET=Value \n\n - On Win32: \n set ANONTWI_TOKEN_SECRET=Value\n\nTry: anontwi --tokens on shell mode, if you don't understand this error.\n")
            sys.exit()
        self.enc = { 'enc' : False,
                     'pin' : None, }

    def get_reply_user(self, id):
        status = self.wrapper.get_reply_user(id)
        user = status.user.screen_name
        return user

    def run(self, nick, host, port, channel):
        print "Connecting to: " + host + "," + port
        self.s = s = socket.socket ()
        s.connect ((host, int(port)))
        s.send ("NICK %s\r\n" % nick)
        s.send ("USER %s %s bla :%s\r\n" % (nick, host, nick))
        if channel != "":
            s.send ("JOIN #" + channel + "\r\n")
            for line in HELLO.split("\n"):
                self.s.send ( 'PRIVMSG #' + channel + " :" + str(line) + "\n")
        rb = ""
        while 1:
            rb = rb + s.recv(4096)
            temp = rb.split("\n")
            rb = temp.pop ()
        
            for line in temp:
                args = line.split(' ')
                print ">>>> " + line
        
                if (args[1] == "PRIVMSG"):
                    user = getuser (args[0])
                    msg = string.join (args[3:]," ")[1:]
                    msgargs = msg.split(' ')
                    print "<" + user + "> " + msg
                    self.runcmd(user, msgargs)
                elif (args[1] == "PING\r"):
                    s.send("PONG %s\r\n" % args[2])

if __name__=="__main__":
    print "TODO: irc test"
