from core.webwrapper import WebWrapperAnontwi

wwa = WebWrapperAnontwi()

cout = wwa.parse_url_opts(args)

#cout += "<div><pre>"+wwa.get_out_log()+"</pre></div>"
#cout += "<div style='color:red;font-weight:bold'>Error log  : <pre>"+wwa.get_err_log()+"</pre></div>"

output= """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <title>AnonTwiWeb v0.1 - http://anontwi.sf.net</title>
<style>
.tweet{
background:white;
padding:4px;
width:auto;
overflow:auto;
margin-bottom:10px;
border-bottom:1px solid black;
}
</style>
</head>
<body>
"""+cout+"""
</body>
</html>"""
