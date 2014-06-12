#! /usr/bin/env python
# coding:utf-8
import ConfigParser
from pypump import PyPump, Client

class newAccount():
	def __init__(self, profile):
		self.profile = profile
		self.account = str(raw_input("Do you want to create \n 1 - Twitter \n 2 - Pump \n 3 - Both \n Type number: "))
		self.config = ConfigParser.RawConfigParser()
		self.accounts = {'1' : self.auth_twitter(), '2' : self.auth_pump(), '3' : self.auth_both()}
		self.accounts[self.account]
		
	def auth_pump(self):
		client = Client(
			webfinger=raw_input('Insert your Pump ID (user@node): '),
			type="native",
			name="AnonTwi"
		)
		pump = PyPump(client=client, verifier_callback=self.simple_verifier)
		client_credentials = pump.get_registration() 
		client_tokens = pump.get_token()
		self.config.add_section('Pump')
		self.config.set('Pump', 'client_key', client_credentials[0])
		self.config.set('Pump', 'client_secret', client_credentials[1])
		self.config.set('Pump', 'token_key', client_tokens[0])
		self.config.set('Pump', 'token_secret', client_tokens[1])
		with open('config', 'wb') as configfile:
			self.config.write(configfile)
			print "Pump config written"

	def auth_twitter(self):
		self.request_url(

	def auth_both(self):
		self.auth_twitter()
		self.auth_pump()

	def simple_verifier(self, url):
		print 'Open the following url and enter the Verifier: ' + url
		return raw_input('Verifier: ')
	
	def request_url(self, consumer_key = '', consumer_secret = '', source_api = '', gtk = False):
		"""Request Access Tokens"""
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
		
		#if gtk:
				#self.consumer_key = consumer_key
				#self.consumer_secret = consumer_secret
				#self.source_api = source_api
		#signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
		#oauth_consumer             = oauth.Consumer(key = self.consumer_key, secret = self.consumer_secret)
		#if self.source_api == "identi.ca/api":
			#self.request_token_url = "https://identi.ca/api/oauth/request_token?oauth_callback=http://anontwi.sf.net"
		#oauth_client               = oauth.Client(oauth_consumer, proxy_info = proxy_info)
		#eprint ('\n')
		
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

 

account = newAccount('Default')
