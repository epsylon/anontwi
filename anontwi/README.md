===============================================
AnonTwi (http://anontwi.03c8.net)
===============================================

FIGHT CENSORSHIP!! being more safe on social networking sites...

                .   :   .            
            '.   .  :  .   .'        
         ._   '._.-'''-._.'   _.     
           '-..'         '..-'       
        --._ /.==.     .==.\ _.--    
            ;/_o__\   /_o__\;        
       -----|`     ) (     `|-----   
           _: \_) (\_/) (_/ ;_       
        --'  \  '._.=._.'  /  '--    
          _.-''.  '._.'  .''-._      
         '    .''-.(_).-''.    '     
             '   '  :  '   '.        
                '   :   '            
                    '                

AnonTwi provides you:

      + AES + HMAC-SHA1 encryption on Tweets and Direct Messages 
      + Secure Sockets Layer (SSL) to interact with API
      + Proxy Socks (for example, to connect to the TOR network)
      + Random HTTP header values
      + Send long messages splitted automatically
      + Automatic decryption of tweet's urls or raw inputs
      + Backup messages to your disk (max: 3200)
      + Send fake geolocation places
      + Remove data and close account (suicide!)
      + View global Trending Topics
      + UTF-8 + Unicode support (chinese, arabic, symbols, etc)
      + Multiplatform: GNU/Linux, MacOS, Win32
      + Detailed colourful output results
      + Generate tools and modules
      + GTK+ interface
      + An IRC bot slave

And many other features than you can see detailed below:

======
INDEX:
======

 1) How-To Start
 2) Examples
 3) Contribute
 3) Contact

=============
How-To Start:
=============

--------
Install:
--------
Code runs on many platforms. It requires Python and the following libraries:

      - python-crypto   - cryptographic algorithms and protocols for Python

      - python-httplib2 - comprehensive HTTP client library written for Python

      - python-pycurl   - python bindings to libcurl

      - python-glade2   - GTK+ bindings: Glade support 

