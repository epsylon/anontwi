import os,sys
import HTMLParser
import sys, traceback
from core.wrapper import * 
from core.config_web import * 



class WebWrapperAnontwi(WrapperAnontwi):
    """ Wrapper for anontwi webserver"""

    def __init__(self):
        self.log = logging.getLogger('WebAnontwi')
        #.addHandler(logging.NullHandler)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.log.addHandler(ch)
        self.log.setLevel(logging.WARNING)
        self.app = anontwi()
        self.options = '' 
        self.at=self.get_access_tokens()
        self.ct=self.get_consumer_tokens()
        self.sa=self.get_source_api()
        self.ui=False
        self.proxy=None
        self.proxy_ip_address=None
        self.proxy_port=None
        os.environ["ANONTWI_TOKEN_KEY"]=self.at['access_token']
        os.environ["ANONTWI_TOKEN_SECRET"]=self.at['secret_token']


    def init_log(self):
        out_log = file('outlog', 'w')
        err_log = file('errlog', 'w', 0)
        sys.stdout.flush()
        sys.stderr.flush()
        os.dup2(out_log.fileno(), sys.stdout.fileno())
        os.dup2(err_log.fileno(), sys.stderr.fileno())


    def get_config(self):
        return "at : "+ str(self.at) +" | ct : " + str(self.ct) +" | sa : " + str(self.sa)

    def parse_url_opts(self,args):
        h=HTMLParser.HTMLParser()
        func = "get_config"
        self.proxy=self.get_proxy(args)
#        print Proxy : "+repr(self.proxy)
        cmdargs=[]
        
        cret=[]
        cout=""
        key=""
        
        if(args.has_key('control')):
            self.init_log()
            if h.unescape(args['control'][0]) == "search_messages" :
                if args.has_key("search"):
                    p=args["search"][0].strip().replace(" ","+")
                    print p
                    q=p.decode('utf-8', 'xmlcharrefreplace')
                    print q
                    r=h.unescape(q).encode("ascii", 'xmlcharrefreplace')
                    print r
                    cret =  self.search_messages(str(r),"10", self.proxy)
                    if(len(cret)>0):
                        for i  in range(len(cret)):
                            cout += self.render_tweet(cret[i])
                    else:
                            cout+="<i>no results found.</i>"
                else:
                    cout+="<i>You need to specify a search term !</i>"

            if(h.unescape(args['control'][0]) == "send_tweet"):
                func="send_tweet"
                mtc = getattr(self,func)
                enc = {'enc':False}
                if 'pin' in args:
                    if(len(args['pin'][0])>0):
                        enc = { 'enc' : True,
                                'pin' : args['pin'][0], }
                t=mtc(args['tweet'][0],{'pm':False,'user':''},False,False,enc,self.proxy_obj())
                return self.get_out_log()

            if(h.unescape(args['control'][0]) == "send_message"):
                func="send_tweet"
                mtc = getattr(self,func)
                enc = {'enc':False}
