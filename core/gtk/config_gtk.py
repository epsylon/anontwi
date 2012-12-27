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
import os, sys

PATH_APP = os.path.dirname(os.path.abspath(__file__))
DIR_GTK = '/ui/'
DIR_GTK_IMG = '/ui/images/'

DIR_HOME_ANON = os.getenv('HOME') + '/.anontwi-gtk'
DIR_TOKENS = DIR_HOME_ANON + '/tokens/'
FILE_CONS_TKN = 'cons_tokens.key'
FILE_ACC_TKN = 'acc_tokens.key'	
FILE_SOURCE_API = 'source_api'
sys.path.append(PATH_APP + '/anontwi/')