On Debian-based systems (ex: Ubuntu), run:

      - directly:

              sudo apt-get install python-crypto python-httplib2 python-pycurl python-glade2

      - using setup-tools (http://pypi.python.org/pypi/setuptools):

              easy_install <packages>

On Windows systems, is working (tested!) with:

      - python 2.7      - http://www.python.org/getit/
      - pycrypto 2.3    - http://www.voidspace.org.uk/downloads/pycrypto-2.3.win32-py2.7.zip
      - httplib2 0.7.4  - http://httplib2.googlecode.com/files/httplib2-0.7.4.zip
      - pycurl 7.19.5.1 - http://pycurl.sourceforge.net/download/
      - pygtk 2.24      - http://www.pygtk.org/downloads.html

      - using setup-tools (http://pypi.python.org/pypi/setuptools):

              easy_install.exe <packages>


------------------------
"Consumer" keys:
------------------------
   + To use OAuth you need this tokens: 'consumer key' and 'consumer secret'.

   - Create a third party APP on your profile. 

      + GNU/Social:
         - Login to your account         
         - Go to: Settings
         - Click on: "Register an OAuth client application"
         - Click on: "Register a new application"
             * <yoursocialnetwork.net>/settings/oauthapps/new

         - Fill form correctly
             * Icon: You can use AnonTwi website logo
             * Name: (ex: AnonTwi)            
             * Description: (ex: Anontwi -GNU/Social edition-)
             * Source URL: (ex: http://anontwi.03c8.net)
             * Organization: (ex: AnonTwi)
             * Homepage: (ex: http://anontwi.03c8.net)

             * Callback URL: (leave this BLANK)
             * Type of Application: Desktop
             * Default access for this application: Read-Write

     + Twitter:
         - Login to your account         
         - Go to: https://apps.twitter.com/
         - Click on: "Create New App"
             * https://apps.twitter.com/app/new

         - Fill form correctly
             * Name: (ex: AnonTwi)            
             * Description: (ex: Anontwi -GNU/Social edition-)
             * Website: (ex: http://anontwi.03c8.net)
             * Callback URL: (leave this BLANK)

   - Get your OAuth settings: Click on the name of your new APP connector (ex: AnonTwi)
   - Open "config.py" (THIS FILE!) with a text editor, and enter tokens (below!)

   - Remember:
             * If you go to use shell mode, you should generate your tokens with command: --tokens 
             * For connect using TOR add: --proxy "http://127.0.0.1:8118"

   - Run ./anontwi or python anontwi (To use interface: ./anontwi --gtk)


---------------------
"Token" keys:
---------------------
   + To use OAuth you need this tokens: 'token key' and 'token secret'.
     
      - Launch: ./anontwi --tokens
      - Follow the link to read your "PinCode"
      - Enter your PinCode
      - After a few seconds, you will reviece a response like this:
               
                 "Generating and signing request for an access token
                  Your Twitter Access Token key: xxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                  Access Token secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      
   + With these tokens, you can start to launch -AnonTwi- commands like this:

       ./anontwi [-m 'text' | -r 'ID' | -d @user | -f @nick | -u @nick] [OPTIONS] 'token key' 'token secret'

   + Remember that you can EXPORT tokens like environment variables to your system, to don't use them every time
     If you did it, you can start to launch -AnonTwi- commands like this:

       ./anontwi [-m 'text' | -r 'ID' | -d @user | -f @nick | -u @nick] [OPTIONS]


=========
Examples:                                 
=========

   + To remember:

         - Connections to API are using fake headers automatically
         - To launch TOR, add this command: --proxy "http://127.0.0.1:8118"
         - Check if you are doing geolocation in your messages (usually is 'off' by default)
         - You can generate 'token key' and 'token secret' every time that you need
         - View output results with colours using parameter: --rgb (better with obscure backgrounds)
         - Use --gen to generate STRONG PIN/keys (ex: --pin '1Geh0RBm9Cfj82NNhuQyIFFHR8F7fI4q7+7d0a3FrAI=')
         - Try to add encryption to your life :)

-----------------------------------
Retrieve you API tokens, using TOR:
-----------------------------------

        ./anontwi --tokens --proxy "http://127.0.0.1:8118"

----------------------------------------------------
Generate PIN key for encrypting/decrypting messages:
----------------------------------------------------

        ./anontwi --gen

PIN key: K7DccSf3QPVxvbux85Tx/VIMkkDkcK+tFzi45YZ5E+g= 

Share this key privately with the recipients of your encrypted messages.
Don't send this key over insecure channels such as email, SMS, IM or Twitter.
Use the sneakernet! ;)

----------------------
Launch GTK+ Interface:
----------------------

        Enjoy visual mode experience ;)

        ./anontwi --gtk

------------------------
Launch an IRC bot slave:
------------------------

        Launch it and you will have a bot slave waiting your orders on IRC.

        ./anontwi --irc='nickname@server:port#channel'

        If you don't put a nickname or a channel, AnonTwi will generate randoms for you :)
 
        ./anontwi --irc='irc.freenode.net:6667'

------------------------
Short an url, using TOR:
------------------------

        ./anontwi --short "url" --proxy "http://127.0.0.1:8118"

-----------------------------------
Send a plain-text tweet, using TOR:
-----------------------------------

        ./anontwi -m "Hello World" --proxy "http://127.0.0.1:8118" 

------------------------
Send an encrypted tweet:
------------------------

        ./anontwi -m "Hello World" --enc --pin "K7DccSf3QPVxvbux85Tx/VIMkkDkcK+tFzi45YZ5E+g="

--------------
Remove a tweet: 
---------------

        You need the ID of the tweet that you want to remove.

                 - launch "--tu @your_nick 'num'" to see tweets IDs of your timeline.

        ./anontwi --rm-m "ID"

------------------
Retweet a message:
------------------

        You need the ID of the tweet that you want to RT. 
                
                 - launch "--tu @nick 'num'" to see tweets IDs of a user.
 
        ./anontwi -r "ID"

-------------------------------------------------
Send a plain-text DM (Direct Message), using TOR:
-------------------------------------------------

        ./anontwi -m "See you later" -d "@nick" --proxy "http://127.0.0.1:8118"

---------------------
Send an encrypted DM:
---------------------

        ./anontwi -m "See you later" -d "@nick" --enc --pin "K7DccSf3QPVxvbux85Tx/VIMkkDkcK+tFzi45YZ5E+g="

---------------
Remove a DM:
---------------

        You need the ID of the DM that you want to remove.

                 - launch "--td 'num'" to see Direct Messages IDs of your account.

        ./anontwi --rm-d "ID"

--------------------------------------
Send a media message, using TOR:
--------------------------------------

        Twitter will show your media links. For example, if you put a link to an image

        ./anontwi -m "https://host/path/file.jpg" --proxy "http://127.0.0.1:8118"

----------------------------------------
Send reply in a conversation, using TOR:
----------------------------------------

        You need the ID of the message of the conversation.

                 - launch "--tu @nick 'num'" to see tweets IDs of a user timeline.
                 - launch "--tf 'num'" to see tweets IDs of your 'home'.

        Add names of users that participates on conversation at start of your message.

        ./anontwi -m "@user1 @user2 text" --reply "ID" --proxy "http://127.0.0.1:8118"

---------------------------------
Send a friend request, using TOR:
---------------------------------

        ./anontwi -f "@nick" --proxy "http://127.0.0.1:8118"

----------------------------------
Stop to follow a user, using TOR:
----------------------------------

        ./anontwi -u "@nick" --proxy "http://127.0.0.1:8118"

----------------------------------
Create a favorite, using TOR:
----------------------------------

        ./anontwi --fav "ID" --proxy "http://127.0.0.1:8118"

----------------------------------
Destroy favorite, using TOR:
----------------------------------

        ./anontwi --unfav "ID" --proxy "http://127.0.0.1:8118"

------------------------
Block a user, using TOR:
------------------------

        ./anontwi --block "@nick" --proxy "http://127.0.0.1:8118"

--------------------------
Unblock a user, using TOR:
--------------------------

        ./anontwi --unblock "@nick" --proxy "http://127.0.0.1:8118"

-----------------------------------------
Show a number of recent tweets of a user:
-----------------------------------------

        You can control number of tweets to be reported. For example, 10 most recent tweets is like this:

        ./anontwi --tu "@nick 10"

-------------------------------------------------------
Show a number of recent tweets of your 'home' timeline:
-------------------------------------------------------

        You can control number of tweets to be reported. For example, 10 most recent tweets is like this:

        ./anontwi --tf "10"

-------------------------------------------------------
Show a number of recent favorites
-------------------------------------------------------

        You can control number of tweets to be reported. For example, 10 most recent tweets is like this:

        ./anontwi --tfav "@nick 10"

----------------------------------
Split a long message into "waves":
----------------------------------

        Very usefull if you want to send long messages. 
        It uses Twitter restrictions as much efficient as possible. 
        Encryption is allowed :)
       
        ./anontwi -m "this is a very long message with more than 140 characters..." --waves

----------------------------------
Send fake geolocation coordenates:
----------------------------------

        If you dont put any (--gps), coordenates will be random :)
        
        ./anontwi -m "text" --gps "(-43.5209),146.6015"

