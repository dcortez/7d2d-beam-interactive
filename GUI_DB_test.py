from tkinter import *
from tkinter import ttk
import interactive
import tkinter as tk
import sqlite3
from tkinter import Tk, Entry, END 

class InteractiveApp(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		
		# Use this as a flag to indicate if the box was clicked.
		global clicked   
		clicked = False
		
		# Delete the contents of the Entry widget. Use the flag
		# so that this only happens the first time.
		def callback(event):
			global clicked
			if (clicked == False):
				self.beamPlayerUN.delete(0, END)
				clicked = True
				
		root = self
		root.title("7Dtd Beam Interactive")

		self.mainframe = ttk.Frame(root, padding="3 3 12 12")
		self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		self.mainframe.columnconfigure(0, weight=1)
		self.mainframe.rowconfigure(0, weight=1)
		
		conn = sqlite3.connect('test.sqlite')
		cur = conn.cursor()
		
		# print("Opened database successfully")
		
		cur.execute('''CREATE TABLE IF NOT EXISTS beam
			(ID INTEGER PRIMARY KEY   AUTOINCREMENT,
			username TEXT NOT NULL,
			password TEXT NOT NULL);''')
			
		# print("Table created successfully")
		
		cur.execute('''CREATE TABLE IF NOT EXISTS server
			(ID INTEGER PRIMARY KEY   AUTOINCREMENT,
			username TEXT NOT NULL,
			host TEXT NOT NULL,
			port INTEGER NOT NULL,
			password TEXT NOT NULL);''')
			
		# print("Table created successfully")
		
		
		beam = cur.execute("SELECT count(*) FROM beam")
		beam = cur.fetchone()[0]
		
		server = cur.execute("SELECT count(*) FROM server")
		server = cur.fetchone()[0]
		
		if beam==0 or server==0:
			self.beamPlayerUN = ttk.Entry(self.mainframe)  
			self.beamPlayerUN.grid(column=1, row=2, sticky=(W, E))
			
			self.beamPlayerPW = ttk.Entry(self.mainframe, show='*')
			self.beamPlayerPW.grid(column=1, row=3, sticky=(W, E))
			
			self.telnetAdd = ttk.Entry(self.mainframe)
			self.telnetAdd.grid(column=1, row=5, sticky=(W, E))
			
			self.telnetPt = ttk.Entry(self.mainframe)
			self.telnetPt.grid(column=1, row=6, sticky=(W, E))

			ttk.Label(self.mainframe, text="Password").grid(column=2, row=7, sticky=W)
			self.telnetPW = ttk.Entry(self.mainframe, show='*')
			self.telnetPW.grid(column=1, row=7, sticky=(W, E))
			
			self.steamID = ttk.Entry(self.mainframe)
			self.steamID.grid(column=1, row=9, sticky=(W, E))

			self.button = ttk.Button(self.mainframe, text="Start Interactive", command=self.on_button_DB).grid(columnspan=2, row=10, sticky=W)
			
		else:
			cur.execute("SELECT * FROM beam")
			beamPlayerValue = cur.fetchall()[0]
			beamPlayerUNValue = beamPlayerValue[1]
			beamPlayerPWValue = beamPlayerValue[2]
			
			self.beamPlayerUN = ttk.Entry(self.mainframe)
			self.beamPlayerUN.bind("<Button-1>", callback)
			self.beamPlayerUN.insert(0, beamPlayerUNValue)  
			self.beamPlayerUN.grid(column=1, row=2, sticky=(W, E))
			
			self.beamPlayerPW = ttk.Entry(self.mainframe, show='*')
			self.beamPlayerPW.bind("<Button-1>", callback)
			self.beamPlayerPW.insert(0, beamPlayerPWValue)
			self.beamPlayerPW.grid(column=1, row=3, sticky=(W, E))
			
			cur.execute("SELECT * FROM server")
			serverValues = cur.fetchall()[0]
			serverUNValue = serverValues[1]
			serverHTValue = serverValues[2]
			serverPTValue = serverValues[3]
			serverPWValue = serverValues[4]
			
			self.telnetAdd = ttk.Entry(self.mainframe)
			self.telnetAdd.bind("<Button-1>", callback)
			self.telnetAdd.insert(0, serverHTValue)
			self.telnetAdd.grid(column=1, row=5, sticky=(W, E))
			
			self.telnetPt = ttk.Entry(self.mainframe)
			self.telnetPt.bind("<Button-1>", callback)
			self.telnetPt.insert(0, serverPTValue)
			self.telnetPt.grid(column=1, row=6, sticky=(W, E))

			self.telnetPW = ttk.Entry(self.mainframe, show='*')
			self.telnetPW.bind("<Button-1>", callback)
			self.telnetPW.insert(0, serverPWValue)
			self.telnetPW.grid(column=1, row=7, sticky=(W, E))
			
			self.steamID = ttk.Entry(self.mainframe)
			self.steamID.bind("<Button-1>", callback)
			self.steamID.insert(0, serverUNValue)
			self.steamID.grid(column=1, row=9, sticky=(W, E))
			
			self.button = ttk.Button(self.mainframe, text="Start Interactive", command=self.on_button)\
			.grid(columnspan=2, row=10, sticky=W)

			
		# Beam Interactive Info
		ttk.Label(self.mainframe, text="BEAM INTERACTIVE LOGIN INFO:").grid(columnspan=3, row=1, sticky=W)
		ttk.Label(self.mainframe, text="Username").grid(column=2, row=2, sticky=W)
		ttk.Label(self.mainframe, text="Password").grid(column=2, row=3, sticky=W)

		# Game Server Info
		ttk.Label(self.mainframe, text="7DTD SERVER TELNET INFO:").grid(columnspan=3, row=4, sticky=W)
		ttk.Label(self.mainframe, text="Address").grid(column=2, row=5, sticky=W)
		ttk.Label(self.mainframe, text="Port").grid(column=2, row=6, sticky=W)
		ttk.Label(self.mainframe, text="Password").grid(column=2, row=7, sticky=W)
	
		# 7dtd Player Info
		ttk.Label(self.mainframe, text="7DTD PLAYER INFO:").grid(columnspan=3, row=8, sticky=W)

		ttk.Label(self.mainframe, text="Steam ID").grid(column=2, row=9, sticky=W)
		
		for child in self.mainframe.winfo_children():
			child.grid_configure(padx=5, pady=5)
			
		self.beamPlayerUN.focus()
		self.bind('<Return>', self.on_button)
		
	def on_button(self):
		server = dict(host='', port='', username='', password='')
		server["host"] = self.telnetAdd.get()
		server['port'] = self.telnetPt.get()
		server['password'] = self.telnetPW.get()

		streamer = dict(username='', password='')
		streamer["username"] = self.beamPlayerUN.get()
		streamer['password'] = self.beamPlayerPW.get()
		
		steamid = dict(playerid='')
		steamid['playerid'] = self.steamID.get()
		
		print(steamid['playerid'])

		# interactive.test(streamer, steamid, server)
		
	def on_button_DB(self):
		server = dict(host='', port='', username='', password='')
		server["host"] = self.telnetAdd.get()
		server['port'] = self.telnetPt.get()
		server['password'] = self.telnetPW.get()

		streamer = dict(username='', password='')
		streamer["username"] = self.beamPlayerUN.get()
		streamer['password'] = self.beamPlayerPW.get()
		
		steamid = dict(playerid='')
		steamid['playerid'] = self.steamID.get()
		
		print(steamid['playerid'])
		
		conn = sqlite3.connect('test.sqlite')
		cur = conn.cursor()
		
		conn.execute('''INSERT INTO beam (username, password) VALUES(?, ?);''', (streamer['username'], streamer['password']))
		conn.execute('''INSERT INTO server (username, host, port, password) VALUES(?, ?, ?, ?);''', (steamid['playerid'], server['host'], server['port'], server['password']))		
		
		conn.commit()
		print("Records created successfully")
		conn.close()

		# interactive.test(streamer, steamid, server)

app = InteractiveApp()
app.mainloop()
