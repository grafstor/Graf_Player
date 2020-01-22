#Graf_Player
'''
	author: grafstor
	date: 19.01.2020
'''
__version__ = "4.6"

from os import startfile,  listdir
# , getpid
# from psutil import Process, HIGH_PRIORITY_CLASS
import eyed3
from mutagen.mp3 import MP3
import win32api
from time import sleep
from tkinter import *
from tkinter.filedialog import askdirectory
from PIL import ImageTk 
from pygame import mixer

class Palyer:

	def __init__(self,root):
		# PRIORIT = Process(getpid())
		# PRIORIT.nice(HIGH_PRIORITY_CLASS)
		self.root = root
		self.pause = False
		self.togle_list = False
		self.main_hover = False
		
		self.volume = 70
		self.now_time = 0
		self.main_track = 0
		self.main_timeline = 0
		self.main_length = 1
		self.main_path = ''

		mixer.init(44100, -16, 4, 8192)

		self.tk_bild()

		try:
			dirr = open("bd.txt","r")
			text = dirr.read()
			if not text:
				dirr.close()
				dirr = open("bd.txt","w")
				self.ask_dir()
				dirr.write(self.main_path)
			else:
				self.main_path = text
			dirr.close()
		except:
			dirr = open("bd.txt","w")
			self.ask_dir()
			dirr.write(self.main_path)
			dirr.close()

		self.directory()

		self.main_frame()
		# self.main_path = "D:\\media\\audio\\m"

	def tk_bild(self):
		vol_colorr = self.from_rgb((79,64,255))
		g_colorr = self.from_rgb((34,34,34))

		self.root.overrideredirect(1)
		self.root.geometry("{0}x{1}+{2}+{3}".format(30,160,0,-160))
		self.root.config(bg="grey10")
		self.root.lift()
		self.root.attributes('-topmost',True)
		self.root.wm_attributes("-transparentcolor", "black")

		self.image = ImageTk.PhotoImage(file="1.png")
		self.image2 = ImageTk.PhotoImage(file="2.png")
		self.image3 = ImageTk.PhotoImage(file="3.png")
		self.image5 = ImageTk.PhotoImage(file="5.png")

		self.list_m = Toplevel(self.root)
		self.list_m.geometry("{0}x{1}+{2}+{3}".format(0,160,25,-160))
		self.list_m.config(bg=g_colorr)
		self.list_m.lift()
		self.list_m.attributes('-topmost',True)
		self.list_m.wm_attributes("-transparentcolor", "black")
		self.list_m.overrideredirect(1)

		lab1 = Label(self.list_m,image=self.image5, bd=0)
		lab1.pack(side="right")

		self.main_textbox = Listbox(self.list_m,height=100,width=100)  
		self.main_textbox.config(bd=0,
								 bg=g_colorr,
								 fg="white",
								 font=("Calibri", 12),
								 selectbackground="grey40",
								 highlightcolor="grey40",
								 selectmode="SINGLE",
								 highlightthickness=0,
								 activestyle="none"
								 )
		self.main_textbox.pack(side='right',fill="x")

		self.list_botton = Canvas(self.root,bg="black",height=30,width=30)
		self.list_botton.config(bg=g_colorr,
								bd=0,
								relief='ridge',
								highlightthickness=0,)
		self.list_botton.create_image(15, 15, image=self.image2)
		self.list_botton.create_arc(1, 1, 28, 28, 
									start=0,
									extent=359,
									style=ARC,
									outline='white',
									width=2
									)
		self.time_line = self.list_botton.create_arc(1, 1, 28, 28, 
													start=90,
													extent=0,
													style=ARC,
													outline='green',
													width=3
													)
		self.list_botton.pack(side="top")

		self.canvas = Canvas(self.root)
		self.canvas.config(bg=g_colorr,
						   bd=0,
						   relief='ridge',
						   highlightthickness=0,)
		self.rect_m = self.canvas.create_rectangle(0, 0,30, 100,fill=vol_colorr,outline=vol_colorr)
		self.canvas.move(self.rect_m,0,round(self.volume))
		self.rect_m_c = self.canvas.create_oval(0, 0, 30,30,outline=vol_colorr,fill=vol_colorr)
		self.canvas.move(self.rect_m_c,0,round(self.volume)-15)

		self.play_botton = Button(self.root,image=self.image,height=30,width=30)
		self.play_botton.config(bd=0,
								bg="grey10",
								command=self.start_file,)
		self.play_botton.pack( side='bottom')

		self.canvas.pack(side="top",fill="both")

		self.main_textbox.bind('<ButtonRelease-1>', self.select_play)
		self.list_botton.bind("<Button-1>", self.play_list)
		self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
		self.root.bind("<Button-3>", self.close)

	def directory(self):
		self.music_dir = listdir(self.main_path)
		self.music_dir = [i for i in self.music_dir if i.find("mp3") != -1]

		for i in range(len(self.music_dir)):
			main_author = ''
			audiofile = eyed3.load(f"{self.main_path}\\{self.music_dir[i]}")
			try:
				main_author = audiofile.tag.artist
			except:
				pass
			if main_author:
				self.main_textbox.insert(i,f'     {self.music_dir[i][:-4]} - {main_author}')
			else:
				self.main_textbox.insert(i,f'     {self.music_dir[i][:-4]}')

	def ask_dir(self):
		self.main_path = askdirectory(initialdir="C:/Users/",
										  title = "Choose a folder with music")
	def main_frame(self):
		if self.main_hover:
			if not self.is_hover(40,100,260) and not (self.is_hover(440,100,260) and self.togle_list):
				if self.togle_list:self.hide_list()
				self.make_animation(self.root,10,-30,100)
				self.main_hover = False

		else:
			if self.is_hover(40,100,260):
				self.make_animation(self.root,-30,10,100)
				self.main_hover = True

		if not mixer.music.get_busy() and self.pause:
			self.play_next()

		self.now_time = mixer.music.get_pos()//1000 + self.main_timeline
		self.time_long(round(360*self.now_time/self.main_length))

		root.after(160,self.main_frame)

	def start_file(self):
		try:
			now_track = self.main_textbox.curselection()[0]

			if self.pause:
				self.pause_track()

			else:
				if now_track == self.main_track:
					self.play_botton.config(image=self.image3)
					mixer.music.unpause()
					self.pause = True

				else:
					self.play_track(now_track)

		except:
			pass

	def time_long(self,length):

		self.list_botton.itemconfigure(self.time_line,extent=length)

	def on_mousewheel(self,event):
		if self.main_hover:
			dire = -1*(event.delta/120)*5

			if self.is_hover(40,130,230):
				if not (self.volume+dire>100.0 or self.volume+dire<15):
					self.volume+=dire
					mixer.music.set_volume((100-(self.volume))/100)
					self.canvas.move(self.rect_m,0,int(dire))
					self.canvas.move(self.rect_m_c,0,int(dire))

			elif self.is_hover(40,230,260):
				if dire < 0:
					self.play_next()

				else:
					self.play_last()

			elif self.is_hover(40,100,130):
				if self.main_timeline - dire < 360 and self.main_timeline - dire > 0:
					self.main_timeline = mixer.music.get_pos()//1000 + self.main_timeline
					self.main_timeline -= dire
					if self.pause:
						mixer.music.play(0,self.main_timeline)

	def select_track(self,index):
		self.main_textbox.select_clear(0, "end")
		self.main_textbox.activate(index)
		self.main_textbox.see(index)
		self.main_textbox.selection_anchor(index)
		self.main_textbox.selection_set(index)

	def select_play(self,event):
		now_track = self.main_textbox.curselection()[0]
		if self.pause and self.main_track == now_track:
			self.pause_track()
		else:
			self.play_track(now_track)

	def play_track(self,index):
		path = f"{self.main_path}\\{self.music_dir[index]}"

		self.play_botton.config(image=self.image3)
		self.time_long(0)

		mixer.music.load(path)
		mixer.music.play()

		music =  MP3(path)
		self.main_length = int(music.info.length)

		self.pause = True
		self.main_timeline = 0
		self.main_track = index

	def pause_track(self):
		self.play_botton.config(image=self.image)

		mixer.music.pause()

		self.pause = False

	def play_list(self,event):
		if self.togle_list:
			self.hide_list()

		else:
			self.look_list()

	def play_next(self):
		mixer.music.pause()
		self.main_track+=1
		if self.main_track > len(self.music_dir)-1:
			self.main_track = 0
		self.select_track(self.main_track)
		self.play_track(self.main_track)

	def play_last(self):
		mixer.music.pause()
		self.main_track-=1
		if self.main_track < 0:
			self.main_track = len(self.music_dir)-1
		self.select_track(self.main_track)
		self.play_track(self.main_track)

	def close(self,event):
		self.root.destroy()
		exit()

	def hide_list(self):
		self.make_animation_size(self.list_m,400,0,160,0)
		self.set_poz(self.list_m,0,-160)
		self.togle_list = False
		self.list_m.attributes('-topmost', True)
		self.select_track(self.main_track)

	def look_list(self):
		self.list_m.attributes('-topmost', False)
		self.set_poz(self.list_m,25, 100)
		self.make_animation_size(self.list_m,0,400,0,160)
		self.togle_list = True

	def make_animation(self,obj,x1,x2,y1):
		way_x = x2 - x1
		steps_x = way_x / 10

		for i in range(1,11):
			f_x = round(x1 + i * steps_x)
			f_y = round(y1)
			obj.geometry(f"+{f_x}+{f_y}")
			root.update()
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
			root.update()
			sleep(0.001)

	def set_size(self,obj,w,h):

		obj.geometry(f"{w}x{h}")

	def set_poz(self,obj,x,y):

		obj.geometry(f'+{x}+{y}') 	

	def from_rgb(self,rgb):
		
		return "#%02x%02x%02x" % rgb 

	def is_hover(self,x1,y1,y2,x2=-2):
		x, y = win32api.GetCursorPos()
		if (x < x1 and x > x2) and (y > y1 and y < y2):
			return True
		return False

if __name__ == "__main__":
	root = Tk()
	main_player = Palyer(root)
	mainloop()
