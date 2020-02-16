#Graf_Player
'''
	author: grafstor
	date: 22.01.2020
'''
__version__ = "5.3"

from tkinter.filedialog import askdirectory
from PIL import ImageTk 
from time import sleep
from tkinter import *
import win32api
from os import startfile,  listdir
from mutagen.mp3 import MP3
from random import randint
from pygame import mixer
import eyed3
import sys

class Audio:

	def __init__(self):
		self.track_paths = []
		self.ispause = True
		self.main_length = 1
		self.nowplay = -1
		self.volume = 70

		mixer.init(44100, -16, 64, 8192)
		self.set_volume(0)

	def play(self, num):
		mixer.music.load(self.track_paths[num])
		mixer.music.play()

		self.nowplay = num
		self.main_length = self.get_track_length(num)
		self.ispause = False

	def pause(self):
		mixer.music.pause()

		self.ispause = True

	def unpause(self):
		mixer.music.unpause()
		
		self.ispause = False

	def playlist_bild(self, path):
		names_playlist = []
		music_names = listdir(path)
		music_names = [i for i in music_names if i.find("mp3") != -1]

		for track_name in music_names:
			track_path = f'{path}\\{track_name}'
			track_info = eyed3.load(track_path)
			track_author = ' '

			try:
				artist = track_info.tag.artist.encode("cp1252").decode("cp1251")
				n_artist = artist.split()
				for word in n_artist:
					if word.lower() in track_name.lower():
						break
				else:
					track_author = f' - {artist}'

			except:
				pass

			self.track_paths.append(track_path)
			names_playlist.append(f'     {track_name[:-4]}{track_author}')
		return names_playlist

	def set_timeline(self, time): 

		mixer.music.play(0, time)

	def set_volume(self,num):
		self.volume += num
		mixer.music.set_volume((100-(self.volume))/100)

	def get_now_play(self):

		return self.nowplay

	def get_track_length(self, num):
		music =  MP3(self.track_paths[num])
		return int(music.info.length)

	def get_length(self):

		return self.main_length

	def get_time(self):

		return mixer.music.get_pos()//1000

	def get_volume(self):

		return self.volume

	def is_pause(self):

		return self.ispause

	def is_busy(self):

		return mixer.music.get_busy()

class File_Manager:

	def get_path(self):
		try:
			path = self.read_path()
			if not path:
				path = self.ask_dir()
				return path
			return path
		except:
			path = self.ask_dir()
			return path

	def ask_dir(self):
		path = askdirectory(initialdir="C:/Users/",
							title = "Choose a folder with music")
		self.write_path(path)
		return path

	def write_path(self, path):
		dirr = open("bd.txt","w")
		dirr.write(path)
		dirr.close()

	def read_path(self):
		dirr = open("bd.txt","r")
		path = dirr.read()
		dirr.close()
		return path.strip()

