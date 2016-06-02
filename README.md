# YOU MUST INSTALL PYTHON 3.3 or ABOVE

_These instructions have been tested and work on Windows/Linux/mac_

1. Download and install Python 3.3 or above
   * Follow instructions at - https://www.python.org/downloads/

2. Go to - https://github.com/WatchBeam/beam-interactive-python
    * Download all files and folders... 
    * Unzip the files into an easy to remember location

3. Open cmd(windows) or terminal(linux/unix)
   * cd to the directory where you unziped the files in step 1.
    * Run setup.py script _(from the files you just downloaded)_
        * py -3 setup.py install _(windows)_
        * python3 setup.py install _(linux/unix)_
    * Install requests module
         * pip3 install requests _(window/linux/unix)_
            * _If if it warns about pip being outdated update it_

4. Open the interactive.py script _(open with text editor of your choosing)_
   * Change the info on line's 6 - 16
   * Save the changes

5. Open the telnet.py script
   * Change the info on line's 4 - 6
   * Save the changes

6. Open cmd(windows) or terminal(linux/unix)
   * cd to the directory where you unziped the files in step 1.
   * Run the interactive script
      * py -3 interactive.py _(windows)_
      * python3 interactive.py _(linux/unix)_

