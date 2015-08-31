#!/usr/bin/env python 
"""
$Id$

This file is part of the anontwi project, http://anontwi.03c8.net

Copyright (c) 2012/2013/2014/2015 by psy <epsylon@riseup.net>

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
# This file contains your API tokens and secrets for AnonTwi
# Remember that you can bridge data across different social networking sites to evade tracking.

# ex: HOME->Tor->IRC->GNUSocial->Twitter->Facebook..

#   - Create a third party APP on your profile. 

#      + GNU/Social:
#         - Login to your account         
#         - Go to: Settings
#         - Click on: "Register an OAuth client application"
#         - Click on: "Register a new application"
#             * <yoursocialnetwork.net>/settings/oauthapps/new

#         - Fill form correctly
#             * Icon: You can use AnonTwi website logo
#             * Name: (ex: AnonTwi)            
#             * Description: (ex: Anontwi -GNU/Social edition-)
#             * Source URL: (ex: http://anontwi.03c8.net)
#             * Organization: (ex: AnonTwi)
#             * Homepage: (ex: http://anontwi.03c8.net)

#             * Callback URL: (leave this BLANK)
#             * Type of Application: Desktop
#             * Default access for this application: Read-Write

#      + Twitter:
#         - Login to your account         
#         - Go to: https://apps.twitter.com/
#         - Click on: "Create New App"
#             * https://apps.twitter.com/app/new

#         - Fill form correctly
#             * Name: (ex: AnonTwi)            
#             * Description: (ex: Anontwi -GNU/Social edition-)
#             * Website: (ex: http://anontwi.03c8.net)
#             * Callback URL: (leave this BLANK)

#   - Get your OAuth settings: Click on the name of your new APP connector (ex: AnonTwi)
#   - Open "config.py" (THIS FILE!) with a text editor, and enter tokens (below!)

#   - Remember:
#             * If you go to use shell mode, you should generate your tokens with command: --tokens 
#             * For connect using TOR add: --proxy "http://127.0.0.1:8118"

#   - Run ./anontwi or python anontwi (To use interface: ./anontwi --gtk)

from core.gtk.config_gtk import *

#"""GTK Environment"""
try:
    token = open(DIR_TOKENS + FILE_CONS_TKN).readlines()
        
    APItokens = [{'consumer_key': token[0].strip(),
                      'consumer_secret' : token[1].strip()}]

    api = open(DIR_TOKENS + FILE_SOURCE_API).readlines()
    APIsources = [{'source_api' : api[0].strip()}]

except:
    """Non GTK"""
    APItokens = [
		{
                  'consumer_key'    : "", # enter your consumer_key
                  'consumer_secret' : "", # enter your consumer_secret
		}
	    ]
    APIsources = [
                {
                  'source_api' : "", # enter your source API: <yoursocialnetwork.net>/api
                }
            ]
