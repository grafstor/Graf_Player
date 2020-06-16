# f-player

'''
    author: grafstor
    date: 22.01.2020

    version 5.5:
        - add menu shape

    version 5.4:
        - refaktoring

    version 5.3:
        - file encode problems
        - volume
        - tracks rewinding
        - rewinding
        - audio list
        - pause
'''

__version__ = "5.5"

from random import randint
from tkinter import Tk, mainloop
from time import sleep
import sys
from filemanager import File_Manager
from display import Display
from audio import Audio

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
                                     self.togle_play,
                                     self.open_menu)

        main_path = self.filemanager.get_path()

        playlist = self.ap.playlist_bild(main_path)
        self.playlist_length = len(playlist)
        optionslist = [" тема",
                       " поиск",
                       " + папка",
                       " настройки",]

        self.dp.draw_list(playlist)
        self.dp.draw_menu(optionslist)

        self.dp.look_root()

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
                    if self.dp.is_menuopen():
                        self.dp.hide_menu()
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
            if self.dp.is_menuopen():
                self.dp.hide_menu()
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
                    self.main_time_change -= dire*1.7
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
                    
    def open_menu(self, event):
        self.dp.look_menu()

    def close(self,event):
        self.dp.close()
        exit()

if __name__ == "__main__":
    root = Tk()
    main_player = Player(root)
    mainloop()