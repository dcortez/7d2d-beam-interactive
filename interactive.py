import asyncio, requests, os, json, random
from beam_interactive import start
from beam_interactive import proto

#Beam Interactive Login
path = "https://beam.pro/api/v1"
game_version = GAME_VERSION_ID
share_code = "SHARECODE"
Player = {
    "username": "USERNAME",
    "password": "PASSWORD"
}

#Path to Python.. can be python2.7 or above for this entry
#PYTHON_PATH = '<PATH_TO_PYTHON>'; 

#Path to Python Telnet Script - USE "/" as seperator even on Windows
PYSCRIPT_PATH = '<PATH_TO_TELNET.PY>'; 

#7 Days to Die Player Name
GAME_PLAYERID = '<7Days_Playername>'

#Spawn Lists
#items = [ITEM, QUANTITY]
items = [
	['gunPistol', 1],
	['gunPumpShotgun', 1],
	['gunSawedOffPumpShotgun', 1],
	['gunAK47', 1],
	['gun44Magnum', 1],
	['gunHuntingRifle', 1],
	['gunSniperRifle', 1],
	['nailgun', 1],
	['shotgunShell', 20],
	['shotgunSlug', 20],
	['10mmBullet', 20],
	['9mmBullet', 20],
	['762mmBullet', 20],
	['44MagBullet', 20],
	['miningHelmet', 1]
]

enemies = [
	'zombieSteve',
	'zombieBoe',
	'zombieMoe',
	'zombieJoe',
	'zombieArlene',
	'zombieDarlene',
	'zombieMarlene',
	'zombieSteveCrawler',
	'animalBear'
]

friends = [
	'animalRabbit',
	'animalChicken',
	'animalStag',
	'animalPig'
]
#Random range of numbers
num = random.randrange(0, 100)

###################################################################################
###########################   NO EDIT BELOW THIS LINE   ###########################
###################################################################################

loop = asyncio.get_event_loop()

class AuthenticationException(Exception):

   def __init__(self, value):
        self.parameter = value
   def __str__(self):
        return repr(self.parameter)

class Beam():

	def get_tetris(self, session, channel):
		"""Retrieve interactive connection information."""
		return session.get(path + "/tetris/{id}/robot".format(id=channel)).json()

	def go_interactive(self, session, channel_id, version, code):
		interactiveDetails = dict(tetrisGameId=version, tetrisShareCode=code, interactive=1)
		return session.put(path + "/channels/{id}".format(id=channel_id), interactiveDetails).json()

	def on_handshake(self, line, conn):
		print("Shaking hands\n")

	def on_handshake_ack(self, line, conn, player):
		print("Shaken hands\n")

	def on_error(self, error, conn):
		"""This is called when we get an Error packet. It contains
		a single attribute, 'message'.
		"""
		print('Oh no, there was an error!\n')
		print(error.message)

	def login(self, session, username, password):
		"""Log into the Beam servers via the API."""
		user = dict(username=username, password=password)
		return session.post(path + "/users/login", user).json()


		
	def on_report(self, report, conn, player):

        #Example of how to parse the reports
		for tactile in report.tactile:

            #Spawn Animal
			if tactile.pressFrequency > 0 and tactile.id == 0:
				KEY = random.randrange(0, len(friends))
				os.system(('python {} 3 spawnentity {} {}').format(PYSCRIPT_PATH, GAME_PLAYERID, friends[KEY]))
            
            #Spawn Enemy
			elif tactile.pressFrequency > 0 and tactile.id == 1:
				KEY = random.randrange(0, len(enemies))
				if num == 73:
					os.system(('python {} 2 spawnwanderinghorde').format(PYSCRIPT_PATH))
				else:
					os.system(('python {} 2 spawnentity {} {}').format(PYSCRIPT_PATH, GAME_PLAYERID, enemies[KEY]))
					
            #Spawn Item    
			elif tactile.pressFrequency > 0 and tactile.id == 2:
				KEY = random.randrange(0, len(items))
				if num == 73:
					os.system(('python {} 1 spawnairdrop').format(PYSCRIPT_PATH))
				else:
					os.system(('python {} 4 spawnentity {} {} {}').format(PYSCRIPT_PATH, GAME_PLAYERID, items[KEY][0], items[KEY][1]))
										
			#Spawn Horde
			elif tactile.pressFrequency > 0 and tactile.id == 3:
				KEY = random.randrange(0, len(enemies))
				os.system(('python {} 2 spawnwanderinghorde').format(PYSCRIPT_PATH))

			#Spawn Feral
			elif tactile.pressFrequency > 0 and tactile.id == 4:
				KEY = random.randrange(0, len(enemies))
				os.system(('python {} 2 spawnentity {} zombieFeral').format(PYSCRIPT_PATH, GAME_PLAYERID))

			elif tactile.pressFrequency > 0 and tactile.id == 5:
				KEY = random.randrange(0, len(enemies))
				os.system(('python {} 2 spawnentity {} zombieScreamer').format(PYSCRIPT_PATH, GAME_PLAYERID))

			#Spawn Airdrop
			elif tactile.pressFrequency > 0 and tactile.id == 6:
				KEY = random.randrange(0, len(enemies))
				os.system(('python {} 1 spawnairdrop').format(PYSCRIPT_PATH))
            

	@asyncio.coroutine
	def connect(self, user, player):
		session = requests.Session()
		channel_data = Beam().login(session, **user)

		if not "channel" in channel_data:
			raise AuthenticationException("Incorrect username or password\n")

		channel_id = channel_data["channel"]["id"]
		data = Beam().get_tetris(session, channel_id)
		interactiveData = Beam().go_interactive(session, channel_id, game_version, share_code)
		conn = yield from start(data['address'], channel_id, data['key'], loop)
		print("Using channel ID: ", channel_id, "\n")

        # Handlers definitions
		handlers = {
			proto.id.error: Beam().on_error,
			proto.id.report: Beam().on_report,
			proto.id.handshake: Beam().on_handshake,
			proto.id.handshake_ack: Beam().on_handshake_ack
		}

        # Actual parsing of the recieved packet
		while (yield from conn.wait_message()):
			decoded, packet_bytes = conn.get_packet()
			packet_id = proto.id.get_packet_id(decoded)
			if decoded is None:
				print('We got a bunch of unknown bytes.')
			elif packet_id in handlers:
				handlers[packet_id](decoded, conn, player)
			else:
				print("We got packet {} but didn't handle it!".format(packet_id))
				print("Closing\n")
				conn.close()

# Create another object like this to add another player
player = Beam()

try:
    # Do a new line similar to this line but with objects for the new player
    asyncio.async(player.connect(Player, "1"))
    loop.run_forever()
except KeyboardInterrupt:
    print("Disconnected.")
finally:
    loop.close()
