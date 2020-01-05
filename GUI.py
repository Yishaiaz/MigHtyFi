import os
import pandas as pd
import tkinter as tk
from tkinter import *
from time import sleep
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import AudioFeatureExtractor
from PredictionModule import DataPreprocessor, PredictionModule
from SongFeatureExtractor import song_processing
from FileSimpleAnalyse import FileSimpleAnalyse as fsa
import warnings

LARGE_FONT = ("Verdana", 20)
FRAMESIZE = "850x500"
STYLEFILESFOLDER = "StyleFiles"


class MainApplication(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry(FRAMESIZE)
        # self.iconbitmap('{0}/equalizer1.ico'.format(STYLEFILESFOLDER))
        self.iconbitmap('{0}/equalizer.ico'.format(STYLEFILESFOLDER))

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
                                          command=lambda: self.controller.show_frame(PageOne))
        button_to_about_page.grid(row=3, column=0)

        # button_to_home_page = ttk.Button(self, text="About",
        #                                  command=lambda: self.controller.show_frame(SongAnalyserPage))
        # button_to_home_page.grid(row=3, column=0)


class SongAnalyserPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#211F1E")
        self.parent = parent
        self.file_path = ""
        self.file_path_to_trained_model = ""
        self.pred_model = None
        self.data_processor = DataPreprocessor()

        label = ttk.Label(self, text="Start Page", font=LARGE_FONT)
        label.grid(row=0, column=0, columnspan=3)

        # main photo
        main_photo = Image.open("{0}/spectrum_image.png".format(STYLEFILESFOLDER))
        main_photo = ImageTk.PhotoImage(main_photo)
        photo_label = ttk.Label(self, image=main_photo)
        label.image = main_photo
        photo_label.grid(row=1, column=0, columnspan=2)
        # lyrics text box
        self.lyrics_text = tk.Text(self, width=20, height=20)
        self.lyrics_text.insert('1.0', "Song Lyrics:\n")
        self.lyrics_text.grid(row=1, column=2, columnspan=1)
        # load model button
        button_to_open_files = ttk.Button(self, text="Load Model", command=self.load_model_clicked)
        button_to_open_files.grid(row=2, column=3)

        button_to_open_files = ttk.Button(self, text="Open files", command=self.open_file_clicked)

        button_to_open_files.grid(row=2, column=1)

        button_to_analyze_file = ttk.Button(self, text="Analyze File", command=self.analyse_song_clicked)
        button_to_analyze_file.grid(row=2, column=0)

        button2 = ttk.Button(self, text="Home Page",
                             command=lambda: controller.show_frame(EntryPage))
        button2.grid(row=2, column=2)

    def open_file_clicked(self):
        name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
                               filetypes=(("m4a file", "*.m4a"), ("mp3 file", "*.mp3"), ("Wave File", "*.wav"), ("All Files", "*.*")),
                               title="Choose a file."
                               )
        self.file_path = name

    def load_model_clicked(self):
        name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
                               filetypes=(("SAV file", "*.sav"), ("All Files", "*")),
                               title="Choose a file.")
        self.file_path_to_trained_model = name

    def analyse_song_clicked(self):
        if self.file_path == "":
            messagebox.showinfo("ERROR!", "no file was selected!")
            return
        # file_analyse = fsa(self.file_path)
        # file_analyse.plot_all()
        # afe = AudioFeatureExtractor.SingleAudioFeatureExtractor(self.file_path)
        # print(afe.extract_features())
        # print(afe.get_features_labels())
        # df = pd.DataFrame(data=afe.get_feature_dict(), index=[self.file_path])
        self.pred_model = PredictionModule(trained_already=self.file_path_to_trained_model)
        self.lyrics_text.insert(tk.END, "again")

        messagebox.showinfo("Thank you", "Your song {0} is analysed\nA browser window will be open with the results".format(self.file_path[:-4]))


class AboutPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#363332")
        label = ttk.Label(self, text="About Page", font=LARGE_FONT)
        label.grid(row=0, column=0)

        label_about_us = tk.Text(self, width=100, height=20)
        label_about_us.insert('1.0', open("{0}/aboutmightyfi.txt".format(STYLEFILESFOLDER)).read())
        label_about_us.grid(row=1, column=0, columnspan=3)
        button1 = ttk.Button(self, text="Home Page",
                             command=lambda: controller.show_frame(EntryPage))
        button1.grid(row=2, column=1)

        button2 = ttk.Button(self, text="To Our Song Analyzer",
                             command=lambda: controller.show_frame(SongAnalyserPage))
        button2.grid(row=2, column=2)


class PageOne(tk.Frame):

    def get_song_name(self, entry):
        # todo: here activate the crawler.
        print("hello {0}".format(self.content.get()))

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        Label(self, text='Song Path').grid(row=0)
        Label(self, text='Song Name').grid(row=1)
        Label(self, text='Artist name').grid(row=2)

        self.entry_song_path = Entry(self)
        self.entry_song_name = Entry(self)
        self.entry_artist_name = Entry(self)

        self.entry_song_path.grid(row=0, column=1)
        self.entry_song_name.grid(row=1, column=1)
        self.entry_artist_name.grid(row=2, column=1)

        b1 = Button(self, text='Browse Song File', command=self.browse_button)
        b1.grid(row=0, column=2, sticky=W, pady=4)

        b2 = Button(self, text='Predict', command=self.get_feature)
        b2.grid(row=3, column=0, sticky=W, pady=4)

        # b2 = Button(master, text='Browse', command=lambda: browse_button('MODEL')).grid(row=1, column=2, sticky=W,
        #                                                                                 pady=4)
        # b3 = Button(master, text='Predict', command=predict).grid(row=2, column=1, sticky=W, pady=4)

        # button1 = ttk.Button(self, text="Load File", command=self.open_file_clicked,textvariable=self.path)
        # # button1.bind("<Button-1>", self.open_file_clicked
        # button1.pack()
        #
        # button2 = ttk.Button(self, text="Predict Song",
        #                      command=self.get_feature(e1, e2.get()))
        # button2.pack()

    def browse_button(self):
        self.entry_song_path.delete(0, END)
        self.entry_song_path.insert(0, askopenfilename(initialdir=os.path.join( os.environ['HOMEPATH'], 'Desktop'), title='Select File'))

    # def open_file_clicked(self):
    #     print('entered')
    #     name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
    #                            filetypes=(("m4a file", ".m4a"), ("mp3 file", ".mp3"), ("Wave File", ".wav"), ("All Files", ".*")),
    #                            title="Choose a file."
    #                            )
    #     self.file_path = name


    def get_feature(self):
        song_dict = song_processing(self.entry_song_path.get(), self.entry_song_name.get(), self.entry_artist_name.get())
        print(song_dict)



# style = ttk.Style()
# style.map("C.TButton",
#     foreground=[('pressed', 'red'), ('active', 'blue')],
#     background=[('pressed', '!disabled', 'black'), ('active', 'white')]
#     )

if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        app = MainApplication()
        app.mainloop()