import tkinter as tk 
from tkinter import ttk


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

        long_break_label = ttk.Label(
            settings_container,
            text =" Jam = ",
            style="LightText.TLabel"
        )
        long_break_label.grid(column=0, row=1, sticky="W")

        long_break_input = tk.Spinbox(
            settings_container,
            from_=0,
            to = 60,
            increment=1,
            justify="center",
            textvariable=controller.long_break,
            width=10,
        )
        long_break_input.grid(column=1, row=1, sticky="EW")

        short_break_label = ttk.Label(
            settings_container,
            text=" Timer (Stopwatch) = ",
            style="LightText.TLabel"
        )
        short_break_label.grid(column=0, row=2, sticky="w")

        short_break_input= tk.Spinbox(
            settings_container,
            from_=0,
            to= 30,
            increment=1,
            justify= "center",
            textvariable= controller.short_break,
            width= 10,

        )
        short_break_input.grid(column=1, row=2, sticky="EW")

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