class Display:

	def __init__(self,root):
		self.root = root
		self.is_list_open = False
		self.is_win_hover = False
		self.is_bottons_open = False

	def draw_mainwindow(self, play_foo, list_togle_foo, mousewheel_foo, close_foo, togle_play_foo):

		vol_colorr = self.from_rgb((79,64,255))
		g_colorr = self.from_rgb((34,34,34))

		self.root.overrideredirect(1)
		self.root.geometry("{0}x{1}+{2}+{3}".format(30,160,0,-160))
		self.root.config(bg="grey10")
		self.root.lift()
		self.root.attributes('-topmost',True)
		self.root.wm_attributes("-transparentcolor", "black")

		self.image1 = ImageTk.PhotoImage(file="1.png")
		self.image2 = ImageTk.PhotoImage(file="2.png")
		self.image3 = ImageTk.PhotoImage(file="3.png")
		self.image5 = ImageTk.PhotoImage(file="5.png")

		self.main_list_win = Toplevel(self.root)
		self.main_list_win.geometry("{0}x{1}+{2}+{3}".format(0,159,25,-160))
		self.main_list_win.config(bg=g_colorr)
		self.main_list_win.lift()
		self.main_list_win.attributes('-alpha', 0.9)
		self.main_list_win.attributes('-topmost',True)
		self.main_list_win.wm_attributes("-transparentcolor", "black")
		self.main_list_win.overrideredirect(1)

		list_border = Label(self.main_list_win,image=self.image5, bd=0)
		list_border.pack(side="right")

		self.main_list = Listbox(self.main_list_win,height=100,width=100)  
		self.main_list.config(bd=0,
								 bg=g_colorr,
								 fg="white",
								 font=("Calibri", 12),
								 selectbackground="grey40",
								 highlightcolor="grey40",
								 selectmode="SINGLE",
								 highlightthickness=0,
								 activestyle="none"
								 )
		self.main_list.pack(side='right',fill="x")

		self.timeline_wheel = Canvas(self.root,bg="black",height=30,width=30)
		self.timeline_wheel.config(bg=g_colorr,
								bd=0,
								relief='ridge',
								highlightthickness=0,)
		self.timeline_wheel.create_image(15, 15, image=self.image2)
		self.timeline_wheel.create_arc(1, 1, 28, 28, 
									start=0,
									extent=359,
									style=ARC,
									outline='white',
									width=2
									)
		self.time_line = self.timeline_wheel.create_arc(1, 1, 28, 28, 
													start=90,
													extent=0,
													style=ARC,
													outline='green',
													width=3
													)
		self.timeline_wheel.pack(side="top")

		self.canvas = Canvas(self.root)
		self.canvas.config(bg=g_colorr,
						   bd=0,
						   relief='ridge',
						   highlightthickness=0,)
		self.rect_m = self.canvas.create_rectangle(0, 0,30, 100,fill=vol_colorr,outline=vol_colorr)
		self.canvas.move(self.rect_m,0,70)
		self.rect_mc = self.canvas.create_oval(0, 0, 30,30,outline=vol_colorr,fill=vol_colorr)
		self.canvas.move(self.rect_mc,0,70-15)

		self.play_botton = Button(self.root,image=self.image1,height=30,width=30)
		self.play_botton.config(bd=0,
								bg="grey10",
								command=togle_play_foo)
		self.play_botton.pack( side='bottom')

		self.canvas.pack(side="top",fill="both")

		self.main_list.bind('<ButtonRelease-1>', play_foo)
		self.timeline_wheel.bind("<Button-1>", list_togle_foo)
		self.canvas.bind_all("<MouseWheel>", mousewheel_foo)
		self.root.bind("<Button-3>", close_foo)

	def draw_list(self,tracklist):
		for i in range(len(tracklist)):
			self.main_list.insert(i,tracklist[i])

	def button_play(self):

		self.play_botton.config(image=self.image3)

	def button_pause(self):

		self.play_botton.config(image=self.image1)

	def set_timeline_long(self,length):

		self.timeline_wheel.itemconfigure(self.time_line,extent=length)

	def select_track(self,index):
		self.main_list.select_clear(0, "end")
		self.main_list.activate(index)
		self.main_list.see(index)
		self.main_list.selection_anchor(index)
		self.main_list.selection_set(index)

	def move_volume(self,num):
		self.canvas.move(self.rect_m, 0, num)
		self.canvas.move(self.rect_mc, 0, num)

	def hide_list(self,num):
		self.make_animation_size(self.main_list_win,400,0,159,0)
		self.main_list_win.attributes('-topmost', True)
		self.select_track(num)
		self.set_poz(self.main_list_win,-10,-160)
		self.is_list_open = False

	def look_list(self,num):
		self.select_track(num)
		self.main_list_win.attributes('-topmost', False)
		self.set_poz(self.main_list_win,25, 101)
		self.make_animation_size(self.main_list_win,0,400,0,159)
		self.is_list_open = True

	def hide_root(self):
		self.make_animation(self.root,10,-30,100)
		self.is_win_hover = False

	def look_root(self):
		self.make_animation(self.root,-30,10,100)
		self.is_win_hover = True

	def make_animation(self,obj,x1,x2,y1,y2=-1):
		way_x = x2 - x1
		steps_x = way_x / 10

		way_y = y2 - y1
		steps_y = way_y / 10

		for i in range(1,11):
			f_x = round(x1 + i * steps_x)
			if y2 == -1:
				f_y = round(y1)
			else:
				f_y = round(y1 + i * steps_y)

			obj.geometry(f"+{f_x}+{f_y}")
			self.root.update()
			sleep(0.004)

	def make_animation_size(self,obj,x1,x2,y1,y2):
		way_x = x2 - x1
		steps_x = way_x / 10

		way_y = y2 - y1
		steps_y = way_y / 10

		for i in range(1,11):
			f_x = round(x1 + i * steps_x)
			f_y = round(y1 + i * steps_y)

			obj.geometry(f"{f_x}x{f_y}")
			self.root.update()
			sleep(0.001)

	def get_now_select(self):
		now_track = None
		try:
			now_track = self.main_list.curselection()[0]
		except:
			pass
		return now_track

	def set_size(self,obj,w,h):

		obj.geometry(f"{w}x{h}")

	def set_poz(self,obj,x,y):

		obj.geometry(f'+{x}+{y}') 	

	def from_rgb(self,rgb):
		
		return "#%02x%02x%02x" % rgb 

	def is_listopen(self):

		return self.is_list_open

	def is_winhover(self):

		return self.is_win_hover

	def is_bottonsopen(self):

		return self.is_bottons_open

	def is_hover(self,x1,y1,y2,x2=-2):
		x, y = win32api.GetCursorPos()
		if (x < x1 and x > x2) and (y > y1 and y < y2):
			return True
		return False

	def close(self):

		self.root.destroy()

