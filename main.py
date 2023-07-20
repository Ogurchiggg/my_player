from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import shutil
from mutagen.mp3 import MP3
from time import time
import pygame as pg
import asyncio

from PIL import Image, ImageTk

import sqlite3


'''class App:
    async def exec(self):
        self.window = Window(asyncio.get_event_loop())
        await self.window.show()


class Window(tk.Tk):
    def __init__(self, loop):
        self.loop = loop
        self.root = tk.Tk()
        self.animation = "░▒▒▒▒▒"
        self.label = tk.Label(text="")
        self.label.grid(row=0, columnspan=2, padx=(8, 8), pady=(16, 0))
        self.progressbar = ttk.Progressbar(length=280)
        self.progressbar.grid(row=1, columnspan=2, padx=(8, 8), pady=(16, 0))
        button_block = tk.Button(text="Calculate Sync", width=10, command=self.calculate_sync)
        button_block.grid(row=2, column=0, sticky=tk.W, padx=8, pady=8)
        button_non_block = tk.Button(text="Calculate Async", width=10, command=lambda: self.loop.create_task(self.calculate_async()))
        button_non_block.grid(row=2, column=1, sticky=tk.W, padx=8, pady=8)

    async def show(self):
        while True:
            self.label["text"] = self.animation
            self.animation = self.animation[1:] + self.animation[0]
            self.root.update()
            await asyncio.sleep(.1)

    def calculate_sync(self):
        max = 3000000
        for i in range(1, max):
            self.progressbar["value"] = i / max * 100

    async def calculate_async(self):
        max = 3000000
        for i in range(1, max):
            self.progressbar["value"] = i / max * 100
            if i % 1000 == 0:
                await asyncio.sleep(0)'''


pg.mixer.init()

if not os.path.exists('music'):
    os.mkdir("music")

con = sqlite3.connect('test.db')
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS music(
   music_id INTEGER PRIMARY KEY AUTOINCREMENT,
   name TEXT,
   length TEXT,
   time_create TEXT);
""")

cur.execute("""CREATE TABLE IF NOT EXISTS playlists(
   playlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
   name TEXT,
   time_create TEXT,
   musics TEXT);
""")


con.commit()

def finish():
    root.destroy()  # ручное закрытие окна и всего приложения
    print("Закрытие приложения")


root = Tk()     # создаем корневой объект - окно
root.title("Плеер")     # устанавливаем заголовок окна
root.geometry("300x600-0-0")    # устанавливаем размеры окна
root.minsize(300,600)
icon = ImageTk.PhotoImage(Image.open('ico.png'))
root.iconphoto(False, icon)
root.protocol("WM_DELETE_WINDOW", finish)
root.attributes("-alpha", 0.8)
root.attributes("-toolwindow", False)
root.config(bg="#000000")

root.columnconfigure(index=0, weight=1)
root.columnconfigure(index=1, weight=1)

scale_vars = dict()

def show_all_music():
    global all_music_frame, scale_vars

    all_music_frame.destroy()
    all_music_frame = ttk.Frame(borderwidth=0, relief=SOLID)

    all_music_frame.grid(row=4, column=0, columnspan=2, padx=0, pady=0, sticky=EW)

    cur.execute("SELECT name, length FROM music")

    c = 1
    for m in cur.fetchall():
        frame = ttk.Frame(all_music_frame, borderwidth=1, relief=SOLID, padding=5)
        music_label = ttk.Label(frame, text=f"{m[0]}")

        ttk.Button(frame, text="", width=3, image=icon, command=lambda name=f"{m[0]}": play_music(name)).grid(row=0, column=0, padx=2, pady=2, sticky=W)

        if not (f"{m[0]}" in scale_vars):
            scale_vars[f"{m[0]}"] = IntVar(value=0)
        ttk.Scale(frame, orient=HORIZONTAL, length=250, from_=0.0, to=m[1], variable=scale_vars[f"{m[0]}"]).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=EW)

        music_label.grid(row=0, column=1, padx=5, pady=0, sticky=EW)

        frame.grid(row=c, padx=5, pady=5, sticky=EW)

        c += 1

    print("show_all_music")
    #print(scale_vars)


def show_playlists():
    global all_music_frame
    print("show_playlists")
    all_music_frame.destroy()
    all_music_frame = ttk.Frame(borderwidth=0, relief=SOLID)

def add_music():
    filepath = filedialog.askopenfilename()
    if filepath != "":
        name = filepath[filepath.rfind('/')+1:]
        f = MP3(filepath)
        l = f.info.length*1000//1

        shutil.copyfile(filepath, f'music/{name}')

        cur.execute(f"INSERT INTO music (name, length, time_create) VALUES ('{name}', {l}, {time()})")
        con.commit()
        show_all_music()


def play_music(name):
    global scale_vars

    print(name)
    pg.mixer.music.load(f"music\{name}")
    pg.mixer.music.play()
    scale_vars[f"{name}"].set(20000)
    #show_all_music()
    '''while pg.mixer.music.get_busy():
        print(scale_vars[name])
        k = input()
        if k == "s":
            pg.mixer.music.stop()
        scale_vars[name] = pg.mixer.music.get_pos()
        pg.time.wait(500)'''


def search():
    print("search")

def activ_search(event):
    search_bar.delete(0, END)

def not_activ_search(event):
    search_bar.delete(0, END)
    search_bar.insert(0, "Найти")


btn1 = ttk.Button(text="Вся музыка", width=20, command=show_all_music)
btn1.grid(row=0, column=0, padx=5, pady=5, sticky=NW)

btn2 = ttk.Button(text="Плейлисты", width=20, command=show_playlists)
btn2.grid(row=0, column=1, padx=5, pady=5, sticky=NE)

btn_d = ttk.Button(text="Добавить музыку", width=20, command=add_music)
btn_d.grid(row=1, column=0, padx=5, pady=5, sticky=NW)

search_bar = ttk.Entry()
search_bar.grid(row=2, column=0, columnspan=2, padx=[5, 27], pady=5, sticky=EW)
btnp = ttk.Button(text="", width=3, command=search)
btnp.grid(row=2, column=1, sticky=E)
search_bar.insert(0, "Найти")

search_bar.bind("<FocusIn>", activ_search)
search_bar.bind("<FocusOut>", not_activ_search)

'''def test_change(new_val):
    print(test_var.get())
    #print(new_val)

test_var = IntVar(value=0)
scale = ttk.Scale(orient=HORIZONTAL, length=200, from_=1.0, to=100.0, variable=test_var, command=test_change)
scale.grid(row=3, column=0, columnspan=2, sticky=EW)
test_var.set(50)
print(test_var)'''

all_music_frame = ttk.Frame(borderwidth=0, relief=SOLID)


if __name__ == "__main__":
    #asyncio.run(App().exec())
    show_all_music()
    root.mainloop()
    pg.quit()
