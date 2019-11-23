import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)


class MainApplication(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, "MigHtyFi")

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomePage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()


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
                             command=lambda: controller.show_frame)
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(HomePage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                             command=lambda: controller.show_frame(PageOne))
        button2.pack()


app = MainApplication()
app.mainloop()
