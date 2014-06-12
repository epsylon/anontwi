#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""
$Id$

This file is part of the anontwi project, http://anontwi.sourceforge.net.

Copyright (c) 2012/2013 psy <root@lordepsylon.net> - <epsylon@riseup.net>

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

Anontwi: Anonymous Twitter Wave Interface
"""
import os, sys, traceback, random
import core.twitter
import core.oauth2 as oauth
import re, urllib2, socket
import core.socks
import HTMLParser
import traceback
from urllib2 import URLError
from core.encrypt import Cipher, generate_key
from core.twitter import TwitterError
from core.options import AnonTwiOptions
from core.shorter import ShortURLReservations
from core.webserver import AnonTwiWebserver
try:
    from urlparse import parse_qsl
except:
    from cgi import parse_qsl

# set to emit debug messages about errors (0 = off).
DEBUG = 1

class anontwi(object):
    """
    AnonTwi application class
    """
    def __init__(self):
        # init AnonTwi
        self.anontwi = []
        self.consumer_key = ''
        self.consumer_secret = ''
        self.access_token_key = ''
        self.access_token_secret = ''
        self.source_api = ''
        self.num_tweets = 1
        self.proxy = None
        self.isurl = 0
        self.search = None
        self.timeline = None
        self.timelinedm = None
        self.timelinef = None
        self.nickid = ''      
 
        self.save = None
        self.savefavs = None
        self.savefriends = None

        # setting random user-agent and blank referer for connections
        self.request_headers = {'User-Agent': self.set_random_user_agent(), 'Referer': ''}
        #faking geoposition
        self.geoposition = self.set_random_location()

        # take consumer and token: secrets and keys
        from config import APItokens
        for token in APItokens:
            self.consumer_key = token['consumer_key']
            self.consumer_secret = token['consumer_secret']

        # take source api
        from config import APIsources
        for source in APIsources:
            self.source_api = source['source_api']

        self.request_token_url = 'https://' + self.source_api + '/oauth/request_token'
        self.access_token_url = 'https://' + self.source_api + '/oauth/access_token'
        self.authorization_url = 'https://' + self.source_api + '/oauth/authorize'
        self.signin_url = 'https://' + self.source_api + '/oauth/authenticate'

    def set_options(self, options):
        """
        Set anontwi options
        """
        self.options = options

    def create_options(self, args=None):
        """
        Create the program options for OptionParser.
        """
        self.optionParser = AnonTwiOptions()
        self.options = self.optionParser.get_options(args)
        if not self.options:
            return False
        return self.options

    def try_running(self, func, error, args=None):
        """
        Try running a function and print some error if it fails and exists with
        a fatal error.
        """
        options = self.options
        args = args or []
        try:
            return func(*args)
        except Exception as e:
            if options.timeline or options.timelinedm or options.save:
                print("\n[Error] - Something wrong or this user doesn't exists!!. Aborting..."), "\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            if options.savef:
                print("\n[Error] - Something wrong!. Probably you haven't enought permissions to extract friendships. Aborting..."), "\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            if options.timelinef:
                print("\n[Error] - Something wrong fetching friend's timeline. Aborting..."), "\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            if options.tweet:
                print "\n[Warning] - Something wrong sending message:\n\n",e,"\n\nRemember that text must be less than or equal to 140 characters.\nConsider using --wave to split it on different blocks if has more than 1 wave. Aborting... \n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            if options.rmtweet:
                print("\n[Error] - Something wrong removing message. Check that you are using a correct ID. Aborting..."), "\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            if options.rmdm:
                print("\n[Error] - Something wrong removing direct message. Check that you are using a correct ID. Aborting..."), "\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            if options.retweet:
                print("\n[Error] - Something wrong with tweet's ID!!. Aborting..."), "\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            if options.friend:
                print"\n[Error] - Something wrong creating your friendship. Aborting...", "\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            if options.massfriend:
                print "\n[Error] - Something wrong creating your list of friendships. Aborting...", "\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            if options.dfriend:
                print "\n[Error] - Something wrong destroying your friendship. Aborting...", "\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            if options.massdfriend:
                print "\n[Error] - Something wrong destroying your list of friendships. Aborting...", "\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            if options.mentions:
                print("\n[Error] - Something wrong fetching your mentions. Aborting..."), "\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            if options.block:
                print("\n[Error] - Something wrong blocking user"), options.block,"\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            if options.unblock:
                print("\n[Error] - Something wrong unblocking user"), options.unblock,"\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            else:
                print(error, "error")
                if DEBUG:
                    traceback.print_exc()

    def get_messages(self):
        """
        Get messages to send (Tweet, Image or DM)
        """
        messages = []
        options = self.options
        p = self.optionParser

        if options.tweet:
            if options.dm:
                print('='*75)
                print(str(p.version))
                print('='*75)
                print("Starting to send your DM (direct message)... :)")
                print('='*75)
            elif options.mdm:
                print('='*75)
                print(str(p.version))
                print('='*75)
                print("Starting to send a massively DM (direct message) to friends... :)")
                print('='*75)
            elif options.ldm:
                print('='*75)
                print(str(p.version))
                print('='*95)
                print("Starting to send a massively DM (direct message) to a list of friends extracted from file... :)")
                print('='*95)
            elif options.wave:
                print('='*75)
                print(str(p.version))
                print('='*75)
                print("Starting to send your waves... :)")
                print('='*75)
            else:
                print('='*75)
                print(str(p.version))
                print('='*75)
                print("Starting to send your tweet... :)")
                print('='*75)
            messages = [options.tweet]

        #if options.image:
        #    print('='*75)
        #    print(str(p.version))
        #    print('='*75)
        #    print("Starting to send your image... :)")
        #    print('='*75)
        #    messages = [options.image]

        #if options.friend and not (options.tweet or options.image):
        if options.friend and not options.tweet:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print "Creating friendship with:", options.friend, " :)"
            print('='*75)
        elif options.friend:
            print "Creating friendship:", options.friend
            print('='*75)

        if options.massfriend and not options.tweet:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print "Creating friendships from a list of users, extracted from a file :)"
            print('='*75)
        elif options.massfriend:
            print "Creating friendships from a list of users, extracted from a file :)"
            print('='*75)

        #if options.dfriend and not (options.tweet or options.image):
        if options.dfriend and not options.tweet:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print "Destroying friendship with:", options.dfriend, " :)"
            print('='*75)
        elif options.dfriend:
            print "Destroying friendship:", options.dfriend
            print('='*75)

        if options.massdfriend and not options.tweet:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print "Destroying friendships from a list of users, extracted from a file :)"
            print('='*75)
        elif options.massdfriend:
            print "Destroying friendships from a list of users, extracted from a file :)"
            print('='*75)

        if options.decaes:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print "Decrypting message... :)"
            print('='*75)

        if options.block:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print "Blocking user:", options.block, " :)"
            print('='*75)        

        if options.unblock:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print "Unblocking user:", options.unblock, " :)"
            print('='*75)

        if options.favorite:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print "Creating favorite... :)"
            print('='*75)

        if options.unfavorite:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print "Destroying favorite... :)"
            print('='*75)

        return messages

    def get_tweetids(self):
        """
        Get messages to send (Tweet, Image or DM)
        """
        tweetids = []
        options = self.options
        p = self.optionParser

        if options.retweet:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print("Starting to reTweet... :)")
            print('='*75)

        elif options.rmtweet:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print("Starting to remove tweet... :)")
            print('='*75)

        elif options.rmdm:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print("Starting to remove direct message... :)") 
            print('='*75)

        return tweetids

    def request_url(self,
                    consumer_key = '',
                    consumer_secret = '',
                    source_api = '',
                    gtk = False):
        """
        Request Access Tokens
        """
        options = self.options
        proxy = options.proxy
        eprint = sys.stderr.write
        proxy_info = None
        if proxy is not None:
            try:
                match = re.finditer(":",proxy)
                positionlist = []
                for m in match:
                    positionlist.append(m.start())
            
                pos1 = positionlist[0]
                pos2 = positionlist[1]
                host = proxy[pos1+3:pos2]
                slen = len(proxy)
                port = proxy[pos2+1:slen]
                proxy_info = core.socks.setdefaultproxy(core.socks.PROXY_TYPE_HTTP, host, int(port))
                socket.socket = core.socks.socksocket

            except IndexError:
                eprint ("\n[Error] - Proxy is malformed. For example, to launch with TOR use: --proxy 'http://127.0.0.1:8118'")
                eprint ("\nAborting...\n")
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            except ValueError:
                eprint ("[Error] - Proxy is malformed. For example, to launch with TOR use: --proxy 'http://127.0.0.1:8118'")
                eprint ("\nAborting...\n")
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
        
        if gtk:
            self.consumer_key = consumer_key
            self.consumer_secret = consumer_secret
            self.source_api = source_api
        signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
        oauth_consumer             = oauth.Consumer(key = self.consumer_key, secret = self.consumer_secret)
        if self.source_api == "identi.ca/api":
            self.request_token_url = "https://identi.ca/api/oauth/request_token?oauth_callback=http://anontwi.sf.net"
        oauth_client               = oauth.Client(oauth_consumer, proxy_info = proxy_info)
        eprint ('\n')
        if options.rgb:
            eprint ('Requesting \033[1;36mtemporal\033[1;m tokens...')
        else:
            eprint ('Requesting temporal tokens...')
        eprint ('\n\n')

        try:
            print "GET :"+ self.request_token_url
            resp, content = oauth_client.request(self.request_token_url, 'GET', headers=self.request_headers)
        except:
            if options.rgb:
                eprint ("\033[1;31mConnection refused!\033[1;m\n\n")
            else:
                eprint ("Connection refused!\n\n")
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)

        if resp['status'] != '200':
            eprint ('\n')
            eprint ('Invalid response!!. http code is: %s' % resp['status']+ "\n")
            eprint ('----------------'+ "\n")
            if options.rgb:
                eprint ('Review \033[1;31mconfig.py\033[1;m file to see if your API consumer and token values (secret and key) are correct')
            else:
                eprint ('Review config.py file to see if your API consumer and token values (secret and key) are correct' + "\n")
            eprint ('If you are using a proxy, check that is working correctly'+ "\n")
            eprint ('\n')
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        else:
            request_token = dict(parse_qsl(content))
        eprint ('Please visit this page and retrieve the pincode to be used')
        eprint ('\n')
        eprint ('in the next step to obtaining an Authentication Token:')
        
        eprint ('\n\n')
        if not gtk:
            if options.rgb:
                eprint ('\033[1;34m%s?oauth_token=%s\033[1;m' % (self.authorization_url, request_token['oauth_token']))
            else:
                print request_token['oauth_token']
                eprint ('%s?oauth_token=%s' % (self.authorization_url, request_token['oauth_token']))
            return [request_token['oauth_token'], 
                    request_token['oauth_token_secret']] 
        else:
            return [self.authorization_url + '?oauth_token=' + request_token['oauth_token'], 
                   request_token['oauth_token'],
                   request_token['oauth_token_secret']] 
        
    def insert_pincode(self,
                       _oauth_token,
                       _oauth_token_secret,
                       _consumer_key,
                       _consumer_secret,
                       source_api = '',
                       _pin = "",
                       gtk = False):
        
        consumer_key = _consumer_key
        consumer_secret = _consumer_secret
        oauth_token = _oauth_token
        oauth_token_secret = _oauth_token_secret
       
        #proxy setup - copy from request_url
        options = self.options
        proxy = options.proxy
        eprint = sys.stderr.write
        proxy_info = None
        if proxy is not None:
            try:
                match = re.finditer(":",proxy)
                positionlist = []
                for m in match:
                    positionlist.append(m.start())
            
                pos1 = positionlist[0]
                pos2 = positionlist[1]
                host = proxy[pos1+3:pos2]
                slen = len(proxy)
                port = proxy[pos2+1:slen]
                proxy_info = core.socks.setdefaultproxy(core.socks.PROXY_TYPE_HTTP, host, int(port))
                socket.socket = core.socks.socksocket

            except IndexError:
                eprint ("\n[Error] - Proxy is malformed. For example, to launch with TOR use: --proxy 'http://127.0.0.1:8118'")
                eprint ("\nAborting...\n")
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            except ValueError:
                eprint ("[Error] - Proxy is malformed. For example, to launch with TOR use: --proxy 'http://127.0.0.1:8118'")
                eprint ("\nAborting...\n")
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)

        eprint ("\n\n") 
        if self.source_api == "api.twitter.com":
            if gtk:
                pincode = _pin
            else:
                eprint ("Pincode? ") 
                pincode = raw_input ()
            token = oauth.Token(oauth_token, oauth_token_secret)
            token.set_verifier(pincode)
        else:
            if gtk:
                pincode = _pin
            else:
                eprint ("Pincode? ")
                pincode = raw_input ()
            token = oauth.Token(oauth_token, oauth_token_secret)
            token.set_verifier(pincode)

        eprint ('\n')
        eprint ('Generating and signing request for an access token...')
        eprint ('\n\n')
        
        oauth_consumer = oauth.Consumer(key = self.consumer_key, secret = self.consumer_secret)
        oauth_client = oauth.Client(oauth_consumer, token, proxy_info = proxy_info)
        try:
            resp, content = oauth_client.request(self.access_token_url, method='POST', body='oauth_verifier=%s' % pincode, headers=self.request_headers)
        except:
            if options.rgb:
                eprint ("\033[1;31mConnection refused!\033[1;m\n\n")
            else:
                eprint ("Connection refused!\n\n")
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)

        access_token  = dict(parse_qsl(content))

        if resp['status'] != '200':
            eprint ('The request for Tokens did not succeed: %s' % resp['status'])
            eprint ('\n\n')
        else:
            if options.rgb:
                eprint ('Your Access Token key: \033[1;31m%s\033[1;m' % access_token['oauth_token'])
                eprint ('\n')
                eprint ('          Access Token secret: \033[1;31m%s\033[1;m' % access_token['oauth_token_secret'])
                eprint ('\n')
            else:
                eprint ('Your Access Token key: %s' % access_token['oauth_token'])
                eprint ('\n')
                eprint ('          Access Token secret: %s' % access_token['oauth_token_secret'])
                eprint ('\n')

            access_token_key = access_token['oauth_token']
            access_token_secret = access_token['oauth_token_secret']
 
            eprint ('\n')
            eprint ('Trying to export tokens like environment variables...')
            eprint ('\n\n')
            eprint ('          + Unix/MacOS: ')
            eprint ('\n')
            eprint ('                 - If you launched: "eval $(python anontwi --tokens)" you can START to use it!!')
            eprint ('\n')
            eprint ('                 - If you launched: "python anontwi --tokens" COPY next EXPORT lines to your shell:')
            eprint ('\n\n')
            eprint ('-------------------------------------------------------------------------')
            eprint ('\n')
            if options.rgb:
                print(' \033[1;31mexport ANONTWI_TOKEN_KEY=' + access_token_key + "\033[1;m")
                print(' \033[1;31mexport ANONTWI_TOKEN_SECRET=' + access_token_secret + "\033[1;m")
            else:
                print(' export ANONTWI_TOKEN_KEY=' + access_token_key)
                print(' export ANONTWI_TOKEN_SECRET=' + access_token_secret)
            eprint ('-------------------------------------------------------------------------')
            eprint ('\n\n')
            eprint ('          + Windows: ')
            eprint ('\n')
            eprint ('                 - COPY next EXPORT lines to your shell:')
            eprint ('\n\n')
            eprint ('-------------------------------------------------------------------------')
            eprint ('\n')
            if options.rgb:
                print(' \033[1;31mSET ANONTWI_TOKEN_KEY=' + access_token_key + "\033[1;m")
                print(' \033[1;31mSET ANONTWI_TOKEN_SECRET=' + access_token_secret + "\033[1;m")
            else:
                print(' SET ANONTWI_TOKEN_KEY=' + access_token_key)
                print(' SET ANONTWI_TOKEN_SECRET=' + access_token_secret)
            eprint ('-------------------------------------------------------------------------')
            eprint ('\n\n')
            eprint ('Is you save these tokens like environment variables on your system')
            eprint ('\n')
            eprint ('You can use the tool directly without entering them every time')
            eprint ('\n')
            eprint ('Remember that you can request new temporal tokens again if is needed')
            eprint ('\n')
            if options.rgb:
                eprint ('So at the end, time to \033[1;33menjoy\033[1;m #AnonTwi ;)')
            else:
                eprint ('So at the end, time to enjoy #AnonTwi ;)')
            eprint ('\n\n')

    def get_env_tokens(self):
        """
        Get temporal access token key and secret from env, or go to command argvs
        """
        options = self.options
        try:
            self.access_token_key = os.environ['ANONTWI_TOKEN_KEY']
            self.access_token_secret = os.environ['ANONTWI_TOKEN_SECRET']
        except:
            (self.access_token_key, self.access_token_secret) = self.get_access_token(options)

    def unicoding(self, message):
        message = message.decode("utf-8")
        return message

    def send_dm(self, message, dm):
        """
        Send Direct Message (DM)
        """
        options = self.options

        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")

        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
        try:
            status = api.PostDirectMessage(dm, message)
        except URLError as u:
            print "[Error] - ",u.reason.strerror, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        except TwitterError as t:
            try:
                print "[Error] - ",t, "\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            except Exception:
                print "Oops! It seems that you've said that\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)

    def send_mdm(self, message, mdm):
        """
        Send a Direct Message (DM) massively to all your friends, or to a list of friends extracted from a file
        """
        # step 1) list friends ids: https://dev.twitter.com/docs/api/1/get/friends/ids
        # ex: https://api.twitter.com/1/friends/ids.json?cursor=-1&screen_name=anontwinews
        #
        # step 2) get users lookup: https://dev.twitter.com/docs/api/1/get/users/lookup
        # ex: https://api.twitter.com/1/users/lookup.json?screen_name=anontwinews,lord_epsylon&include_entities=true 

        options = self.options

        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)

        # get following friends from a file, print a list in output results and send a direct message to all of them
        if options.ldm:
            try:
                friends = lines = [line.strip() for line in open(options.ldm)]
		#friends = tuple(open(options.ldm, 'r'))
                count = len(friends)
                #print friends
                if friends == []:
                    print "You haven't a correct list of friends on that file. Try to put user screen names sepparated line by line.\n"
                try:
                    for update in friends:
                        print update
                        api.PostDirectMessage(update, message)
                except TwitterError as t:
                    print update.name + " is not following you... DM to him/her has been aborted."
            except URLError as u:
                print "\n[Error] - ",u.reason.strerror, "\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            except TwitterError as t:
                print "\n[Error] - ",t, "\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            except Exception:
                print "\nOops! Error sending a message to all your friends\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)

        # get following friends directly from user profile, print a list in output results and send a direct message to all of them
        elif options.mdm:
            try:
                friends = api.GetFriends()
                count = len(friends)
                if friends == []:
                    print "You haven't friends, yet.\n"
                for update in friends:
                    try:
                        print update.name
                        api.PostDirectMessage(update.screen_name, message)
                    except TwitterError as t:
                        print update.name + " is not following you... DM to him/her has been aborted."
            except URLError as u:
                print "[Error] - ",u.reason.strerror, "\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            except TwitterError as t:
                try:
                    print "[Error] - ",t, "\n"
                    if options.gtk or options.webserver:
                        return
                    else:
                        sys.exit(2)
                except Exception:
                    print "\nOops! Error sending a message to all your friends\n"
                    if options.gtk or options.webserver:
                        return
                    else:
                        sys.exit(2)

    def send_tweet(self, message, reply, lat, long):
        """
        Send messages
        """
        options = self.options
        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
        try:
            for m in message:
                message = self.unicoding(m)
            status = api.PostUpdate(status=message, in_reply_to_status_id=reply, latitude=lat, longitude=long)
        except URLError as u:
            print "\n[Error] - ",u.reason.strerror, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)

    def send_wave(self, message, reply, lat, long):
        """
        Send waves of messages
        """
        options = self.options

        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
        try:
            for m in message:
                message = self.unicoding(m)
                status = api.PostUpdates(status=message, in_reply_to_status_id=reply, latitude=lat, longitude=long)
#                status = self.send_tweet(message, reply, lat, long)
        except URLError as u:
            print "\n[Error] - ",u.reason.strerror, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        except TwitterError as t:
            print "\n[Error] - ",t, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)

    def remove_tweet(self):
        """
        Remove tweet by id
        """
        options = self.options

        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
        try:
            status = api.DestroyStatus(options.rmtweet)
        except URLError as u:
            print "\n[Error] - ",u.reason.strerror, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        except TwitterError as t:
            print "\n[Error] - ",t, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)

    def remove_dm(self):
        """ 
        Remove direct message by id
        """ 
        options = self.options

        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
        try:
            status = api.DestroyDirectMessage(options.rmdm)
        except URLError as u:
            print "\n[Error] - ",u.reason.strerror, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        except TwitterError as t:
            print "\n[Error] - ",t, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)

    def send_retweet(self):
        """
        Send retweets of users by id
        """ 
        options = self.options

        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
        try:
            id = int(options.retweet)
            status = api.PostRetweet(id)
        except URLError as u:
            print "\n[Error] - ",u.reason.strerror, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        except TwitterError as t:
            print "\n[Error] - ",t, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)

#    def send_image(self, message, image):
#        """
#        Send image on Twitpic
#        """
#        options.self.options
#        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
#        api = twitpic.TwitPicOAuthClient(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
#        try: 
#            status = api.create("upload", message, image)
#            print(status) 
#        except URLError as u:
#            print "[Error] - ",u.reason.strerror, "\n"
#            sys.exit(2)
#        except TwitterError as t:
#            print "[Error] - ",t, "\n"
#            sys.exit(2)

    def search_messages(self):
        """
        Search messages
        """
        options = self.options
        search = options.search
        try:
            num = options.args[0]
        except:
            num = 10
        words = options.search.split()
        if len(words) is 2:
            search = words[0]
            num = words[1]
        else:
            search = options.search
        try:
            if int(num) <= 0:
                print "[Error] - Number of ocurrences must be an integer greater than zero. (ex: --ts 'AnonTwi 5')\n" 
                print "Aborting ....\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
        except ValueError:
            print "[Error] - Number of ocurrences must be an integer greater than zero. (ex: --ts 'AnonTwi 3')\n"
            print "Aborting ....\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)

        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")

        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)

        status = api.GetSearch(term=search, per_page=num)
        return status

    def search_topics(self):
        """
        Search trending topics 
        """ 
        options = self.options
        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
	status = api.GetTrendsCurrent()
        return status

    def save_timeline(self):
        """
        Save a number of tweets of a user timeline
        """
        options = self.options
        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
	count = 15
        user = ""
	words = options.save.split()
        if len(words) is 2:
            user = words[0]
            count = words[1]
        else:
            word = options.save
            try:
		count = int(word)
	    except:
		user = word
        try:
        	status = api.GetUserTimeline(user, count=count, include_rts=1)
        	return status, count
	except URLError as u:
            print "\n[Error] - ",u.reason.strerror, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        except TwitterError as t:
            print "\n[Error] - ",t, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)   

    def show_timeline(self):
        """
        Show a number of tweets of a user timeline
        """
        options = self.options
        try:
            num = options.args[0]
        except:
            num = 10

        words = options.timeline.split()

        if len(words) is 2:
            user = words[0]
            num = words[1]
        else:
            user = options.timeline
        try:
            if int(num) <= 0:
                print "[Error] - Number of ocurrences must be an integer greater than zero. (ex: --tu '@user 5')\n" 
                print "Aborting ....\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
        except ValueError:
            print "[Error] - Number of ocurrences must be an integer greater than zero. (ex: --tu '@user 5')\n"
            print "Aborting ....\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)

        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")

        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
        try:
            status = api.GetUserTimeline(user, count=num, include_rts=1)
        except TwitterError as t:
            print "[Error] - ",t,"\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        return status

    def show_timelinedm(self):
        """
        Show a number of DMs
        """
        options = self.options
        try:
            dm = options.timelinedm
            try:
                if int(dm) <= 0:
                    print "[Error] - Number of ocurrences must be an integer greater than zero. (ex: --td '5')\n"
                    print "Aborting ....\n"
                    if options.gtk or options.webserver:
                        return
                    else:
                        sys.exit(2)
            except Exception as e:
                print "[Error] - Number of ocurrences must be an integer greater than zero. (ex: --td '3')\n"
                print "Aborting ....\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
        except Exception:
             dm = 10

        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")

        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
        try:
            status = api.GetDirectMessages()
        except TwitterError as t:
            print "[Error] - ",t,"\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        return status, dm

    def show_timeline_friends(self):
        """ 
        Show a number of tweets of your friends
        """     
        options = self.options
        try:
            num = options.timelinef
        except:
            num = 10
        try:
            if int(num) <= 0:
                print "[Error] - Number of ocurrences must be an integer greater than zero. (ex: --tf '5')\n"
                print "Aborting ....\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
        except ValueError:
            print "[Error] - Number of ocurrences must be an integer greater than zero. (ex: --tf '3')\n"
            print "Aborting ....\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)

        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")         
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)           
        try:
            status = api.GetFriendsTimeline(count=num, include_rts=1)
        except TwitterError as t:
            traceback.print_exc()
            print "[Error] - ",t,"\n"
            if options.gtk or options.webserver:
                return
            else:
                print "[Error] - ",t,"\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
        return status, num


    def friendlist(self):
        """
        Get your friends
        """
        options = self.options
        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)           
        try:
            status=api.GetFriends()
        except TwitterError as t:
            traceback.print_exc()
            print "[Error] - ",t,"\n"
            if options.gtk or options.webserver:
                return
            else:
                print "[Error] - ",t,"\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)

        return status

    def show_mentions(self):
        """
        Show a number of mentions about you
        """
        options = self.options
        try:
            mention = options.mentions
            try:
                if int(mention) <= 0:
                    print "[Error] - Number of ocurrences must be an integer greater than zero. (ex: --me '5')\n"
                    print "Aborting ....\n"
                    if options.gtk or options.webserver:
                        return
                    else:
                        sys.exit(2)
            except Exception as e:
                print "[Error] - Number of ocurrences must be an integer greater than zero. (ex: --me '3')\n"
                print "Aborting ....\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
        except Exception:
             mention = 10

        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")

        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
        try:
            status = api.GetMentions()
        except TwitterError as t:
            print "[Error] - ",t,"\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        return status, mention

    def set_friend(self):
        """
        Create a friendship with a user
        """
        options = self.options
        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)

        if options.friend:
            status = api.CreateFriendship(options.friend)
        elif options.massfriend:
            try:
                friends = lines = [line.strip() for line in open(options.massfriend)]
                count = len(friends)
                if friends == []:
                    print "You haven't a correct list of friends on the file. Try to put user screen names sepparated line by line.\n"
                for update in friends:
                    print update
                    status = api.CreateFriendship(update)
            except URLError as u:
                print "\n[Error] - ",u.reason.strerror, "\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            except TwitterError as t:
                try:
                    print "\n[Error] - ",t, "\n"
                    if options.gtk or options.webserver:
                        return
                    else:
                        sys.exit(2)
                except Exception:
                    print "\nOops! Error creating a list of friends from file\n"
                    if options.gtk or options.webserver:
                        return
                    else:
                        sys.exit(2)
        return status

    def remove_friend(self):
        """ 
        Destroy a friendship with a user, or a list of users extracted from file
        """ 
        options = self.options
        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ") 
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)

        if options.dfriend:
            status = api.DestroyFriendship(options.dfriend)
        elif options.massdfriend:
            try:
                friends = lines = [line.strip() for line in open(options.massdfriend)]
                count = len(friends)
                if friends == []:
                    print "You haven't a correct list of friends on that file. Try to put user screen names sepparated line by line.\n"
                for update in friends:
                    print update
                    status = api.DestroyFriendship(update)
            except URLError as u:
                print "\n[Error] - ",u.reason.strerror, "\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            except TwitterError as t:
                try:
                    print "\n[Error] - ",t, "\n"
                    if options.gtk or options.webserver:
                        return
                    else:
                        sys.exit(2)
                except Exception:
                    print "\nOops! Error destroying a list of friends from file\n"
                    if options.gtk or options.webserver:
                        return
                    else:
                        sys.exit(2)
        return status

    def create_block(self):
        """
        Create block with a user
        """
        options = self.options
        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")

        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
        user = api.CreateBlock(screen_name=options.block)
        if user.id is None:
            print("\n[Error] - Something wrong or this user doesn't exists!!. Aborting..."), "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)

    def destroy_block(self):
        """
        Destroy blockwith a user
        """
        options = self.options
        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")

        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
        user = api.DestroyBlock(screen_name=options.unblock)
        if user.id is None:
            print("\n[Error] - Something wrong or this user doesn't exists!!. Aborting..."), "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)

    def get_access_token(self, options):
        """
        Get access token key and secret from argvs
        """
        try:
            access_token_key = options.args[0]
        except:
            if options.rgb:
                print "[Error] - you must provide a valid access '\033[1;31mtoken key\033[1;m'\n"
                print "[Info]  - to use tool, entering tokens every time: ./anontwi [OPTIONS] '\033[1;31mtoken key\033[1;m' 'token secret'"
                print "[Info]  - to use tool, \033[1;32mWITHOUT\033[1;m entering tokens every time: \033[1;32m./anontwi --tokens\033[1;m"
                print "\nAborting...\n"
            else:
                print "[Error] - you must provide a valid access 'token key'\n"
                print "[Info]  - use tool, entering tokens every time: ./anontwi [OPTIONS] 'token key' 'token secret'"
                print "[Info]  - use tool, WITHOUT entering tokens every time: ./anontwi --tokens"
                print "\nAborting...\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        try:
            access_token_secret = options.args[1]
        except:
            if options.rgb:
                print "[Error] - you must provide a valid access '\033[1;31mtoken secret\033[1;m'\n"
                print "[Info]  - use tool entering tokens every time: ./anontwi [OPTIONS] 'token key' '\033[1;31mtoken secret\033[1;m'"
                print "[Info]  - use tool \033[1;32mWITHOUT\033[1;m entering tokens every time: \033[1;32m./anontwi --tokens\033[1;m"
                print "\nAborting...\n"
            else:
                print "[Error] - you must provide a valid access 'token secret'\n"
                print "[Info]  - use tool entering tokens every time: ./anontwi [OPTIONS] 'token key' 'token secret'"
                print "[Info]  - use tool WITHOUT entering tokens every time: ./anontwi --tokens"
                print "\nAborting...\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)

        return (access_token_key, access_token_secret)
    
    def get_location(self):
        """
        Get latitude and longitude parameters
        """
        options = self.options
        try:
            geo = options.args[0]
            try:
                words = geo.split(',')
                lat = words[0]
                # remove parser branches and blank spaces on input parameters
                lat = lat.replace("(", "")
                lat = lat.replace(")", "")
                lat = lat.replace(" ", "")
                long = words[1]
                long = long.replace("(", "")
                long = long.replace(")", "")
                long = long.replace(" ", "")
            except Exception as e:
                print "[Error] - You must provide correct latitude and longitude (ex: --gps '(-43.5209),146.6015')"
                print "          If you dont put any (--gps), coordenates will be random :)\n"
                print "[Error] - Sending message process has being aborted!\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
        except Exception:
            words = self.geoposition.split(',')
            lat = words[0]
            long = words[1]
        return (lat, long)

    def set_random_location(self):
        # setting random fake geoposition
        self.geo = []
        self.geo.append('0.000000,0.000000')       # pangea starts ;-)
        self.geo.append('33.449777,-40.935974')    
        self.geo.append('82.729312,-51.188507')    
        self.geo.append('14.826575,-24.697266')    
        self.geo.append('(-43.592825),146.374855') 
        self.geo.append('54.334036,-4.438477')     
        self.geo.append('19.277270,-81.276855')    
        self.geo.append('(-11.833246),96.824212')  
        self.geo.append('38.897738,-77.03632')     
        self.geo.append('38.870601,-77.055727')    
        self.geo.append('41.902916,12.453389')     
        self.geo.append('37.826664,-122.423012')   
        self.geo.append('40.444555,-3.73592')      
        self.geo.append('62.393096,-145.150442')   
        self.geo.append('34.0231,84.3617')         
        self.geo.append('19.573938,-4.463196')     
        self.geo.append('(-22.917923),23.640747')  
        self.geo.append('28.455556,-80.527778')    
        self.geo.append('39.7025,44.3')            
        self.geo.append('30.958769,88.831787')     
        self.geo.append('32.676138,-117.157763')   
        self.geo.append('51.9898,5.8176')          
        self.geo.append('43.264335,-2.945844')      
        self.geo.append('40.711841,-74.012986')    
        self.geo.append('51.563412,-68.997803')    
        self.geo.append('35.168195,-106.848335')   
        self.geo.append('44.072363,3.522747')      
        self.geo.append('37.749510,140.468180')   
        self.geo.append('16.720385,38.305662')    
        self.geo.append('13.239945,13.608397')     
        self.geo.append('(-28.22697),-56.967775')
        self.geo.append('8.341953,39.06372')       
        self.geo.append('25.740529,49.764404')  
        self.geo.append('31.868957,35.211325')     
        self.geo.append('32.097918,34.810345')     
        self.geo.append('(-44.496505),-69.000549') 
        self.geo.append('6.256122,-75.630636')
        self.geo.append('29.017748,-112.393799') 
        self.geo.append('41.808781,-72.649244')
        self.geo.append('67.187,-101.341553') 
        self.geo.append('23.775291,10.193481') 
        self.geo.append('28.623104,82.999878')  
        self.geo.append('44.801327,100.694733')
        self.geo.append('55.699743,37.611777')
        self.geo.append('42.382894,77.28447')
        self.geo.append('57.280527,-4.482622')
        self.geo.append('27.985648,86.923649')
        self.geo.append('39.913791,116.392191')
        self.geo.append('41.403737,2.173555')
        self.geo.append('37.971618,23.726893')
        self.geo.append('29.975939,31.130404')
        self.geo.append('51.176599,-1.826048')
        self.geo.append('(-14.725285),-75.151978')
        self.geo.append('48.865724,2.319070')
        self.geo.append('48.874362,2.294501')
        self.geo.append('48.861022222222,2.335825')
        self.geo.append('39.466581,-0.376314')
        self.geo.append('51.39294721838891,30.097381701104')
        self.geo.append('55.754186,37.618475')
        self.geo.append('34.39708129807727,132.4436864109491')
        self.geo.append('32.73333333333333,129.8666666666667')
        self.geo.append('33.304331,44.408380')
        self.geo.append('(-3.109128),37.366866')
        self.geo.append('51.097251,1.156139')
        self.geo.append('48.852870,2.349465')
        self.geo.append('(-34.603640),-58.381552')
        self.geo.append('41.878593,-87.635853')
        self.geo.append('51.500462,-0.177262')
        self.geo.append('41.902277,12.455245')
        self.geo.append('55.751982,37.616007')
        self.geo.append('27.17461,78.0447')
        self.geo.append('(-25.413609),-54.586945')
        self.geo.append('(-27.493629),-56.730309')
        self.geo.append('(-73.03408598119988),-50.47799897195181')
        self.geo.append('20.989825,-11.252160')
        self.geo.append('(-32.6563109388),-70.0027805163')
        self.geo.append('(-27.11266944),-109.3469139')
        self.geo.append('(-0.329588),-90.681152')
        return random.choice(self.geo).strip()
        
    def set_random_user_agent(self):
        self.agents = []
        self.agents.append('Mozilla/5.0 (iPhone; U; CPU iOS 2_0 like Mac OS X; en-us)')
        self.agents.append('Mozilla/5.0 (Linux; U; Android 0.5; en-us)')
        self.agents.append('Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)')
        self.agents.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
        self.agents.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13')
        self.agents.append('Opera/9.25 (Windows NT 6.0; U; en)')
        self.agents.append('Mozilla/2.02E (Win95; U)')
        self.agents.append('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')
        self.agents.append('Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)')
        self.agents.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)')
        self.agents.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729) (Prevx 3.0.5)')
        self.agents.append('(Privoxy/1.0)')
        self.agents.append('CERN-LineMode/2.15')
        self.agents.append('cg-eye interactive')
        self.agents.append('China Local Browser 2.6')
        self.agents.append('ClariaBot/1.0')
        self.agents.append('Comos/0.9_(robot@xyleme.com)')
        self.agents.append('Crawler@alexa.com')
        self.agents.append('DonutP; Windows98SE')
        self.agents.append('Dr.Web (R) online scanner: http://online.drweb.com/')
        self.agents.append('Dragonfly File Reader')
        self.agents.append('Eurobot/1.0 (http://www.ayell.eu)')
        self.agents.append('FARK.com link verifier')
        self.agents.append('FavIconizer')
        self.agents.append('Feliz - Mixcat Crawler (+http://mixcat.com)')
        self.agents.append('TwitterBot (http://www.twitter.com)')

        return random.choice(self.agents).strip() 
            
    #def set_via(self):
    #    """
    #    Set 'source' value to be displayed on the website
    #    """
    #    options = self.options
    #    tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")

    #    api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
    #    status = api.SetSource(options.via)

    def encrypt(self, messages, key):
        """
        Encrypt messages
        """
        options = self.options
        if key is None:
            if options.rgb:
                print"\n\033[1;31m[Error] - PIN/Key option (--pin) is required!\033[1;m"
            else:
                print"\n[Error] - PIN/Key option (--pin) is required!"
            print "\nAborting...\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        else:
            m_encrypt = set()
            for m in messages:
                e = Cipher(key, m)
                m_enc = e.encrypt()
                m_encrypt.add(m_enc)
            return m_encrypt

    def decrypt(self, messages, key):
        """
        Decrypt messages
        """
        options = self.options
        if key is None:
            if options.rgb:
                print "\n\033[1;31m[Error] - PIN/Key option (--pin) is required!\033[1;m"
            else:
                print "\n[Error] - PIN/Key option (--pin) is required!"
            print "\nAborting...\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        else:
            options = self.options
            # url
            if "https://" in options.decaes:
                match = re.finditer("/", options.decaes)
                positionlist = []
                for m in match:
                    positionlist.append(m.start())
                slen = len(options.decaes)
                try:
                    pos = positionlist[4]
                    id = options.decaes[pos+1:slen]
                
                    tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
                    api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
                    status = api.GetStatus(id)
                    ciphertext = status.text
                except IndexError:
                    print "\n[Error] - URL is not valid"
                    print "\nAborting...\n"
                    if options.gtk or options.webserver:
                        return
                    else:
                        sys.exit(2)
                except TwitterError as t:
                    print "\n[Error] - ",t
                    print "\nAborting...\n"
                    if options.gtk or options.webserver:
                        return
                    else:
                        sys.exit(2)
            # raw_message
            else:
                ciphertext = options.decaes
         
            key = options.key
            d = Cipher(key, ciphertext)
            plaintext = d.decrypt()
            if plaintext is None:
                print "\n[Error] - PIN key is incorrect or message is corrupted"
                print "\nAborting...\n"
                print "key " + key
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            print "\nPlainText:", plaintext, "\n"
            return plaintext 

    def suicide(self):
        """
        Remove all possible data and try to close account
        """
        import time
        options = self.options       
        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
 
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)

        pag  = 1
        status  = []

        print "Unfollowing:"
        print "----------------\n"

        #destroy friendship
        try:
            friends = api.GetFriends()
            count = len(friends)
            num = 1
            if friends == []:
                print "No results found.\n"
            for update in friends:
                print "Number of message: [", num, "/", count, "]"
                num = num + 1
                print "ID:", update.id
                print update.screen_name
                status = api.DestroyFriendship(update.id)
                print "\nREMOVED!"
                print "-----------"
                pag  = pag + 1
            
        except TwitterError as t:
            print "[Info] Sleeping for 10 minutes. This is because the API is trying to block you." 
            print "       Stop this (ctrl+C) and change your IP, if you dont want to wait. ZZzzzzZZzz...\n"
            time.sleep(600) # Sleep for 10 minutes and try again.

        print "Removing Direct Messages:"
        print "--------------------------\n"

        #destroy direct messages
        try:
            status = api.GetDirectMessages(page=pag)
            count = len(status)
            num = 1
            if status == []:
                print "No results found.\n"
            for update in status:
                print "Number of message: [", num, "/", count, "]"
                num = num + 1
                print "ID:", update.id
                print update.text
                print "\nREMOVED!"
                api.DestroyDirectMessage(update.id)
                print "-----------"
                pag  = pag + 1

        except TwitterError as t:
            print "[Info] Sleeping for 10 minutes. This is because the API is trying to block you."
            print "       Stop this (ctrl+C) and change your IP, if you dont want to wait. ZZzzzzZZzz...\n"
            time.sleep(600) # Sleep for 10 minutes and try again.

        print "Removing Tweets:"
        print "----------------\n"

        #destroy tweets
	try:
            status = api.GetUserTimeline(include_rts=1, page=pag)
            count = len(status)
            num = 1
            if status == []:
                print "No more data.\n" 
            for update in status:
                print "Number of message: [", num, "/", count, "]"
                num = num + 1
                print "ID:", update.id
                print update.text
                print "\nREMOVED!"
                api.DestroyStatus(update.id)
                print "-----------"
                pag  = pag + 1

        except TwitterError as t:
            print "[Info] Sleeping for 10 minutes. This is because the API is trying to block you."
            print "       Stop this (ctrl+C) and change your IP, if you dont want to wait. ZZzzzzZZzz...\n"
            time.sleep(600) # Sleep for 10 minutes and try again.
        
        print "======", "\n"

    def create_favorite(self):
        """
	Create Favorite
	"""
	options = self.options
	tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
	try:
	    api.CreateFavorite(status=options.favorite)	
	except URLError as u:
            print "\n[Error] - ",u.reason.strerror, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        except TwitterError as t:
            print "\n[Error] - ",t, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)

    def destroy_favorite(self):
	"""
	Destroy Favorite
	"""
	options = self.options
	tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
	try:
            api.DestroyFavorite(status=options.unfavorite)
        except URLError as u:
            print "\n[Error] - ",u.reason.strerror, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        except TwitterError as t:
            print "\n[Error] - ",t, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)

    def show_favorites(self):
        """
        Get Favorites
        """
        options = self.options
        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
	count = 10
        user = ""
	words = options.showfavs.split()
        if len(words) is 2:
            user = words[0]
            count = words[1]
        else:
            word = options.showfavs
            try:
		count = int(word)
	    except:
		user = word
        try:
        	status = api.GetFavorites(user=user,count=count)
        	return status, count
	except URLError as u:
            print "\n[Error] - ",u.reason.strerror, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        except TwitterError as t:
            print "\n[Error] - ",t, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)

    def save_friends(self):
        """
        Save all friendships, of an authorized user, into a file
        """
        options = self.options
        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
        
        try:
            friends = api.GetFriends()
            count = len(friends)
            total_friends = 0
            if friends == []:
                print "You haven't friends, yet.\n"
            for update in friends:
                print update.screen_name
                total_friends = total_friends + 1
                if not os.path.isdir("backups/"):
                    os.mkdir("backups/") 
                if not os.path.exists("backups/"):
                    path = os.mkdir("backups/")
                path = "backups/"
                # some unicode issues
                name = ''
                name = u' '.join((name, update.screen_name)).encode('utf-8').strip()
                h = "/friends.txt"
                f = open(path+h, 'a')
                f.write(name + "\n")
            f.close()
            print "\n[Info] Congratulations. Saved", total_friends ,"friendships... \n"

        except URLError as u:
            print "[Error] - ",u.reason.strerror, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        except TwitterError as t:
            try:
                print "[Error] - ",t, "\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            except Exception:
                print "\nOops! Error saving friendships on file\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2) 

    def save_favorites(self):
        """
        Save Favorites
        """
        options = self.options
        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
        count = 10
        user = ""
        words = options.savefavs.split()
        if len(words) is 2:
            user = words[0]
            count = words[1]
        else:
            word = options.savefavs
            try:
                count = int(word)
            except:
                user = word
        try:
                status = api.GetFavorites(user=user,count=count)
                return status, user
        except URLError as u:
            print "\n[Error] - ",u.reason.strerror, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        except TwitterError as t:
            print "\n[Error] - ",t, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)

    def short_url(self):
        """
        Short URL
        """
        options = self.options
        proxy = options.proxy
        eprint = sys.stderr.write
        proxy_info = None
        if proxy is not None:
            try:
                match = re.finditer(":",proxy)
                positionlist = []
                for m in match:
                    positionlist.append(m.start())

                pos1 = positionlist[0]
                pos2 = positionlist[1]
                host = proxy[pos1+3:pos2]
                slen = len(proxy)
                port = proxy[pos2+1:slen]
                proxy_info = core.socks.setdefaultproxy(core.socks.PROXY_TYPE_HTTP, host, int(port))
                socket.socket = core.socks.socksocket

            except IndexError:
                eprint ("\n[Error] - Proxy is malformed. For example, to launch with TOR use: --proxy 'http://127.0.0.1:8118'")
                eprint ("\nAborting...\n")
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            except ValueError:
                eprint ("[Error] - Proxy is malformed. For example, to launch with TOR use: --proxy 'http://127.0.0.1:8118'")
                eprint ("\nAborting...\n")
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)

        shortener = ShortURLReservations()
        shortener = shortener.process_url(options.shorturl, proxy)
        print "\nShort url:", shortener, "\n"
        return shortener

    def IRCdeploy(self, user, host, port, chan):
        """
        Deploy IRC Bot
        """
        from core.irc.bot import AnonTwiIrcBot
        AnonBot = AnonTwiIrcBot().run (user, host, port, chan)
        return AnonBot

    def get_status(self,id):
        """
        Get Status
        """
        options = self.options
        tokens = self.try_running(self.get_env_tokens, "\nInternal error getting -Tokens- ")
        api = core.twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret, proxy=options.proxy, request_headers=self.request_headers)
        try:
            status = api.GetStatus(id=id)
            return status
        except URLError as u:
            print "\n[Error] - ",u.reason.strerror, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)
        except TwitterError as t:
            print "\n[Error] - ",t, "\n"
            if options.gtk or options.webserver:
                return
            else:
                sys.exit(2)

    def run(self, opts=None):
        """ 
        Run AnonTwi
        """ 
        eprint = sys.stderr.write
        if opts:
            options = self.create_options(opts)
            self.set_options(options)
        options = self.options
        p = self.optionParser

        # check proxy options
        proxy = options.proxy
        if options.proxy:
            try:
                pattern = 'http[s]?://(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):[0-9][0-9][0-9][0-9]'
                m = re.search(pattern, proxy)
                if m is None:
                    print('='*75)
                    print(str(self.optionParser.version))
                    print('='*75)
                    print ("\n[Error] - Proxy is malformed. For example, to launch with TOR use: --proxy 'http://127.0.0.1:8118'")
                    print ("\nAborting...\n")
                    if options.gtk or options.webserver:
                        return
                    else:
                        sys.exit(2)
            except Exception:
                print('='*75)
                print(str(self.optionParser.version))
                print('='*75)
                print ("\n[Error] - Proxy is malformed. For example, to launch with TOR use: --proxy 'http://127.0.0.1:8118'")
                print ("\nAborting...\n")
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)

        if options.webserver:
            eprint("Running webserver\n")
            AnonTwiWebserver(self)
            sys.exit(0)
        
        if options.ircbot:
	    eprint("Running irc bot client\n")
            if options.gtk or options.webserver:
                pass
            else:
                try:
                    [user, rest] = options.ircbot.split ('@')
                except Exception, e:
                    import random
                    import string
                    char_set = string.ascii_uppercase + string.ascii_lowercase + string.digits
                    char_prefix = string.ascii_lowercase + string.ascii_uppercase
                    user_pre = ''.join(random.sample(char_prefix,2))
                    user = ''.join(random.sample(char_set,10))
                    user = user_pre + user
                    #user = "anontwibot" 
                    rest = options.ircbot
                try:
                    [host, port] = rest.split (':')
                except Exception:
                    print "\nPlease specify irc host and port, correctly!\n"
                    sys.exit(1)
                try:
                    [port, chan] = port.split ('#')
                except Exception:
                    chan = ""
                    print "\nNo channel specified. Assigning a random one to deploy bot\n"
                    char_set = string.ascii_uppercase + string.ascii_lowercase + string.digits
                    char_prefix = string.ascii_lowercase + string.ascii_uppercase
                    chan_pre = ''.join(random.sample(char_prefix,2))
                    chan = ''.join(random.sample(char_set,10))
                    chan = chan_pre + chan
                    
            self.IRCdeploy(user, host, port, chan)
	    sys.exit(0)

        if options.gtk or options.webserver: 
            from core.gtk.anontwigtk import AnontwiGTK
            AnontwiGTK.run()
            sys.exit(0)

        # step 0: tokens, list searches, timelines, friendships, favorites
        if options.tokens:
            eprint('='*75+'\n')
            eprint(str(p.version)+'\n')
            eprint('='*75+'\n')
            if options.rgb:
                eprint("Getting your API tokens (\033[1;31mkey\033[1;m & \033[1;31msecret\033[1;m)...\n")
            else:
                eprint("Getting your API tokens (key & secret)...\n")
            eprint('='*75+"\n")
            #self.try_running(self.request_tokens, "\nInternal error getting access tokens ", ())
            tokens = self.request_url()
            self.insert_pincode(tokens[0], 
                                tokens[1], 
                                self.consumer_key, 
                                self.consumer_secret)
            
        if options.search:
            print('='*75)
            print(str(p.version))
            print('='*75)
            self.search = options.search
            words = options.search.split()
            if len(words) is 2:
                self.search = words[0]
            if options.rgb:
                print("Starting to search:"), "\033[1;34m", self.search, "\033[1;m"
            else:
                print("Starting to search:"), options.search
            print('='*75), "\n"
            searches = self.try_running(self.search_messages, "\nInternal error searching -message-. look at the end of this Traceback.")
            
            if searches==None:
                print "Search returns None.\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            if len(searches) <= 0:
                print "Search doesn't get any results.\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            else:
                print("Search Results:")
                h = HTMLParser.HTMLParser()
                for s in searches:
                    print "======"
                    if options.rgb:
                        if s.user.name is not None:
			    print "Name:\033[1;31m", h.unescape(s.user.name), "\033[1;m", "- Nick:\033[1;34m", s.user.screen_name, "\033[1;m"
                        else:
                            print "Nick:\033[1;34m", s.user.screen_name, "\033[1;m"
                    else:
                        if s.user is not None:
                            if s.user.name is not None:
                                print "Name:", h.unescape(s.user.name), "- Nick:", s.user.screen_name
                            else:
                                print "Nick:", s.user.screen_name
 		    if options.rgb:
                        print "Tweet-ID:\033[1;36m", s.id, "\033[1;m"
                    else:
                        print "Tweet-ID:", s.id
                    if options.rgb:
                        print s.created_at
                    else:
                        print s.created_at
                    if options.rgb:
                        print "\033[1;37m", h.unescape(s.text), "\033[1;m"
                    else:
                        print h.unescape(s.text)
                    if s.place is not None:
                        if options.rgb:
                            print "Location: \033[1;31m", s.place["name"], "\033[1;m"
                        else:
                            print "Location:", s.place["name"]
                print "======", "\n"

        if options.topics:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print("Seaching Global Trending Topics (TT) ")
            print('='*75), "\n"
            if self.source_api == "identi.ca/api":
                print "[Info] This feature is not allowed by identi.ca yet...\n"
                trendingtopics = ""
            else:
                trendingtopics = self.try_running(self.search_topics, "\nInternal error searching -trending topics-. look at the end of this Traceback.")
            if len(trendingtopics) <= 0:
                print "Something wrong getting trending topics... Aborting!\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            else:
                print("Trending Topics:")
                h = HTMLParser.HTMLParser()
                print("========\n")
                for item in trendingtopics:
                    self.topic = item.name
                    if options.rgb:
                        print "\033[1;31m", h.unescape(self.topic), "\033[1;m"
                    else:
                        print(h.unescape(self.topic))
                print "======", "\n"

        if options.suicide:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print("Suiciding !!!!!!! :-D ")
            print('='*75), "\n" 
            # ask question to be sure
            print "You go to 'remove' your account, for that, AnonTwi will try to delete all your tweets"
            print "and direct messages. Remember that some social networks were storing your data on their servers"
            print "so, this process will use the tools that the API that you are connecting using AnonTwi allows to you to use\n"
            print "If you had a lot of activity, it can takes long time. After remove ALL data, your account will be deactivated...\n"
            zen = raw_input("Ready (y/n)")
            if zen is "y":
                print "\nStarting to destroy your data:"
                print "------------------------------\n"
                # remove all tweets
                suicides = self.try_running(self.suicide, "\nInternal error -suiciding-. look at the end of this Traceback.")
                print "All data correctly deleted!\n"
                # close account 
                if self.source_api == "api.twitter.com":
                    print "[Info] Remember that Twitter.com does not delete your data. If you want to deactive your account, you must to"
                    print "       do some some steps. Follow this link to complete your suicide:\n" 
                    print "       https://support.twitter.com/articles/15358-how-to-deactivate-your-account#\n"
                    print "[Info] You should reclaim your rights about your personal data. Twitter.com is in California.\n"
            else:
                print "\nWhen you cease to make a contribution, then you begin to die. Anna Eleanor Roosevelt.\n"

        if options.mentions:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print("Showing mentions about you...")
            print('='*75), "\n"
            (mentions, num) = self.try_running(self.show_mentions, "\nInternal error searching -mentions- about you. look at the end of this Traceback.")
            if len(mentions) <= 0:
                print "Search doesn't get any results.\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            else:
                print("Mentions:")
                print("========")
                n = int(len(mentions))
                h = HTMLParser.HTMLParser()
                if int(num) < int(len(mentions)):
                    n = int(num)
                for i in range(int(n)):
                    if options.rgb:
                        print "Name:\033[1;31m", h.unescape(mentions[i].user.name), "\033[1;m", "- Nick:\033[1;34m", mentions[i].user.screen_name, "\033[1;m"
                    else:
                        print "Name:", h.unescape(mentions[i].user.name), "- Nick:", mentions[i].user.screen_name
                    if options.rgb:
                        print "Tweet-ID:\033[1;36m", mentions[i].id, "\033[1;m"
                    else:
                        print "Tweet-ID:", mentions[i].id
                    if options.rgb:
                        print mentions[i].created_at
                    else:
                        print mentions[i].created_at
                    if options.rgb:
                        print "\033[1;37m", h.unescape(mentions[i].text), "\033[1;m"
                    else:
                        print h.unescape(mentions[i].text)
                    if mentions[i].place is not None: 
                        if options.rgb:
                            print "\033[1;37m", mentions[i].place["name"], "\033[1;m"
                        else:
                            print mentions[i].place["name"]
                    else:
                        pass
                    print "======"

        if options.timeline:
            print('='*75)
            print(str(p.version))
            print('='*75)
            self.timeline = options.timeline
            words = options.timeline.split()
            if len(words) is 2:
                self.timeline = words[0]
            if options.rgb:
                print("Showing timeline of:"), "\033[1;34m", self.timeline, "\033[1;m"
            else:
                print("Showing timeline of:"), options.timeline
            h = HTMLParser.HTMLParser()
            print('='*75), "\n"
            timelines = self.try_running(self.show_timeline, "\nInternal error searching -timeline-. look at the end of this Traceback.")
            
            if len(timelines) <= 0:
                print "This user hasn't tweeted yet.\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            else:
                print("Name:"),
                for s in timelines:
                    self.nickid = h.unescape(s.user.name)
                if options.rgb:
                    print "\033[1;31m", self.nickid, "\033[1;m"
                else:
                    print(self.nickid)
                print("Nick:"),
                for s in timelines:
                    user = s.user.screen_name
                if options.rgb:
                    print "\033[1;34m", s.user.screen_name, "\033[1;m"
                else:
                    print(user)
                print("Description:"),
                for s in timelines:
                    description = h.unescape(s.user.description)
                if options.rgb:
                    print"\033[1;30m", description, "\033[1;m"
                else:
                    print(description)
                print("Friends:"),
                for s in timelines:
                    friends = s.user.friends_count
                if options.rgb:
                    print "\033[1;32m", friends, "\033[1;m"
                else:
                    print(friends)
                print("Followers:"),
                for s in timelines:
                    followers = s.user.followers_count
                if options.rgb:
                    print "\033[1;32m", followers, "\033[1;m"
                else:
                    print(followers)
                print "Timeline requests:"
                print("---------")
                for s in timelines:
                    if options.rgb:
                        print "Tweet-ID:", "\033[1;36m", s.id, "\033[1;m"
                    else:
                        print "Tweet-ID:", s.id
                    if options.rgb:
                        print s.created_at
                    else:
                        print s.created_at 
                    if options.rgb:
                        print "\033[1;37m", h.unescape(s.text), "\033[1;m"
                    else:
                        print h.unescape(s.text)
                    if s.place is not None:
                        if options.rgb:
                            print "Location: \033[1;35m", s.place["name"], "\033[1;m"
                        else:
                            print "Location:", s.place["name"]
                    print "======"

        if options.timelinedm:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print("Showing Direct Messages...")
            h = HTMLParser.HTMLParser()
            print('='*75), "\n"
            (dms, num) = self.try_running(self.show_timelinedm, "\nInternal error searching -direct messages-. look at the end of this Traceback.")

            if len(dms) <= 0:
                print "Search doesn't get any results.\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            else:
                print "Your conversations:"
                print("---------")
                n = int(len(dms))
                if int(num) < int(len(dms)):
                    n = int(num)
                for i in range(int(n)):
                    if options.rgb:
                        print "DM-ID:\033[1;31m", dms[i].id, "\033[1;m"
                    else:
                        print "DM-ID:", dms[i].id
                    if options.rgb:
                        print dms[i].created_at
                    else:
                        print dms[i].created_at
                    if options.rgb:
                        print "From:\033[1;34m", h.unescape(dms[i].sender_screen_name), "\033[1;m"
                    else:
                        print "From:", h.unescape(dms[i].sender_screen_name)
                    if options.rgb:
                        print "\033[1;37m", h.unescape(dms[i].text), "\033[1;m"
                    else:
                        print h.unescape(dms[i].text)
                    print "======"

        if options.timelinef:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print("Showing your 'home' timeline")
            h = HTMLParser.HTMLParser()
            print('='*75), "\n"
            num = options.timelinef
            (timelinesf, count) = self.try_running(self.show_timeline_friends, "\nInternal error searching -timeline-. look at the end of this Traceback.")
            if len(timelinesf) <= 0:
                print "This user hasn't tweeted yet.\n"
                if options.gtk or options.webserver:
                    return
                else:                      
                    sys.exit(2)
            else:
                print "Timeline requests:"
                print "---------"

                if int(len(timelinesf)) < int(count):
                    count = int(len(timelinesf))
                for i in range(int(count)):
                    if options.rgb:
                        print "Name:\033[1;31m", h.unescape(timelinesf[i].user.name), "\033[1;m", "- Nick:\033[1;34m", timelinesf[i].user.screen_name, "\033[1;m"
                        #print("Description:"), "\033[1;30m", timelinesf[i].user.description, "\033[1;m"
                        #print("Friends:"), "\033[1;32m", timelinesf[i].user.friends_count, "\033[1;m"
                        #print("Followers:"), "\033[1;32m", timelinesf[i].user.followers_count, "\033[1;m"
                    else:
                        print "Name:", h.unescape(timelinesf[i].user.name), "- Nick:", timelinesf[i].user.screen_name
                        #print("Description:"), timelinesf[i].user.description
                        #print("Friends:"), timelinesf[i].user.friends_count
                        #print("Followers:"), timelinesf[i].user.followers_count
                        #print "\nTimeline requests:"
                    if options.rgb:
                        print "Tweet-ID:", "\033[1;36m", timelinesf[i].id, "\033[1;m"
                    else:
                        print "Tweet-ID:", timelinesf[i].id
                    if options.rgb:
                        print timelinesf[i].created_at
                    else:
                        print timelinesf[i].created_at
                    if options.rgb:
                        print "\033[1;37m", h.unescape(timelinesf[i].text), "\033[1;m"
                    else:
                        print h.unescape(timelinesf[i].text)
                    if timelinesf[i].place is not None:
                        if options.rgb:
                            print "Location: \033[1;35m", timelinesf[i].place["name"], "\033[1;m"
                        else:
                            print "Location:", timelinesf[i].place["name"]
                    print "======"

        if options.showfavs:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print("Showing favorites")
            h = HTMLParser.HTMLParser()
            print('='*75), "\n"
            (favorites, count) = self.try_running(self.show_favorites, "\nInternal error searching -favorites-. look at the end of this Traceback.")
            if len(favorites) <= 0:
                print "No results.\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            else:
                if int(len(favorites)) < int(count):
                    count = int(len(favorites))
                for i in range(int(count)):
                    if options.rgb:
                        print "Name:\033[1;31m", h.unescape(favorites[i].user.name), "\033[1;m", "- Nick:\033[1;34m", favorites[i].user.screen_name, "\033[1;m"
                    else:
                        print "Name:", h.unescape(favorites[i].user.name), "- Nick:", favorites[i].user.screen_name
                    if options.rgb:
                        print "Tweet-ID:", "\033[1;36m", favorites[i].id, "\033[1;m"
                    else:
                        print "Tweet-ID:", favorites[i].id
                    if options.rgb:
                        print favorites[i].created_at
                    else:
                        print favorites[i].created_at
                    if options.rgb:
                        print "\033[1;37m", h.unescape(favorites[i].text), "\033[1;m"
                    else:
                        print h.unescape(favorites[i].text)
                    if favorites[i].place is not None:
                        if options.rgb:
                            print "Location: \033[1;35m", favorites[i].place["name"], "\033[1;m"
                        else:
                            print "Location:", favorites[i].place["name"]
                    print "=================="

        # step 1: get message/image/DM to send and sanitize them
        messages = self.try_running(self.get_messages, "\nInternal error getting -message-. look at the end of this Traceback.")
        #(messages, dm, image) = self.sanitize_messages(messages)
        (messages, dm, mdm) = self.sanitize_messages(messages)
       
        # send retweets
        retweets = self.try_running(self.get_tweetids, "\nInternal error sending -retweet-. look at the end of this Traceback.")

        # remove tweets
        if options.rmtweet:
            rmtweets = self.try_running(self.remove_tweet, "\nInternal error removing -message-. look at the end of this Traceback.")

        # step 2: de/encryption processes
        if options.encaes:
            key = options.key
            try:
                messages = self.encrypt(messages, key)
            except ValueError:
                print len(key)
                print "\n[Error] - Invalid PIN key. Try to generate automatically (ex: --gen)"
                print "\nAborting...\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)

        if options.decaes:
            key = options.key
            try:
                self.decrypt(messages, key)
            except ValueError:
                print "\n[Error] - Invalid PIN key. Try to generate automatically (ex: --gen)"
                print "\nAborting...\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)

        # step3: send tweet/waves/DM
        if options.tweet and not options.decaes:
            if options.dm:
                dm = self.try_running(self.send_dm, "\nInternal error sending -DM- ", (messages, dm))
                print "[Info] DM sent correctly!", "\n"
            elif options.mdm:
                mdm = self.try_running(self.send_mdm, "\nInternal error sending massive -DMs- to all your friends ", (messages, mdm))
                print "\n[Info] Massive DM to all your friends sent correctly!", "\n"
            elif options.ldm:
                ldm = self.try_running(self.send_mdm, "\nInternal error sending massive -DMs- to all your friends ", (messages, options.ldm))
                print "\n[Info] Massive DM to your list of friends sent correctly!", "\n"
            elif options.wave:
                if options.location:
                    (latitude, longitude) = self.get_location()
                    if options.reply:
                        reply = options.reply
                    else:
                        reply = None
                    waves = self.try_running(self.send_wave, "\nInternal error sending -Wave- ", (messages, reply, latitude, longitude))
                    print "[Info] Your geolocation place was changed to coordenates:", latitude, ",", longitude
                    if options.reply:
                        print "\n[Info] Waves reply to conversation sent correctly!", "\n"
                    else:
                        print "\n[Info] Waves sent correctly!", "\n"
                else:
                    if options.reply:
                        reply = options.reply
                    else:
                        reply = None
                    waves = self.try_running(self.send_wave, "\nInternal error sending -Wave- ", (messages, reply, None, None))
                    if options.reply:
                        print "\n[Info] Waves reply to conversation sent correctly!", "\n"
                    else:
                        print "\n[Info] Waves sent correctly!", "\n"
            # fake geolocation
            elif options.location and not options.wave:
                (latitude, longitude) = self.get_location()
                # reply to tweet conversation with fake geolocation
                if options.reply:
                    reply = options.reply
                else:
                    reply = None
                tweet = self.try_running(self.send_tweet, "\nInternal error sending -Tweet- ", (messages, reply, latitude, longitude))
                print "[Info] Your geolocation place was changed to coordenates:", latitude, ",", longitude
                if options.reply:
                    print "\n[Info] Tweet reply to conversation sent correctly!", "\n"
                else:
                    print "\n[Info] Tweet sent correctly!", "\n"
            else:
                # reply to tweet conversation
                if options.reply:
                    reply = options.reply
                else:
                    reply = None
                tweet = self.try_running(self.send_tweet, "\nInternal error sending -Tweet- ", (messages, reply, None, None))
                if options.reply:
                    print "\n[Info] Tweet reply to conversation sent correctly!", "\n"
                else:
                    print "\n[Info] Tweet sent correctly!", "\n"
        # send image
        #elif options.image:
        #    images = self.try_running(self.send_image, "\nInternal error sending -Image- " (messages, image))
        #    print "[Info] Image uploaded correctly!", "\n"

        # send retweet
        elif options.retweet:
            retweet = self.try_running(self.send_retweet, "\nInternal error sending -reTweet- ", retweets)
            print "\n[Info] reTweet sent correctly!", "\n"

        # remove tweet
        elif options.rmtweet:
            rmtweet = self.try_running(self.remove_tweet, "\nInternal error removing -message- ", rmtweets)
            print "\n[Info] Tweet removed correctly!", "\n"

        # remove direct message
        elif options.rmdm:
            rmdm = self.try_running(self.remove_dm, "\nInternal error removing -message- ")
            print "\n[Info] Direct Message removed correctly!", "\n"

        # create friendship
        if options.friend:
            friend = self.try_running(self.set_friend, "\nInternal error creating -friendship- ")
            print "\n[Info] Your request to friendship with:", options.friend, "was successfully sent!", "\n"

        #  create massively friendships from file (file.txt)
        if options.massfriend:
            massfriend = self.try_running(self.set_friend, "\nInternal error creating massively -friendships- from file ")
            print "\n[Info] Your massively creating request friendships list was successfully sent!", "\n"

        # destroy friendship
        if options.dfriend:
            dfriend = self.try_running(self.remove_friend, "\nInternal error destroying -friendship- ")
            print "\n[Info] Your request to destroy friendship with:", options.dfriend, "was successfully sent!", "\n"

        # destroy massively friendships from file (file.txt)
        if options.massdfriend:
            massdfriend = self.try_running(self.remove_friend, "\nInternal error destroying massively -friendships- from file ")
            print "\n[Info] Your massively destroy request friendships list was successfully sent!", "\n"

        # create block
        if options.block:
            block = self.try_running(self.create_block, "\nInternal error destroying -friendship- ")
            print "\n[Info] Your request to create block with:", options.block, "was successfully sent!", "\n"

        # destroy block
        if options.unblock:
            unblock = self.try_running(self.destroy_block, "\nInternal error destroying -friendship- ")
            print "\n[Info] Your request to destroy block with:", options.unblock, "was successfully sent!", "\n"

	# create favorite
	if options.favorite:
	    favorite = self.try_running(self.create_favorite, "\nInternal error creating -favorite- ")
	    print "\n[Info] Your request to create favorite was successfully sent!", "\n"	

	# destroy favorite
	if options.unfavorite:
	    favorite = self.try_running(self.destroy_favorite, "\nInternal error destroying -favorite- ")
            print "\n[Info] Your request to destroy favorite was successfully sent!", "\n"

	# get friend list
	if options.friendlist:
	    friendlist = self.try_running(self.friendlist, "\nInternal error getting -friendlist- ")
            if friendlist:
                print "\n[Info] Your friends are : ", "\n"
                for f in friendlist :
                    print "       "+f.GetName()+ '(' + f.GetScreenName() +")\n"
            else:
                print "\n[Info] You don't have any friends! ", "\n"
                
            
        # change 'source' value
        #if options.via:
        #    source = self.try_running(self.set_via, "\nInternal error setting -via- detailed on website ")
        #    print "[Info] Your 'via' value was changed to:", options.via, "\n"

        # store tweets to disk
        if options.save:
	    print('='*75)
            print(str(p.version))
            print('='*75)
            print("Starting to save your messages into a file. This can take a time... :)")
            print('='*75)
	    (saved,user) = self.try_running(self.save_timeline, "\nInternal error getting -Tokens- ")
          
            if saved == []:
                print "This user hasn't tweet anything yet.\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            sn = 0
            for s in saved:
                h = HTMLParser.HTMLParser()
                sn = sn + 1
                if options.rgb:
                    print "[Saved]:", s.created_at,
                    print "\033[1;37m", h.unescape(s.text), "\033[1;m"
                else:
                    print "[Saved]:", s.created_at, ":",  h.unescape(s.text)

                if not os.path.isdir("backups"):
                    os.mkdir("backups") 
                if not os.path.exists("backups/%s"%(user)):
                    path = os.mkdir("backups/%s"%(user))

                path = "backups/%s"%(user)
                # some unicode issues
                logs = ''
                logs = u' '.join((logs, s.text)).encode('utf-8').strip()
                nick = ''
                nick = u' '.join((nick, s.user.screen_name)).encode('utf-8').strip()
                name = ''
                name = u' '.join((name, s.user.name)).encode('utf-8').strip()
                created_at = ''
                created_at = u' '.join((created_at, s.created_at)).encode('utf-8').strip()
                id = ''
                id = u' '.join((id, str(s.id))).encode('utf-8').strip()
                place = ''
                if s.place is not None:
                    place = u' '.join((place, s.place["name"])).encode('utf-8').strip()

                h = "/tweets.txt"
                f = open(path+h, 'a')
                f.write("Name: " + name + " - ")
                f.write("Nick: " + nick + "\n")
                f.write("Tweet-ID: " + id + "\n")
                f.write(created_at + "\n")
                f.write(logs + "\n")
                if s.place is not None:
                    f.write(place + "\n")
                f.write("======" + "\n")
            f.close()
            print "\n[Info] Congratulations. Saved", sn ,"messages... \n"

        # store friendships to disk
        if options.savef:
	    print('='*75)
            print(str(p.version))
            print('='*75)
            print("Starting to save your friendships into a file. This should be faster! :)")
            print('='*75)
            h = HTMLParser.HTMLParser()
	    saved = self.try_running(self.save_friends, "\nInternal error getting -Tokens- ")

        # store favorites to disk
        if options.savefavs:
	    print('='*75)
            print(str(p.version))
            print('='*75)
            print("Starting to save your favorites into a file. This can take a time... :)")
            print('='*75)
            h = HTMLParser.HTMLParser()
	    (savedfavs,user) = self.try_running(self.save_favorites, "\nInternal error getting -Tokens- ")
       
            if savedfavs == []:
                print "This user hasn't create favorites yet.\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)
            fn = 0
            for s in savedfavs:
                fn = fn + 1
                if options.rgb:
                    print "[Saved]:", s.created_at,
                    print "\033[1;37m", h.unescape(s.text), "\033[1;m"
                else:
                    print "[Saved]:", s.created_at, ":",  h.unescape(s.text)

                if not os.path.isdir("backups"):
                    os.mkdir("backups") 
                if not os.path.exists("backups/%s"%(user)):
                    path = os.mkdir("backups/%s"%(user))

                path = "backups/%s"%(user)
                # some unicode issues
                logs = ''
                logs = u' '.join((logs, s.text)).encode('utf-8').strip()
                nick = ''
                nick = u' '.join((nick, s.user.screen_name)).encode('utf-8').strip()
                name = ''
                name = u' '.join((name, s.user.name)).encode('utf-8').strip()
                created_at = ''
                created_at = u' '.join((created_at, s.created_at)).encode('utf-8').strip()
                id = ''
                id = u' '.join((id, str(s.id))).encode('utf-8').strip()
                place = ''
                if s.place is not None:
                    place = u' '.join((place, s.place["name"])).encode('utf-8').strip()

                h = "/favorites.txt"
                f = open(path+h, 'a')
                f.write("Name: " + name + " - ")
                f.write("Nick: " + nick + "\n")
                f.write("Tweet-ID: " + id + "\n")
                f.write(created_at + "\n")
                f.write(logs + "\n")
                if s.place is not None:
                    f.write(place + "\n")
                f.write("======" + "\n")
            f.close()

            print "\n[Info] Congratulations. Saved", fn ,"favorites... \n"

        # generate a PIN key if requested
        if options.genkey:
            key = generate_key()
            print "\nPIN key:", key, "\n\nShare this key privately with the recipients of your encrypted messages.\nDon't send this key over insecure channels such as email, SMS, IM or Twitter.\nUse the sneakernet! ;)\n"

        # generate a short url if requested
        if options.shorturl:
            proxy = options.proxy
            eprint = sys.stderr.write
            proxy_info = None
            if proxy is not None:
                try:
                    match = re.finditer(":",proxy)
                    positionlist = []
                    for m in match:
                        positionlist.append(m.start())
        
                    pos1 = positionlist[0]
                    pos2 = positionlist[1]
                    host = proxy[pos1+3:pos2]
                    slen = len(proxy)
                    port = proxy[pos2+1:slen]
                    proxy_info = core.socks.setdefaultproxy(core.socks.PROXY_TYPE_HTTP, host, int(port))
                    socket.socket = core.socks.socksocket

                except IndexError:
                    eprint ("\n[Error] - Proxy is malformed. For example, to launch with TOR use: --proxy 'http://127.0.0.1:8118'")
                    eprint ("\nAborting...\n")
                    if options.gtk or options.webserver:
                        return
                    else:
                        sys.exit(2)
                except ValueError:
                    eprint ("[Error] - Proxy is malformed. For example, to launch with TOR use: --proxy 'http://127.0.0.1:8118'")
                    eprint ("\nAborting...\n")
                    if options.gtk or options.webserver:
                        return
                    else:
                        sys.exit(2)

            shortener = ShortURLReservations()
            shortener = shortener.process_url(options.shorturl, proxy)
            print "\nShort url:", shortener, "\n"

    def sanitize_messages(self, messages):
        """
        Sanitize correct input of message/image/dm to send
        """
        options = self.options
        all_messages = set()
        dm_user = set()
        mdm_user = set()
        #image = set()

        for message in messages:
            if options.tweet:
                lenght_tweet = len(options.tweet)
                self.num_tweets = int(lenght_tweet/140) + 1 #140 characters/tweet
                if options.rgb:
                    print "\nMessage [ \033[1;34mNumber of words:\033[1;m\033[1;37m", lenght_tweet, "\033[1;m- \033[1;34mNumber of waves:\033[1;m\033[1;37m", self.num_tweets, "\033[1;m]"
                else:
                    print "\nMessage [ Number of words:", lenght_tweet, "- Number of waves:", self.num_tweets, "]"
                print "-------------"
                if options.rgb:
                    print "\033[1;35m", options.tweet, "\033[1;m"
                else:
                    print options.tweet
                print "-------------"
                all_messages.add(options.tweet)

                if options.dm:
                    if "@" in options.dm and "identi.ca" in self.source_api:
                        options.dm=options.dm[1:len(options.dm)]
                    if options.rgb:
                        print "To:\033[1;31m", options.dm, "\033[1;m"
                    else:
                        print "To:", options.dm
                    print "------\n"
                    dm_user.add(options.dm)

                elif options.mdm:
                    if "@" in options.mdm and "identi.ca" in self.source_api:
                        options.mdm=options.mdm[1:len(options.mdm)]
                    if options.rgb:
                        print "Sending to friends of:\033[1;31m", options.mdm, "\033[1;m"
                    else:
                        print "Sending to friends of:", options.mdm
                    print "------"
                    mdm_user.add(options.mdm)

            if options.dm and not options.tweet:
                print "\n[Error] - you must enter a message to send, using option -m (ex: -d '@nick' -m 'text')\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)

            elif options.mdm and not options.tweet:
                print "\n[Error] - you must enter a message to send massively, using option -m (ex: --mdm '@nick' -m 'text')\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)

            elif options.ldm and not options.tweet:
                print "\n[Error] - you must enter a message to send to the list of friends of your file, try using option -m (ex: --ldm 'file.txt' -m 'text')\n"
                if options.gtk or options.webserver:
                    return
                else:
                    sys.exit(2)

        #return all_messages, dm_user, image
        return all_messages, dm_user, mdm_user

    #GTK/Wrapper
    def get_user_info(self,
                  consumer_key,
                  consumer_secret,
                  access_token_key,
                  access_token_secret,
                  proxy):
        """
        Get user info
        """
        api = core.twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret, proxy=proxy, request_headers=self.request_headers)

        try:
            #at the moment, get user timeline for future feature
            status = api.GetUserTimeline(api.VerifyCredentials().screen_name, count=0, include_rts=1)
        except TwitterError as t:
            print "[Error] - ",t,"\n"
            return "hmm"

        try:
            for s in status:
                nickid = s.user.name
                user = s.user.screen_name
                description = s.user.description
                friends = s.user.friends_count
                followers = s.user.followers_count
                #following = s.user.following_count
                url_profile = s.user.profile_image_url
                statuses_count = s.user.statuses_count
                
            user_info = {'nickid':nickid,
                         'user':user,
                         'description':description,
                         'friends':friends,
                         'followers':followers,
                         'url_profile':url_profile,
                         'statuses_count':statuses_count}
        except Error as e:
            print "[Error] - ",t,"\n"
            return {}
            
                
        return user_info

if __name__ == "__main__":
    app = anontwi()
    options = app.create_options()
    if options:
        app.set_options(options)
        app.run()
