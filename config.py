#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
# vim: set expandtab tabstop=4 shiftwidth=4:
"""
$Id$

This file is part of the anontwi project, http://anontwi.sourceforge.net.

Copyright (c) 2011/2012/2013/2014 - <epsylon@riseup.net>

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
# This file contains your API tokens and secrets to use with Twitter/Identi.ca/etc...

#   - Create a third party APP in your 'developer' account. 

#      + on Twitter: https://dev.twitter.com        
#         - Go to: Profile/My Applications. 
#         - Click on "Create new application"
#         - Input data on form, correctly.
#         - Remember to give all permisions (write/read/etc)
#      + on Identi.ca (Profile/Apps): https://identi.ca

#   - Get your OAuth "consumer": secret and key
#   - Open "config.py" (THIS FILE!) with a text editor, and enter tokens (below!)
#   - If you go using shell, next is to launch --tokens (remember, for TOR: --proxy "http://127.0.0.1:8118")

#   - Run ./anontwi or python anontwi (interfaces: --gtk / --web)

from core.gtk.config_gtk import *
import traceback

#"""GTK Environment"""
try:
    token = open(DIR_TOKENS + FILE_CONS_TKN).readlines()
        
    APItokens = [{'consumer_key': token[0].strip(),
                      'consumer_secret' : token[1].strip()}]

    api = open(DIR_TOKENS + FILE_SOURCE_API).readlines()
    APIsources = [{'source_api' : api[0].strip()}]

except:
    #traceback.print_bt()
    #exit
    """Non GTK"""
    APItokens = [
		{
                  'consumer_key'    : "", # enter your consumer_key
                  'consumer_secret' : "", # enter your consumer_secret
		}
	    ]
    APIsources = [
                {
                  'source_api' : "api.twitter.com", #enter your source api
                  #'source_api' : "identi.ca/api" #enter your source api
                }
            ]
