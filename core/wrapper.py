#!/usr/bin/env python
# -*- coding: utf-8 -*-"
# vim: set expandtab tabstop=4 shiftwidth=4:
"""
Copyright (C) 2012 Jhonny5 <jhonny5@riseup.net> + psy <epsylon@riseup.net>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os, sys
import logging

from core.gtk.config_gtk import * 
from core.gtk.error import AnontwiError
from core.main import anontwi
from core.encrypt import generate_key

class IOManager(object):
    def __init__(self):
        self.backup = ''
    
    def CaptureOutput(self):
        from cStringIO import StringIO

        self.backup = sys.stdout
        sys.stdout = StringIO()

    def GetOutput(self):
        return sys.stdout.getvalue()

    def RestoreOutput(self):
        sys.stdout.close()
        sys.stdout = self.backup

class WrapperAnontwi():
    """Wrapper Anontwi class."""
    
    """ PRIVATE """
    def __init__(self):
        self.log = logging.getLogger('Anontwi-Wrapper')
        self.app = anontwi()
        self.options = '' 

    def _create_options(self, cmd):
        access = self.get_access_tokens()
        self.log.debug('Access Token: ' + access['access_token'])   
        self.log.debug('Secret Token: ' + access['secret_token'])
        cmd.append(access['access_token'])
        cmd.append(access['secret_token'])
        self.log.debug('[_create_options] cmd: ' + str(cmd))

        self.options = self.app.create_options(cmd)
        self.app.set_options(self.options)

    def _run(self, cmd):
        self.log.debug('Running Anontwi with commands: ' + str(cmd))
        self.app.run(cmd[1:])

    def get_app(self):
        return self.app
    
    """ ANONTWI GTK """
    def get_access_tokens(self):
        """Get AccessTokens from file.
            Returns: 
                Dict with: {'access_token' : 'Access Token',
                            'secret_token' : 'Secret Token'}
        """
        file_path = DIR_TOKENS + FILE_ACC_TKN
        try:
            lines = open(file_path).readlines()
            return {'access_token' : lines[0].strip(), 
                    'secret_token' : lines[1].strip() }
        except: 
            self.log.info("Access tokens NOT found, path: %s" % file_path)
            return {}

    def get_consumer_tokens(self):
        """Get ConsumerTokens from file.
            Returns: 
                ToDo
        """
        file_path = DIR_TOKENS + FILE_CONS_TKN
        try:
            lines = open(file_path).readlines()
            self.log.debug('[get_consumer_tokens]')
            self.log.debug('Path: ' + file_path)
            self.log.debug('- consumer_key: ' + lines[0].strip())
            self.log.debug('- consumer_secret: ' + lines[1].strip())

            return {'consumer_key' : lines[0].strip(), 
                    'consumer_secret' : lines[1].strip() }
        except: 
            self.log.info("Consumer tokens NOT found, path: %s" % file_path)
            return {}

    def get_source_api(self):
        """Get SourceApi from file.
            Returns: 
                ToDo
        """
        file_path = DIR_TOKENS + FILE_SOURCE_API
        try:
            lines = open(file_path).readlines()
            self.log.debug('[get_source_api]')
            self.log.debug('Path: ' + file_path)
            self.log.debug('Source API: ' + lines[0].strip())

            return {'source_api' : lines[0].strip()}
        except: 
            self.log.info("Source API NOT found, path: %s" % file_path)
            return {}
   
    def write_tokens(self, access, consumer, source_api):
        self.log.info('Writing tokens')
        # check directories
        if not os.path.exists(DIR_HOME_ANON):
            self.log.info(DIR_HOME_ANON + " created.")
            os.makedirs(DIR_HOME_ANON)
        if not os.path.exists(DIR_TOKENS):
            self.log.info(DIR_TOKENS + " created.")
            os.makedirs(DIR_TOKENS)
        open(DIR_TOKENS + FILE_ACC_TKN, 'w').write(access['access_token'] + '\n' + access['secret_token'])
        open(DIR_TOKENS + FILE_CONS_TKN, 'w').write(consumer['consumer_key'] + '\n' + consumer['consumer_secret'])
        open(DIR_TOKENS + FILE_SOURCE_API, 'w').write(source_api)

    """ ANONTWI CORE """
    def send_tweet(self, tweet, 
                        pm = None,
                        gps = None,
                        wave = None,
                        enc = None,
                        proxy = None):
        """Send tweet.
            Args: 
                tweet: text message to send.
                pm:    {'pm' : 'bool value - is a pm message?,
                        'user' : 'name of the user recipient'} 
                enc:   {'enc' : 'bool value - encrypt the message?,
                        'pin : 'pin key for encrypted msg.' }
                proxy: {'proxy' : 'bool value - is proxy enable?',
                        'ip_address' : 'ip addres for proxy',
                        'port' : 'port for proxy'}
        """
        if os.path.isfile ('anontwi'):
            cmd = ['./anontwi']
        else:
            cmd = ['anontwi']
        if pm['pm'] is False:
            cmd.append('-m ' + tweet.strip() )
        else:
            cmd.append('-m ' + tweet.strip() )
            cmd.append('-d ' + pm['user'])
        if enc and enc['enc']:
            cmd.append('--enc')
            cmd.append('--pin=' + enc['pin'])
        if gps:
            cmd.append('--gps')
            app = self.get_app()
            cmd.append(app.geoposition)
        if wave:
            cmd.append('--waves')
        if proxy and proxy['proxy']:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        try: 
            print "CMD ", cmd
            self._create_options(cmd)
            return self._run(cmd)
        except:
            return False

    def encrypt(self, message, key):
        cmd = ['anontwi']
        cmd.append('--enc')
        cmd.append('--pin=' + key)
        self._create_options(cmd)
        app = self.get_app()
        m_encrypt = app.encrypt(message, key)
        self.log.debug('[encrypt] Msg encrypted: ' + str(m_encrypt))
        return m_encrypt
    
    def decrypt(self, messages, key):
        cmd = ['anontwi']
        cmd.append('--dec=' + messages)
        cmd.append('--pin=' + key)
        self._create_options(cmd)
        app = self.get_app()
        msg = app.decrypt(messages, key)
        self.log.debug('[decrypt] Msg decrypted: ' + str(msg))
        return msg

    def get_user_info(self, proxy):
        self.log.debug('[get_user_info] loading info...')
        app = self.get_app()
        consumer = self.get_consumer_tokens()
        access = self.get_access_tokens()
        if not consumer or not access:
            self.log.critical('Tokens not found! Could not retrieve user information.')
        
        info = app.get_user_info(consumer['consumer_key'],
                                 consumer['consumer_secret'],
                                 access['access_token'],
                                 access['secret_token'],
                                 proxy)                          
        return info

    def get_url(self, access, consumer, source_api, proxy):
        data = ''
        cmd = ['anontwi']
        cmd.append('--tokens')

        if proxy is not None and proxy['proxy'] is True:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
 
        self.log.debug("GetUrl cmd: " + str(cmd))
        try:
            self.write_tokens(access, consumer, source_api)
            self._create_options(cmd)
            app = self.get_app()
            data = app.request_url(consumer['consumer_key'], 
                                   consumer['consumer_secret'],
                                   source_api = source_api,
                                   gtk = True)
            self.log.debug("Sucesfull GetUrl")
            return data
        except:
            self.log.debug("Error GetUrl")
            return ''

    def insert_pincode(self, pin, oauth_token, oauth_token_secret, 
                       consumer, source_api, proxy=None):
        cmd = ["anontwi"]
        cmd.append("--tokens")
        if proxy:
            cmd.append('--proxy=' + proxy)
        self._create_options(cmd)
        app = self.get_app()
        consumer = self.get_consumer_tokens()
        try:
            self.log.debug("Inserting pincode.")
            app.insert_pincode(oauth_token,
                               oauth_token_secret,
                               consumer['consumer_key'],
                               consumer['consumer_secret'],
                               source_api,
                               pin, gtk = True)
        except:
            self.log.debug("Fail to insert pincode.")
            raise
    
    def get_reply_user(self, id):
        status = self.app.get_status(id)
        user = status.user.screen_name
        return user
    
    def reply(self, ID, msg, gps = None, enc = None, proxy = None):
        user = self.get_reply_user(ID)
        cmd = ['anontwi']
        cmd.append('-m ' + '@' + user + ' ' + msg )
        cmd.append('--reply=' + ID)
        if enc['enc'] is True:
            cmd.append('--enc')
            cmd.append('--pin=' + enc['pin'] +'')
        if gps:
            cmd.append('--gps')
            app = self.get_app()
            cmd.append(app.geoposition)
        if proxy['proxy'] is True:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        self._create_options(cmd)
        self._run(cmd)
    
    def retweet_tweet(self, ID, proxy=None):
        cmd = ['anontwi']
        cmd.append('-r')
        cmd.append(ID)
        if proxy:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        self._create_options(cmd)
        app = self.get_app()
        topics = app.send_retweet()    

    def save_messages(self, user, num_ocurrences, proxy=None):
        cmd = ["anontwi"]
        cmd.append('--save')
        cmd.append(user + " " + num_ocurrences)
        if proxy:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        self.log.debug('[Backup] CMD: ' + str(cmd)) 
        self._create_options(cmd)
        app = self.get_app()
        self.log.debug('[Backup] Creating app: OK')
        saves = app.save_timeline()
        self.log.debug('[Backup] Return lines: ' + str(saves))
        return saves
    
    def favorite(self, ID, proxy=None):
        cmd = ['anontwi']
        cmd.append('--fav=' + ID)
        if proxy:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        self._create_options(cmd)
        self._run(cmd)

    def unfavorite(self, ID, proxy=None):
        cmd = ['anontwi']
        cmd.append('--unfav=' + ID)
        if proxy:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        self._create_options(cmd)
        self._run(cmd)

    def delete_tweet(self, ID, proxy=None):
        cmd = ['anontwi']
        cmd.append('--rm-m=' + ID)
        if proxy:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        self._create_options(cmd)
        self._run(cmd)

    def delete_private(self, ID, proxy=None):
        cmd = ['anontwi']
        cmd.append('--rm-d=' + ID)
        if proxy:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        self._create_options(cmd)
        self._run(cmd)

    def search_messages(self, textsearch, 
                        num_ocurrences, proxy=None):
        cmd = ["anontwi"]
        cmd.append('--ts=' + textsearch + " " + num_ocurrences)
        if proxy:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        self._create_options(cmd)
        app = self.get_app()
        messages = app.search_messages()
        return messages

    def generate_key(self):
        key = generate_key()
        return key

    def search_topics(self, proxy=None):
        cmd = ["anontwi"]
        cmd.append('--tt')
        if proxy:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        self._create_options(cmd)
        app = self.get_app()
        topics = app.search_topics()
        trendingtopics = ""
        for t in topics:
            for item in t.timestamp["trends"]:
                self.topic = item["name"]
                trendingtopics = trendingtopics + self.topic + '\n'
        return trendingtopics

    def home_timeline(self, num, proxy=None):
        cmd = ["anontwi"]
        cmd.append("--tf")
        if proxy:
            cmd.append('--proxy=' + proxy)
        self.log.debug('[Home] CMD: ' + str(cmd))
        self._create_options(cmd)
        app = self.get_app()
        self.log.debug('[Home] Creating app: OK')
        (timelines, n) = app.show_timeline_friends()
        self.log.debug('[Home] Return lines: ' + str(timelines))
        return timelines, num

    def search_favorite(self, user, num_ocurrences, proxy=None):
        cmd = ["anontwi"]
        cmd.append('--tfav=' + user + " " + num_ocurrences)
        if proxy:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        self.log.debug('[Favorites] CMD: ' + str(cmd)) 
        self._create_options(cmd)
        app = self.get_app()
        self.log.debug('[Favorites] Creating app: OK')
        favorites = app.show_favorites()
        self.log.debug('[Favorites] Return lines: ' + str(favorites))
        return favorites

    def mentions(self, num_ocurrences, proxy=None):
        cmd = ["anontwi"]
        cmd.append("--me=" + num_ocurrences)
        if proxy:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        self.log.debug('[Mentions] CMD: ' + str(cmd))
        self._create_options(cmd)
        app = self.get_app()
        self.log.debug('[Mentions] Creating app: OK')
        (mentions,num) = app.show_mentions()
        self.log.debug('[Mentions] Return lines: ' + str(mentions))
        return mentions, num

    def show_private(self, num_ocurrences, proxy=None):
        cmd = ["anontwi"]
        cmd.append('--td=' + num_ocurrences)
        if proxy:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        self.log.debug('[Private] CMD: ' + str(cmd))
        self._create_options(cmd)
        app = self.get_app()
        dms = app.show_timelinedm()
        self.log.debug('[Private] Creating app: OK')
        self.log.debug('[Private] Return lines: ' + str(dms))
        return dms

    def show_public(self, user, num_ocurrences, proxy=None):
        cmd = ["anontwi"]
        cmd.append('--tu=' + user + " " + num_ocurrences)
        if proxy:
            cmd.append('--proxy=' + proxy)
        self.log.debug('[Public] CMD: ' + str(cmd))
        self._create_options(cmd)
        app = self.get_app()
        self.log.debug('[Public] Creating app: OK')
        tweets = app.show_timeline()
        self.log.debug('[Public] Return lines: ' + str(tweets))
        return tweets

    def short_url(self, url, proxy=None):
        cmd = ['anontwi']
        cmd.append('--short=' + url) 
        if proxy:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        print "CMD ", cmd
        self._create_options(cmd)
        app = self.get_app()
        short_url = app.short_url()
        self.log.debug('[Shorten URL] Shorten URL: ' + str(short_url))
        return short_url

    def suicide(self, proxy=None):
        cmd = ['anontwi']
        cmd.append('--suicide')
        if proxy:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        self._create_options(cmd)
        app = self.get_app()
        topics = app.suicide(self)
        self.log.debug('[Suicide]')

    def follow(self, user, proxy=None):
        cmd = ['anontwi']
        cmd.append('-f')
        cmd.append(user)
        if proxy:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        self._create_options(cmd)
        app = self.get_app()
        status = app.set_friend()
        self.log.debug('[Follow]' + str(user))
        return status

    def unfollow(self, user, proxy=None):
        cmd = ['anontwi']
        cmd.append('-u')
        cmd.append(user)
        if proxy:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        self._create_options(cmd)
        app = self.get_app()
        status = app.remove_friend()
        self.log.debug('[Unfollow]' + str(user))
        return status

    def block(self, user, proxy=None):
        cmd = ['anontwi']
        cmd.append('--block=' + user)
        if proxy:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        self._create_options(cmd)
        app = self.get_app()
        status = app.set_friend()
        self.log.debug('[Block]' + str(user))
        return status

    def unblock(self, user, proxy=None):
        cmd = ['anontwi']
        cmd.append('--unblock=' + user)
        if proxy:
            cmd.append('--proxy=' + proxy['ip_address'] + ':' + proxy['port'])
        self._create_options(cmd)
        app = self.get_app()
        status = app.remove_friend()
        self.log.debug('[Unblock]' + str(user))
        return status

    def IRCdeploy(self, user, host, port, chan):
        app = self.get_app()
        AnonBot = app.IRCdeploy(user, host, port, chan)
        return AnonBot
