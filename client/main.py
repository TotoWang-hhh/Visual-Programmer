# Python Visual Programmer
# 2023 By 小康2022 & 真_人工智障
# v0.1.0

import tkinter as tk
import tkinter.ttk as ttk
import tkintertools as tkt
import tttk
import tkinter.messagebox as msgbox
import tkinter.simpledialog as sd
import tkinter.filedialog as fd

import os
import sys
import time
import threading
import math

import pyvpmodules.ui as ui
import pyvpmodules.clipboard as clipboard
import pyvpmodules.editor as editor

from PIL import ImageTk, Image
import pyclip
import webbrowser
import socket
import json
import warnings
import ast


# 全局变量
global_ver = '.demo'
global_debug = {'net': False}
global_server_addr = ("116.198.35.73", 10009)
global_about_useslist = {'Python': "https://www.python.org/", 'xiaokang2022/tkintertools': "https://github.com/xiaokang2022/tkintertools/",
                         'spyoungtech/pyclip': "https://github.com/spyoungtech/pyclip/", 'totowang-hhh/tttk': "https://github.com/totowang-hhh/tttk/"}
global_file = []

os.chdir(os.path.split(os.path.realpath(__file__))[0])
print(os.getcwd())
# os.chdir(sys.argv[0])

pyvpclipboard = clipboard.Clipboard()

root = tkt.Tk()
root.withdraw()

