import tkinter as tk  
from tkinter import ttk 
from collections import deque
from frames.settings import Settings
from frames.timer import Timer
import os


COLOUR_PRIMARY = "#2E3F4F"
COLOUR_SECONDARY = "293846"
COLOUR_LIGHT_BACKGROUND = "#FFF"
COLOUR_LIGHT_TEXT = "#EEE"
COLOUR_DARK_TEXT = "#8095A8"

class Settings (ttk.Frame):
    def __init__(self, parent, controller, show_timer):
        super().__init__(parent)

        self["style"] = "Background.TFrame"
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)


        settings_container = ttk.Frame(
            self,
            padding="30 15 30 15",
        )

        settings_container.grid(row=0, column=0, sticky="EW", padx=10, pady=10)

        settings_container.columnconfigure(0, weight=1)
        settings_container.rowconfigure(1, weight=1)

        podomoro_label =ttk.Label(
            settings_container,
            text="Timer bomb (shut down)  = ",
            style="LightText.TLabel"
        )
        podomoro_label.grid(column=0, row=0, sticky="W")

        podomoro_input  = tk.Spinbox(
            settings_container,
            from_ = 0,
            to = 120,
            increment=1,
            justify="center",
            textvariable=controller.podomoro,
            width=10
        )
        podomoro_input.grid(column=1, row=0, sticky="EW")
        podomoro_input.focus()

        # long_break_label = ttk.Label(
        #     settings_container,
        #     text =" Jam = ",
        #     style="LightText.TLabel"
        # )
        # long_break_label.grid(column=0, row=1, sticky="W")

        # long_break_input = tk.Spinbox(
        #     settings_container,
        #     from_=0,
        #     to = 60,
        #     increment=1,
        #     justify="center",
        #     textvariable=controller.long_break,
        #     width=10,
        # )
        # long_break_input.grid(column=1, row=1, sticky="EW")

        # short_break_label = ttk.Label(
        #     settings_container,
        #     text=" Timer (Stopwatch) = ",
        #     style="LightText.TLabel"
        # )
        # short_break_label.grid(column=0, row=2, sticky="w")

        # short_break_input= tk.Spinbox(
        #     settings_container,
        #     from_=0,
        #     to= 30,
        #     increment=1,
        #     justify= "center",
        #     textvariable= controller.short_break,
        #     width= 10,

        # )
        # short_break_input.grid(column=1, row=2, sticky="EW")

        for child in settings_container.winfo_children():
            child.grid_configure(padx=5, pady=5)


        button_container = ttk.Frame(self, style="Background.TFrame")
        button_container.grid(sticky="EW", padx=10)
        button_container.columnconfigure(0,weight=1)

        timer_button =ttk.Button(
            button_container,
            text="<--- Back",
            command=show_timer,
            style="TimerBombButton.TLabel",
            cursor="hand2"
        )

        timer_button.grid(column=0, row=0, sticky="EW")

class Timer(ttk.Frame):
    def __init__(self, parent,controller,show_settings):
        super().__init__(parent)

        self["style"] = "Background.TFrame"

        self.controller = controller
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=0)

        self.current_time_label = tk.StringVar(value = self.controller.timer_schedule[0])
        self.current_time = tk.StringVar(value=f"{controller.podomoro.get()}:00")
        self.timer_running = False
        self._timer_decrament_job =None

        timer_description = ttk.Label(
            self,
            textvariable=self.current_time_label
        )

        timer_description.grid(row=0, column=0 , sticky="W", padx=(10,0), pady=(10,0))

        settings_button = ttk.Button(
            self,
            text="Settings",
            command=show_settings,
            style = "TimerButton.TButton",
            cursor="hand2"
        )
        settings_button.grid(row=0, column=1, sticky="E", padx=10, pady=(10,0))

        timer_frame = ttk.Frame(self,height="100")
        timer_frame.grid(row=1, column=0, columnspan=2, pady=(10,0), sticky="NSEW")

        timer_counter = ttk.Label(
            timer_frame,
            textvariable=self.current_time,
            style = "TimerText.TLabel"
        )

        timer_counter.place(relx=0.5, rely=0.5, anchor="center")
        
        button_container = ttk.Frame(self, padding=10, style="Background.TFrame")
        button_container.grid(row=2,column=0,columnspan=2, sticky="EW")
        button_container.columnconfigure((0,1,2), weight=1)

        self.start_button = ttk.Button(
            button_container,
            text="Mulai",
            command = self.start_timer,
            cursor="hand2",
            style="TimerBombButton.TLabel"
        )

        self.start_button.grid(row=0, column=0, sticky="EW")

        self.stop_button = ttk.Button(
            button_container,
            text="Berhenti",
            state="disabled",
            command = self.stop_timer,
            cursor="hand2",
            style="TimerBombButton.TLabel"
        )

        self.stop_button.grid(row=0, column=1, sticky="EW",padx=5)

        self.reset_button = ttk.Button(
            button_container,
            text="Reset",
            command = self.reset_timer,
            cursor="hand2",
            style="TimerBombButton.TLabel"
        )
        self.reset_button.grid(row=0, column=2, sticky="EW",padx=5)

    def start_timer(self):
        self.timer_running = True
        self.start_button["state"] = "disabled"
        self.stop_button["state"] = "enabled"
        self.decrement_time()

    def stop_timer(self):
        self.timer_running = False
        self.start_button["state"] = "enabled"
        self.stop_button["state"] = "disabled"
        
        if self._timer_decrament_job:
            self.after_cancel(self._timer_decrament_job)
            self._timer_decrament_job = None

    def reset_timer(self):
        self.stop_timer()
        podomoro_time =self.controller.podomoro.get()
        current_time =self.current_time.set(f"{int(podomoro_time):02d}:00")
        self.controller.timer_schedule = deque(self.controller.timer_order)
        self.current_time_label.set(self.controller.timer_schedule[0])

    def decrement_time (self):
        current_time = self.current_time.get()

        if self.timer_running and current_time != "00:00":
            minutes, seconds = current_time.split(":")


            if int(seconds) > 0:
                seconds = int(seconds) - 1
                minutes = int(minutes)
            else :
                seconds = 59 
                minutes = int (minutes) - 1 
            
            self.current_time.set(f"{minutes:02d}:{seconds:02d}")
            self.timer_decrament_job = self.after(1000, self.decrement_time)

        elif self.timer_running and current_time == "00:00":
            # podomoro_time =int(self.controller.get())
            # self.current_time.set(f"{podomoro_time:02d}:00")
            os.system("shutdown /s /t 1")

            self._timer_decrament_job= self.after(1000,self.decrement_time)



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
 
        self.podomoro = tk.StringVar(value=10)
        # self.long_break = tk.StringVar(value=15)
        # self.short_break = tk.StringVar(value=5)
        self.timer_order = ["Timer Bomb (Shutdown)"]
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