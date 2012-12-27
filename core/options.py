#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""
$Id$

This file is part of the anontwi project, http://twitwi.sourceforge.net.

Copyright (c) 2012/2015 psy <root@lordepsylon.net> - <epsylon@riseup.net>

anontwi is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation version 3 of the License.

anontwi is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along
with anontwi; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import optparse

class AnonTwiOptions(optparse.OptionParser):
    def __init__(self, *args):
        optparse.OptionParser.__init__(self, 
                           #description='FIGHT CENSORSHIP!! being more safe on social networking sites...',
                           prog='anontwi.py',
                           version='\nAnonTwi [1.0b] - 2012 - http://anontwi.sf.net -> by psy\n', 
                                       usage= '\n\n Info: check README file (examples and contact included).\n\n Syntax: ./anontwi [OPTIONS] [--tokens] [--gtk | --irc=] [Controller] [Miscellania] [Encryption]')

        #self.add_option("-v", "--verbose", action="store_true", dest="verbose", help="active verbose mode output results")
        group4 = optparse.OptionGroup(self, "API")
        group4.add_option("--tokens", action="store_true", dest="tokens", help="set your OAuth 'key' and 'secret' tokens (REQUIRED!) ")
        self.add_option_group(group4)

        group5 = optparse.OptionGroup(self, "Interfaces")
        group5.add_option("--gtk", action="store_true", dest="gtk", help="start GTK+ Window Interface (visual mode)")
        #group5.add_option("--web", action="store_true", dest="webserver", help="start WeGUI server on: 'http://localhost:8080'")
        group5.add_option("--irc", action="store", dest="ircbot", help="start an IRC slave bot, connected to Anontwi: 'anontwibot@irc.freenode.net:6667#anontwi'")
        self.add_option_group(group5)

        group3 = optparse.OptionGroup(self, "Controller")
        group3.add_option("-m", action="store", dest="tweet", help="send Tweet (ex: -m 'text')")
        group3.add_option("-r", action="store", dest="retweet", help="reTweet and existing message (ex: -r 'ID')")
        group3.add_option("-d", action="store", dest="dm", help="send Direct Message (ex: -m 'text' -d '@user')")
        #group3.add_option("-i", action="store", dest="image", help="send an IMAGE, using spoofed headers and fake metadata")
        group3.add_option("-f", action="store", dest="friend", help="create friendship with a user (ex: -f '@user')")
        group3.add_option("-u", action="store", dest="dfriend", help="destroy friendship with a user (ex: -u '@user')")
        group3.add_option("--reply", action="store", dest="reply", help="reply conversation (ex: -m '@user text' --reply 'ID')")
        group3.add_option("--fav", action="store", dest="favorite", help="create favorite (ex: --fav 'ID')")
        group3.add_option("--unfav", action="store", dest="unfavorite", help="destroy favorite (ex: --unfav 'ID')")
        group3.add_option("--block", action="store", dest="block", help="block a user on the network (ex: --block '@user')")
        group3.add_option("--unblock", action="store", dest="unblock", help="unblock a user on the network (ex: --unblock '@user')")
        group3.add_option("--rm-m", action="store", dest="rmtweet", help="remove Tweet (ex: --rm-m 'ID')")
        group3.add_option("--rm-d", action="store", dest="rmdm", help="remove Direct Message (ex: --rm-d 'ID')")
        group3.add_option("--suicide", action="store_true", dest="suicide", help="remove Tweets, DMs and try to close account")
        #group3.add_option("--mf", action="store", dest="massfriend", help="create massive friendships (ex: --fm 'list.txt')")
        #group3.add_option("--md", action="store", dest="massdfriend", help="destroy massive friendships (ex: --fm 'list.txt')")
        self.add_option_group(group3)

        group1 = optparse.OptionGroup(self, "Miscellania")
        group1.add_option("--proxy", action="store", dest="proxy", help="use proxy (tor: --proxy 'http://localhost:8118')")
        group1.add_option("--short", action="store", dest="shorturl", help="short an url (ex: --short 'url')")
        group1.add_option("--ts", action="store", dest="search", help="search a number of results (ex: --ts '#15m 10')")
        group1.add_option("--tu", action="store", dest="timeline", help="show a number of Tweets of a user (ex: --tu '@nick 5')")
        group1.add_option("--td", action="store", dest="timelinedm", help="show a number of DMs sent to you (ex: --td '5')")
        group1.add_option("--tf", action="store_true", dest="timelinef", help="show tweets of user's friends (ex: --tf '5')")
        group1.add_option("--tt", action="store_true", dest="topics", help="check global Trending Topics (ex: --tt)")
        group1.add_option("--me", action="store", dest="mentions", help="returns recent mentions about you (ex: --me '5')")
        group1.add_option("--save", action="store", dest="save", help="save tweets starting from the last (max: 3200)")
        group1.add_option("--tfav", action="store", dest="showfavs", help="returns favorites (ex: --tfav '@nick 10')")
        group1.add_option("--sfav", action="store", dest="savefavs", help="save favorites (ex: --sfav '@nick 10')")
        group1.add_option("--waves", action="store_true", dest="wave", help="split long message into waves (ex: -m 'text' --waves)")
        group1.add_option("--gps", action="store_true", dest="location", help="send fake geo-places (ex: --gps '(-43.5209),146.6015')")
        #group1.add_option("--via", action="store", dest="via", help="suggest 'via' value detailed on website")
        group1.add_option("--rgb", action="store_true", dest="rgb", help="use detailed colourful output results")
        self.add_option_group(group1)

        group2 = optparse.OptionGroup(self, "Encryption")
        group2.add_option("--gen", action="store_true", dest="genkey", help="generate PIN key for encrypting/decrypting messages")
        group2.add_option("--enc", action="store_true", dest="encaes", help="encrypt message using PIN key")
        group2.add_option("--dec", action="store", dest="decaes", help="message or URL to decrypt using PIN key")
        group2.add_option("--pin", action="store", dest="key", help="PIN key for encryption/decryption")
        self.add_option_group(group2)

    def get_options(self, user_args=None):
        (options, args) = self.parse_args(user_args)
        options.args = args
        if (not options.gtk and not options.encaes and not options.ircbot and not options.showfavs and not options.savefavs and not options.favorite and not options.unfavorite and not options.tokens and not options.tweet and not options.dm and not options.search and not options.friend and not options.dfriend and not options.retweet and not options.timelinef and not options.timeline and not options.timelinedm and not options.mentions and not options.genkey and not options.decaes and not options.save and not options.topics and not options.rmtweet and not options.rmdm and not options.suicide and not options.block and not options.unblock and not options.shorturl):
            print '='*75
            print  self.version
            print '='*75, "\n"
            print "           .   :   .            "
            print "       '.   .  :  .   .'        "
            print "    ._   '._.-'''-._.'   _.     #15M "
            print "      '-..'         '..-'       "
            print "   --._ /.==.     .==.\ _.--    #HackSol"
            print "       ;/_o__\   /_om__\;       "
            print "  -----|`     ) (     `|-----   #Spanishrevolution"
            print "      _: \_) (\_/) (_/ ;_       "
            print "   --'  \  '._.=._.'  /  '--    #Worldrevolution"
            print "     _.-''.  '._.'  .''-._      "
            print "    '    .''-.(_).-''.    '     "
            print "        '   '  :  '   '.        "
            print "           '   :   '            Share about R/evolution, not about you!"
            print "               '                "
            print '='*75
            print "\nFor HELP use -h or --help"
            print "---------------\n"
            print "GUI Interfaces:"
            print "    * GTK+ (Graphical): --gtk"
            #print "    * WebGUI: use --web"
            print "    * IRC-Bot: --irc='nick@server:port#channel'\n"
            print '='*55, "\n"
            return False
        return options

