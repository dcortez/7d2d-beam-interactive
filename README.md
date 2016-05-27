# beam-interactive-7d2d
Beam Interactive controls for 7 Days to Die


This will be a working repo for our Interactive controls for a 7 Days to Die server.

Basic design is as follows:
  - Viewer presses a button while viewing your stream to perform an action
    -- Actions include: spawn airdrop, debuffplayer, givequest, and more
  - 7d2d.js receives input and passes appropriate action to telnet.py (Python telnet script)
  - telnet.py connects to 7DaysToDie_Dedicated_Server telnet and sends command based on action passed.
  - ???
  - Profit?


NODE INSTALL REQUIREMENTS

  nodejs
  
  python2.7
  
  node-gyp  ( Follow the guide: https://github.com/nodejs/node-gyp#installation )
  
  npm
  
  
NODE DEPENDENCIES
  npm -g install beam-client-node beam-interactive-node python-shell random-js
  
After install - from command line:
  cd <7d2d-DIR LOCATION>
  node 7dtd.js
  
Enjoy!!!!!!!11
