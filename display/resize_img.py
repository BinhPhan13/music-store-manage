from PIL import Image, ImageTk
import ttkbootstrap as ttk

def resize_picture(path, w, h):
    img_import = Image.open(path)
    resize = img_import.resize((w,h))
    img = ImageTk.PhotoImage(resize)
    return img 