-------------------------------------------------
Show a number of Direct Messages of your account:
-------------------------------------------------

        You can control number of DMs to be reported. For example, 5 most recent DMs is like this:

        ./anontwi --td "5"

-------------------------------------------
Returns global Trending Topics, using TOR:
-------------------------------------------

        ./anontwi --tt --proxy "http://127.0.0.1:8118"

-------------------------------------------
Returns last mentions about you, using TOR:
-------------------------------------------

	You can control number of tweets to be reported. For example last recent tweet:

        ./anontwi --me "1" --proxy "http://127.0.0.1:8118"

---------------------------------------------
Decrypt a tweet directly from URL, using TOR:
---------------------------------------------
        
        Remeber, to decrypt, you need the PIN/Key that another user has used to encrypt the message (symmetric keys)
        To decrypt you don't need 'token key' and 'token secret' :)

        ./anontwi --dec "http://twitter.com/encrypted_message_path" --pin "K7DccSf3QPVxvbux85Tx/VIMkkDkcK+tFzi45YZ5E+g=" --proxy "http://127.0.0.1:8118" 

----------------------------------------
Decrypt a tweet directly from raw input:
----------------------------------------

        Remeber, to decrypt, you need the PIN/Key that another user has used to encrypt the message (symmetric keys)
        To decrypt you don't need 'token key' and 'token secret' :)
 
        ./anontwi --dec "7asNGpFFDKQl7ku9om9CQfEKDq1ablUW+srgaFiEMa+YK0no8pXsx8pR" --pin "K7DccSf3QPVxvbux85Tx/VIMkkDkcK+tFzi45YZ5E+g="

----------------------------------------------------------
Save tweets starting from the last (max: 3200), using Tor:
----------------------------------------------------------

	You can control number of tweets to be reported. For example last 1000 tweets:

	./anontwi --save "1000" --proxy "http://127.0.0.1:8118"

-------------------------------------------------
Save favorites starting from the last, using Tor:
-------------------------------------------------

	You can control number of tweets to be reported. For example last 100 tweets:

	./anontwi --sfav "@nick 100" --proxy "http://127.0.0.1:8118"

-------------------
Suicide, using TOR:
-------------------

        This will try to delete your tweets, your DMs and if is possible, your account.

        ./anontwi --suicide --proxy "http://127.0.0.1:8118"

===========
Contribute:
===========

        To make donations use the following hashes:

	- Bitcoin: 1Q63KtiLGzXiYA8XkWFPnWo7nKPWFr3nrc
	- Ecoin: 6enjPY7PZVq9gwXeVCxgJB8frsf4YFNzVp

========
Contact:
========

	To report bugs, questions and help, for suggestions or new development tasking forces, you welcome on: 
    
      - irc.freenode.net (channel: #AnonTwi)

