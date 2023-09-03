import tkinter as tk  
from tkinter import ttk 
from collections import deque
from frames.settings import Settings
from frames.timer import Timer


COLOUR_PRIMARY = "#2E3F4F"
COLOUR_SECONDARY = "293846"
COLOUR_LIGHT_BACKGROUND = "#FFF"
COLOUR_LIGHT_TEXT = "#EEE"
COLOUR_DARK_TEXT = "#8095A8"

class TimerBomb(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Timer.TFrame", background=COLOUR_LIGHT_BACKGROUND)
        style.configure("Background.TFrame", background=COLOUR_PRIMARY)
        style.configure(
            "TimerText.TLabel",
            background =COLOUR_LIGHT_BACKGROUND,
            foreground = COLOUR_DARK_TEXT,
            font = "Courier 38"
        )

        style.configure(
            "LightText.TLabel",
            background =COLOUR_PRIMARY,
            foreground = COLOUR_DARK_TEXT,
        )

        style.configure(
            "TimerBombText.TButton",
            background =COLOUR_SECONDARY,
            foreground = COLOUR_DARK_TEXT,
        )

        style.map(
            "TimerBombButton.TLabel",
            background =[("active",COLOUR_PRIMARY),("disabled",COLOUR_PRIMARY)]
        )

        self["background"] = COLOUR_PRIMARY
        
        self.title("Timer Bomb")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
 
        self.podomoro = tk.StringVar(value=25)
        self.long_break = tk.StringVar(value=15)
        self.short_break = tk.StringVar(value=5)
        self.timer_order = ["Pomodoro","Short Break", "Pomodoro", "Short Break", "Pomodoro", "Long Break"]
        self.timer_schedule = deque(self.timer_order) 

        container = ttk.Frame(self)
        container.grid()
        container.columnconfigure(0, weight=1)

        self.frames = {}

        timer_frame = Timer(container, self, lambda: self.show_frame(Settings))
        settings_frames = Settings(container,self, lambda:self.show_frame(Timer))
        timer_frame.grid(row=0 ,column=0, sticky="NESW")
        settings_frames.grid(row=0, column=0, sticky="NESW")

        self.frames[Timer] = timer_frame
        self.frames[Settings] = settings_frames

        self.show_frame(Timer)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

app =TimerBomb()
app.mainloop()