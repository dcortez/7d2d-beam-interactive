# 7 Days to Die - ScottyBot Integration (Python)
## YOU MUST INSTALL PYTHON 3.3 or ABOVE


### CAVEATS
    NOTE: YOU MUST HAVE A DEDICATED SERVER WITH TELNET ENABLED, THIS WILL NOT CONNECT TO GAME CLIENT!
        
        you should have a serverconfig.xml file with the following lines:
        <property name="TelnetPassword" value="<TELNET_PASSWORD>"/>
        <property name="TelnetPort" value="<TELNET_PORT>"/>
        <property name="TelnetEnabled" value="true"/>

_These instructions have been tested and work on Windows/Linux/mac_

1. Download and install Python 3.3 or above
   * Follow instructions at - https://www.python.org/downloads/

2. Download our files _(telnet.py, scottyint.py & items.py)_
  * Download the files and folders _(will download 7d2d-beam-interactive-python.zip)_
  * Unzip the files into an easy to remember location _(will create a folder called 7d2d-beam-interactive-python)_
  * Open the newly unzipped folder and copy telnet.py & interactive.py
  * Paste our files in the folder created in step 2 _(beam-interactive-python-master - you can change the folder name)_

3. Open the scottyint.py script _(open with text editor of your choosing)_
   * Change the info on line's 14 & 18 - 21
   * Save the changes

4. Open cmd(windows) or terminal(linux/unix)
   * cd to the directory where you unziped the files in step 2.
   * Run the scottyint script
      * py -3 scottyint.py _(windows)_
      * python3 scottyint.py _(linux/unix)_

_If you get module errors when trying to run_

5. Open cmd(windows) or terminal(linux/unix)
   * Install module modules you are missing
         * pip3 install <module> _(window/linux/unix)_
            * _If if it warns about pip being outdated update it_
            * _You may have to do this for multiple modules_
