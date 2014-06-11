# AnonTwiWeb v0.1 - psy <epsylon@riseup.net> - 2012
from core.webwrapper import WebWrapperAnontwi
wwa = WebWrapperAnontwi()
error=False
try:
    un=wwa.get_username()
except Exception as e:
    un=""
    error="Error : "+e.message

output = """
<html>
<head>
  <title>AnonTwiWeb v0.1 - http://anontwi.sf.net</title>

  <link href="images/favicon.ico" rel="shortcut icon" type="image/x-icon" />

<script>
        function toggle3() {
                var ele = document.getElementById("togglepro");
                var text = document.getElementById("displaypro");
                if(ele.style.display == "block") {
                        ele.style.display = "none";
                        text.innerHTML = "show";
                }
                else {
                        ele.style.display = "block";
                        text.innerHTML = "hide";
                }
                         } 

function NavigateToSite(){
    window.location = "webgui.py";
}
</script>

</head>
<body bgcolor="#ccc">
    <form method="post" action="webgui.py">
	<div>
         <table align="center" bgcolor="white">
            <tr>
             <td>
           <center>
            <img src="images/anontwi.png" alt="anontwi" target="_blank"> <br /><br />
            <center>@"""+un+"""</center> <br />
            Use proxy: <input type="checkbox" name="proxy" value="proxy" id="displaypro" onchange="javascript:toggle3();"> 
           </center><br />
         <fieldset>
                <div name="proxy" style="display: none" id="togglepro">
                Server: <input name="proxy_url" type="text" size="16" value="http://127.0.0.1"> 
                Port: <input name="proxy_port" type="text" size="4" value="8118">
                </div>
         </fieldset>
            <br />
            <div align="center"><button type="submit" style="width: 168px">Connect!</button></div>
            <br />
             </td>
            </tr>
          </table>
"""
if error:
    output+="""<div align="center">"""+error+"""</div>"""
output+="""	</div>
    </form>
</body>
</html>
"""
