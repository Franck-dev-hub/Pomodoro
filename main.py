#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 07/03/2025 by Franck
"""

import json
import tkinter as tk
from tkinter import messagebox

# Constants
SETTINGS_FILE = "settings.json"
VERSION = "V1.3"


class Settings:
    def __init__(self):
        self.work_time = 60 * 60  # Default work time in seconds
        self.break_time = 5 * 60  # Default break time in seconds
        self.remaining_time = 0
        self.is_working = False
        self.is_running = False
        self.root = None
        self.time_label = None
        self.work_hours_entry = None
        self.work_minutes_entry = None
        self.break_hours_entry = None
        self.break_minutes_entry = None
        self.start_button = None


def load_settings(stg: Settings):
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
            stg.work_time = settings.get("work_time", 60 * 60)
            stg.break_time = settings.get("break_time", 5 * 60)
    except (FileNotFoundError, json.JSONDecodeError):
        pass


def save_settings(stg: Settings):
    settings = {
        "work_time": stg.work_time,
        "break_time": stg.break_time
    }
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)


def update_time_display(stg: Settings):
    hours = stg.remaining_time // 3600
    minutes = (stg.remaining_time % 3600) // 60
    seconds = stg.remaining_time % 60
    status = "Work: " if stg.is_working else "Break: "
    stg.time_label.config(text=f"{status}{hours:02}:{minutes:02}:{seconds:02}")


def show_message(title, message):
    top = tk.Toplevel()
    top.attributes('-topmost', True)
    top.withdraw()
    messagebox.showinfo(title, message, parent=top)
    top.destroy()


def pomodoro_timer(stg: Settings):
    def run():
        if not stg.is_running:
            return
        if stg.remaining_time > 0:
            stg.remaining_time -= 1
            update_time_display(stg)
            stg.root.after(1000, run)
        else:
            if stg.is_working:
                show_message("Pomodoro", "Work time is over! Take a break.")
                stg.is_working = False
                stg.remaining_time = stg.break_time
            else:
                show_message("Pomodoro", "Break is over! Back to work.")
                stg.is_working = True
                stg.remaining_time = stg.work_time
            update_time_display(stg)
            stg.root.after(1000, run)

    run()


def toggle_pause_resume(stg: Settings):
    if stg.is_running:
        # Pause
        stg.is_running = False
        stg.start_button.config(text="Resume", bg="#ffc107")
    else:
        # Resume
        stg.is_running = True
        pomodoro_timer(stg)
        stg.start_button.config(text="Pause", bg="#dc3545")


def reset_timer(stg: Settings):
    stg.is_running = False
    stg.start_button.config(text="Pause", bg="#dc3545")
    if stg.is_working:
        stg.remaining_time = stg.work_time
    else:
        stg.remaining_time = stg.break_time
    update_time_display(stg)


def apply_settings(stg: Settings):
    work_hours = int(stg.work_hours_entry.get())
    work_minutes = int(stg.work_minutes_entry.get())
    break_hours = int(stg.break_hours_entry.get())
    break_minutes = int(stg.break_minutes_entry.get())
    stg.work_time = work_hours * 3600 + work_minutes * 60
    stg.break_time = break_hours * 3600 + break_minutes * 60
    save_settings(stg)
    if stg.is_working:
        stg.remaining_time = stg.work_time
    else:
        stg.remaining_time = stg.break_time
    update_time_display(stg)


def populate_settings_entries(stg: Settings):
    work_hours, work_minutes = divmod(stg.work_time, 3600)
    break_hours, break_minutes = divmod(stg.break_time, 3600)

    stg.work_hours_entry.delete(0, tk.END)
    stg.work_hours_entry.insert(0, str(work_hours))
    stg.work_minutes_entry.delete(0, tk.END)
    stg.work_minutes_entry.insert(0, str((stg.work_time % 3600) // 60))

    stg.break_hours_entry.delete(0, tk.END)
    stg.break_hours_entry.insert(0, str(break_hours))
    stg.break_minutes_entry.delete(0, tk.END)
    stg.break_minutes_entry.insert(0, str((stg.break_time % 3600) // 60))


def validate_input(P):
    return P == "" or P.isdigit()


def main(stg: Settings):
    load_settings(stg)

    # Tkinter UI setup
    root = tk.Tk()
    root.title(f"Pomodoro Timer {VERSION}")
    root.geometry("400x400")
    root.config(bg="#FF6347")

    # UI elements
    font_style = ("Helvetica", 14)

    time_label = tk.Label(root, text="Pomodoro Timer", font=("Helvetica", 20, "bold"), bg="#FF6347", fg="white")
    time_label.pack(pady=20)

    settings_frame = tk.Frame(root, bg="#FF6347")
    settings_frame.pack(pady=10)

    # Settings entries
    tk.Label(settings_frame, text="Work time (hours):", font=font_style, bg="#FF6347", fg="white").grid(row=0, column=0, padx=10, pady=5)
    work_hours_entry = tk.Entry(settings_frame, font=font_style, width=5, validate="key", validatecommand=(root.register(validate_input), "%P"))
    work_hours_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(settings_frame, text="Work time (minutes):", font=font_style, bg="#FF6347", fg="white").grid(row=1, column=0, padx=10, pady=5)
    work_minutes_entry = tk.Entry(settings_frame, font=font_style, width=5, validate="key", validatecommand=(root.register(validate_input), "%P"))
    work_minutes_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(settings_frame, text="Break time (hours):", font=font_style, bg="#FF6347", fg="white").grid(row=2, column=0, padx=10, pady=5)
    break_hours_entry = tk.Entry(settings_frame, font=font_style, width=5, validate="key", validatecommand=(root.register(validate_input), "%P"))
    break_hours_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(settings_frame, text="Break time (minutes):", font=font_style, bg="#FF6347", fg="white").grid(row=3, column=0, padx=10, pady=5)
    break_minutes_entry = tk.Entry(settings_frame, font=font_style, width=5, validate="key", validatecommand=(root.register(validate_input), "%P"))
    break_minutes_entry.grid(row=3, column=1, padx=10, pady=5)

    button_frame = tk.Frame(root, bg="#FF6347")
    button_frame.pack(pady=20)

    # Buttons
    start_button = tk.Button(button_frame, text="Pause", command=lambda: toggle_pause_resume(stg), font=("Helvetica", 16), bg="#dc3545", fg="white", relief="raised", bd=5)
    start_button.grid(row=0, column=0, padx=10, pady=5)

    reset_button = tk.Button(button_frame, text="Reset", command=lambda: reset_timer(stg), font=("Helvetica", 16), bg="#6c757d", fg="white", relief="raised", bd=5)
    reset_button.grid(row=0, column=1, padx=10, pady=5)

    apply_button = tk.Button(button_frame, text="Apply", command=lambda: apply_settings(stg), font=("Helvetica", 16), bg="#007bff", fg="white", relief="raised", bd=5)
    apply_button.grid(row=0, column=2, padx=10, pady=5)

    stg.root = root
    stg.time_label = time_label
    stg.work_hours_entry = work_hours_entry
    stg.work_minutes_entry = work_minutes_entry
    stg.break_hours_entry = break_hours_entry
    stg.break_minutes_entry = break_minutes_entry
    stg.start_button = start_button

    populate_settings_entries(stg)
    update_time_display(stg)
    stg.is_working = True
    reset_timer(stg)
    stg.is_running = True
    pomodoro_timer(stg)
    root.mainloop()

if __name__ == "__main__":
    main(Settings())