#                print repr(args)
                if 'pin' in args:
                    if(len(args['pin'][0])>0):
                        enc = { 'enc' : True,
                        'pin' : args['pin'][0], }
                if(len(args['message_to'][0])>0):
                    t=mtc(args['tweet'][0],{'pm':True,'user':args['message_to'][0].strip()},False,False,enc,self.proxy_obj())
                else:
                    return "You need to specify a username !"
                return self.get_out_log()

            if(h.unescape(args['control'][0]) == "get_out_log"):
                func="get_out_log"
                mtc = getattr(self,func)
                cout += mtc()

            if(h.unescape(args['control'][0]) == "get_err_log"):
                func="get_err_log"
                mtc = getattr(self,func)
                cout += mtc()

            if(h.unescape(args['control'][0]) == "get_err_log"):
                func="get_err_log"
                mtc = getattr(self,func)
                cout += mtc()

            if(h.unescape(args['control'][0]) == "friendlist"):
                func="friendlist"
                mtc = getattr(self,func)
                fl=mtc(self.proxy_obj())
                for f in fl:
                    cout += f.GetName()+ ' (' + f.GetScreenName()+")<br/>";

            if(h.unescape(args['control'][0]) == "get_timeline"):
                func="get_time_line"
                mtc = getattr(self,func)
                cout += mtc()

            if(h.unescape(args['control'][0]) == "get_public_timeline"):
                func="show_public"
                if not self.ui :
                    self.ui = self.get_userinfo(self.get_proxy())
                    mtc = getattr(self,func)
                    status= mtc(self.ui["user"],"10", self.get_proxy())
                    for c in status:
                        cout+=self.render_tweet(c)

            if(h.unescape(args['control'][0]) == "get_private_timeline"):
                func="show_private"
                mtc = getattr(self,func)
                (status,dm) = mtc("10", self.proxy_obj())
                for c in status:
                    cout+=self.render_message(c)
                    

            if(h.unescape(args['control'][0]) == "decrypt"):
                func=args['control'][0]
                mtc = getattr(self,func)
                try:
                    cout += mtc(args['tweet'][0],args['pin'][0])
                except:
                    cout += "Error decoding message"

            if(h.unescape(args['control'][0]) == "gen_pin"):
                try:
                    cout += self.generate_key()
                except:
                    cout += "Error generating pin ! "
                    
            if(h.unescape(args['control'][0]) == "unfollow"):
                func=args['control'][0]
                mtc = getattr(self,func)
                try:
                    u=mtc(args['name'][0], self.proxy_obj())
                    cout += "no longer following " + u.GetName()
                except:
                    cout += "Error unfollowing "+ args['name'][0]
                    #cout +=traceback.format_exc()

            if(h.unescape(args['control'][0]) == "follow"):
                func=args['control'][0]
                mtc = getattr(self,func)
                try:
                    u=mtc(args['name'][0], self.proxy_obj())
                    cout += "now following " + u.GetName()
                except:
                    cout += "Error following "+ args['name'][0]

            if(h.unescape(args['control'][0]) == "encrypt"):
                func=args['control'][0]
                mtc = getattr(self,func)
                cout += mtc(args['tweet'][0],)

            if(h.unescape(args['control'][0]) == "get_trends"):
                l=self.search_topics(self.proxy_obj())
                if(len(l)):
                    cout+="<ul>"
                    for t in l:
                        cout += "<li>"+t
                    else:
                        cout+="<i>no results found.</i>"
                    cout+="</ul>"

        try:
            if(cout==""):
                mtc = getattr(self,func)
                cret =  mtc()
                cout+=cret.strip()
        except Exception as e:
            cout +=traceback.format_exc()
        return cout

    def get_out_log(self):
        sys.stdout.flush()
        out_log = file('outlog', 'r')
        return out_log.read().replace('\n','<br />\n')

    def get_err_log(self):
        sys.stderr.flush()
        err_log = file('errlog', 'r')
        return err_log.read()


    def get_trends(self):
        tt="";
        try:
            ts = self.search_topics(count=10)
            for t in ts:
                tt+="<li>"+t
        except Exception as e:

            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "*** print_tb:"+e.message
            traceback.print_tb(exc_traceback, file=sys.stdout)
            return "Error: getting trends <br/>" + e.message+" <br/>" + str(exc_type)
        return tt


    def get_time_line(self,proxy=None):
        tl=False;
        try:
            (tl,no) = self.home_timeline(10,proxy)
        except Exception as e:

            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "*** print_tb:"
            traceback.print_tb(exc_traceback, file=sys.stdout)
            return "Error: Showing home timeline <br/>" + e.message+" <br/>" + str(exc_type)
        out=""
        for i in tl:
                out += self.render_status(i)
        return out
                #        return "timeline"
                #    cout +="args: " + args["control"][0] + "<br/>"

    def render_date(self,text):
        return "<i> at " +text[11:19] +" (GMT) on "+ text[4:10]+" " +text[27:30]+'</i><br/>'
        
    def render_html(self,text):
        import re
        t1=re.sub(r'(https?://([-\w\.]+)+(/([\w/_\.]*(\?\S+)?(#\S+)?)?)?)',r'<a target="_blank" style="color:red" href="\1">\1</a>',text)
        t2=re.sub(r'^@(\w+)',r'<a style="color:red" href="http://twitter.com/\1">@\1</a>',t1)
        t3=re.sub(r'\s@(\w+)',r' <a style="color:red" href="http://twitter.com/\1">@\1</a>',t2)
        #t3=re.sub(r'\s+#(\w+)',r'<a href="http://search.twitter.com/search?q=%23\1">#\1</a>',t2);
        t4=re.sub(r'\s#(\w+)',r' <a target=""c_output" style="color:green" href="control.py?control=search_messages&search=\1&'+self.proxy_getvars()+r'">#\1</a>',t3);
        text=re.sub(r'^#(\w+)',r' <a target=""c_output" style="color:green" href="control.py?control=search_messages&search=\1&'+self.proxy_getvars()+r'">#\1</a>',t4);
        return text
        
    def render_tweet(self,message):
        if message.user is None:
            return ('<div class="tweet">'+self.render_date(message.created_at)+self.render_html(message.text)+'</div>')
        else:
            return ('<div class="tweet"><img style="float:left"  src="'+message.user.profile_image_url+'"><div style="margin-left:50px;">'+message.user.screen_name +'<br/>'+self.render_date(message.created_at)+'</div><br/><br/>'+self.render_html(message.text)+'</div>')

    def render_status(self,status):
        return ('<div class="tweet"><img style="float:left"  src="'+status.user.profile_image_url+'"><div style="margin-left:50px;">User: '+status.user.screen_name+'<br/>'+ self.render_date(status.created_at)+'</div><br/>'+self.render_html(status.text)+'</div>')

    def render_message(self,message):
        return ('<div class="tweet">From: <b>'+message.sender_screen_name+'</b> To :<b> '+message.recipient_screen_name+'</b><br/>'+self.render_date(message.created_at)+'<br/>'+self.render_html(message.text)+'</div>')


    def get_userinfo(self,proxy=None):
