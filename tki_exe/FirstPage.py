# View more python learning tutorial on my Youtube and Youku channel!!!

# Youtube video tutorial: https://www.youtube.com/channel/UCdyjiB5H8Pu7aDTNVXTTpcg
# Youku video tutorial: http://i.youku.com/pythontutorial

import tkinter as tk
from tkinter import messagebox  # import this to fix messagebox error
import pickle
import test

window = tk.Tk()
window.title('毕业设计：GUI')
window.geometry('450x300')

# welcome image
canvas = tk.Canvas(window, height=200, width=500)
image_file = tk.PhotoImage(file='welcome.gif')
image = canvas.create_image(0,0, anchor='nw', image=image_file)
canvas.pack(side='top')

# user information
tk.Label(window, text='用户名: ').place(x=50, y= 150)
tk.Label(window, text='密 码: ').place(x=50, y= 190)

var_usr_name = tk.StringVar()
var_usr_name.set(' ')
entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
entry_usr_name.place(x=160, y=150)
var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=160, y=190)

def usr_login():
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    try:
        with open('usrs_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        with open('usrs_info.pickle', 'wb') as usr_file:
            usrs_info = {'admin': 'admin'}
            pickle.dump(usrs_info, usr_file)
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            tk.messagebox.showinfo(title='登陆成功', message='欢迎回来，' + usr_name)
        else:
            tk.messagebox.showerror(message='输入的用户名或密码错误。')
    else:
        is_sign_up = tk.messagebox.askyesno('欢迎',
                               '该账户不存在，是否需要注册？')
        if is_sign_up:
            usr_sign_up()

def usr_sign_up():
    def sign_to_Mofan_Python():
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        nn = new_name.get()
        with open('usrs_info.pickle', 'rb') as usr_file:
            exist_usr_info = pickle.load(usr_file)
        if np != npf:
            tk.messagebox.showerror('错误', '两次密码输入不一致！')
        elif nn in exist_usr_info:
            tk.messagebox.showerror('错误', '该账户已注册！')
        else:
            exist_usr_info[nn] = np
            with open('usrs_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
            tk.messagebox.showinfo('欢迎回来', '登陆成功！')
            window_sign_up.destroy()
    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('350x200')
    window_sign_up.title('Sign up window')

    new_name = tk.StringVar()
    new_name.set('')
    tk.Label(window_sign_up, text='用户名: ').place(x=10, y= 10)
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)
    entry_new_name.place(x=150, y=10)

    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='密 码: ').place(x=10, y=50)
    entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_usr_pwd.place(x=150, y=50)

    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='确认密码: ').place(x=10, y= 90)
    entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_usr_pwd_confirm.place(x=150, y=90)

    btn_comfirm_sign_up = tk.Button(window_sign_up, text='注册', command=sign_to_Mofan_Python)
    btn_comfirm_sign_up.place(x=150, y=130)

# login and sign up button
btn_login = tk.Button(window, text='开启摄像头', command=test.openCamera)
btn_login.place(x=170, y=230)
btn_sign_up = tk.Button(window, text='注册', command=usr_sign_up)
btn_sign_up.place(x=270, y=230)

window.mainloop()