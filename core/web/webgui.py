# AnonTwiWeb v0.1 - psy <epsylon@riseup.net> - 2012/ 2013
# retrieve data about user (with indications of previous window)

from core.webwrapper import WebWrapperAnontwi
wwa = WebWrapperAnontwi()

tc=""
tt=""
pt=""
ph=""
pgv=""
    
try:
    ucc = wwa.get_userinfo(wwa.get_proxy(post))
    uc= u"Nick : "+ ucc['nickid']+" - Tweets : "+ str(ucc['statuses_count'])+" - Followers : "+ str(ucc['followers'])+" - Friends : "+str(ucc['friends'])+" - User : "+ucc['user']
except Exception as e:
    import traceback
    import sys
    uc="failed to get user information... (post: "+repr(post)+")"+ e.message+"<!--"+traceback.format_exc()+"-->"
try: 
    pi= wwa.get_profile_image()
except Exception as e:
    import traceback
    import sys
    pi="failed to get profile image..."+ e.message+"<!--"+traceback.format_exc()+"-->"    
try:
    pt=wwa.proxy_html(post)
    ph=wwa.proxy_header(post)
    pgv=wwa.proxy_getvars(post)
except Exception as e:
    import traceback
    import sys
    ph="failed to parse proxy : "+ e.message+"<!--"+traceback.format_exc()+"-->"
    
output = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
  <title>AnonTwiWeb v0.1 - http://anontwi.sf.net</title>

  <link href="images/favicon.ico" rel="shortcut icon" type="image/x-icon" />
<script lang="javascript">
/*
function taken from

http://stackoverflow.com/questions/246801/how-can-you-encode-a-string-to-base64-in-javascript#246813
*/

  function generate_pin() {
    var output = "";
    var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
    var i = 0;
    var _keyStr= "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    var input="";
    for(i=0;i<32;i++)
        input += Math.floor(Math.random()*10);
    i=0;

    while (i < input.length) {

        chr1 = input.charCodeAt(i++);
        chr2 = input.charCodeAt(i++);
        chr3 = input.charCodeAt(i++);

        enc1 = chr1 >> 2;
        enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
        enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
        enc4 = chr3 & 63;

        if (isNaN(chr2)) {
            enc3 = enc4 = 64;
        } else if (isNaN(chr3)) {
            enc4 = 64;
        }

        output = output +
        _keyStr.charAt(enc1) + _keyStr.charAt(enc2) +
        _keyStr.charAt(enc3) + _keyStr.charAt(enc4);

    }
    document.getElementById("id_generate_pin").value=output;
}
</script>
</head>
<body bgcolor="#fbfbfb">
   <div>
       <div align="center">
"""+pi+"""<pre>"""+uc+"""</pre>
"""+ph+"""
     <div>
     <hr>
<center>
<table>
  <tr>
    <td>"""
output+="""
               <!--<iframe name="c_outlog" height="340px" src="/control?control=get_out_log"></iframe> <br />-->
               <iframe name="c_timeline" height="380px" width="380px" src="control?control=get_timeline&"""+pgv+""""></iframe> <br />
     </td>

     <td>
               <iframe name="c_public" height="380px" width="380px" src="control?control=get_public_timeline&"""+pgv+""""></iframe> <br />
      </td>
     <td>
               <iframe name="c_private" height="380px" width="380px" src="control?control=get_private_timeline&"""+pgv+""""></iframe> <br />
      </td>
  </tr>
   <tr>

    <td> 
<center>              
       <!--<form target="c_outlog" action="control"><input type="hidden" name="control" value="get_out_log"/><input type="submit" value="Output"/></form>
       <form target="c_outlog" action="control"><input type="hidden" name="control" value="get_err_log"/><input type="submit" value="Error Log"/></form>-->
       <form target="c_timeline" action="control">"""+pt+"""<input type="hidden" name="control" value="get_timeline"/><input type="submit" value="Refresh Home"/></form>
</center>
    </td>

    <td>
<center>              
<form target="c_public" action="control">"""+pt+"""<input type="hidden" name="control" value="get_public_timeline"/><input type="submit" value="Refresh Public"/></form>
</center>
    </td>

    <td>
<center>              
       <form target="c_private" action="control">"""+pt+"""<input type="hidden" name="control" value="get_private_timeline"/><input type="submit" value="Refresh Private"/></form>
</center>
    </td>
    </tr>
  </table>
</center>
<hr >
 <center>
         <table cellpadding="4">
            <tr>
              <td>
                <form name="messages" action="control"  target="c_output">
                <input type="hidden" value="decrypt" name="control"/>
                   Decrypt text or <u>tweet's url</u>: <br />
                   <textarea name="tweet" rows="5" cols="50"></textarea>
              </td>
              <td>   
                   PIN: <input name="pin" type="text" size="46" value=""><br /><br />
                   <button type="submit"  style="width:140px">Decrypt!</button> 
                 </form>
              </td>
            </tr>
         </table>
 </center>
<hr >
    <center>
          <table align="center" cellpadding="6">
            <tr>
              <td>
                  <form name="messages" action="control"  target="c_output">
                   <div>
		   Tweet <input type="radio" name="control" CHECKED value="send_tweet"/> <br />
		   Direct Message <input type="radio" name="control" value="send_message"/><br /><br />
                   to <input type="text" name="message_to"/ value="@"><br />
 		   <textarea name="tweet" rows="5" cols="47"> </textarea><br /><br />
       <input type="button" onclick="generate_pin()" value="Generate PIN"/> <input id="id_generate_pin" name="pin" type="text" size="24" value=""><br /><br />
         """+pt+"""
	        <div><button type="submit" style="width: 168px">Send!</button></div>
                   </div>
                 </form>
               </td>

               <td>
             <div name="recievebox">
               <iframe name="c_output" width="740px" height="300px"></iframe>
             </div>
               </td>
           </tr>
           </table>

         </center>


	 </fieldset>
<hr>
  <center>
    <table cellpadding="4">
     <tr>
      <td>
        <form name="messages" action="control" target="c_output">
         <input type="hidden" value="search_messages" name="control"/>                      
           <div>
              Text or Tag(s): <input name="search" type="text"  size="20" value="">
              <button type="submit"  style="width: 103px">Search!</button>
              """+pt+"""
           </div>
        </form>
      </td>
      <td>
 <form name="messages" action="control"  target="c_output">
      Follow: <input type="radio" CHECKED name="control" value="follow"> 
           Unfollow: <input type="radio" name="control" value="unfollow"> 
                """+pt+"""
                    <input name="name" type="text" size="16" value="@">
                        <button type="submit">Do it!</button>
                         </form>
      </td>
      <td>
         <form target="c_output" action="control">"""+pt+"""<input type="hidden" name="control" value="friendlist"/><input type="submit" value="Friendlist"/></form>                                                  
         </form>
      </td>
      <td>
        <form target="c_output" action="control">"""+pt+"""<input type="hidden" name="control" value="get_trends"/>
                 <input type="submit" value="Trending Topics"/>
                         </form>

      </td>
     </tr>
   </table>
  </center>

<hr size=1/>
 <center>
<a href="http://anontwi.sf.net/howto.html" target="_blank">How to use AnonTwi</a> <br />
<a href="http://anontwi.sf.net/anontwi-encrypt.html" target="_blank">How secure is encryption?</a> <br />
<b>irc.freenode.net / #anontwi)</b>
</center>
</body>
</html>
"""
