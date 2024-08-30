import tkinter as tk
import time

def animation(btn,window,tipmsg,step=15):
    global tipbase
    window.update()
    tipbase=None
    if tipbase!=None:
        if tipbase.winfo_exists():
            tipbase.destroy()
    try:
        tipbase=tk.Frame(window,bg="#303030",height=btn.winfo_height())
        tip=tk.Label(tipbase,text="",anchor="w",bg="#303030",fg="#ffffff")
        tip.pack(fill=tk.BOTH)
        tipbase.place(x=btn.winfo_x()+btn.winfo_width(),y=btn.winfo_y(),height=btn.winfo_height())
        # Get the final width
        tip["text"]=tipmsg
        window.update()
        final_width=tipbase.winfo_width()+72
        tip["text"]=""
        tipbase.place_configure(width=0)
        window.update()
        for i in range(final_width//step):
            tipbase.place_configure(width=i*step)
            window.update()
            time.sleep(0.01)
        tip["text"]=tipmsg
    except: #If anything fails, the base frame might have been destroyed.
        return

win=tk.Tk()
win.title("Demo For Sidebar Floating Animation")
win.minsize(540,480)

sidebar=tk.Frame(width=50,bg="#202020")
sidebar.pack(side=tk.LEFT,fill=tk.Y)
sidebar.pack_propagate(False)

buttons=[]

for i in range(5):
    buttons.append(tk.Button(sidebar,text="O",relief="flat",bd=0,bg="#202020",fg="#ffffff"))

for button in buttons:
    button.pack(fill=tk.X)
    button.bind("<Enter>",lambda event,this=button:animation(this,win,f"Text Placeholder {buttons.index(this)}"))
    button.bind("<Leave>",lambda event:tipbase.destroy())

win.mainloop()