#        print "proxy for userinfo : "+repr(proxy);
        if not self.ui :
            self.ui = self.get_user_info(proxy)
        return self.ui

    def get_nickname(self,proxy=None):
        if not self.ui :
            self.ui = self.get_userinfo(proxy)
        return self.ui['nickid']

    def get_username(self,proxy=None):
        if not self.ui :
            self.ui = self.get_userinfo(proxy)
        return self.ui['user']

    def get_profile_image(self,proxy=None):
        if not self.ui :
            self.ui = self.get_userinfo(proxy)
        return "<img src='"+ self.ui['url_profile']+"' alt='avatar'></img>"
            
    def write_tokens(self, access, consumer, source_api, proxy):
        print('Writing tokens')
        return
        # check directories

    def nono_write_tokens(self, access, consumer, source_api, proxy):
        if not os.path.exists(DIR_HOME_ANON):
            #            self.log.info(DIR_HOME_ANON + " created.")
            os.makedirs(DIR_HOME_ANON)
        if not os.path.exists(DIR_TOKENS):
        #            self.log.info(DIR_TOKENS + " created.")
            os.makedirs(DIR_TOKENS)
            open(DIR_TOKENS + FILE_ACC_TKN, 'w').write(access['access_token'] + '\n' + access['secret_token'])
            open(DIR_TOKENS + FILE_CONS_TKN, 'w').write(consumer['consumer_key'] + '\n' + consumer['consumer_secret'])
        if source_api.has_key('source_api'):
                open(DIR_TOKENS + FILE_SOURCE_API, 'w').write(source_api['source_api'])
        if not proxy == None:
                if proxy.has_key('ip_address') and proxy.has_key('port'):
                        open(DIR_TOKENS + FILE_PROXY_URL, 'w').write(proxy['ip_address']+'\n' + proxy['port'])
                else:
                        open(DIR_TOKENS + FILE_PROXY_URL, 'w').write("None")
        else:
                open(DIR_TOKENS + FILE_PROXY_URL, 'w').write("None")

    def get_proxy(self, args=None):
        """
        Get proxy from POST parameters
            Returns: proxy
        """
        purl=""
        pport=""
        if(self.proxy != None):
            return self.proxy
        if args== None:
            return None
        if 'proxy' in args :
                try:
                    purl=args['proxy_url'].strip()
                    pport=args['proxy_port'].strip()
                    self.proxy={'proxy':True,'ip_address':purl,'port':pport}
                    print repr(self.proxy)
                    return self.proxy
                except:
                    try:
                        purl=args['proxy_url'][0].strip()
                        pport=args['proxy_port'][0].strip()
                        self.proxy={'proxy':True,'ip_address':purl,'port':pport}
                    except: 
                        try:
                            purl=args['proxy_url'][0].strip()
                            pport=args['proxy_port'][0].strip()
                            self.proxy={'proxy':True,'ip_address':purl,'port':pport}
                        except: 
                            print("no proxy found")
                            return None
        else:
            return None    
        self.proxy=purl+":"+pport
        self.proxy_ip_address=purl
        self.proxy_port=pport

        return self.proxy