class Player:

	def __init__(self,root):
		self.audioplayer = Audio()
		self.ap = self.audioplayer
		self.filemanager = File_Manager()
		self.display = Display(root)
		self.dp = self.display

		self.main_time_change = 0

		self.display.draw_mainwindow(self.togle_play,
									 self.togle_list,
									 self.on_mousewheel,
									 self.close,
									 self.togle_play,)

		main_path = self.filemanager.get_path()

		playlist = self.ap.playlist_bild(main_path)
		self.playlist_length = len(playlist)

		self.dp.look_root()
		self.dp.draw_list(playlist)

		sleep(1.2)

		for name in sys.argv:
			if name.isdigit():
				self.play_track(randint(1,len(playlist)))
			else:
				for track in range(len(playlist)):
					if name in playlist[track].lower():
						self.play_track(track)
						if not randint(0,6):
							break

		self.main_frame()

	def main_frame(self):
		if self.dp.is_winhover():
			if not self.dp.is_hover(40,100,260):
				if not (self.dp.is_hover(440,100,260) and self.dp.is_listopen()):
					if self.dp.is_listopen():
						self.dp.hide_list(self.ap.get_now_play())
					self.dp.hide_root()

		else:
			if self.dp.is_hover(40,100,260):
				self.dp.look_root()

		if not self.ap.is_busy() and not self.ap.is_pause():
			self.play_next()
		now_time = self.ap.get_time() + self.main_time_change
		self.dp.set_timeline_long(round(360*now_time/self.ap.get_length()))

		self.dp.root.after(160,self.main_frame)

	def play_track(self,num):
		self.dp.button_play()
		self.dp.set_timeline_long(0)

		self.ap.play(num)

		self.main_time_change = 0

	def play_next(self):
		now_track = self.ap.get_now_play()
		if now_track + 1 > self.playlist_length -1:
			now_track = -1
		self.dp.select_track(now_track + 1)
		self.play_track(now_track + 1)

	def play_last(self):
		now_track = self.ap.get_now_play()
		if now_track - 1 < 0:
			now_track = self.playlist_length
		self.dp.select_track(now_track - 1)
		self.play_track(now_track - 1)

	def pause_track(self):
		self.dp.button_pause()

		self.ap.pause()

	def unpause_track(self):
		self.dp.button_play()

		self.ap.unpause()

	def togle_list(self,event):
		if self.dp.is_listopen():
			self.dp.hide_list(self.ap.get_now_play())
		else:
			self.dp.look_list(self.ap.get_now_play())

	def on_mousewheel(self,event):
		if self.dp.is_winhover():
			dire = -1*(event.delta/120)*5
			volume = self.ap.get_volume()
			if self.dp.is_hover(40,130,230):
				if not (volume+dire>100.0 or volume+dire<15):
					self.ap.set_volume(dire)
					self.dp.move_volume(dire)

			elif self.dp.is_hover(40,230,260):
				if dire < 0:
					self.play_next()

				else:
					self.play_last()

			elif self.dp.is_hover(40,100,130):
				if self.main_time_change - dire < 360 and self.main_time_change - dire > 0:
					self.main_time_change = self.ap.get_time() + self.main_time_change
					self.main_time_change -= dire
					if not self.ap.is_pause():
						self.ap.set_timeline(self.main_time_change)

	def togle_play(self,event=0):
		num = self.dp.get_now_select()
		is_same = num == self.ap.get_now_play()
		if not self.ap.is_pause() and is_same:
			self.pause_track()
		else:
			if is_same:
				self.unpause_track()
			else:
				if num != None:
					self.play_track(num)

	def close(self,event):
		self.dp.close()
		exit()

if __name__ == "__main__":
	root = Tk()
	main_player = Player(root)
	mainloop()
