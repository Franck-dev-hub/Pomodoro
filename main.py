#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 07/03/2025 by Franck
"""

import tkinter as tk
from tkinter import messagebox
import time
import threading

# Variables globales
work_time = 60 * 60  # Temps de travail en secondes
break_time = 5 * 60  # Temps de pause en secondes
remaining_time = 0
is_working = False
is_running = False

def update_time_display():
    hours = remaining_time // 3600
    minutes = (remaining_time % 3600) // 60
    seconds = remaining_time % 60
    status = "Travail: " if is_working else "Pause: "
    time_label.config(text=f"{status}{hours:02}:{minutes:02}:{seconds:02}")

def show_message(title, message):
    top = tk.Toplevel()
    top.attributes('-topmost', True)
    top.withdraw()
    messagebox.showinfo(title, message, parent=top)
    top.destroy()

def pomodoro_timer():
    global remaining_time, is_working, is_running
    while is_running:
        if remaining_time > 0:
            time.sleep(1)
            remaining_time -= 1
            update_time_display()
        else:
            if is_working:
                show_message("Pomodoro", "Temps de travail terminé ! Prenez une pause.")
                is_working = False
                remaining_time = break_time
            else:
                show_message("Pomodoro", "Pause terminée ! Retour au travail.")
                is_working = True
                remaining_time = work_time

def start_timer():
    global is_running, is_working, remaining_time
    if not is_running:
        is_running = True
        is_working = True
        remaining_time = work_time
        threading.Thread(target=pomodoro_timer, daemon=True).start()
        start_button.config(text="Arrêter", bg="#FF6347", fg="white")
    else:
        is_running = False
        start_button.config(text="Démarrer", bg="#28a745", fg="white")

def apply_settings():
    global work_time, break_time, remaining_time
    work_hours = int(work_hours_entry.get())
    work_minutes = int(work_minutes_entry.get())
    break_hours = int(break_hours_entry.get())
    break_minutes = int(break_minutes_entry.get())
    work_time = work_hours * 3600 + work_minutes * 60
    break_time = break_hours * 3600 + break_minutes * 60
    if is_working:
        remaining_time = work_time
    else:
        remaining_time = break_time
    update_time_display()

# Fonction pour valider les entrées et n'accepter que des chiffres
def validate_input_input(P):
    if P == "" or P.isdigit():
        return True
    return False

# Création de la fenêtre principale
root = tk.Tk()
root.title("Pomodoro Timer")
root.geometry("400x400")
root.config(bg="#FF6347")

# Style de la police et du texte
font_style = ("Helvetica", 14)

# Label du temps restant
time_label = tk.Label(root,
                      text="Pomodoro Timer",
                      font=("Helvetica", 20, "bold"),
                      bg="#FF6347",
                      fg="white")
time_label.pack(pady=20)

# Entrées pour la configuration du temps de travail et de pause
settings_frame = tk.Frame(root, bg="#FF6347")
settings_frame.pack(pady=10)

tk.Label(settings_frame,
         text="Temps de travail (heures):",
         font=font_style,
         bg="#FF6347",
         fg="white").grid(row=0, column=0, padx=10, pady=5)
work_hours_entry = tk.Entry(settings_frame,
                            font=font_style,
                            width=5,
                            validate="key",
                            validatecommand=(root.register(validate_input_input), "%P"))
work_hours_entry.insert(0, "1")
work_hours_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(settings_frame,
         text="Temps de travail (minutes):",
         font=font_style,
         bg="#FF6347",
         fg="white").grid(row=1, column=0, padx=10, pady=5)
work_minutes_entry = tk.Entry(settings_frame,
                              font=font_style,
                              width=5,
                              validate="key",
                              validatecommand=(root.register(validate_input_input), "%P"))
work_minutes_entry.insert(0, "0")
work_minutes_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(settings_frame, text="Temps de pause (heures):",
         font=font_style,
         bg="#FF6347",
         fg="white").grid(row=2, column=0, padx=10, pady=5)
break_hours_entry = tk.Entry(settings_frame,
                             font=font_style,
                             width=5,
                             validate="key",
                             validatecommand=(root.register(validate_input_input), "%P"))
break_hours_entry.insert(0, "0")
break_hours_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(settings_frame,
         text="Temps de pause (minutes):",
         font=font_style,
         bg="#FF6347",
         fg="white").grid(row=3, column=0, padx=10, pady=5)
break_minutes_entry = tk.Entry(settings_frame,
                               font=font_style,
                               width=5,
                               validate="key",
                               validatecommand=(root.register(validate_input_input), "%P"))
break_minutes_entry.insert(0, "5")
break_minutes_entry.grid(row=3, column=1, padx=10, pady=5)

# Boutons pour démarrer et appliquer les paramètres
button_frame = tk.Frame(root, bg="#FF6347")
button_frame.pack(pady=20)

start_button = tk.Button(button_frame,
                         text="Démarrer",
                         command=start_timer,
                         font=("Helvetica", 16),
                         bg="#28a745",
                         fg="white",
                         relief="raised",
                         bd=5)
start_button.grid(row=0, column=0, padx=10, pady=5)

apply_button = tk.Button(button_frame,
                         text="Appliquer",
                         command=apply_settings,
                         font=("Helvetica", 16),
                         bg="#007bff",
                         fg="white",
                         relief="raised",
                         bd=5)
apply_button.grid(row=0, column=1, padx=10, pady=5)

update_time_display()

# Lancer le compteur automatiquement
start_timer()

root.mainloop()