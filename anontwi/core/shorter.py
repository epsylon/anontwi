#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
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

x90.es - nopcode.org secure short links (allies)
"""
import urllib, sys
import pycurl
from cStringIO import StringIO

class ShortURLReservations(object):
    def __init__(self, service='x90.es'):
        self._service = service
        self._parse_shortener()
        self._extra = {}

    def _parse_shortener(self):
        """
	List of valid links shorterers 
	"""
        if self._service == 'x90.es' or not self._service:
            self._url = 'http://x90.es/api.php'
            self._par = 'url'
            self._method = 'post'
	
    def process_url(self, url, proxy):
        dest = urllib.urlencode({self._par: url})
        dest = dest + "&action=shorturl" # see x90.es API features
        # add some fake user-agent and referer
        user_agent = 'Mozilla/5.0 (Linux; U; Android 0.5; en-us)'
        referer = '' 
        out = StringIO()
        c = pycurl.Curl()
        if self._method == 'post':
            c.setopt(c.POST, 1)
            c.setopt(c.POSTFIELDS, dest)
            #c.setopt(c.VERBOSE, True)
            target = self._url
        c.setopt(c.URL, target)
        c.setopt(c.FOLLOWLOCATION, 1)
        c.setopt(c.REFERER, referer)
        c.setopt(c.USERAGENT, user_agent)
        # try connection with proxy
        if proxy is None:
            pass
        else:
	    c.setopt(c.PROXY, proxy)
        c.setopt(c.WRITEFUNCTION, out.write)
        try:
            c.perform()
        except Exception as e:
            if proxy is None:
                print "\n[Error] Something wrong connecting to short url service provider:", self._service, '[', e[1], '].' , "Aborting!...\n"
            else:
                print "\n[Error] Something wrong connecting to short url service provider:", self._service, "[ Couldn't connect to proxy ]." , "Aborting!...\n"
            sys.exit(2)
        shorturl = out.getvalue()
        return shorturl
        c.close()
