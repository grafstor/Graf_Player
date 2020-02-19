from os import startfile,  listdir
from mutagen.mp3 import MP3
from pygame import mixer
import eyed3


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