#>>>>>>> a12f5106d7a1b3d34f7ea2420906b412579a8f66

    def nono_get_proxy(self):
        file_path = DIR_TOKENS + FILE_PROXY_URL
        try:
            lines = open(file_path).readlines()
            #            self.log.debug('[get_proxy_url]')
            #            self.log.debug('Path: ' + file_path)
            #            self.log.debug('Proxy URL: ' + lines[0].strip())
            if lines[0].strip()== 'None':
                return None
                #            self.log.debug('Proxy Port: ' + lines[1].strip())
                self.proxy={'proxy':True,'ip_address':lines[0].strip(),'port':lines[1].strip()}
                return self.proxy
        except: 
                #            self.log.info("Proxy URL NOT found, path: %s" % file_path)
                print("Proxy URL NOT found, path: %s" % file_path)

        return {'proxy':0,'ip_address':None,'port':None}


    def save_proxy(self,args):
        self.proxy={'proxy':True,'ip_address':h.unescape(args['proxy_url'][0]),'port':h.unescape(args['proxy_port'][0])}
        self.write_tokens(self.at,self.ct,self.sa,self.proxy)

    def delete_proxy(self):
        self.proxy=None
        self.write_tokens(self.at,self.ct,self.sa,self.proxy)


    def proxy_html(self,args):
        self.get_proxy(args)
        if self.proxy!=None:
            ret= """<input type="hidden" name="proxy" value="proxy" id="displaypro" > <input name="proxy_url" type="hidden" size="16" value='"""
            ret+=self.proxy_ip_address
            ret+="""'> <input name="proxy_port" type="hidden" size="4" value='"""
            ret+=self.proxy_port
            ret+="""'>"""
            return ret
        else:
            return ""
            
    def proxy_header(self,args):
        self.get_proxy(args)
        if self.proxy!=None:
            ret= """Using proxy """
            ret+=self.proxy_ip_address+":"
            ret+=self.proxy_port
            ret+= """(<a href="/">change</a>)"""
            return ret
        else:
            ret= """No proxy (<a href="/">set proxy</a>)"""
            return ret
            
    def proxy_getvars(self,args=None):
        self.get_proxy(args)
        if self.proxy !=None:
            ret= """proxy=proxy&proxy_url="""
            ret+=self.proxy_ip_address+"&proxy_port="
            ret+=self.proxy_port
            return ret
        else:
            return ""

    def proxy_obj(self):
        if self.proxy==None:
            return None #  {'proxy':0,'ip_address':None,'port':None}
        return  {'proxy':1,'ip_address':self.proxy_ip_address,'port':self.proxy_port}
            
