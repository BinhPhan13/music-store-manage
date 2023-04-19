import ttkbootstrap as ttk
from tkinter import * 
from ttkbootstrap.constants import *
from display.resize_img import resize_picture
from project_code.entity_manager import *
from display.page import Page

class Home(Page):
    def __init__(self, main_frame:ttk.Frame, user_mng:UserManager, song_mng:SongManager):
        super().__init__(main_frame)

        self.user_mng = user_mng
        self.song_mng = song_mng
                
    def _init_frame(self):
        # label: homepage 
        ttk.Label(self._frame, text='Homepage', font=(self._font,25,'bold')).place(x=20, y=20)

        separator = ttk.Separator(self._frame, orient='horizontal', bootstyle='fg')
        separator.place(x=20,y=65,width=180)

        self.__load_image()
        # users 
        frame_bootstyle = 'secondary'
        label_bootstyle = frame_bootstyle + 'inverse'
        
        user_frame = ttk.Frame(self._frame, bootstyle=frame_bootstyle)
        user_frame.place(x=30, y=90, width=300, height=150)
        
        ttk.Label(user_frame, image= self.__user_img, bootstyle=label_bootstyle).place(x=150, y=20)
        ttk.Label(user_frame, text='\nTotal User', font=(self._font,14), bootstyle=label_bootstyle).place(x=20,y=70)

        self.no_user_label = ttk.Label(user_frame, font=(self._font,40,'bold'), bootstyle=label_bootstyle)
        self.no_user_label.place(x=20,y=10)
  
        # songs
        frame_bootstyle = 'danger'
        label_bootstyle = frame_bootstyle + 'inverse'

        song_frame = ttk.Frame(self._frame, bootstyle=frame_bootstyle)
        song_frame.place(x=400, y=90, width=300, height=150)
        
        ttk.Label(song_frame, image=self.__song_img, bootstyle=label_bootstyle).place(x=155, y=20)
        ttk.Label(song_frame, text='\nTotal Song', font=(self._font,14), bootstyle=label_bootstyle).place(x=20,y=70)

        self.no_song_label = ttk.Label(song_frame, font=(self._font,40,'bold'), bootstyle=label_bootstyle)
        self.no_song_label.place(x=20,y=10)

        # categories
        frame_bootstyle = 'warning'
        label_bootstyle = frame_bootstyle + 'inverse'

        category_frame = ttk.Frame(self._frame, bootstyle=frame_bootstyle)
        category_frame.place(x=30, y=275, width=300, height=150)
        
        ttk.Label(category_frame, image=self.__category_img, bootstyle=label_bootstyle).place(x=155, y=10)
        ttk.Label(category_frame, text='\nTotal Category', font=(self._font,14), bootstyle=label_bootstyle).place(x=20,y=70)
        
        self.no_category_label = ttk.Label(category_frame, font=(self._font,40,'bold'), bootstyle=label_bootstyle)
        self.no_category_label.place(x=20,y=10)

        # singers
        frame_bootstyle = 'info'
        label_bootstyle = frame_bootstyle + 'inverse'
        
        singer_frame = ttk.Frame(self._frame, bootstyle=frame_bootstyle)
        singer_frame.place(x=400, y=275, width=300, height=150)
        ttk.Label(singer_frame, image=self.__singer_img, bootstyle=label_bootstyle).place(x=155, y=20)
        ttk.Label(singer_frame, text='\nTotal Singer', font=(self._font,14), bootstyle=label_bootstyle).place(x=20,y=70)

        self.no_singer_label = ttk.Label(singer_frame, font=(self._font,40,'bold'), bootstyle=label_bootstyle)
        self.no_singer_label.place(x=20,y=10)

    def __load_image(self):
        img_path = 'images/home/'
        self.__user_img = resize_picture(img_path + 'user.png',125,125)
        self.__song_img = resize_picture(img_path + 'song.png',110,110)
        self.__category_img = resize_picture(img_path + 'category.png',135,135)
        self.__singer_img = resize_picture(img_path + 'singer.png',110,110)

    def _reload(self):
        no_user = len(self.user_mng._data)
        no_song = len(self.song_mng._data)
        singer_group, category_group = self.song_mng.group()
        no_category = len(category_group)
        no_singer = len(singer_group)

        self.no_user_label.configure(text=no_user)
        self.no_song_label.configure(text=no_song)
        self.no_category_label.configure(text=no_category)
        self.no_singer_label.configure(text=no_singer)
        

if __name__ == "__main__":
    umng = UserManager()
    smng = SongManager()
    
    ws = ttk.Window()
