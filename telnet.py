import telnetlib, sys, re

#Games server info     
host = '<IP/HOST_NAME>'
port = <TELNET_PORT>
password = '<TELNET_PASSWORD>'
 
########################################################################
######################## NO EDIT PAST THIS LINE ######################## 
########################################################################

#Chat Dictionary
chat = {
	1 : 'AIR DROP INCOMING!!',
	2 : 'ZOMBIE ALERT!!',
	3 : 'There is a moose loose in the building!',
	4 : 'LOOK DOWN... Someone gave you',
}

#Test if args supplied
if __name__ == "__main__":
     
    if(len(sys.argv) < 2) :
        print 'ERROR: No args supplied'
        sys.exit()
        
#Get the game command
cmdList = []

#Loop through args provided
for x in sys.argv:
	#Add to the cmdList list for storage
	cmdList.append(x)
	
#Store arg for chat logic
whatToSay = int(cmdList[1])

#Placeholders
user = ''
item = ''

#Check if we have a user in args
if(len(sys.argv) > 3) :
	user = cmdList[3].upper()
	
if(len(sys.argv) > 4) :
	item = cmdList[4].upper()
	item = re.sub('^GUN', '', item)
	
#Remove the first and second element as it is not needed past here
cmdList.pop(0)
cmdList.pop(0)

#Convert the list into a strin seperated by a space
cmd = ' '.join(cmdList)
 
# connect to remote host
try :
	tn = telnetlib.Telnet(host, port)
except :
	print 'Unable to connect'
	sys.exit()
  
#Send Password
tn.read_until('Password: ', 2)
tn.write(password + '\n') 	

#BASIC Say something in game when button pressed
#Will make this more robust in the future
if whatToSay == 1 :
	tn.write('say " ' + chat[1] + '" \n')
elif whatToSay == 2 :
	tn.write('say " ' + user + ' ' + chat[2] + '" \n')
elif whatToSay == 3 :
	tn.write('say " ' + chat[3] + '" \n')
elif whatToSay == 4 :
	if item == "WOOD" :
		tn.write('say " ' + user + ' ' + chat[4] + ' some ' + item + '!" \n')
	else :
		tn.write('say " ' + user + ' ' + chat[4] + ' a ' + item + '!" \n')
else :
	print 'OOPS!!'
	sys.exit()

#Send the command to the game server
tn.write(cmd + '\n')
sys.exit()

#Allow interaction with telnet
tn.mt_interact()
