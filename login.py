import ttkbootstrap as ttk
from tkinter import * 
from ttkbootstrap.constants import *
import os
from display.resize_img import resize_picture
from ttkbootstrap.dialogs import Messagebox

root = ttk.Window(themename='minty')
root.title("Login - Group 3 - DS - Advance Python Project")
root.geometry('980x650+170+20')
root.resizable(width = False, height = False)
root.config(bg='#EDF7F2')
#ededed: grey
#f0eced
#EDF7F2
#F3FAF6
my_font = 'bookman old style'

#CEEADC
frame = ttk.Frame(root,width=800,height=450)
frame.place(x=90,y=90)

img= resize_picture(r'images/main/login.png',350,443)
ttk.Label(frame,image=img).place(x=1,y=1)

# heading 
ttk.Label(frame, text='Log in',font=(my_font,35,'bold'),bootstyle='primary').place(x=510,y=50)

# admin name
admin = ttk.Entry(frame,font=(my_font,15))
admin.place(x=450,y=170)
admin.insert(0,'Admin name')

def on_enter(e):
    admin.delete(0,'end')
def on_leave(e):
    name=admin.get()
    if name=='':
        admin.insert(0,'Admin name')

admin.bind('<FocusIn>',on_enter)
admin.bind('<FocusOut>',on_leave)

# password
code = ttk.Entry(frame,font=(my_font,15))
code.place(x=450,y=250)
code.insert(0,'Password')

def on_enter(e):
    code.config(show='*')
    code.delete(0,'end')
def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Password')

code.bind('<FocusIn>',on_enter)
code.bind('<FocusOut>',on_leave)

# sign in
def login():
    admin_name = admin.get()
    password = code.get()
    valid_admin = 'Admin'
    valid_password = '1234'

    if (admin_name==valid_admin and password==valid_password):
        root.destroy()
        # excute command in shell
        os.system('python test.py')
    elif (admin_name != valid_admin):
        Messagebox.show_error('Invalid admin name!','Invalid input')
    elif (password != valid_password):
        Messagebox.show_error('Invalid admin password!','Invalid input')

btn_style = ttk.Style()
btn_style.configure('secondary.TButton', font=(my_font,10,'bold'))

ttk.Button(frame,text='Log in', style='secondary.TButton', cursor='hand2', command=login).place(x=650,y=350)

root.mainloop()