# 浅做一个启动界面
startwin = tk.Toplevel()
startwin.overrideredirect(True)
startwin.title('Starting PyVP')
startwin.geometry('256x256'+'+'+str((startwin.winfo_screenwidth()-256) //
                  2)+'+'+str((startwin.winfo_screenheight()-256)//2))
icon_pil = Image.open("./icon.png")
icon256_pil = icon_pil.resize((256, 256))
icon256_tk = ImageTk.PhotoImage(image=icon256_pil)
tk.Label(startwin, image=icon256_tk, bg='#000000').pack()
startwin.configure(background='#000000')
startwin.wm_attributes('-transparentcolor', '#000000')
startwin.wm_attributes('-alpha', 0)
# 入场动画
for i in range(0, 10):
    startwin.wm_attributes('-alpha', i/10)
    startwin.update()
    time.sleep(0.05)
startwin.update()

# 在这里写启动准备工作，时不时记得update()一下防止未响应
# 加载界面中一定包含的图片图标等
# 左边栏图像
sidebarimgpil = []
sidebarimg = []
sidebarimgpil.append(Image.open("./img/sidebar/folder.png"))
sidebarimgpil.append(Image.open("./img/sidebar/code.png"))
sidebarimgpil.append(Image.open("./img/sidebar/function.png"))
sidebarimgpil.append(Image.open("./img/sidebar/class.png"))
sidebarimgpil.append(Image.open("./img/sidebar/modules.png"))

for imgpil in sidebarimgpil:
    sidebarimg.append(ImageTk.PhotoImage(image=imgpil))

# 左边栏图像
sidebarbtmimgpil = []
sidebarbtmimg = []
sidebarbtmimgpil.append(Image.open("./img/sidebarbtm/more.png"))
sidebarbtmimgpil.append(Image.open("./img/sidebarbtm/run.png"))

for imgpil in sidebarbtmimgpil:
    sidebarbtmimg.append(ImageTk.PhotoImage(image=imgpil))

# 其他图像资源
icon96_pil = icon_pil.resize((96, 96))
icon96_tk = ImageTk.PhotoImage(image=icon96_pil)

# 准备完成后的拖延时间
for i in range(0, 20):
    startwin.update()
    time.sleep(0.1)
# 出场动画
for i in range(0, 10):
    startwin.wm_attributes('-alpha', 1-i/10)
    startwin.update()
    time.sleep(0.05)
startwin.update()
startwin.destroy()


# 类与函数
def launch(funcid):
    '''根据传入的字符串找到并执行函数'''
    funcid_splited = funcid.split('.')
    match funcid_splited[0]:
        case 'sidebar':  # 侧边栏按钮
            match funcid_splited[1]:
                case '0':
                    change_sidept_page('file')
                    change_mainpt_page('file')
                case '1':
                    change_sidept_page('code')
                    change_mainpt_page('code')
                case '2':
                    change_sidept_page('func')
                    change_mainpt_page('func')
                case '3':
                    change_sidept_page('class')
                    change_mainpt_page('class')
                case '4':
                    change_sidept_page('modules')
                    change_mainpt_page('modules')
                case _:
                    msgbox.showerror(
                        '错误', 'launch()没有根据给定的id找到相应的函数\n出错id层级: '+funcid_splited[1])
        case 'sidebarbtm':  # 侧边栏底部按钮 顺序从下到上
            match funcid_splited[1]:
                case '0':
                    print('more')
                case '1':
                    print('run')
                case _:
                    msgbox.showerror(
                        '错误', 'launch()没有根据给定的id找到相应的函数\n出错id层级: '+funcid_splited[1])
        case _:
            msgbox.showerror(
                '错误', 'launch()没有根据给定的id找到相应的函数\n出错id层级: '+funcid_splited[0])


def get_fr_server(send_data):
    global global_server_addr
    skt = socket.socket()
    print('[get_fr_server()] Connecting to server...')
    skt.connect(global_server_addr)
    skt.send(json.dumps(send_data).encode('utf-8'))
    print('[get_fr_server()] Waiting for response from server...')
    res = json.loads(skt.recv(1024).decode('utf-8'))
    skt.close()
    return res


def change_sidept_page(pagename):
    global fileframe, resframe, functionframe, classframe, moduleframe
    sidept_pages = {'file': fileframe, 'code': resframe,
                    'func': functionframe, 'class': classframe, 'modules': moduleframe}
    global global_sidept_currpage
    sidept_pages[global_sidept_currpage].pack_forget()
    sidept_pages[pagename].pack(fill=tk.BOTH, expand=True)
    sidept_pages[pagename].pack_propagate(False)
    global_sidept_currpage = pagename


def change_mainpt_page(pagename):
    global welcomepage, editpage
    mainpt_pages = {'spare': welcomepage, 'file': welcomepage, 'code': editpage,
                    'func': welcomepage, 'class': welcomepage, 'modules': welcomepage}
    global global_mainpt_currpage
    mainpt_pages[global_mainpt_currpage].pack_forget()
    mainpt_pages[pagename].pack(fill=tk.BOTH, expand=True)
    mainpt_pages[pagename].pack_propagate(False)
    global_mainpt_currpage = pagename


def about():
    global global_ver, about_updtxt, global_server_addr, global_about_useslist
    aboutwin = tk.Toplevel()
    aboutwin.title('关于PyVP')
    aboutwin.transient(root)
    aboutwin.configure(background='#ffffff')
    # ui.blur_window_background(aboutwin)
    about_pt = tk.Frame(aboutwin, bg='#ffffff')
    icon128_pil = icon_pil.resize((128, 128))
    icon128_tk = ImageTk.PhotoImage(image=icon128_pil)
    tk.Label(about_pt, image=icon128_tk, bg='#ffffff').pack(side=tk.LEFT)
    abouttxtpt = tk.Frame(about_pt, bg='#ffffff')
    tk.Label(abouttxtpt, text='Python Visual Programmer',
             bg='#ffffff', font=('微软雅黑', 20), anchor='w').pack()
    aboutrowb = tk.Frame(abouttxtpt, bg='#ffffff')
    tk.Label(aboutrowb, text='2023 By 小康2022 & 真_人工智障',
             bg='#ffffff', anchor='w').pack(side=tk.LEFT)
    tk.Label(aboutrowb, text='v'+global_ver, bg='#ffffff',
             fg='#909090', anchor='e').pack(side=tk.RIGHT)
    aboutrowb.pack(fill=tk.X)
    ttk.Separator(abouttxtpt).pack(fill=tk.X, pady=10)
    aboutrowc = tk.Frame(abouttxtpt, bg='#ffffff')
    about_updtxt = tk.Label(aboutrowc, text='请等待版本检查就绪',
                            bg='#ffffff', anchor='w')
    about_updtxt.pack(side=tk.LEFT)
    ui.AnimatedButton(aboutrowc, aboutwin, text='项目GitHub', bg='#cccccc', fg='#000000', floatingbg='#000000', floatingfg='#ffffff',
                      command=lambda: webbrowser.open("https://github.com/xiaokang2022/visual-programmer")).pack(side=tk.RIGHT)
    aboutrowc.pack(fill=tk.X)
    uses_pt = tk.Frame(aboutwin, bg='#dddddd')
    tk.Label(uses_pt, text='本项目使用', bg='#303030', fg='#ffffff').pack(fill=tk.X)
    ulist_pt = tk.Frame(uses_pt, bg='#dddddd')
    ulist_cola = tk.Frame(ulist_pt, bg='#dddddd')
    ulist_colb = tk.Frame(ulist_pt, bg='#dddddd')
    curr_col = 0
    for proj in global_about_useslist.keys():
        if curr_col == 0:
            txt = tk.Label(ulist_cola, text=proj, bg='#dddddd', anchor='w')
            curr_col = 1
        elif curr_col == 1:
            txt = tk.Label(ulist_colb, text=proj, bg='#dddddd', anchor='w')
            curr_col = 0
        else:
            warnings.warn('Uses list packing failed')
        txt.bind("<Button-1>", lambda event,
                 url=global_about_useslist[proj]: webbrowser.open(url))
        txt.pack(fill=tk.X)
    ulist_cola.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    ulist_colb.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    ulist_pt.pack(fill=tk.BOTH, expand=True)
    about_pt.pack(fill=tk.X)
    uses_pt.pack(fill=tk.X, padx=10, pady=10)
    abouttxtpt.pack(fill=tk.BOTH, side=tk.RIGHT, padx=15)
    aboutwin.update()
    aboutwin.resizable(False, False)
    try:
        res = get_fr_server(
            {"func": "ver.get_ifnewver", "clientver": global_ver})
        # print(res)
        about_updtxt['text'] = res['msg']
    except:
        about_updtxt['text'] = '暂时无法检查更新'
    aboutwin.mainloop()


def scan_class():
    # print('Scanning Class...')
    try:
        classes = find_classes_in_file(global_file[0]) # BUG: 当切换文件时无法切换索引
        for names in classes:
            classlist.insert('end', names)
        # classlist.pack(fill='both', expand=True)
    except IndexError as e:
        print(e)
        msgbox.showerror("错误", "请先选择一个文件！\n\n详细错误信息请见Console。")


def create_new_class(): # BUG: 无法添加新的列表项
    ask = ui.Dialog(root, "创建新类", ["新类名", "继承名"], btntext="确定")
    ask.mainloop()
    classlist.insert("end", ask.combine_entries()[1])


def del_sel_class():
    sel = classlist.curselection()
    for i in sel:
        print(classlist.get(i))
        classlist.delete(i)


def submit_server_addr(ip_enter, port_enter, askwin=None):
    global global_server_addr
    isvalid = True
    # for pt in ip_enter.get().split('.'):
    #    if not pt.isdigit():
    #        isvalid=False
    if not port_enter.get().isdigit():
        isvalid = False
    if isvalid:
        global_server_addr = (ip_enter.get(), int(port_enter.get()))
    print(get_fr_server({"func": "connection.check", "ver": global_ver}))
    if not get_fr_server({"func": "connection.check", "ver": global_ver})['response']:
        isvalid = False
    if isvalid:
        if askwin != None:
            askwin.destroy()
    else:
        msgbox.showerror('输入信息无效', '指定的服务器配置信息无效\n请编辑确认后再次提交')


def ask_server_addr(root_win=None):
    askaddr_win = tk.Toplevel()
    if root_win != None:
        askaddr_win.transient(root_win)
    askaddr_win.title('指定服务器')
    ip_enter = tttk.TipEnter(askaddr_win, text='地址')
    # ip_enter.tip['anchor']='e'
    # ip_enter.tip['width']=6
    ip_enter.pack(fill=tk.X)
    port_enter = tttk.TipEnter(askaddr_win, text='端口')
    # port_enter.tip['anchor']='e'
    # port_enter.tip['width']=6
    port_enter.pack(fill=tk.X)
    ttk.Button(askaddr_win, text='提交', command=lambda: submit_server_addr(
        ip_enter, port_enter, askaddr_win)).pack(fill=tk.X)
    askaddr_win.update()
    askaddr_win.geometry('300x'+str(askaddr_win.winfo_height()))
    askaddr_win.resizable(0, 0)
    askaddr_win.mainloop()


def change_file(selection: str):
    # 在边栏文件列表中切换文件时执行
    global view_btns
    file = selection['values'][0]
    print("已选择文件："+str(file))
    # 根据文件后缀决定是否执行针对.py文件的内容
    if file.split('.')[len(file.split('.'))-1].lower() == 'py':
        print('Opened .py file running extra tasks...')
        # print('Still not availale')
        # 启用/禁用视图切换
        for btn in view_btns:
            btn.enable()
        # 加载文件代码
        open_code(selection)
        # 读取文件内的类
        scan_class()
    else:
        for btn in view_btns:
            btn.disable()
            # print(btn.disablefg,btn.fg


def open_code(selection):
    # 读取所选的文件 加载代码
    file_path = selection['values'][0]
    pf = open(file_path, 'r', encoding='utf-8')
    data = pf.read()
    if code.get('1.0', tk.END) == '':
        code.insert(tk.END, data)
    else:
        code.delete('1.0', tk.END)
        code.insert(tk.END, data)
    global_file.append(file_path)
    pf.close()


def save_code():
    data = code.get("1.0", "end")
    filename = fd.asksaveasfilename()
    with open(filename, 'w', encoding="utf-8") as sf:
        sf.write(data)


def find_classes_in_file(filename):
    print("Scanning for and listing classes...")
    with open(filename, "r", encoding='utf-8') as file:
        node = ast.parse(file.read(), filename=filename)
    class_names = []
    for item in ast.walk(node):
        if isinstance(item, ast.ClassDef):
            class_names.append(item.name)
    return class_names


# Things in console #
if not '--noclear' in sys.argv:
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


# UI BELOW #
root.deiconify()
root.title('Python Visual Programmer')
root.iconbitmap("./icon.ico")
root.configure(background='#cccccc')
root.minsize(640, 360)
root.geometry(size=(800, 540))

# py_win_style.apply_style(root,'aero')

btmbar = tk.Frame(root, bg='#1e1e1e', height=24)
btmbar.pack(side=tk.BOTTOM, fill=tk.X)

sidebar = tk.Frame(root, bg='#1e1e1e', width=48)
sidebar.pack(side=tk.LEFT, fill=tk.Y)
sidebar.pack_propagate(False)

# print(sidebarimg)
tmp_index = 0
for img in sidebarimg:
    ui.FlatButton(sidebar, image=img, bg='#1e1e1e', floatingbg='nochange', command=lambda index=tmp_index: launch(
        'sidebar.'+str(index))).pack(padx=2, pady=2, side=tk.TOP)
    tmp_index += 1

tmp_index = 0
for img in sidebarbtmimg:
    ui.FlatButton(sidebar, image=img, bg='#1e1e1e', floatingbg='nochange', command=lambda index=tmp_index: launch(
        'sidebarbtm.'+str(index))).pack(padx=2, pady=2, side=tk.BOTTOM)
    tmp_index += 1

sidept = tk.Frame(root, bg='#ffffff', width=200)

global_sidept_currpage = 'file'
global_mainpt_currpage = 'spare'

fileframe = tk.Frame(sidept, bg='#ffffff', width=200)
tk.Label(fileframe, text='FILES', bg='#ffffff', anchor='w').pack(fill=tk.X)

main_file_viewer = ui.FileTree(fileframe, selcommand=change_file)
main_file_viewer.left_frame.pack(fill=tk.BOTH, expand=True)
main_file_viewer.open_dir()

fileframe.pack_propagate(False)

file_rightclick_menu = tttk.Menu(root, {'剪切': lambda: pyvpclipboard.cut(main_file_viewer.tree.item(main_file_viewer.tree.focus())['values'][0], 'file'),
                                        '复制': lambda: pyvpclipboard.copy(main_file_viewer.tree.item(main_file_viewer.tree.focus())['values'][0], 'file'),
                                        '粘贴': lambda: pyvpclipboard.paste_at_file(main_file_viewer.get_focus_dir()),
                                        '永久删除': lambda: print('del'), '重命名': lambda: print('rename')})
main_file_viewer.tree.bind('<Button-3>', lambda event: file_rightclick_menu.show()
                           if len(main_file_viewer.tree.focus()) != 0 else None)
# main_file_viewer.tree.bind(
#    '<<TreeviewSelect>>', lambda _event: change_file(main_file_viewer.tree.focus()))

resframe = tk.Frame(sidept, bg='#ffffff', width=200)
tk.Label(resframe, text='资源库', bg='#ffffff', anchor='w').pack(fill=tk.X)

resframe.pack_propagate(False)

functionframe = tk.Frame(sidept, width=200, bg='#ffffff')
tk.Label(functionframe, text='函数', bg='#ffffff', anchor=tk.W).pack(fill=tk.X)

functionframe.pack_propagate(False)

classframe = tk.Frame(sidept, bg='#ffffff', width=200)
tk.Label(classframe, text='本文件中的类', bg='#ffffff', anchor=tk.W).pack(fill=tk.X)

classlist = tk.Listbox(classframe, bg='#ffffff',
                       relief='flat', bd=0, selectmode=tk.SINGLE)
classlist.pack(fill='both', expand=True)
bottombar = tk.Frame(classframe, bg='#eeeeee', height=20)
bottombar.pack(fill=tk.X, side='bottom')
newclass = ui.FlatButton(
    bottombar, text='新类', bg='#eeeeee', fg='#000000', command=create_new_class)
newclass.pack(side='left', fill='x', expand=True)
delsel = ui.FlatButton(
    bottombar, text='移除选中', bg='#eeeeee', fg='#000000', command=del_sel_class)
delsel.pack(side='right', fill='x', expand=True)

classframe.pack_propagate(False)

moduleframe = tk.Frame(sidept, bg='#ffffff', width=200)
tk.Label(moduleframe, text='模块', bg='#ffffff', anchor=tk.W).pack(fill=tk.X)

moduleframe.pack_propagate(False)

sidept.pack(side=tk.LEFT, fill=tk.Y)

status_color = '#00aa00'
statuspt = tk.Frame(
    btmbar, width=sidebar['width'], height=btmbar['height'], bg=status_color)
statustxt = tk.Label(statuspt, bg=status_color, text='状态', fg='#ffffff')
statustxt.pack(fill=tk.BOTH, expand=True)
statuspt.pack(side=tk.LEFT, fill=tk.Y)
statuspt.pack_propagate(False)

about_txt = tk.Button(btmbar, text='Python Visual Programmer v'+global_ver, bg='#1e1e1e',
                      fg='#ffffff', bd=0, font=('微软雅黑', 7), command=about).pack(side=tk.RIGHT, fill=tk.Y)

view_switch = tk.Frame(btmbar)
view_btns = [ui.FlatButton(view_switch, '顺序视图', bg='#1e1e1e', fg='#ffffff', floatingbg='lighter', floatingfg='nochange', disablefg='darker'),
             ui.FlatButton(view_switch, '蓝图视图', bg='#1e1e1e', fg='#ffffff', floatingbg='lighter', floatingfg='nochange', disablefg='darker')]
for btn in view_btns:
    btn.pack(side=tk.LEFT, fill=tk.Y)
view_switch.pack(side=tk.RIGHT, fill=tk.Y)

root.update()

# 工作区
# win=editor.Editor(root)
win = tk.Frame(root)  # 左侧Frame
win.pack(fill='both', expand=True)
win.pack_propagate(False)


welcomepage = tk.Frame(win)
tk.Label(welcomepage, text="", font=("consolas", 20)).pack()
tk.Label(welcomepage, image=icon96_tk).pack()
tk.Label(welcomepage, text="Welcome to", font=("consolas", 20)).pack()
tk.Label(welcomepage, text="PyVP", font=("consolas", 25)).pack()
tk.Label(welcomepage, text="", font=("consolas", 20)).pack()
tk.Label(welcomepage, text="Where should we start from?",
         font=("consolas", 14)).pack()


editpage = tk.Frame(win)

right_pt = tk.Frame(editpage, width=240, bg='#eeeeee')  # 右侧Frame
right_pt.pack(fill=tk.Y, side=tk.RIGHT)
right_pt.pack_propagate(False)

code = tk.Text(right_pt, width=240, bg='#000000', fg='#ffffff',
               font=('Consolas',), height=10)  # 代码区域
code.pack(side='bottom', fill='x', expand=False)

program_pt = tk.Frame(editpage, bg='#cccccc')
program_pt.pack(fill=tk.BOTH, expand=True)


welcomepage.pack(fill=tk.BOTH, expand=True)


print('root width   ', root.winfo_width())
print('sidebar width   ', sidebar['width'])
print('sidept width   ', sidept['width'])
print('canvas width   ', root.winfo_width()-sidebar['width']-sidept['width'])

root.update()

# 手动指定服务器
if global_server_addr == 'ask':
    ask_server_addr(root_win=root)

main_file_viewer.sync_t.start()

root.protocol("WM_DELETE_WINDOW", lambda: os._exit(1))  # 防止主进程没杀死的问题

root.mainloop()
