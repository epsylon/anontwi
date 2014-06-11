#!/usr/bin/python
# -*- coding: utf8 -*-
"""
Copyright (C) 2012 Jhonny5 <jhonny5@riseup.net> + epsylon <epsylon@riseup.net>
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
import urllib2
import logging
import HTMLParser
from core.gtk.config_gtk import *
from core.wrapper import WrapperAnontwi
from core.encrypt import Cipher, generate_key

try:
    import gtk, gtk.glade
except:
    print ("Gkt / Glade  not found\n")
    sys.exit(1)
#print ("Gtk / GLade found.")

WIN_TITLE = "AnonTwi v1.0 - GTK"

# proxy globals
hProxyOn = False
proxyServer = None
proxyPort = None

class GuiUtils(object):
    @staticmethod
    def GetBuilder(name):
        builder = gtk.Builder()
        #print path + '/gtk/' + name + '.xml'
        if not builder.add_from_file(PATH_APP + DIR_GTK + name + '.xml'):
            print 'XML file not found!'
            sys.exit(1)
        else:
            return builder

    @staticmethod
    def Error(title, text):
        """Show error popup"""
        dialog = gtk.MessageDialog(
            parent         = None,
            flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
            type           = gtk.MESSAGE_ERROR,
            buttons        = gtk.BUTTONS_OK,
            message_format = text)
        dialog.set_title(title)
        dialog.connect('response', lambda dialog, response: dialog.destroy())
        dialog.show()
        print text
    
    @staticmethod
    def Info(title, text):
        """Show info popup"""
        dialog = gtk.MessageDialog(
            parent         = None,
            flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
            type           = gtk.MESSAGE_INFO,
            buttons        = gtk.BUTTONS_OK,
            message_format = text)
        dialog.set_title(title)
        dialog.connect('response', lambda dialog, response: dialog.destroy())
        dialog.show()
 
    @staticmethod
    def Loading(title, text):
        """Show loading popup"""
        dialog = gtk.MessageDialog(
            parent         = None,
            flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
            type           = gtk.MESSAGE_INFO,
            buttons        = gtk.BUTTONS_NONE,
            message_format = text)
        dialog.set_title(title)
        dialog.connect('response', lambda dialog, response: dialog.destroy())
        dialog.show()
        return dialog

    @staticmethod
    def Warning(title, text):
        """Show warning popup"""
        dialog = gtk.MessageDialog(
            parent         = None,
            flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
            type           = gtk.MESSAGE_WARNING,
            buttons        = gtk.BUTTONS_OK,
            message_format = text)
        dialog.set_title(title)
        dialog.connect('response', lambda dialog, response: dialog.destroy())
        dialog.show()
        return dialog

    @staticmethod
    def Question(title, text):
        """Show question popup"""
        dialog = gtk.MessageDialog(
            parent         = None,
            flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
            type           = gtk.MESSAGE_QUESTION,
            buttons        = gtk.BUTTONS_YES_NO,
            message_format = text)
        dialog.set_title(title)
        dialog.connect('response', lambda dialog, response: dialog.destroy())
        dialog.show()
        return dialog

class GuiStarter(object):
    """
    Init the starter GUI box before to connect externally to any API.
    """
    def __init__(self):
        """
        Start the GUI up and set the connections with the components.
        """
        # export env tokens from file to shell
        self.wrapper = WrapperAnontwi()
        acc_tokens = self.wrapper.get_access_tokens()
        os.environ['ANONTWI_TOKEN_KEY'] = acc_tokens["access_token"]
        os.environ['ANONTWI_TOKEN_SECRET'] = acc_tokens["secret_token"]

        builder = GuiUtils.GetBuilder('wStart')
        self.log = logging.getLogger('GTK Starter Window') 

        # get objects
        self.window = builder.get_object('wStart')
        self.eUser = builder.get_object('eUser')
        self.cProxy = builder.get_object('cProxy')
        self.hProxy = builder.get_object('hProxy')
        self.eServer = builder.get_object('eServer')
        self.ePort = builder.get_object('ePort')
        self.bConnect = builder.get_object('bConnect')
        self.iAnontwi = builder.get_object('iAnontwi')

        # defaults
        self.hProxy.set_visible(False)

        # signals
        self.toggled = 0
        self.cProxy.connect('toggled', lambda w: self.switch('Proxy'))
        self.bConnect.connect('clicked', lambda w: self.Next())
        self.window.connect('destroy', lambda w: gtk.main_quit())

        # AnonTwi image
        self.iAnontwi.set_from_file(PATH_APP + DIR_GTK_IMG + 'anontwi_small.png')
        self.Show()

    def switch(self, layer):
        if self.toggled is 0:
            self.toggled = 1
            self.hProxy.set_visible(not self.hProxy.get_visible())
            global hProxyOn
            hProxyOn = True
            global proxyServer
            proxyServer = self.eServer.get_text()
            global proxyPort
            proxyPort = self.ePort.get_text()
        else:
            self.toggled = 0
            self.hProxy.set_visible(not self.hProxy.get_visible())
            global hProxyOn
            hProxyOn = False
            global proxyServer
            proxyServer = None
            global proxyPort
            proxyPort = None
            self.eServer.set_text("http://127.0.0.1")
            self.ePort.set_text("8118")

    def Show(self):
        self.window.set_icon_from_file(PATH_APP + DIR_GTK_IMG + 'anontwi_ico.png')
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_title(WIN_TITLE)
        self.window.show()

    def Next(self):
        global proxyServer
        global proxyPort
        if proxyServer is not None or proxyPort is not None:
            proxyServer = self.eServer.get_text()
            proxyPort = self.ePort.get_text()
        self.window.hide()
        self.log.debug('Loading user information...') 
        load_dialog = GuiUtils.Loading("Loading Data...Please wait", "Retrieving user information: Done!\n\nBuilding Interface: Done!\n\nUpdating home: Done!") 
        gui_main = GuiMain()
        gui_main.Show()
        load_dialog.destroy()

class GuiMain(object):
    """
    Init the GUI interface and connect properties.
    """
    def __init__(self):
        """
        Start the GUI up and set the connections with the components.
        """
        builder = GuiUtils.GetBuilder('wMain')
        self.log = logging.getLogger('GTK Main') 

        # get objects
        self.window = builder.get_object('wMain')
        self.tvTweet = builder.get_object('tEntryTweet')
        self.tvTweetDec = builder.get_object('tvTweetDec')
        self.tvDecrypt = builder.get_object('tvDecrypt')
        self.tvDecrypted = builder.get_object('tvDecrypted')
        self.tbPinEncrypt = builder.get_object('tbPinEncrypt')
        self.tbPinDecrypt = builder.get_object('tbPinDecrypt')
        self.bDecrypt = builder.get_object('bDecrypt')
        self.bSend = builder.get_object('bSend')
        self.cWave = builder.get_object('cWave')
        self.tbIPAddress = builder.get_object('tbIPAddress')
        self.tbPort = builder.get_object('tbPort')
        self.rbTweet = builder.get_object('rbTweet')
        self.rbPM = builder.get_object('rbPM')
        self.tbPM = builder.get_object('tbPM')
        self.hbPM = builder.get_object('hbPM')
        self.hbMDM = builder.get_object('hbMDM')
        self.hbLDM = builder.get_object('hbLDM')
        self.chkMdm = builder.get_object('chkMdm')
        self.chkGps = builder.get_object('chkGps')
        self.chkCipher = builder.get_object('chkCipher')
        self.chkTor = builder.get_object('chkTor')
        self.hbPin = builder.get_object('hbPin')
        self.hbTor = builder.get_object('hbTor')
        self.vbDecryptedMsg = builder.get_object('vbDecryptedMsg')        
        self.lNick = builder.get_object('lNick')
        self.lName = builder.get_object('lName')
        self.taDescription = builder.get_object('taDescription')
        self.lFollowers = builder.get_object('lFollowers')
        self.lFriends = builder.get_object('lFriends')
        self.iAvatar = builder.get_object('iAvatar')
        self.lTweets = builder.get_object('lTweets')
        self.lNumChars = builder.get_object('lNumChars')
        self.lNumWaves = builder.get_object('lNumWaves')
        self.iAnontwi = builder.get_object('iAnontwi')
        self.bRandomPin = builder.get_object('bRandomPin')
        self.bRefreshTopics = builder.get_object('bRefreshTopics')
        self.lTrendingTopics = builder.get_object('lTrendingTopics')
        self.eTermsSearch = builder.get_object('eTermsSearch')
        self.sSearch = builder.get_object('sSearch')
        self.taSearch = builder.get_object('taSearch')
        self.eIdSearch = builder.get_object('eIdSearch')
        self.bReplySearch = builder.get_object('bReplySearch')
        self.bReplyHome = builder.get_object('bReplyHome')
        self.bReplyPublic = builder.get_object('bReplyPublic')
        self.bReplyPrivate = builder.get_object('bReplyPrivate')
        self.bReplyMentions = builder.get_object('bReplyMentions')
        self.bReplyFavorites = builder.get_object('bReplyFavorites')
        self.bFavoriteHome = builder.get_object('bFavoriteHome')
        self.bFavoritePublic = builder.get_object('bFavoritePublic')
        self.bFavoriteMentions = builder.get_object('bFavoriteMentions')
        self.bFavoriteFavorites = builder.get_object('bFavoriteFavorites')
        self.bFavoriteSearch = builder.get_object('bFavoriteSearch')
        self.bUnFavoriteHome = builder.get_object('bUnFavoriteHome')
        self.bUnFavoritePublic = builder.get_object('bUnFavoritePublic')
        self.bUnFavoriteMentions = builder.get_object('bUnFavoriteMentions')
        self.bUnFavoriteFavorites = builder.get_object('bUnFavoriteFavorites')
        self.bUnFavoriteSearch = builder.get_object('bUnFavoriteSearch')
        self.bSearchFavorites = builder.get_object('bSearchFavorites')
        self.bTry = builder.get_object('bTry')
        self.bSave = builder.get_object('bSave')
        self.eIdHome = builder.get_object('eIdHome')
        self.eIdPublic = builder.get_object('eIdPublic')
        self.eIdPrivate = builder.get_object('eIdPrivate')
        self.eIdMentions = builder.get_object('eIdMentions')
        self.eIdFavorites = builder.get_object('eIdFavorites')
        self.bHome = builder.get_object('bHome')
        self.sHome = builder.get_object('sHome')
        self.taHome = builder.get_object('taHome')
        self.sFavorites = builder.get_object('sFavorites')
        self.taFavorites = builder.get_object('taFavorites')
        self.taMentions = builder.get_object('taMentions')
        self.sMentions = builder.get_object('sMentions')
        self.bSearchMentions = builder.get_object('bSearchMentions')
        self.sPrivate = builder.get_object('sPrivate')
        self.taPrivate = builder.get_object('taPrivate')
        self.bSearchPrivate = builder.get_object('bSearchPrivate')
        self.sPublic = builder.get_object('sPublic')
        self.taPublic = builder.get_object('taPublic')
        self.taSave = builder.get_object('taSave')
        self.sSave = builder.get_object('sSave')
        self.eUserPrivate =  builder.get_object('eUserPrivate')
        self.bSearchPublic = builder.get_object('bSearchPublic')
        self.eUserPublic =  builder.get_object('eUserPublic')
        self.eUserFavorites = builder.get_object('eUserFavorites')
        self.eUserSave = builder.get_object('eUserSave')
        self.bShortUrl = builder.get_object('bShortUrl')
        self.bDraft = builder.get_object('bDraft')
        self.tvShortUrl = builder.get_object('textview4')
        self.eShortUrl = builder.get_object('entry3')
        self.tbID = builder.get_object('tbID')
        self.bRetweetHome = builder.get_object('bRetweetHome')
        self.bRetweetPublic = builder.get_object('bRetweetPublic')
        self.bRetweetMentions = builder.get_object('bRetweetMentions')
        self.bRetweetFavorites = builder.get_object('bRetweetFavorites')
        self.bRetweetSearch = builder.get_object('bRetweetSearch')
        self.bDeleteHome = builder.get_object('bDeleteHome')
        self.bDeletePublic = builder.get_object('bDeletePublic')
        self.bDeletePrivate = builder.get_object('bDeletePrivate')
        self.bFollowPublic = builder.get_object('bFollowPublic')
        self.bUnfollowPublic = builder.get_object('bUnfollowPublic')
        self.bBlockPublic = builder.get_object('bBlockPublic')
        self.bUnblockPublic = builder.get_object('bUnblockPublic')        
        self.bSuicide = builder.get_object('bSuicide')
        self.tbIPAddress = builder.get_object('tbIPAddress')
        self.tbPort = builder.get_object('tbPort')
#        self.eIRCNick = builder.get_object('eIRCNick')
#        self.eIRCServer = builder.get_object('eIRCServer')
#        self.eIRCport = builder.get_object('eIRCport')
#        self.eIRCchannel = builder.get_object('eIRCchannel')
#        self.bIRCDeploy = builder.get_object('bIRCDeploy')
#        self.taIRC = builder.get_object('taIRC')
#        self.tabIRCKill = builder.get_object('bIRCKill')

        # signals
        self.bSend.connect('clicked', lambda w: self.send_tweet())
        self.window.connect('destroy', lambda w: gtk.main_quit())
        self.chkCipher.connect('toggled', lambda w: self.switch('Cipher'))
        self.chkTor.connect('toggled', lambda w: self.switch('Tor'))
        self.rbPM.connect('toggled', lambda w: self.switch('PM'))
        self.rbTweet.connect('toggled', lambda w: self.tweet_mdm())
        self.bDecrypt.connect('clicked', lambda w: self.decrypt())
        self.bRandomPin.connect('clicked', lambda w: self.generate_key())
        self.bTry.connect('clicked', lambda w: self.search_messages())
        self.bSave.connect('clicked', lambda w: self.save_messages())
        self.bHome.connect('clicked', lambda w: self.home_timelines())
        self.bRefreshTopics.connect('clicked', lambda w: self.search_topics())
        self.bSearchFavorites.connect('clicked', lambda w: self.search_favorites())
        self.bSearchMentions.connect('clicked', lambda w: self.mentions())
        self.bSearchPrivate.connect('clicked', lambda w: self.privates())
        self.bSearchPublic.connect('clicked', lambda w: self.public_timelines())
        self.bShortUrl.connect('clicked', lambda w: self.short_url())
        self.bReplySearch.connect('clicked', lambda w: self.on_bReplySearch_pressed())
        self.bReplyHome.connect('clicked', lambda w: self.on_bReplyHome_pressed())
        self.bReplyPublic.connect('clicked', lambda w: self.on_bReplyPublic_pressed())
        self.bReplyPrivate.connect('clicked', lambda w: self.on_bReplyPrivate_pressed())
        self.bReplyMentions.connect('clicked', lambda w: self.on_bReplyMentions_pressed())
        self.bReplyFavorites.connect('clicked', lambda w: self.on_bReplyFavorites_pressed())
        self.bRetweetHome.connect('clicked', lambda w: self.on_bRetweetHome_pressed())
        self.bRetweetPublic.connect('clicked', lambda w: self.on_bRetweetPublic_pressed())
        self.bRetweetFavorites.connect('clicked', lambda w: self.on_bRetweetFavorites_pressed())
        self.bRetweetMentions.connect('clicked', lambda w: self.on_bRetweetMentions_pressed())
        self.bRetweetSearch.connect('clicked', lambda w: self.on_bRetweetSearch_pressed())
        self.bDeleteHome.connect('clicked', lambda w: self.on_bDeleteHome_pressed())
        self.bDeletePublic.connect('clicked', lambda w: self.on_bDeletePublic_pressed())
        self.bDeletePrivate.connect('clicked', lambda w: self.on_bDeletePrivate_pressed())
        self.bFavoriteHome.connect('clicked', lambda w: self.on_bFavoriteHome_pressed())
        self.bFavoritePublic.connect('clicked', lambda w: self.on_bFavoritePublic_pressed())
        self.bFavoriteFavorites.connect('clicked', lambda w: self.on_bFavoriteFavorites_pressed())
        self.bFavoriteMentions.connect('clicked', lambda w: self.on_bFavoriteMentions_pressed())
        self.bFavoriteSearch.connect('clicked', lambda w: self.on_bFavoriteSearch_pressed())
        self.bUnFavoriteHome.connect('clicked', lambda w: self.on_bUnFavoriteHome_pressed())
        self.bUnFavoritePublic.connect('clicked', lambda w: self.on_bUnFavoritePublic_pressed())
        self.bUnFavoriteFavorites.connect('clicked', lambda w: self.on_bUnFavoriteFavorites_pressed())
        self.bUnFavoriteMentions.connect('clicked', lambda w: self.on_bUnFavoriteMentions_pressed())
        self.bUnFavoriteSearch.connect('clicked', lambda w: self.on_bUnFavoriteSearch_pressed())
        self.bFollowPublic.connect('clicked', lambda w: self.on_bFollowPublic_pressed())
        self.bUnfollowPublic.connect('clicked', lambda w: self.on_bUnfollowPublic_pressed())
        self.bBlockPublic.connect('clicked', lambda w: self.on_bBlockPublic_pressed())
        self.bUnblockPublic.connect('clicked', lambda w: self.on_bUnblockPublic_pressed())
        self.bSuicide.connect('clicked', lambda w: self.on_bSuicide_pressed())
        self.bDraft.connect('clicked', lambda w: self.draft_tweet())
        self.cWave.connect('clicked', lambda w: self.on_cWave_toggled())
        self.chkGps.connect('clicked', lambda w: self.on_chkGps_toggled())
#        self.bIRCDeploy.connect('clicked', lambda w: self.on_bIRCDeploy_pressed())
        self.chkMdm.connect('clicked', lambda w: self.on_chkMdm_toggled())

        # defaults
        self.hbPin.set_visible(False)
        self.hbTor.set_visible(False)
        self.hbPM.set_visible(False)
        self.hbMDM.set_visible(False)
        self.hbLDM.set_visible(False)
        self.chkGps.set_visible(True)
        self.tbPinEncrypt.set_max_length(44)
        self.tbPinDecrypt.set_max_length(44)
        self.eTermsSearch.set_text('#AnonTwi')

        # some proxy output issues
        if hProxyOn == True:
            self.chkTor.set_active(True)
        ps = proxyServer
        if ps is not None:
            self.tbIPAddress.set_text(str(ps))
        else:
            self.tbIPAddress.set_text("http://127.0.0.1")
        pp = proxyPort
        if pp is not None:
            self.tbPort.set_text(str(pp))
        else:
            self.tbPort.set_text("8118")

        # buttons default off
        self.bReplySearchOn = False
        self.bReplyHomeOn = False
        self.bReplyPublicOn = False
        self.bReplyPrivateOn = False
        self.bReplyMentionsOn = False
        self.bReplyFavoritesOn = False
        self.bDeleteHomeOn = False
        self.bDeletePublicOn = False
        self.bDeletePrivateOn = False
        self.bRetweetHomeOn = False
        self.bRetweetPublicOn = False
        self.bRetweetMentionsOn = False
        self.bRetweetFavoritesOn = False
        self.bRetweetSearchOn = False
        self.bFavoriteHomeOn = False
        self.bFavoritePublicOn = False
        self.bFavoriteMentionsOn = False
        self.bFavoriteFavoritesOn = False
        self.bFavoriteSearchOn = False
        self.bUnFavoriteHomeOn = False
        self.bUnFavoritePublicOn = False
        self.bUnFavoriteMentionsOn = False
        self.bUnFavoriteFavoritesOn = False
        self.bUnFavoriteSearchOn = False
        self.bFollowPublicOn = False
        self.bUnfollowPublicOn = False
        self.bBlockPublicOn = False
        self.bUnblockPublicOn = False
        self.cWaveOn = False
#        self.bIRCDeployOn = False

        # spinners
        self.sSearch.set_range(1, 50)
        self.sSearch.set_value(5)  
        self.sSearch.set_increments(1, 1)
        self.sFavorites.set_range(1, 50)
        self.sFavorites.set_value(5)                   
        self.sFavorites.set_increments(1, 1)
        self.sMentions.set_range(1, 50)
        self.sMentions.set_value(5)                   
        self.sMentions.set_increments(1, 1)
        self.sPrivate.set_range(1, 50)
        self.sPrivate.set_value(5)                   
        self.sPrivate.set_increments(1, 1)
        self.sPublic.set_range(1, 50)
        self.sPublic.set_value(5)                   
        self.sPublic.set_increments(1, 1)
        self.sHome.set_range(1, 50)
        self.sHome.set_value(5)                   
        self.sHome.set_increments(1, 1)
        self.sSave.set_range(1, 3200)
        self.sSave.set_value(15)                   
        self.sSave.set_increments(1, 1)
        
        # AnonTwi image
        self.iAnontwi.set_from_file(PATH_APP + DIR_GTK_IMG + 'anontwi_small.png')

        self.log.debug('Runing main Window')
        self.Show()
        self.Begin()
       
    def setTextLength(self, length):
        self.tbPin.set_max_length(length)

    def switch(self, layer):
        if layer == 'Cipher':
            self.hbPin.set_visible(not self.hbPin.get_visible())
        if layer == 'Tor': 
            self.hbTor.set_visible(not self.hbTor.get_visible())
        if layer == 'PM':
            self.hbPM.set_visible(True)
            self.hbMDM.set_visible(True)
            self.hbLDM.set_visible(True)
            self.chkGps.set_visible(not self.chkGps.get_visible())

    def Show(self):
        self.window.set_icon_from_file(PATH_APP + DIR_GTK_IMG + 'anontwi_ico.png')
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_size_request(800, 600)
        self.window.set_title(WIN_TITLE)
        self.window.show() #move to another place

    def Begin(self):
        # checking if 'temp' tokens are on correct position
        if os.getenv("ANONTWI_TOKEN_KEY") is None and os.getenv("ANONTWI_TOKEN_SECRET") is None: 
            GuiUtils.Warning("Warning: AnonTwi cannot authenticate you correctly!", "There is a problem with your tokens.\n\n You must provide a correct 'ANONTWI_TOKEN_KEY' and 'ANONTWI_TOKEN_SECRET' environment variables to the shell that launchs this GTK interface.\n\n - On Unix: \n export ANONTWI_TOKEN_KEY=Value\n export ANONTWI_TOKEN_SECRET=Value \n\n - On Win32: \n set ANONTWI_TOKEN_KEY=Value\n set ANONTWI_TOKEN_SECRET=Value\n\nTry: anontwi --tokens on shell mode, if you don't understand this error.")
            return
        if os.getenv("ANONTWI_TOKEN_KEY") is None:
            GuiUtils.Warning("Warning: AnonTwi cannot authenticate you correctly!", "There is a problem with tokens. You must provide a correct 'ANONTWI_TOKEN_KEY' environment variable to the shell that launchs this GTK interface.\n\n - On Unix: \n export ANONTWI_TOKEN_KEY=Value \n\n - On Win32: \n set ANONTWI_TOKEN_KEY=Value\n\nTry: anontwi --tokens on shell mode, if you don't understand this error.")
            return
        elif os.getenv("ANONTWI_TOKEN_SECRET") is None:          
            GuiUtils.Warning("Warning: AnonTwi cannot authenticate you correctly!", "There is a problem with tokens. You must provide a correct 'ANONTWI_TOKEN_SECRET' environment variable to the shell that launchs this GTK interface.\n\n - On Unix: \n export ANONTWI_TOKEN_SECRET=Value \n\n - On Win32: \n set ANONTWI_TOKEN_SECRET=Value\n\nTry: anontwi --tokens on shell mode, if you don't understand this error.")
            return
        try:
            # defaults - user info
            self.wrapper = WrapperAnontwi()
            source_api = self.wrapper.get_source_api()
            self.log.debug('Loading user information...')
            if proxyServer is None or proxyPort is None:
                proxy = None
            else:
                proxy = str(proxyServer + ":" + proxyPort)
            user_info = self.wrapper.get_user_info(proxy)
            if proxy is not None:
                self.log.debug('Profile loaded with proxy: ' + proxy) 
            self.lName.set_text(str(user_info['nickid']))
            if source_api["source_api"] == 'identi.ca/api':
                self.lNick.set_text(str(user_info['user']))
            else:
                self.lNick.set_text(str("@" + user_info['user']))
            # description buffer
            tb = gtk.TextBuffer()
            description = str(user_info['description'])
            self.taDescription.get_buffer().set_text(description)
            # default input forms values extracted from user info
            if source_api["source_api"] == 'identi.ca/api':
                self.eUserFavorites.set_text(str(user_info['user']))
                self.eUserSave.set_text(str(user_info['user']))
                self.eUserPublic.set_text(str(user_info['user']))
            else:
                self.eUserFavorites.set_text(str("@" + user_info['user']))
                self.eUserSave.set_text(str("@" + user_info['user']))
                self.eUserPublic.set_text(str("@" + user_info['user']))
            self.lFollowers.set_text(str(user_info['followers']))
            self.lFriends.set_text(str(user_info['friends']))
            self.lTweets.set_text(str(user_info['statuses_count']))
            # default - user profile picture
            response = urllib2.urlopen(user_info['url_profile'])
            loader = gtk.gdk.PixbufLoader()
            loader.write(response.read())
            loader.close()
            self.iAvatar.set_from_pixbuf(loader.get_pixbuf())   
        except:
            GuiUtils.Error("Error", "Could not retrieve user profile information.\n\nCheck your TOKENS and proxy settings and restart AnonTwi.")
            return

        # launch timelines by default
        self.home_timelines()
        self.public_timelines()
            
    def on_cWave_toggled(self):
        self.cWaveOn = True

    def on_chkGps_toggled(self):
        self.chkGpsOn = True

    def draft_tweet(self):
        tb = gtk.TextBuffer()
        textbuffer = self.tvTweet.get_buffer()
        tweet = textbuffer.get_text(textbuffer.get_start_iter() , textbuffer.get_end_iter())
        enc = { 'enc' : self.chkCipher.get_active(),
                'pin' : self.tbPinEncrypt.get_text(), }
        self.lenght_tweet = len(tweet)
        if self.lenght_tweet == 0:
            self.num_tweets = 0
        else:
            if enc["enc"] is True:
                if enc["pin"] is "":
                    GuiUtils.Info("Encrypting message!", "You must enter a key for your encrypted message before to calculate how much long is it.")
                    return
                else:
                    try:
                        self.log.debug("[Encrypting message!]: Starting to cipher...")    
                        if tweet is not None:
                            if int(self.lenght_tweet) > 69:
                                self.num_tweets_enc = ">140" #count cipher characters
                                self.lNumChars.set_text(str(self.num_tweets_enc))
                                self.lNumWaves.set_text(">1")
                                GuiUtils.Error("Warning on ciphered messages", "Remember that encrypted data has more lenght that your original message.\n\n Characters: 140 plain text = 69 chipered.\n\nThis is to keep strong the encryption algorithm.\n\nTry to remove some characters of your message and re-count again.")
                                return
                            else:
                                self.num_tweets_enc = "<140" #count cipher characters
                                self.lNumChars.set_text(str(self.num_tweets_enc))
                                self.lNumWaves.set_text("1") #btm, only 1 ciphered message by 140 characters
                    except:
                        GuiUtils.Error("Error!", " PIN key is incorrect. Use 'Random Secret!' button to generate a valid one.")
                        return
            else:
                self.num_tweets = int(self.lenght_tweet/141) +1 #140 characters/tweet
                self.lNumChars.set_text(str(self.lenght_tweet))
                self.lNumWaves.set_text(str(self.num_tweets))

    def send_mdm(self):
        tb = gtk.TextBuffer()
        textbuffer = self.tvTweet.get_buffer()
        tweet = textbuffer.get_text(textbuffer.get_start_iter() , textbuffer.get_end_iter())
        user = str(self.eUserPublic.get_text())
        enc = { 'enc' : self.chkCipher.get_active(),
                'pin' : self.tbPinEncrypt.get_text(), }
        pm = { 'pm' : self.rbPM.get_active(),
               'user' : user, }
        proxy = { 'proxy' : self.chkTor.get_active(),
                  'ip_address' : self.tbIPAddress.get_text(),
                  'port' : self.tbPort.get_text() }

        if proxy['proxy'] is False:
            proxy = None
        self.lenght_tweet = len(tweet)
        if self.lenght_tweet == 0:
            self.num_tweets = 0
        else:
            if enc["enc"] is True:
                if enc["pin"] is "":
                    GuiUtils.Info("Encrypting message!", "You must enter a key for your encrypted message before to calculate how much long is it.")
                    return
                else:
                    try:
                        self.log.debug("[Encrypting message!]: Starting to cipher...")    
                        if tweet is not None:
                            if int(self.lenght_tweet) > 69:
                                self.num_tweets_enc = ">140" #count cipher characters
                                self.lNumChars.set_text(str(self.num_tweets_enc))
                                self.lNumWaves.set_text(">1")
                                GuiUtils.Error("Warning on ciphered messages", "Remember that encrypted data has more lenght that your original message.\n\n Characters: 140 plain text = 69 chipered.\n\nThis is for keep strong the encryption algorithm.\n\nTry to remove some characters of your message and re-count again.")
                                return
                            else:
                                self.num_tweets_enc = "<140" #count cipher characters
                                self.lNumChars.set_text(str(self.num_tweets_enc))
                                self.lNumWaves.set_text("1") #btm, only 1 ciphered message by 140 characters
                    except:
                        GuiUtils.Error("Error!", " PIN key is incorrect. Use 'Random Secret!' button to generate a valid one.")
                        return
            else:
                self.num_tweets = int(self.lenght_tweet/141) +1 #140 characters/tweet
                self.lNumChars.set_text(str(self.lenght_tweet))
                self.lNumWaves.set_text(str(self.num_tweets))
        try:
            # check lenght of message and if waves are required.
            if self.lenght_tweet > 140:
                GuiUtils.Error("Error: Private messages restriction!", "Your message has more than 140 characters. Try to short it.")
                return
            else:
                msg = self.wrapper.send_mdm(tweet, pm, enc, proxy)
                if pm['pm'] is not False:
                    GuiUtils.Info("Private sent!", "Massively private direct message to friends sent!")

                # removing message and restarting counters
                textbuffer = self.tvTweet.get_buffer().set_property("text", "")
                self.lenght_tweet = 0
                self.num_tweets = 0
                self.lNumChars.set_text(str(self.lenght_tweet))
                self.lNumWaves.set_text(str(self.num_tweets))
                if pm['pm'] is not False: #refresh privates timeline
                    self.privates()
        except:
            if pm["pm"] is not False:
                GuiUtils.Error("Error!", "Something went wrong with your massively private direct message! :(") 
            return       

    def send_tweet(self):
        if self.chkMdm.get_active():
            self.send_mdm()
        else:
            tb = gtk.TextBuffer()
            textbuffer = self.tvTweet.get_buffer()
            tweet = textbuffer.get_text(textbuffer.get_start_iter() , textbuffer.get_end_iter())
            enc = { 'enc' : self.chkCipher.get_active(),
                    'pin' : self.tbPinEncrypt.get_text(), }
            pm = { 'pm' : self.rbPM.get_active(),
                   'user' : self.tbPM.get_text(), }
            gps = self.chkGps.get_active()
            wave = self.cWave.get_active()
            proxy = { 'proxy' : self.chkTor.get_active(),
                      'ip_address' : self.tbIPAddress.get_text(),
                      'port' : self.tbPort.get_text() }

            if proxy['proxy'] is False:
                proxy = None
            self.lenght_tweet = len(tweet)
            if self.lenght_tweet == 0:
                self.num_tweets = 0
            else:
                if enc["enc"] is True:
                    if enc["pin"] is "":
                        GuiUtils.Info("Encrypting message!", "You must enter a key for your encrypted message before to calculate how much long is it.")
                        return
                    else:
                        try:
                            self.log.debug("[Encrypting message!]: Starting to cipher...")    
                            if tweet is not None:
                                if int(self.lenght_tweet) > 69:
                                    self.num_tweets_enc = ">140" #count cipher characters
                                    self.lNumChars.set_text(str(self.num_tweets_enc))
                                    self.lNumWaves.set_text(">1")
                                    GuiUtils.Error("Warning on ciphered messages", "Remember that encrypted data has more lenght that your original message.\n\n Characters: 140 plain text = 69 chipered.\n\nThis is for keep strong the encryption algorithm.\n\nTry to remove some characters of your message and re-count again.")
                                    return
                                else:
                                    self.num_tweets_enc = "<140" #count cipher characters
                                    self.lNumChars.set_text(str(self.num_tweets_enc))
                                    self.lNumWaves.set_text("1") #btm, only 1 ciphered message by 140 characters
                        except:
                            GuiUtils.Error("Error!", " PIN key is incorrect. Use 'Random Secret!' button to generate a valid one.")
                            return
                else:
                    self.num_tweets = int(self.lenght_tweet/141) +1 #140 characters/tweet
                    self.lNumChars.set_text(str(self.lenght_tweet))
                    self.lNumWaves.set_text(str(self.num_tweets))
            try:
                # check lenght of message and if waves are required.
                if self.cWaveOn == False and self.lenght_tweet > 140:
                    GuiUtils.Error("Error: Wave required", "Your message has more than 140 characters. You must activate waves mode to send it splitted by blocks.")
                    return
                else:
                    msg = self.wrapper.send_tweet(tweet, pm, gps, wave, enc, proxy)
                    if proxy is not None:
                        self.log.debug('Tweet sent with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])
                    if self.cWaveOn == True:
                        GuiUtils.Info("Wave sent!", "Wave sent correctly!")
                    else:
                        if pm['pm'] is not False:
                            GuiUtils.Info("Private sent!", "Private sent correctly!")
                        else:
                            GuiUtils.Info("Message sent!", "Message sent correctly!")
                    # removing message and restarting counters
                    textbuffer = self.tvTweet.get_buffer().set_property("text", "")
                    self.lenght_tweet = 0
                    self.num_tweets = 0
                    self.lNumChars.set_text(str(self.lenght_tweet))
                    self.lNumWaves.set_text(str(self.num_tweets))
                    if pm['pm'] is not False: #refresh privates timeline
                        self.privates()
                    else: # refresh the other options
                        self.home_timelines()
                        self.public_timelines()
            except:
                if self.cWaveOn == True:
                    GuiUtils.Error("Error!", "Something went wrong with your wave! :(")
                    return
                else:
                    if pm["pm"] is not False:
                        GuiUtils.Error("Error!", "Something went wrong with your private! :(") 
                    else:
                        GuiUtils.Error("Error!", "Something went wrong with your message! :(")
                    return       
    
    def decrypt(self):
        tb = gtk.TextBuffer()
        h = HTMLParser.HTMLParser()
        textbuffer = self.tvTweetDec.get_buffer()
        tweet = textbuffer.get_text(textbuffer.get_start_iter() , textbuffer.get_end_iter())

        if not self.tbPinDecrypt.get_text():
            GuiUtils.Error("Error!", "Pin is empty!")
            return
        elif not tweet:
            GuiUtils.Error("Error!", "Message is empty!")
            return
        try:
            msg = self.wrapper.decrypt(tweet, self.tbPinDecrypt.get_text())
        except:
            GuiUtils.Error("Error!", " PIN key is incorrect or message is corrupted")
            return
        m = h.unescape(msg)
        self.tvDecrypted.get_buffer().set_text(m)
        self.vbDecryptedMsg.set_visible(True)

    def on_chkMdm_toggled(self):
        self.hbPM.set_visible(not self.hbPM.get_visible())
        self.hbLDM.set_visible(not self.hbLDM.get_visible())

    def tweet_mdm(self):
        self.hbPM.set_visible(not self.hbPM.get_visible())
        self.hbMDM.set_visible(not self.hbMDM.get_visible())
        self.hbLDM.set_visible(False)
        self.chkMdm.set_active(False)

    def on_bReplySearch_pressed(self):
        self.ID = self.eIdSearch.get_text()
        self.bReplySearchOn = True
        self.reply()

    def on_bReplyHome_pressed(self):
        self.ID = self.eIdHome.get_text()
        self.bReplyHomeOn = True
        self.reply()

    def on_bReplyPublic_pressed(self):
        self.ID = self.eIdPublic.get_text()
        self.bReplyPublicOn = True
        self.reply()

    def on_bReplyPrivate_pressed(self):
        self.ID = self.eIdPrivate.get_text()
        self.bReplyPrivateOn = True
        self.reply()

    def on_bReplyMentions_pressed(self):
        self.ID = self.eIdMentions.get_text()
        self.bReplyMentionsOn = True
        self.reply()

    def on_bReplyFavorites_pressed(self):
        self.ID = self.eIdFavorites.get_text()
        self.bReplyFavoritesOn = True
        self.reply()
    
    def reply(self): #in all the tabs allowed
        try:
            ID = self.ID
            self.log.debug("[Reply] ID:", self.ID)
            tb = gtk.TextBuffer()
            textbuffer = self.tvTweet.get_buffer()
            tweet = textbuffer.get_text(textbuffer.get_start_iter() , textbuffer.get_end_iter())

            if not self.ID and not tweet:
                self.log.debug("[Reply] Except: not ID and not Text to send")
                raise 

            enc = { 'enc' : self.chkCipher.get_active(),
                    'pin' : self.tbPinEncrypt.get_text(), }
            gps = self.chkGps.get_active()
            proxy = { 'proxy' : self.chkTor.get_active(),
                      'ip_address' : self.tbIPAddress.get_text(),
                      'port' : self.tbPort.get_text() }

            replies = self.wrapper.reply(ID, tweet, gps, enc, proxy)
            if proxy['proxy'] is True:
                self.log.debug('Reply sent with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])
            if self.bReplySearchOn == True:
                buffer = self.taSearch.get_buffer().set_property("text", "")
                buffer = self.taSearch.get_buffer()
                self.bReplySearchOn = False

            if self.bReplyHomeOn == True:
                buffer = self.taHome.get_buffer().set_property("text", "")
                buffer = self.taHome.get_buffer()
                self.bReplyHomeOn = False

            if self.bReplyPublicOn == True:
                buffer = self.taPublic.get_buffer().set_property("text", "")
                buffer = self.taPublic.get_buffer()
                self.bReplyPublicOn = False

            if self.bReplyPrivateOn == True:
                buffer = self.taPrivate.get_buffer().set_property("text", "")
                buffer = self.taPrivate.get_buffer()
                self.bReplyPrivateOn = False

            if self.bReplyMentionsOn == True:
                buffer = self.taMentions.get_buffer().set_property("text", "")
                buffer = self.taMentions.get_buffer()
                self.bReplyMentionsOn = False        

            if self.bReplyFavoritesOn == True:
                buffer = self.taFavorites.get_buffer().set_property("text", "")
                buffer = self.taFavorites.get_buffer()
                self.bReplyFavoritesOn = False

            #iter = buffer.get_end_iter()
            #buffer.insert(iter, "\nReply sent correctly." + "\n" + "===============\n")
            GuiUtils.Info("Reply sent!", "Reply sent correctly!")
            self.home_timelines()
            self.public_timelines()
            # removing message and restarting counters
            textbuffer = self.tvTweet.get_buffer().set_property("text", "")
            self.lenght_tweet = 0
            self.num_tweets = 0
            self.lNumChars.set_text(str(self.lenght_tweet))
            self.lNumWaves.set_text(str(self.num_tweets))  
        except:
            GuiUtils.Error("Error!", "Could not make a reply! Check ID and @nick on message.")
            return

    def on_bRetweetHome_pressed(self):
        self.IDHome = self.eIdHome.get_text()
        self.bRetweetHomeOn = True
        self.retweet()

    def on_bRetweetPublic_pressed(self):
        self.IDPublic = self.eIdPublic.get_text()
        self.bRetweetPublicOn = True
        self.retweet()

    def on_bRetweetMentions_pressed(self):
        self.IDMentions = self.eIdMentions.get_text()
        self.bRetweetMentionsOn = True
        self.retweet()
 
    def on_bRetweetFavorites_pressed(self):
        self.IDFavorites = self.eIdFavorites.get_text()
        self.bRetweetFavoritesOn = True
        self.retweet()

    def on_bRetweetSearch_pressed(self):
        self.IDSearch = self.eIdSearch.get_text()
        self.bRetweetSearchOn = True
        self.retweet()
        
    def retweet(self):
        try:
            if self.bRetweetHomeOn == True:
                ID = self.IDHome
            elif self.bRetweetPublicOn == True:
                ID = self.IDPublic
            elif self.bRetweetMentionsOn == True:
                ID = self.IDMentions
            elif self.bRetweetFavoritesOn == True:
                ID = self.IDFavorites
            elif self.bRetweetSearchOn == True:
                ID = self.IDSearch
            self.log.debug("[Retweet] ID:" + ID)
            if not ID:
                self.log.debug("[Retweet] Except: not id")
                raise
            proxy = { 'proxy' : self.chkTor.get_active(),
                'ip_address' : self.tbIPAddress.get_text(),
                'port' : self.tbPort.get_text() }
            if proxy['proxy'] is False:
                proxy = None
            retweets = self.wrapper.retweet_tweet(ID, proxy)
            if proxy is not None:
                self.log.debug('Retweet sent with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])
            if self.bRetweetHomeOn == True:
                buffer = self.taHome.get_buffer().set_property("text", "")
                buffer = self.taHome.get_buffer()
                self.bRetweetHomeOn = False
            elif self.bRetweetPublicOn == True:
                buffer = self.taPublic.get_buffer().set_property("text", "")
                buffer = self.taPublic.get_buffer()
                self.bRetweetPublicOn = False
            elif self.bRetweetMentionsOn == True:
                buffer = self.taMentions.get_buffer().set_property("text", "")
                buffer = self.taMentions.get_buffer()
                self.bRetweetMentionsOn = False
            elif self.bRetweetFavoritesOn == True:
                buffer = self.taFavorites.get_buffer().set_property("text", "")
                buffer = self.taFavorites.get_buffer()
                self.bRetweetFavoritesOn = False
            elif self.bRetweetSearchOn == True:
                buffer = self.taSearch.get_buffer().set_property("text", "")
                buffer = self.taSearch.get_buffer()
                self.bRetweetSearchOn = False
            #iter = buffer.get_end_iter()
            #buffer.insert(iter, "\nRetweet sent correctly." + "\n" + "==============\n")
            GuiUtils.Info("Retweet sent!", "Retweet sent correctly!")
            self.home_timelines()
            self.public_timelines()
        except:
            GuiUtils.Error("Error!", "Could not retweet your message!")
            return

    def on_bFavoriteHome_pressed(self):
        self.IDHome = self.eIdHome.get_text()
        self.bFavoriteHomeOn = True
        self.favorite()

    def on_bFavoritePublic_pressed(self):
        self.IDPublic = self.eIdPublic.get_text()
        self.bFavoritePublicOn = True
        self.favorite()

    def on_bFavoriteMentions_pressed(self):
        self.IDMentions = self.eIdMentions.get_text()
        self.bFavoriteMentionsOn = True
        self.favorite()
 
    def on_bFavoriteFavorites_pressed(self):
        self.IDFavorites = self.eIdFavorites.get_text()
        self.bFavoriteFavoritesOn = True
        self.favorite()

    def on_bFavoriteSearch_pressed(self):
        self.IDSearch = self.eIdSearch.get_text()
        self.bFavoriteSearchOn = True
        self.favorite()
    
    def favorite(self):
        try:
            if self.bFavoriteHomeOn == True:
                ID = self.IDHome
            elif self.bFavoritePublicOn == True:
                ID = self.IDPublic
            elif self.bFavoriteMentionsOn == True:
                ID = self.IDMentions
            elif self.bFavoriteFavoritesOn == True:
                ID = self.IDFavorites
            elif self.bFavoriteSearchOn == True:
                ID = self.IDSearch
            self.log.debug("[Favorite] ID:" + ID)
            if not ID:
                self.log.debug("[Favorite] Except: not id")
                raise
            proxy = { 'proxy' : self.chkTor.get_active(),
                'ip_address' : self.tbIPAddress.get_text(),
                'port' : self.tbPort.get_text() }
            if proxy['proxy'] is False:
                proxy = None
            favorites = self.wrapper.favorite(ID, proxy)
            if proxy is not None:
                self.log.debug('Favorited with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])
            if self.bFavoriteHomeOn == True:
                buffer = self.taHome.get_buffer().set_property("text", "")
                buffer = self.taHome.get_buffer()
                self.bFavoriteHomeOn = False
            elif self.bFavoritePublicOn == True:
                buffer = self.taPublic.get_buffer().set_property("text", "")
                buffer = self.taPublic.get_buffer()
                self.bFavoritePublicOn = False
            elif self.bFavoriteMentionsOn == True:
                buffer = self.taMentions.get_buffer().set_property("text", "")
                buffer = self.taMentions.get_buffer()
                self.bFavoriteMentionsOn = False
            elif self.bFavoriteFavoritesOn == True:
                buffer = self.taFavorites.get_buffer().set_property("text", "")
                buffer = self.taFavorites.get_buffer()
                self.bFavoriteFavoritesOn = False
            elif self.bFavoriteSearchOn == True:
                buffer = self.taSearch.get_buffer().set_property("text", "")
                buffer = self.taSearch.get_buffer()
                self.bFavoriteSearchOn = False
            #iter = buffer.get_end_iter()
            #buffer.insert(iter, "\nMessage favorited correctly." + "\n" + "==============\n")
            GuiUtils.Info("Message favorited!", "Message favorited correctly!")
            self.search_favorites()   
        except:
            GuiUtils.Error("Error!", "Could not favorite your message!")
            return

    def on_bUnFavoriteHome_pressed(self):
        self.IDHome = self.eIdHome.get_text()
        self.bUnFavoriteHomeOn = True
        self.unfavorite()

    def on_bUnFavoritePublic_pressed(self):
        self.IDPublic = self.eIdPublic.get_text()
        self.bUnFavoritePublicOn = True
        self.unfavorite()

    def on_bUnFavoriteMentions_pressed(self):
        self.IDMentions = self.eIdMentions.get_text()
        self.bUnFavoriteMentionsOn = True
        self.unfavorite()
 
    def on_bUnFavoriteFavorites_pressed(self):
        self.IDFavorites = self.eIdFavorites.get_text()
        self.bUnFavoriteFavoritesOn = True
        self.unfavorite()

    def on_bUnFavoriteSearch_pressed(self):
        self.IDSearch = self.eIdSearch.get_text()
        self.bUnFavoriteSearchOn = True
        self.unfavorite()
    
    def unfavorite(self):
        try:
            if self.bUnFavoriteHomeOn == True:
                ID = self.IDHome
            elif self.bUnFavoritePublicOn == True:
                ID = self.IDPublic
            elif self.bUnFavoriteMentionsOn == True:
                ID = self.IDMentions
            elif self.bUnFavoriteFavoritesOn == True:
                ID = self.IDFavorites
            elif self.bUnFavoriteSearchOn == True:
                ID = self.IDSearch
            self.log.debug("[Unfavorite] ID:" + ID)
            if not ID:
                self.log.debug("[Unfavorite] Except: not id")
                raise
            proxy = { 'proxy' : self.chkTor.get_active(),
                'ip_address' : self.tbIPAddress.get_text(),
                'port' : self.tbPort.get_text() }
            if proxy['proxy'] is False:
                proxy = None
            unfavorites = self.wrapper.unfavorite(ID, proxy)
            if proxy is not None:
                self.log.debug('Unfavorited with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])
            if self.bUnFavoriteHomeOn == True:
                buffer = self.taHome.get_buffer().set_property("text", "")
                buffer = self.taHome.get_buffer()
                self.bUnFavoriteHomeOn = False
            elif self.bUnFavoritePublicOn == True:
                buffer = self.taPublic.get_buffer().set_property("text", "")
                buffer = self.taPublic.get_buffer()
                self.bUnFavoritePublicOn = False
            elif self.bUnFavoriteMentionsOn == True:
                buffer = self.taMentions.get_buffer().set_property("text", "")
                buffer = self.taMentions.get_buffer()
                self.bUnFavoriteMentionsOn = False
            elif self.bUnFavoriteFavoritesOn == True:
                buffer = self.taFavorites.get_buffer().set_property("text", "")
                buffer = self.taFavorites.get_buffer()
                self.bUnFavoriteFavoritesOn = False
            elif self.bFavoriteSearchOn == True:
                buffer = self.taSearch.get_buffer().set_property("text", "")
                buffer = self.taSearch.get_buffer()
                self.bUnFavoriteSearchOn = False
            #iter = buffer.get_end_iter()
            #buffer.insert(iter, "\nMessage unfavorited correctly." + "\n" + "==============\n")
            GuiUtils.Info("Message Unfavorited!", "Message unfavorited correctly!")
            self.search_favorites()
        except:
            GuiUtils.Error("Error!", "Could not unfavorite your message!")
            return

    def on_bDeleteHome_pressed(self):
        self.IDHome = self.eIdHome.get_text()
        self.bDeleteHomeOn = True
        self.delete()

    def on_bDeletePublic_pressed(self):
        self.IDPublic = self.eIdPublic.get_text()
        self.bDeletePublicOn = True
        self.delete()

    def on_bDeletePrivate_pressed(self):
        self.IDPrivate = self.eIdPrivate.get_text()
        self.bDeletePrivateOn = True
        self.delete()

    def delete(self):
        try:
            if self.bDeleteHomeOn == True:
                ID = self.IDHome
            elif self.bDeletePublicOn == True:
                ID = self.IDPublic
            elif self.bDeletePrivateOn == True:
                ID = self.IDPrivate

            self.log.debug("[Delete] ID:" + ID)
            if not ID:
                self.log.debug("[Delete] Except: not id")
                raise
            proxy = { 'proxy' : self.chkTor.get_active(),
                'ip_address' : self.tbIPAddress.get_text(),
                'port' : self.tbPort.get_text() }
            if proxy['proxy'] is False:
                proxy = None
            if self.bDeletePrivateOn == True:
                deletes = self.wrapper.delete_private(ID, proxy)
                if proxy is not None:
                    self.log.debug('Removing private with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])
            else:
                deletes = self.wrapper.delete_tweet(ID, proxy)
                if proxy['proxy'] is True:
                    self.log.debug('Removing message with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])
            if self.bDeleteHomeOn == True:
                buffer = self.taHome.get_buffer().set_property("text", "")
                buffer = self.taHome.get_buffer()
                self.bDeleteHomeOn = False
            elif self.bDeletePublicOn == True:
                buffer = self.taPublic.get_buffer().set_property("text", "")
                buffer = self.taPublic.get_buffer()
                self.bDeletePublicOn = False
            elif self.bDeletePrivateOn == True:
                buffer = self.taPrivate.get_buffer().set_property("text", "")
                buffer = self.taPrivate.get_buffer()
                self.bDeletePrivateOn = False
    
            #iter = buffer.get_end_iter()
            #buffer.insert(iter, "\nMessage removed correctly." + "\n" + "==============\n")
            GuiUtils.Info("Message removed!", "Message remove correctly!")
            self.home_timelines()
            self.public_timelines()
            self.privates()
        except:
            GuiUtils.Error("Error!", "Could not delete your message!")
            return

    def generate_key(self):
        try:
            key = self.wrapper.generate_key()
            self.tbPinEncrypt.set_text(key)
        except:
            GuiUtils.Error("Error!", "Generating Secret Key")

    def search_messages(self):
        tb = gtk.TextBuffer()
        h = HTMLParser.HTMLParser()
        textsearch = self.eTermsSearch.get_text()
        num_ocurrences = str(self.sSearch.get_value_as_int())
        proxy = { 'proxy' : self.chkTor.get_active(),
            'ip_address' : self.tbIPAddress.get_text(),
            'port' : self.tbPort.get_text() } 
        if proxy['proxy'] is False:
            proxy = None
        try:
            searches = self.wrapper.search_messages(textsearch, num_ocurrences, proxy)
            if proxy is not None:
                self.log.debug('Searching with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])
        except:
            GuiUtils.Error("Error: Searching terms", "Connection refused.")
            return
        # removing previous buffer
        buffer = self.taSearch.get_buffer().set_property("text", "")
        buffer = self.taSearch.get_buffer()
        iter = buffer.get_end_iter()
        buffer.insert(iter, "\nSearch Results:" + "\n" + "===========\n")
        for s in searches:
            #u = h.unescape(s.user.screen_name)
            #buffer.insert(iter, "Nick: " + u + "\n")
            buffer.insert(iter, "ID: " + str(s.id) + "\n") 
            buffer.insert(iter, s.created_at + "\n") 
            t = h.unescape(s.text)
            buffer.insert(iter, t + "\n")
            if s.place is not None:
                buffer.insert(iter, "Location: " + s.place["full_name"] + "\n")
            else:
                pass
            buffer.insert(iter, "------" + "\n") 

    def save_messages(self):
        tb = gtk.TextBuffer()
        # removing previous buffer
        buffer = self.taSave.get_buffer().set_property("text", "")
        buffer = self.taSave.get_buffer()
        iter = buffer.get_end_iter()
        user = str(self.eUserSave.get_text())
        num_ocurrences = str(self.sSave.get_value_as_int())
        proxy = { 'proxy' : self.chkTor.get_active(),
            'ip_address' : self.tbIPAddress.get_text(),
            'port' : self.tbPort.get_text() }
        if proxy['proxy'] is False:
            proxy = None
        try:
            (saves, count) = self.wrapper.save_messages(user, num_ocurrences, proxy)
            if proxy is not None:
                self.log.debug('Saving messages with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])
        except:
            GuiUtils.Error("Error!", "Saving messages")
            return
        buffer.insert(iter, "\nSaving messages of: " + user + "\n" + "=====================\n")

        if len(saves) <= 0:
            buffer.insert(iter, "No results." + "\n" + "===========\n")
            return
        else:
            if int(len(saves)) < int(count):
                count = int(len(saves))
            if not os.path.isdir("backups"):
                os.mkdir("backups")
            if not os.path.exists("backups/%s"%(user)):
                path = os.mkdir("backups/%s"%(user))
            for i in range(int(count)):
                # save disk
                path = "backups/%s"%(user)
                # some unicode issues
                logs = ''
                logs = u' '.join((logs, saves[i].text)).encode('utf-8').strip()
                nick = ''
                nick = u' '.join((nick, saves[i].user.screen_name)).encode('utf-8').strip()
                name = ''
                name = u' '.join((name, saves[i].user.name)).encode('utf-8').strip()
                created_at = ''
                created_at = u' '.join((created_at, saves[i].created_at)).encode('utf-8').strip()
                id = ''
                id = u' '.join((id, str(saves[i].id))).encode('utf-8').strip()
                place = ''
                if saves[i].place is not None:
                    place = u' '.join((place, saves[i].place["name"])).encode('utf-8').strip()

                h = "/tweets.txt"
                f = open(path+h, 'a')
                f.write("Name: " + name + " - ")
                f.write("Nick: " + nick + "\n")
                f.write("Tweet-ID: " + id + "\n")
                f.write(created_at + "\n")
                f.write(logs + "\n")
                if saves[i].place is not None:
                    f.write(place + "\n")
                f.write("======" + "\n")
                # output gtk
                h = HTMLParser.HTMLParser()
                buffer.insert(iter, "Name: " + saves[i].user.name + "\n")
                u = h.unescape(saves[i].user.screen_name)
                buffer.insert(iter, "Nick: " + u + "\n")
                buffer.insert(iter, "ID: " + str(saves[i].id) + "\n")
                buffer.insert(iter, saves[i].created_at + "\n")
                s = h.unescape(saves[i].text)
                buffer.insert(iter, s + "\n")
                if saves[i].place is not None:
                    buffer.insert(iter, "Location: " + saves[i].place["name"] + "\n")
                else:
                    pass
                buffer.insert(iter, "------" + "\n")
            f.close() 

    def home_timelines(self):
        tb = gtk.TextBuffer()
        h = HTMLParser.HTMLParser()
        # removing previous buffer
        buffer = self.taHome.get_buffer().set_property("text", "")
        buffer = self.taHome.get_buffer()
        iter = buffer.get_end_iter()
        num_ocurrences = self.sHome.get_value_as_int()
        proxy = { 'proxy' : self.chkTor.get_active(),
            'ip_address' : self.tbIPAddress.get_text(),
            'port' : self.tbPort.get_text() }
        if proxy is None:
            proxy = str(proxyServer + ":" + proxyPort)
        else:
            if proxy['proxy'] is False:
                proxy = None
            else:
                proxy = str(proxy['ip_address'] + ":" + proxy['port'])
        try:
            (timelines, num) = self.wrapper.home_timeline(num_ocurrences, proxy)
            if proxy is not None:
                self.log.debug('Home timeline with proxy: ' + proxy)
        except:
            GuiUtils.Error("Error: Showing home timeline", "Connection refused.")
            return                                                                                           
        buffer.insert(iter, "\nYour Home:" + "\n" + "===========\n")
        if len(timelines) <= 0:
            buffer.insert(iter, "You haven't any message, yet." + "\n" + "===========\n")
            return
        else:
            if int(len(timelines)) < int(num):
                num = int(len(timelines))
            for i in range(int(num)):
                u = h.unescape(timelines[i].user.screen_name)
                buffer.insert(iter, "Nick: " + u + "\n")
                buffer.insert(iter, "ID: " + str(timelines[i].id) + "\n") 
                buffer.insert(iter, timelines[i].created_at + "\n")
                s = h.unescape(timelines[i].text)
                buffer.insert(iter, s + "\n")
                if timelines[i].place is not None:
                    buffer.insert(iter, "Location: " + timelines[i].place["name"] + "\n")
                else:
                    pass
                buffer.insert(iter, "------" + "\n")

    def mentions(self):
        tb = gtk.TextBuffer()
        h = HTMLParser.HTMLParser()
        # removing previous buffer
        buffer = self.taMentions.get_buffer().set_property("text", "")
        buffer = self.taMentions.get_buffer()
        iter = buffer.get_end_iter()
        num_ocurrences = str(self.sMentions.get_value_as_int())
        proxy = { 'proxy' : self.chkTor.get_active(),
            'ip_address' : self.tbIPAddress.get_text(),
            'port' : self.tbPort.get_text() }
        if proxy['proxy'] is False:
            proxy = None
        try:
            (mentions, num) = self.wrapper.mentions(num_ocurrences, proxy)
            if proxy is not None:
                self.log.debug('Searching mentions with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])  
        except:
            GuiUtils.Error("Error: Showing mentions", "Connection refused.")
            return
        if len(mentions) <= 0:
            buffer.insert(iter, "\nSearch doesn't get any results.\n")
        buffer.insert(iter, "\nMentions about you:" + "\n" + "===========\n")
        n = int(len(mentions))
        if int(num) < int(len(mentions)):
            n = int(num)
        for i in range(int(n)):
            u = h.unescape(mentions[i].user.screen_name)
            buffer.insert(iter, "Nick: " + u + "\n")
            buffer.insert(iter, "ID: " + str(mentions[i].id) + "\n")
            buffer.insert(iter, mentions[i].created_at + "\n")
            s = h.unescape(mentions[i].text)
            buffer.insert(iter, s + "\n")
            if mentions[i].place is not None:
                buffer.insert(iter, "Location: " + mentions[i].place["name"] + "\n")
            else:
                pass
            buffer.insert(iter, "------" + "\n")

    def privates(self):
        tb = gtk.TextBuffer()
        h = HTMLParser.HTMLParser()
        # removing previous buffer
        buffer = self.taPrivate.get_buffer().set_property("text", "")
        buffer = self.taPrivate.get_buffer()
        iter = buffer.get_end_iter()
        num_ocurrences = str(self.sPrivate.get_value_as_int())
        proxy = { 'proxy' : self.chkTor.get_active(),
            'ip_address' : self.tbIPAddress.get_text(),
            'port' : self.tbPort.get_text() }
        if proxy['proxy'] is False:
            proxy = None
        try:
            (privates, num) = self.wrapper.show_private(num_ocurrences, proxy)
            if proxy is not None:
                self.log.debug('Private timeline with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])
        except:
            GuiUtils.Error("Error: Showing privates", "Connection refused.")
            return
        buffer.insert(iter, "\nPrivate messages:" + "\n" + "=====================\n")
        if len(privates) <= 0:
            buffer.insert(iter, "You haven't any private, yet." + "\n" + "===========\n")
            return
        else:
            if int(len(privates)) < int(num):
                num = int(len(privates))
            for i in range(int(num)):
                buffer.insert(iter, "ID: " + str(privates[i].id) + "\n")
                buffer.insert(iter, privates[i].created_at + "\n")
                u = h.unescape(privates[i].sender_screen_name)
                buffer.insert(iter, "From: " + u + "\n")
                s = h.unescape(privates[i].text)
                buffer.insert(iter, s + "\n")
                buffer.insert(iter, "------" + "\n")

    def public_timelines(self):
        tb = gtk.TextBuffer()
        h = HTMLParser.HTMLParser()
        # removing previous buffer
        buffer = self.taPublic.get_buffer().set_property("text", "")
        buffer = self.taPublic.get_buffer()
        user = str(self.eUserPublic.get_text())
        iter = buffer.get_end_iter()
        num_ocurrences = str(self.sPublic.get_value_as_int())
        proxy = { 'proxy' : self.chkTor.get_active(),
            'ip_address' : self.tbIPAddress.get_text(),
            'port' : self.tbPort.get_text() }
        try:
            source_api = self.wrapper.get_source_api()
        except:
            GuiUtils.Error("Error!", "Showing public timelines: Not correct API Source provided.")
        if source_api["source_api"] == 'identi.ca/api':
            import string
            user = string.replace(user, "@", "")	
        if proxy is None:
            proxy = str(proxyServer + ":" + proxyPort)
        else:
            if proxy['proxy'] is False:
                proxy = None
            else:
                proxy = str(proxy['ip_address'] + ":" + proxy['port'])
        try:
            ps = self.wrapper.show_public(user, num_ocurrences, proxy)
            if proxy is not None:
                self.log.debug('Public timeline with proxy: ' + proxy)
        except:
            GuiUtils.Error("Error: Showing public timeline", "Connection refused.")
            return
        buffer.insert(iter, "\nShowing timeline of: " + user + "\n" + "=====================\n")
        for p in ps:
            u = h.unescape(p.user.screen_name)
            buffer.insert(iter, "Nick: " + u + "\n")
            buffer.insert(iter, "ID: " + str(p.id) + "\n")
            buffer.insert(iter, p.created_at + "\n")
            s = h.unescape(p.text)
            buffer.insert(iter, unicode(s) + "\n")
            if p.place is not None:
                buffer.insert(iter, "Location: " + p.place["name"] + "\n")
            else:
                pass
            buffer.insert(iter, "------" + "\n")      
            
    def search_favorites(self):
        tb = gtk.TextBuffer()
        h = HTMLParser.HTMLParser()
        # removing previous buffer
        buffer = self.taFavorites.get_buffer().set_property("text", "")
        buffer = self.taFavorites.get_buffer()
        iter = buffer.get_end_iter()
        user = str(self.eUserFavorites.get_text())
        num_ocurrences = str(self.sFavorites.get_value_as_int())
        proxy = { 'proxy' : self.chkTor.get_active(),
            'ip_address' : self.tbIPAddress.get_text(),
            'port' : self.tbPort.get_text() }
        if proxy['proxy'] is False:
            proxy = None
        try:
            source_api = self.wrapper.get_source_api()
        except:
            GuiUtils.Error("Error!", "Showing public timelines: Not correct API Source provided.")
        if source_api["source_api"] == 'identi.ca/api':
            import string
            user = string.replace(user, "@", "")	
        try:
            (favorites, count) = self.wrapper.search_favorite(user, num_ocurrences, proxy)
            if proxy is not None:
                self.log.debug('Showing favorites with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])
        except:
            GuiUtils.Error("Error: Showing favorites", "Connection refused.")
            return
        buffer.insert(iter, "\nShowing favorites of: " + user + "\n" + "=====================\n")
        if len(favorites) <= 0:
            buffer.insert(iter, "No results." + "\n" + "===========\n")
            return
        else:
            if int(len(favorites)) < int(count):
                count = int(len(favorites))
            for i in range(int(count)):
                buffer.insert(iter, "Name: " + favorites[i].user.name + "\n")
                n = h.unescape(favorites[i].user.screen_name)
                buffer.insert(iter, "Nick: " + n + "\n")
                buffer.insert(iter, "ID: " + str(favorites[i].id) + "\n")
                buffer.insert(iter, favorites[i].created_at + "\n")
                s = h.unescape(favorites[i].text)
                buffer.insert(iter, s + "\n")
                if favorites[i].place is not None:
                    buffer.insert(iter, "Location: " + favorites[i].place["name"] + "\n")
                else:
                    pass
                buffer.insert(iter, "------" + "\n")

    def search_topics(self):
        proxy = { 'proxy' : self.chkTor.get_active(),
            'ip_address' : self.tbIPAddress.get_text(),
            'port' : self.tbPort.get_text() }
        if proxy['proxy'] is False:
            proxy = None
        try:
            source_api = self.wrapper.get_source_api()
        except:
            GuiUtils.Error("Error!", "Searching Trending Topics: Not correct API Source provided.")	      
        try:
            if source_api["source_api"] == "identi.ca/api":
                self.lTrendingTopics.set_text("This feature is not allowed by identi.ca, yet...")
            else:
                topics = self.wrapper.search_topics(proxy)
                if proxy is not None:
                    self.log.debug('Public timeline with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])
                #self.lTrendingTopics.set_text(str(topics))
                self.lTrendingTopics.set_text('\n '.join(topics))
        except:
            GuiUtils.Error("Error!", "Searching Trending Topics.")	

    def short_url(self):
        try:
            url = gtk.TextBuffer()
            url = self.eShortUrl.get_text()
            proxy = { 'proxy' : self.chkTor.get_active(),
                'ip_address' : self.tbIPAddress.get_text(),
                'port' : self.tbPort.get_text() }
            if proxy['proxy'] is False:
                proxy = None
            short_url = self.wrapper.short_url(url, proxy)
            if proxy is not None:
                self.log.debug('Shorting url with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])
            self.tvShortUrl.get_buffer().set_text(short_url)
        except:
            GuiUtils.Error("Error!", "Shorting URL")

    def on_bFollowPublic_pressed(self):
        self.User = self.eUserPublic.get_text()
        self.bFollowPublicOn = True
        self.follow()

    def follow(self):
        try:
            if self.bFollowPublicOn == True:
                user = self.User
            if not user:
                self.log.debug("[Follow] Except: not user name.")
                raise
            proxy = { 'proxy' : self.chkTor.get_active(),
                'ip_address' : self.tbIPAddress.get_text(),
                'port' : self.tbPort.get_text() }
            if proxy['proxy'] is False:
                proxy = None
            status = self.wrapper.follow(user, proxy)
            if proxy is not None:
                self.log.debug('Following with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])
            if self.bFollowPublicOn == True:
                buffer = self.taPublic.get_buffer().set_property("text", "")
                buffer = self.taPublic.get_buffer()
                self.bFollowPublicOn = False
            #iter = buffer.get_end_iter()
            #buffer.insert(iter, "\nFollowing user correctly." + "\n" + "==============\n")
            GuiUtils.Info("Following user!", "Following user correctly!")
            user_info = self.wrapper.get_user_info(proxy)
            self.lFriends.set_text(str(user_info['friends']))
        except:
            GuiUtils.Error("Error!", "Following user")

    def on_bUnfollowPublic_pressed(self):
        self.User = self.eUserPublic.get_text()
        self.bUnfollowPublicOn = True
        self.unfollow()

    def unfollow(self):
        try:
            if self.bUnfollowPublicOn == True:
                user = self.User
            if not user:
                self.log.debug("[Unfollow] Except: not user name.")
                raise
            proxy = { 'proxy' : self.chkTor.get_active(),
                'ip_address' : self.tbIPAddress.get_text(),
                'port' : self.tbPort.get_text() }
            if proxy['proxy'] is False:
                proxy = None
            status = self.wrapper.unfollow(user, proxy)
            if proxy is not None:
                self.log.debug('Unfollowing with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])
            if self.bUnfollowPublicOn == True:
                buffer = self.taPublic.get_buffer().set_property("text", "")
                buffer = self.taPublic.get_buffer()
                self.bUnfollowPublicOn = False
            iter = buffer.get_end_iter()
            #buffer.insert(iter, "\nUnfollowing user correctly." + "\n" + "===============\n")
            #user_info = self.wrapper.get_user_info()
            GuiUtils.Info("Unfollowing user!", "Unfollowing user correctly!")
            user_info = self.wrapper.get_user_info(proxy)
            self.lFriends.set_text(str(user_info['friends']))
        except:
            GuiUtils.Error("Error!", "Unfollowing user")

    def on_bBlockPublic_pressed(self):
        self.User = self.eUserPublic.get_text()
        self.bBlockPublicOn = True
        self.block()

    def block(self):
        try:
            if self.bBlockPublicOn == True:
                user = self.User
            if not user:
                self.log.debug("[Block] Except: not user name.")
                raise
            proxy = { 'proxy' : self.chkTor.get_active(),
                'ip_address' : self.tbIPAddress.get_text(),
                'port' : self.tbPort.get_text() }
            if proxy['proxy'] is False:
                proxy = None
            status = self.wrapper.block(user, proxy)
            if proxy is not None:
                self.log.debug('Blocking with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])
            if self.bBlockPublicOn == True:
                buffer = self.taPublic.get_buffer().set_property("text", "")
                buffer = self.taPublic.get_buffer()
                self.bBlockPublicOn = False
            #iter = buffer.get_end_iter()
            #buffer.insert(iter, "\nBlocking user correctly." + "\n" + "==============\n")
            GuiUtils.Info("Blocking user!", "Blocking user correctly!")
            user_info = self.wrapper.get_user_info(proxy)
            self.lFriends.set_text(str(user_info['friends']))
            self.lFollowers.set_text(str(user_info['followers']))
        except:
            GuiUtils.Error("Error!", "Blocking user")

    def on_bUnblockPublic_pressed(self):
        self.User = self.eUserPublic.get_text()
        self.bUnblockPublicOn = True
        self.unblock()

    def unblock(self):
        try:
            if self.bUnblockPublicOn == True:
                user = self.User
            if not user:
                self.log.debug("[Unblock] Except: not user name.")
                raise
            proxy = { 'proxy' : self.chkTor.get_active(),
                'ip_address' : self.tbIPAddress.get_text(),
                'port' : self.tbPort.get_text() }
            if proxy['proxy'] is False:
                proxy = None
            status = self.wrapper.unblock(user, proxy)
            if proxy is not None:
                self.log.debug('Unblocking with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])
            status = self.wrapper.unblock(user)
            if self.bUnblockPublicOn == True:
                buffer = self.taPublic.get_buffer().set_property("text", "")
                buffer = self.taPublic.get_buffer()
                self.bUnblockPublicOn = False
            #iter = buffer.get_end_iter()
            #buffer.insert(iter, "\nUnblocking user correctly." + "\n" + "==============\n")
            GuiUtils.Info("Unblocking user!", "Unblocking user correctly!")
            user_info = self.wrapper.get_user_info(proxy)
            self.lFriends.set_text(str(user_info['friends']))
            self.lFollowers.set_text(str(user_info['followers']))
        except:
            GuiUtils.Error("Error!", "Unblocking user") 

    def on_bSuicide_pressed(self):
        try:
            dialog = gtk.Dialog("Are you sure?!", None, 0,
            (gtk.STOCK_NO, gtk.RESPONSE_NO,
             gtk.STOCK_YES, gtk.RESPONSE_YES))
            response = dialog.run()
            dialog.destroy()
            while gtk.events_pending():
                gtk.main_iteration(False)
            if response == gtk.RESPONSE_NO:
                GuiUtils.Info("Anna Eleanor Roosevelt.", "When you cease to make a contribution, then you begin to die.")  
            elif response == gtk.RESPONSE_YES:         
                GuiUtils.Warning("Attention!", "Your account starts to be deleted.\n\n AnonTwi will try to remove your private and public messages, your friendships, etc.\n\nThis can take a long time, so be patient!.\n\nAfter that, it will try to close your account. Remember that some social networks were storing your data on their servers and they are not allowing your nowadays, to remove it propertly. \n\nReclaim your privacy rights.") 
                self.log.debug("[Suicide] Starting to suicide your account.")
                proxy = { 'proxy' : self.chkTor.get_active(),
                    'ip_address' : self.tbIPAddress.get_text(),
                    'port' : self.tbPort.get_text() }
                if proxy['proxy'] is False:
                    proxy = None
                status = self.wrapper.suicide(proxy)
                if proxy is not None:
                    self.log.debug('Suiciding with proxy: ' + proxy['ip_address'] + ':' + proxy['port'])
                self.log.debug("[Suicide] PUM!. Die.")                
        except:
            GuiUtils.Error("Error suiciding yourself!", "Sometimes happens... ;(")  

    #def on_bIRCDeploy_pressed(self):
    #    self.bIRCDeployOn = True
    #    self.IRCdeploy()

    #def IRCdeploy(self):
    #    tb = gtk.TextBuffer()
    #    h = HTMLParser.HTMLParser()
        # removing previous buffer
    #    buffer = self.taIRC.get_buffer().set_property("text", "Connecting to IRC... Please wait.")
    #    buffer = self.taIRC.get_buffer()
    #    iter = buffer.get_end_iter() 
    #    try:
    #        if self.bIRCDeployOn == True:
    #            user = str(self.eIRCNick.get_text())
    #            if user is "":
    #                import random
    #                import string
    #                char_set = string.ascii_uppercase + string.digits
    #                user = ''.join(random.sample(char_set,10))
    #            self.log.debug('[IRC] botname: ' + user)
    #            host = str(self.eIRCServer.get_text())
    #            self.log.debug('[IRC] host: ' + host)
    #            port = str(self.eIRCport.get_text())
    #            self.log.debug('[IRC] port: ' + port)
    #            if not host or not port:
    #                GuiUtils.Error("IRC Error", "Please specify irc host and port, correctly!") 
    #                return
    #            chan = str(self.eIRCchannel.get_text())
    #            self.log.debug('[IRC] channel: ' + chan)
    #            if not chan:
    #                GuiUtils.Error("IRC Error", "No channel specified") 
    #                return      
    #            if proxyServer is None or proxyPort is None:
    #                proxy = None
    #            else:
    #                proxy = str(proxyServer + ":" + proxyPort)
    #            try:
    #                AnonBot = self.wrapper.IRCdeploy(user, host, port, chan)
    #            except:
    #                GuiUtils.Error("IRC Error", "Something wrong on data sent :(")
    #                return
    #            buffer.insert(iter, AnonBot);
    #            if proxy is not None:
    #                self.log.debug('[IRC] Connecting to IRC with proxy: ' + proxy)
    #            self.bIRCDeployOn = False
    #    except:
    #        GuiUtils.Error("Error!", "Ops!, there are some problems connecting to IRC server...")             

class GuiWelcome(object):
    def __init__(self):
        builder = GuiUtils.GetBuilder("wWelcome")
        self.log = logging.getLogger('GTK Welcome') 

        # get objects 
        self.window = builder.get_object('wWelcome')
        self.bNext = builder.get_object('bNext')
        self.iAnontwi = builder.get_object('iAnontwi')

        # signals
        self.bNext.connect('clicked', lambda w: self.Next())

        # defaults
        self.iAnontwi.set_from_file(PATH_APP + DIR_GTK_IMG + 'anontwi_small.png')

        # run window
        self.Show()

    def Show(self):
        self.window.set_icon_from_file(PATH_APP + DIR_GTK_IMG + 'anontwi_ico.png')
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_title(WIN_TITLE)
        self.window.show()

    def Next(self):
        self.window.hide() #make more nice
        gui_tokens = GuiTokens()
        gui_tokens.Show()

class GuiTokens(object):
    def __init__(self):
        self.log = logging.getLogger('GuiTokens')
        self.log.debug("Init GuiTokens") 
        self.wrapper = WrapperAnontwi()
        builder = GuiUtils.GetBuilder('wTokens')

        self.oauth_token = None
        self.oauth_token_secret = None
        self.source_api = "api.twitter.com" #start source api

        # get objects 
        self.window = builder.get_object('wTokens')
        self.tbConsumerKey = builder.get_object('tbConsumerKey')
        self.tbConsumerSecret = builder.get_object('tbConsumerSecret')
        self.tbAccessToken = builder.get_object('tbAccessToken')
        self.tbSecretToken = builder.get_object('tbSecretToken')
        self.bNext = builder.get_object('bNext')
        self.tbPin = builder.get_object('tbPin')
        self.bInsertPin = builder.get_object('bInsertPin')
        self.bGetUrl = builder.get_object('bGetUrl')
        self.lkbUrl = builder.get_object('lkbUrl')
        self.chkTor = builder.get_object('chkTor')
        self.tbIPAddress = builder.get_object('tbIPAddress')
        self.tbPort = builder.get_object('tbPort')
        self.hbTor = builder.get_object('hbTor')
        self.rTwitter = builder.get_object('rTwitter')
        self.rIdentica = builder.get_object('rIdentica')

        # signals
        self.bNext.connect('clicked', lambda w: self.Next())
        self.bGetUrl.connect('clicked', lambda x: self.GetUrl())
        self.bInsertPin.connect('clicked', lambda x: self.InsertPinCode())
        self.chkTor.connect('toggled', lambda w: self.switch('Tor'))
        self.rTwitter.connect('toggled', lambda w: self.rTwitter_sourceapi())
        self.rIdentica.connect('toggled', lambda w: self.rIdentica_sourceapi())

        # disable by default
        #self.bNext.set_sensitive(False)
        self.tbPin.set_sensitive(False)
        self.bInsertPin.set_sensitive(False)
        self.hbTor.set_visible(False)
        self.lkbUrl.set_visible(False)

        # run window
        self.Show()
    
    def switch(self, layer):
        if layer == 'Tor': 
            self.hbTor.set_visible(not self.hbTor.get_visible())

    def rTwitter_sourceapi(self):
        self.source_api = "api.twitter.com"

    def rIdentica_sourceapi(self):
        self.source_api = "identi.ca/api"
     
    def Show(self):
        self.window.set_icon_from_file(PATH_APP + DIR_GTK_IMG + 'anontwi_ico.png')
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_title(WIN_TITLE)
        self.window.show()

    def get_tokens(self):
        access = {'access_token':self.tbAccessToken.get_text().strip(),
                  'secret_token':self.tbSecretToken.get_text().strip()}
        consumer = {'consumer_key':self.tbConsumerKey.get_text().strip(),
                    'consumer_secret':self.tbConsumerSecret.get_text().strip()}
        return (access, consumer) 

    def GetUrl(self):
        tokens = self.get_tokens()
        if not tokens[0]['secret_token'] \
            and not tokens[0]['access_token'] \
            and not tokens[1]['consumer_secret'] \
            and not tokens[1]['consumer_key']:
            GuiUtils.Error('Error!', 'Please insert tokens.')
            return

        dialog = GuiUtils.Loading('Requesting url...', 'Connecting to API, please wait...')
        
        try:
            if self.chkTor.get_active():
                proxy = {'proxy':self.chkTor.get_active(),
                         'ip_address':self.tbIPAddress.get_text().strip(),
                         'port':self.tbPort.get_text().strip() }
                self.log.debug("Proxy: " + proxy['ip_address'] + ":" + proxy['port'])
                data = self.wrapper.get_url(tokens[0], tokens[1], self.source_api, proxy) # access, consumer
            else:
                data = self.wrapper.get_url(tokens[0], tokens[1], self.source_api, proxy=None) # access, consumer
         
            if not data:
                if self.chkTor.get_active():
                    GuiUtils.Error("Error!", "Error requesting tokens. Check your proxy configuration.")
                    return
                else:
                    GuiUtils.Error("Error!", "Error requesting tokens")
                    return
        finally:
            dialog.destroy()
        self.oauth_token = data[1]
        self.oauth_token_secret = data[2]
        self.lkbUrl.set_visible(True)
        if self.source_api == "identi.ca/api":
            self.url = "https://identi.ca/api/oauth/authorize?oauth_token=" + self.oauth_token
        else:
            self.url = data[0]
        self.lkbUrl.set_uri(self.url)
        self.lkbUrl.set_label(self.url)
        if self.source_api == "identi.ca/api":
            self.tbPin.set_text("Oauth Verifier: extract it from the url of AnonTwi)")
        self.tbPin.set_sensitive(True)
        self.bInsertPin.set_sensitive(True)
        dialog.destroy()
    
    def InsertPinCode(self):
        tokens = self.get_tokens()
        try:
            if self.chkTor.get_active():
                proxy = self.tbIPAddress.get_text().strip() + ":" \
                        + self.tbPort.get_text().strip()
                self.log.debug("InsertPinCode with proxy: " + str(proxy))
                if self.tbPin.get_text() == "":
                    GuiUtils.Error("Error!", "You PIN key is empty")
                    return
                else:
                    try:    
                        source_api = self.wrapper.get_source_api()
                    except:
                        GuiUtils.Error("Error!", "Inserting Pincode: Not correct API Source provided.")
                    self.wrapper.insert_pincode(self.tbPin.get_text(),
                                                self.oauth_token, self.oauth_token_secret, tokens[1], self.source_api, proxy) # oauth_token, oauth_secret, access, proxy
            else:
                self.log.debug("InsertPinCode non-proxy")
                if self.tbPin.get_text() == "":
                    GuiUtils.Error("Error!", "You PIN key is empty")
                    return
                else:
                    self.wrapper.insert_pincode(self.tbPin.get_text(),
                                                self.oauth_token, self.oauth_token_secret, tokens[1], self.source_api, None) # oauth_token, oauth_secret, access
        except:
            GuiUtils.Error("Error!", "Could not authenticate your PIN")
            return
        GuiUtils.Info("Auth Info", "Successfully authenticate!")
        self.bNext.set_visible(True)		

    def Next(self):
        self.window.hide() #make more nice
        gui_congrats = GuiCongrats()
        gui_congrats.Show()

class GuiCongrats(object):
    def __init__(self):
        builder = GuiUtils.GetBuilder('wCongrats')
        # get objects
        self.window = builder.get_object('wCongrats')
        self.lPathTokens = builder.get_object('lPathTokens')
        self.bFinish = builder.get_object('bFinish')
        self.lPathTokens = builder.get_object('lPathTokens')
        self.iAnontwi = builder.get_object('iAnontwi')

        #defaults
        self.lPathTokens.set_text(DIR_TOKENS)
        self.iAnontwi.set_from_file(PATH_APP + DIR_GTK_IMG + 'anontwi_small.png')

        # signals
        self.bFinish.connect('clicked', lambda w: self.Finish())	
        self.window.connect('destroy', lambda w: gtk.main_quit())

    def Show(self):
        self.window.set_icon_from_file(PATH_APP + DIR_GTK_IMG + 'anontwi_ico.png')
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_title(WIN_TITLE)
        self.window.show()

    def Finish(self):
        self.window.destroy()
        sys.exit()
