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
"""
################################################################### 
# See https://en.wikipedia.org/wiki/HMAC#Implementation
# Example written by: michael@briarproject.org
###################################################################

# Constants for AES256 and HMAC-SHA1
KEY_SIZE = 32
BLOCK_SIZE = 16
MAC_SIZE = 20

from os import urandom
from hashlib import sha1, sha256
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

trans_5C = "".join([chr (x ^ 0x5c) for x in xrange(256)])
trans_36 = "".join([chr (x ^ 0x36) for x in xrange(256)])

def hmac_sha1(key, msg):
    if len(key) > 20:
        key = sha1(key).digest()
    key += chr(0) * (20 - len(key))
    o_key_pad = key.translate(trans_5C)
    i_key_pad = key.translate(trans_36)
    return sha1(o_key_pad + sha1(i_key_pad + msg).digest()).digest()

def derive_keys(key):
    h = sha256()
    h.update(key)
    h.update('cipher')
    cipher_key = h.digest()
    h = sha256()
    h.update(key)
    h.update('mac')
    mac_key = h.digest()
    return (cipher_key, mac_key)

def generate_key():
    return b64encode(urandom(KEY_SIZE))

class Cipher(object):
    """
    Cipher class
    """
    def __init__(self, key="", text=""):
        """
        Init 
        """
        self.block_size = 16
        self.mac_size = 20
        self.key = self.set_key(key)
        self.text = self.set_text(text)
        self.mode = AES.MODE_CFB
  
    def set_key(self, key):
        """
        Set key
        """
        # Base64 decode the key
        try:
            key = b64decode(key)
        except TypeError:
            raise ValueError
        # The key must be the expected length
        if len(key) != KEY_SIZE:
            raise ValueError
        self.key = key
        return self.key

    def set_text(self, text):
        """
        Set text
        """
        self.text = text 
        return self.text

    def encrypt(self):
        """
        Encrypt text
        """
        # The IV, ciphertext and MAC can't be more than 105 bytes
        if BLOCK_SIZE + len(self.text) + MAC_SIZE > 105:
            self.text = self.text[:105 - BLOCK_SIZE - MAC_SIZE]
        # Derive the cipher and MAC keys
        (cipher_key, mac_key) = derive_keys(self.key)
        # Generate a random IV
        iv = urandom(BLOCK_SIZE)
	# Encrypt the plaintext
        aes = AES.new(cipher_key, self.mode, iv)
        ciphertext = aes.encrypt(self.text)
        # Calculate the MAC over the IV and the ciphertext
        mac = hmac_sha1(mac_key, iv + ciphertext)
        # Base64 encode the IV, ciphertext and MAC
        return b64encode(iv + ciphertext + mac)

    def decrypt(self):
        """
        Decrypt text
        """
        # Base64 decode
        try:
            iv_ciphertext_mac = b64decode(self.text)
        except TypeError:
            return None
        # Separate the IV, ciphertext and MAC
        iv = iv_ciphertext_mac[:BLOCK_SIZE]
        ciphertext = iv_ciphertext_mac[BLOCK_SIZE:-MAC_SIZE]
        mac = iv_ciphertext_mac[-MAC_SIZE:]
        # Derive the cipher and MAC keys
        (cipher_key, mac_key) = derive_keys(self.key)
        # Calculate the expected MAC
        expected_mac = hmac_sha1(mac_key, iv + ciphertext)
        # Check the MAC
        if mac != expected_mac:
            return None
        # Decrypt the ciphertext
        aes = AES.new(cipher_key, self.mode, iv)
        return aes.decrypt(ciphertext)

if __name__ == "__main__":
    key = generate_key()
    print 'Key:', key
    # Encrypt and decrypt a short message
    text = 'Hello world!'
    c = Cipher(key, text)
    msg = c.encrypt()
    c.set_text(msg)
    print '\nCiphertext:', msg
    print 'Length:', len(msg)
    print 'Plaintext:', c.decrypt()
    # Encrypt and decrypt a long message
    text = 'Gosh this is a long message, far too long to fit in a tweet I dare say, especially when you consider the encryption overhead'
    c = Cipher(key, text)
    msg = c.encrypt()
    c.set_text(msg)
    print '\nCiphertext:', msg
    print 'Length:', len(msg)
    print 'Plaintext:', c.decrypt()
    # Check that modifying the message invalidates the MAC
    text = 'Hello world!'
    c = Cipher(key, text)
    msg = c.encrypt()
    msg = msg[:16] + msg[17] + msg[16] + msg[18:]
    c.set_text(msg)
    print '\nCiphertext:', msg
    print 'Length:', len(msg)
    print 'Plaintext:', c.decrypt()
