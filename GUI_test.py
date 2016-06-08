from tkinter import *
from tkinter import ttk
import interactive
import tkinter as tk


class InteractiveApp(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		root = self
		root.title("7Dtd Beam Interactive")

		self.mainframe = ttk.Frame(root, padding="3 3 12 12")
		self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		self.mainframe.columnconfigure(0, weight=1)
		self.mainframe.rowconfigure(0, weight=1)

		# Beam Interactive Info
		ttk.Label(self.mainframe, text="BEAM INTERACTIVE LOGIN INFO:").grid(columnspan=3, row=1, sticky=W)

		ttk.Label(self.mainframe, text="Username").grid(column=2, row=2, sticky=W)
		self.beamPlayerUN = ttk.Entry(self.mainframe)
		self.beamPlayerUN.grid(column=1, row=2, sticky=(W, E))

		ttk.Label(self.mainframe, text="Password").grid(column=2, row=3, sticky=W)
		self.beamPlayerPW = ttk.Entry(self.mainframe)
		self.beamPlayerPW.grid(column=1, row=3, sticky=(W, E))

		# Game Server Info
		ttk.Label(self.mainframe, text="7DTD SERVER TELNET INFO:").grid(columnspan=3, row=4, sticky=W)

		ttk.Label(self.mainframe, text="Address").grid(column=2, row=5, sticky=W)
		self.telnetAdd = ttk.Entry(self.mainframe)
		self.telnetAdd.grid(column=1, row=5, sticky=(W, E))

		ttk.Label(self.mainframe, text="Port").grid(column=2, row=6, sticky=W)
		self.telnetPt = ttk.Entry(self.mainframe)
		self.telnetPt.grid(column=1, row=6, sticky=(W, E))

		ttk.Label(self.mainframe, text="Password").grid(column=2, row=7, sticky=W)
		self.telnetPW = ttk.Entry(self.mainframe)
		self.telnetPW.grid(column=1, row=7, sticky=(W, E))

		# 7dtd Player Info
		ttk.Label(self.mainframe, text="7DTD PLAYER INFO:").grid(columnspan=3, row=8, sticky=W)

		ttk.Label(self.mainframe, text="Steam ID").grid(column=2, row=9, sticky=W)
		self.steamID = ttk.Entry(self.mainframe)
		self.steamID.grid(column=1, row=9, sticky=(W, E))

		self.button = ttk.Button(self.mainframe, text="Start Interactive", command=self.on_button)\
			.grid(columnspan=2, row=10, sticky=W)

		for child in self.mainframe.winfo_children():
			child.grid_configure(padx=5, pady=5)

	def on_button(self):
		server = dict(host='', port='', username='', password='')
		server["host"] = self.telnetAdd.get()
		server['port'] = self.telnetPt.get()
		server['password'] = self.telnetPW.get()

		streamer = dict(username='', password='')
		streamer["username"] = self.beamPlayerUN.get()
		streamer['password'] = self.beamPlayerPW.get()
		
		steamid = dict(GAME_PLAYERID='')
		steamid['GAME_PLAYERID'] = self.steamID.get()

		interactive.test(streamer, steamid, server)

app = InteractiveApp()
app.mainloop()
