import os
import tkinter as tk
from time import sleep
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import Image, ImageTk

from FileSimpleAnalyse import FileSimpleAnalyse as fsa

LARGE_FONT = ("Verdana", 20)
FRAMESIZE = "700x500"
STYLEFILESFOLDER = "StyleFiles"

class MainApplication(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry(FRAMESIZE)
        self.iconbitmap('{0}/equalizer1.ico'.format(STYLEFILESFOLDER))

        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, "MigHtyFi")
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (EntryPage, SongAnalyserPage, PageOne, AboutPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(EntryPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class EntryPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#211F1E")
        self.parent = parent
        self.controller = controller

        label = ttk.Label(self, text="Welcome To MigHtYFi!", font=LARGE_FONT)
        label.grid(row=0, column=0, columnspan=2)

        main_photo = Image.open("{0}/spectrum_image.png".format(STYLEFILESFOLDER))
        main_photo = ImageTk.PhotoImage(main_photo)
        photo_label = ttk.Label(self, image=main_photo)
        label.image = main_photo
        photo_label.grid(row=1, column=0, columnspan=2)
        button_to_home_page = ttk.Button(self, text="Go To Song Analyzer", command=lambda: self.controller.show_frame(SongAnalyserPage))
        button_to_home_page.grid(row=3, column=1)
        button_to_about_page = ttk.Button(self, text="About",
                                         command=lambda: self.controller.show_frame(AboutPage))
        button_to_about_page.grid(row=3, column=0)
        # button_to_home_page = ttk.Button(self, text="About",
        #                                  command=lambda: self.controller.show_frame(SongAnalyserPage))
        # button_to_home_page.grid(row=3, column=0)


class SongAnalyserPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#211F1E")
        self.parent = parent
        self.file_path = ""
        label = ttk.Label(self, text="Start Page", font=LARGE_FONT)

        label.grid(row=0, column=0, columnspan=3)

        main_photo = Image.open("{0}/spectrum_image.png".format(STYLEFILESFOLDER))
        main_photo = ImageTk.PhotoImage(main_photo)
        photo_label = ttk.Label(self, image=main_photo)
        label.image = main_photo
        photo_label.grid(row=1, column=0, columnspan=3)

        button_to_open_files = ttk.Button(self, text="Open files", command=self.open_file_clicked)

        button_to_open_files.grid(row=2, column=1)

        button_to_analyze_file = ttk.Button(self, text="Analyze File", command=self.analyse_song_clicked)
        button_to_analyze_file.grid(row=2, column=0)

        button2 = ttk.Button(self, text="Back",
                             command=lambda: controller.show_frame(EntryPage))
        button2.grid(row=2, column=2)

    def open_file_clicked(self):
        name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
                               filetypes=(("m4a file", "*.m4a"), ("mp3 file", "*.mp3"), ("Wave File", "*.wav"), ("All Files", "*.*")),
                               title="Choose a file."
                               )
        self.file_path = name

    def analyse_song_clicked(self):
        if self.file_path == "":
            messagebox.showinfo("ERROR!", "no file was selected!")
            return
        file_analyse = fsa(self.file_path)
        file_analyse.plot_all()

        messagebox.showinfo("Thank you", "Your song {0} is analysed\nA browser window will be open with the results".format(self.file_path[:-4]))


class PageOne(tk.Frame):

    def get_song_name(self, entry):
        # todo: here activate the crawler.
        print("hello {0}".format(self.content.get()))

    def __init__(self, parent, controller):
        self.content = tk.StringVar()
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Insert your song name", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        song_name_entry = ttk.Entry(self, textvariable=self.content)
        song_name_entry.pack()

        button1 = ttk.Button(self, text="Get song Youtube Data")
        button1.bind("<Button-1>", self.get_song_name)
        button1.pack()

        button2 = ttk.Button(self, text="Back Home",
                             command=lambda: controller.show_frame(EntryPage))
        button2.pack()


class AboutPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#363332")
        label = ttk.Label(self, text="About Page", font=LARGE_FONT)
        label.grid(row=0, column=2)

        label_about_us = ttk.Label(self,
                                   text=open("{0}/aboutmightyfi.txt"
                                             .format(STYLEFILESFOLDER)).read())
        label_about_us.grid(row=1, columnspan=3)
        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(EntryPage))
        button1.grid(row=2, column=1)

        button2 = ttk.Button(self, text="To Our Song Analyzer",
                             command=lambda: controller.show_frame(SongAnalyserPage))
        button2.grid(row=3, column=1)

# style = ttk.Style()
# style.map("C.TButton",
#     foreground=[('pressed', 'red'), ('active', 'blue')],
#     background=[('pressed', '!disabled', 'black'), ('active', 'white')]
#     )
app = MainApplication()
app.mainloop()