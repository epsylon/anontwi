#! /usr/bin/env python2
# pancake <nopcode.org>

import os
import sys
from SocketServer import ForkingMixIn, ThreadingMixIn
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import BaseHTTPServer
from runpy import run_module
from urlparse import urlparse
import urllib
from cgi import parse_qs #, parse_header, parse_multipart
import cgi

# to remove when everything is working into the wrapper
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path + '/anontwi/')

port = 8080
wwwroot = "core/web/"
http = {} # global storage

class ForkingTCPServer(ForkingMixIn, HTTPServer): pass
class ThreadingTCPServer(ThreadingMixIn, HTTPServer): pass

def print_exception(type=None, value=None, tb=None, limit=None):
	if type is None:
		type, value, tb = sys.exc_info()
	import traceback
	ret = "<html><body><h2>Traceback (most recent call last):<h2 />"
	ret += "<pre>"
	list = traceback.format_tb(tb, limit) + \
		traceback.format_exception_only(type, value)
	ret += "exception error"
	ret += "%s: %s<br/>\n" % ( ("\n".join(list[:-1])), (list[-1]))
	ret +="</body></html>"
	del tb
	return ret

class HttpHandler(BaseHTTPRequestHandler):

        def __init__(self,a,b,c):
                self.post=None
                BaseHTTPRequestHandler.__init__(self, a,b,c)
                
	# TODO: whitelist out there
	def client_not_allowed(self, addr):
		return False
		if addr == "127.0.0.1":
			return False
		print ("Client not allowed ",addr)
		return True 

	def serve(self):
		self.rfile._sock.settimeout(10)
		output = ""
		uri = self.path
		tmp = uri.find ('?')
		args = parse_qs(urlparse(uri)[4])

		#from ipdb import set_trace;set_trace()
		if tmp != -1:
			uri = uri[0:tmp]
			for a in uri[tmp:-1].split("&"):
				sep = a.find ("=")
				if sep != -1:
					print "%s)(%s"%(a[0:sep],a[sep:-1])
					args[a[0:sep]]=a[sep:-1]
		
		file = wwwroot + "/" + uri
		if self.client_not_allowed (self.client_address[0]):
			self.wfile.write ("HTTP/1.0 503 Not allowed\r\n\r\nYou are not whitelisted")
			return
		content = ""
		try:
			ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
			print "CTYPE IS ",ctype
			if ctype == 'multipart/form-data':
				query = cgi.parse_multipart(self.rfile, pdict)
				content = query.get('upfile')
		except:
			pass
		print "Request from %s:%d"%self.client_address+"  "+uri
		if uri[-1] == '/' or os.path.isdir(file):
			file = file + "/index.py"
		if os.path.isfile(file+".py"):
			file = file + ".py"
		if file.find("py") != -1:
			modname = file.replace(".py", "")
			cwd = modname[0:modname.rfind('/')]+"/"
			modname = modname.replace("/", ".")
			while modname.find("..") != -1:
				modname = modname.replace("..",".")
			globals = {
				"output": output,
				"http": http,
				"post": self.post,
				"uri": uri,
				"args": args,
				"cwd": cwd,
				"headers": self.headers,
				"content": content
			}
			try:
				a = run_module(modname, init_globals=globals)
				output = a["output"]
			except:
				output = print_exception()
		else:
			try:
				f = open (file, "r")
				output = f.read ()
				f.close ()
			except:
				output = "404"
		if output == "404":
			self.wfile.write ("HTTP/1.0 404 Not found\r\n\r\n")
		else:
			self.wfile.write ("HTTP/1.0 200 OK\r\n\r\n")
			try:
                                self.wfile.write (output.encode('ascii', 'xmlcharrefreplace'))
                                #print "ascii output"

                        except:
                                try:
                                        self.wfile.write (output .encode("utf-8" ,"ignore"))
                                        #print "utf8 output"
                                except:
                                        self.wfile.write (output)
                                        #print "raw output"

	def do_POST (self):
                content_len = int(self.headers.getheader('content-length'))
                if content_len >0:
                        post_body = self.rfile.read(content_len)
                        rawlist = post_body.split('&')	# obtain list of key=val strings
                        self.post = {}
                        for k in rawlist:
                                tmpli = k.split('=')			# get key, val list
                                self.post[tmpli[0]] = urllib.unquote(tmpli[1])	# save pair in dict

                        print "found post vars : " + repr(self.post)
                else:
                    self.post=None
                self.serve ()

	def do_GET (self):
		self.serve ()

	def ok_headers():
		self.send_response(200)
		self.send_header("Content-type", "text/html charset=utf-8")
		self.end_headers()


class AnonTwiWebserver():
    def __init__(self, ref, *args):
	HttpHandler.ref = ref
        httpd = HTTPServer(('', port), HttpHandler)
        print "http://127.0.0.1:%d/ : Serving directory '%s/www'" % (port, os.getcwd())
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print 'Server killed on user request (keyboard interrupt).'

if __name__=="__main__":
    wwwroot = "www"
    httpd = HTTPServer(('', port), HttpHandler)
    print "http://127.0.0.1:%d/ : Serving directory '%s/web'" % (port, os.getcwd())
    
    try:
    	httpd.serve_forever()
    except KeyboardInterrupt:
    	print 'Server killed on user request (keyboard interrupt).'
