/*####   SET UP VARS   ####*/

var BEAM_CHANNELID = '<CHANNELID>';  // gathered from https://beam.pro/api/v1/channels/<username> (search for channelID in json)
var BEAM_USER = '<USERNAME>'; // your beam username
var BEAM_PASS = '<PASSWORD>'; // your beam password

var PYTHON_PATH = 'C:/Python27/python.exe'; // Path to Python2.7
var PYSCRIPT_PATH = 'C:/Program Files/nodejs/7d2d'; //Path to Python Telnet Script - USE "/" as seperator even on Windows
var GAME_PLAYERID = '<7Days_Playername>'; // Your player on the 7days server (Could be SteamID, EntityID, or PlayerName)

/*####   NO EDIT PAST THIS LINE ####*/
//setup some random items in arrays

var items = [
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
	['wood', 20],
	['miningHelmet', 1],
	['toolAndDieSet', 1],
	['calipers', 1],
	['clawHammer', 1],
	['fireaxeIron', 1],
	['fireaxeSteel', 1],
	['pickaxeIron', 1],
	['pickaxeSteel', 1],
	['tazasStoneaxe', 1],
	['baconAndEggs', 2],
	['bakedPotato', 2],
	['bottledWater', 2],
	['canStock', 2],
	['beer', 2],
	['grainAlcohol', 2],
	['firstAidKit', 2],
	['firstAidBandage', 2],
	['bandage', 2],
	['antibiotics', 2],
	['painkillers', 2]
];

var enemies = [
	'zombieSteve',
	'zombieBoe',
	'zombieMoe',
	'zombieJoe',
	'zombieArlene',
	'zombieDarlene',
	'zombieMarlene',
	'zombieSteveCrawler',
	'animalBear'
];

var friends = [
	'animalRabbit',
	'animalChicken',
	'animalStag',
	'animalPig'
];

//START EXECUTING
var Beam = require('beam-client-node');
var Tetris = require('beam-interactive-node');
var rjs = require('robotjs');
var pyShell = require('python-shell');

var pyOptions = {
	mode: 'text',
	pythonPath: PYTHON_PATH,
	scriptPath: PYSCRIPT_PATH
}

var beam = new Beam();
beam.use('password', {
    username: BEAM_USER,
    password: BEAM_PASS
}).attempt().then(function () {
    return beam.game.join(BEAM_CHANNELID);
}).then(function (res) {
    var details = {
        remote: res.body.address,
        channel: BEAM_CHANNELID,
        key: res.body.key
    };
    var robot = new Tetris.Robot(details);
    robot.handshake(function (err) {
        if (err) throw new Error('Error connecting to Tetris', err);
    });

    robot.on('report', function (report) {
		
		for (var i=0; i<report.tactile.length; i++) {
			switch (report.tactile[i].id) {
				case 0: 
					
					//Spawn Animal
					if (report.tactile[i].pressFrequency > 0) {
						var key = Math.floor(Math.random() * friends.length);
						pyOptions['args'] = [ 3, 'spawnentity', GAME_PLAYERID, friends[key] ];
					}
					
				break;				
				
					//Spawn Evil
				case 1:
					if (report.tactile[i].pressFrequency > 0) {
						var key = Math.floor(Math.random() * enemies.length);
						
						if ( oddOrEven(Math.random() * 11) == 'even' ) {
							pyOptions['args'] = [ 2, 'spawnwanderinghorde' ];
						}
						
						else {
							pyOptions['args'] = [ 2, 'spawnentity', GAME_PLAYERID, enemies[key] ];
						}
					}
				break;
								
				case 2:
				
					//Give Item(s)
					if (report.tactile[i].pressFrequency > 0) {
						var key = Math.floor(Math.random() * items.length);
						
						if ( oddOrEven(Math.random() * 11) == 'even' ) {
							pyOptions['args'] = [ 4, 'give', GAME_PLAYERID, items[key][0], items[key][1] ];
						}
						else {
							pyOptions['args'] = [ 1, 'spawnairdrop' ];
						}
					}
				break;
								
				case 3:
				
					//Spawn Horde
					if (report.tactile[i].pressFrequency > 0) {
						pyOptions['args'] = [ 2, 'spawnwanderinghorde' ];
					}
				break;
								
				case 4:
				
					//Give Feral
					if (report.tactile[i].pressFrequency > 0) {
						pyOptions['args'] = [ 2, 'spawnentity', GAME_PLAYERID, 'zombieferal' ];
					}
				break;
								
				case 5:
				
					//Give Screamer
					if (report.tactile[i].pressFrequency > 0) {
						pyOptions['args'] = [ 2, 'spawnentity', GAME_PLAYERID, 'zombieScreamer' ];
					}
				break;
								
				case 6:
				
					//Send Airdrop
					if (report.tactile[i].pressFrequency > 0) {
						pyOptions['args'] = [ 1, 'spawnairdrop' ];
					}
				break;

			}
			
			//RUN THE SCRIPT TO TELNET
			if ("args" in pyOptions) {
				pyShell.run('telnet.py', pyOptions, function(err, results) {
					if (err) {
						console.log(err);
					}
				});
				
				delete pyOptions['args'];
			}
		}
		
    });
});

//Some Helper Functions
function oddOrEven(x) {
  return ( x & 1 ) ? "odd" : "even";
}
