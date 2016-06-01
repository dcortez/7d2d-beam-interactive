import asyncio
import requests
from beam_interactive import start
from beam_interactive import proto
from random import random
import json

path = "https://beam.pro/api/v1"
game_version = GAME_VERSIONID
share_code = "SHARECODE"

# Create a second object like this for the credentials of the second player
Player = {
    "username": "<USERNAME>",
    "password": "<PASSWORD>"
}

########################################################################################
#############################   NO EDIT BELOW THIS LINE   ##############################
########################################################################################

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
        print("Shaking hands")

    def on_handshake_ack(self, line, conn):
        print("Shaken hands")

    def on_error(self, error, conn):
        """This is called when we get an Error packet. It contains
        a single attribute, 'message'.
        """
        print('Oh no, there was an error!')
        print(error.message)

    def login(self, session, username, password):
        """Log into the Beam servers via the API."""
        user = dict(username=username, password=password)
        return session.post(path + "/users/login", user).json()

    def on_report(self, report, conn, player):
        """Periodically we'll get Report packets to let us know
        what our viewers are up to. We'll just print out that
        report, then send back a random progress update.

        The progress update, described in more details in the Talking
        to Beam Interactive section, updates the frontend with feedback
        about what the robot is doing. In this case, we'll hint that
        we're a random percentage of the way towards the up arrow
        button (code) being fired.
        """
        print(report)
        """Example of how to parse the reports
        for tactile in report.tactile:
            print(tactile)
            if tactile.holding > 0:
                print(tactile.holding)"""

    @asyncio.coroutine
    def connect(self, user, player):
        session = requests.Session()
        channel_data = Beam().login(session, **user)

        if not "channel" in channel_data:
            raise AuthenticationException("Incorrect username or password")

        channel_id = channel_data["channel"]["id"]
        data = Beam().get_tetris(session, channel_id)
        interactiveData = Beam().go_interactive(session, channel_id, game_version, share_code)
        conn = yield from start(data['address'], channel_id, data['key'], loop)
        print("Using channel ID: ", channel_id)

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
        print("Closing")
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
