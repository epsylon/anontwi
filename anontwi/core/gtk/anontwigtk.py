#!/usr/bin/python
# -*- coding: utf8 -*-
"""
Copyright (C) 2012 Jhonny5 <jhonny5@riseup.net>

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
#import os, sys
#import shutil #for remove directory tree
import logging

#from optparse import OptionParser

from core.gtk.main import GuiWelcome, GuiUtils, GuiStarter
from core.wrapper import WrapperAnontwi
from core.gtk.config_gtk import *
""" 
for windows:
if sys.platform == 'win32':
   os.environ['PATH'] += ";lib;"
else:
"""
#gtk libraries import
try:
    import pygtk
    pygtk.require("2.0")
except:
    print ("PyGkt not found.")
try:
    import gtk, gtk.glade
except:
    print ("Gkt / Glade  not found")
    #sys.exit(1)
#print ("Gtk / GLade found.")

#LOG_LEVEL = logging.DEBUG
LOG_LEVEL = logging.INFO

class AnontwiGTK():
    @staticmethod
    def run():
        logging.basicConfig(level=LOG_LEVEL) 
        logging.debug('Running Program')
        log = logging.getLogger('GTK') 
        
        wrapper = WrapperAnontwi()

        # is first time that program runs ? show assistant : run MainWindow
        if not wrapper.get_consumer_tokens() \
            or not wrapper.get_access_tokens():
            log.debug('Running Assistant')
            GuiWelcome()
            gtk.main()         

        log.debug('Running Starter GUI')
        GuiStarter()
        gtk.main()


