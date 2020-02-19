from PIL import ImageTk 
from time import sleep
from tkinter import *
import win32api

class Display:

    def __init__(self,root):
        self.root = root
        self.is_list_open = False
        self.is_win_hover = False
        self.is_bottons_open = False

    def draw_mainwindow(self,
                        play_foo,
                        list_togle_foo,
                        mousewheel_foo,
                        close_foo,
                        togle_play_foo):

        vol_colorr = self.from_rgb((79,64,255))
        g_colorr = self.from_rgb((34,34,34))

        self.root.overrideredirect(1)
        self.root.geometry(f'{30}x{160}+{0}+{-160}')
        self.root.config(bg="grey10")
        self.root.lift()
        self.root.attributes('-topmost',True)
        self.root.wm_attributes("-transparentcolor", "black")

        self.image1 = ImageTk.PhotoImage(file="1.png")
        self.image2 = ImageTk.PhotoImage(file="2.png")
        self.image3 = ImageTk.PhotoImage(file="3.png")
        self.image5 = ImageTk.PhotoImage(file="5.png")

        self.main_list_win = Toplevel(self.root)
        self.main_list_win.geometry(f'{0}x{159}+{25}+{-160}')
        self.main_list_win.config(bg=g_colorr)
        self.main_list_win.lift()
        self.main_list_win.attributes('-alpha', 0.9)
        self.main_list_win.attributes('-topmost',True)
        self.main_list_win.wm_attributes("-transparentcolor", "black")
        self.main_list_win.overrideredirect(1)

        list_border = Label(self.main_list_win,
                            image=self.image5,
                            bd=0)
        list_border.pack(side="right")

        self.main_list = Listbox(self.main_list_win,
                                height=100,
                                width=100)  
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
        self.main_list.pack(side='right',
                            fill="x")

        self.timeline_wheel = Canvas(self.root,
                                     bg="black",
                                     height=30,
                                     width=30)
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
                                                    outline=self.from_rgb((120,6,255)),
                                                    width=3
                                                    )
        self.timeline_wheel.pack(side="top")

        self.canvas = Canvas(self.root)
        self.canvas.config(bg=g_colorr,
                           bd=0,
                           relief='ridge',
                           highlightthickness=0,)
        self.rect_m = self.canvas.create_rectangle(0, 0,30, 100,
                                                   fill=vol_colorr,
                                                   outline=vol_colorr)
        self.canvas.move(self.rect_m,0,70)
        self.rect_mc = self.canvas.create_oval(0, 0, 30,30,
                                               outline=vol_colorr,
                                               fill=vol_colorr)
        self.canvas.move(self.rect_mc,0,70-15)

        self.play_botton = Button(self.root,
                                  image=self.image1,
                                  height=30,
                                  width=30)
        self.play_botton.config(bd=0,
                                bg="grey10",
                                command=togle_play_foo)
        self.play_botton.pack( side='bottom')

        self.canvas.pack(side="top",
                         fill="both")

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

        self.timeline_wheel.itemconfigure(self.time_line,
                                          extent=length)

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

    def make_animation(self,obj,x1,x2,y1):
        way_x = x2 - x1
        steps_x = way_x / 10

        for i in range(1,11):
            f_x = round(x1 + i * steps_x)
            f_y = round(y1)

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