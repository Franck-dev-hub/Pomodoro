from settings import Settings, save_settings
import tkinter as tk
from tkinter import messagebox

def update_time_display(stg: Settings):
    """
    Met à jour l'affichage du temps restant dans l'interface utilisateur.
    """
    hours = stg.remaining_time // 3600
    minutes = (stg.remaining_time % 3600) // 60
    seconds = stg.remaining_time % 60
    status = "Work: " if stg.is_working else "Break: "
    stg.time_label.config(text=f"{status}{hours:02}:{minutes:02}:{seconds:02}")

def show_message(title, message):
    # Displays a dialog box with a message
    top = tk.Toplevel()
    top.attributes('-topmost', True)
    top.withdraw()
    messagebox.showinfo(title, message, parent=top)
    top.destroy()

def pomodoro_timer(stg: Settings):
    # Manages the timer
    def run():
        if not stg.is_running:
            return
        if stg.remaining_time > 0:
            stg.remaining_time -= 1
            update_time_display(stg)
            stg.root.after(1000, run)
        else:
            if stg.is_working:
                stg.cycle_count += 1
                if stg.cycle_count % 3 == 0:
                    show_message("Pomodoro", "Work time is over! Take a long break.")
                    stg.remaining_time = stg.long_break_time
                    stg.cycle_count = 0
                else:
                    show_message("Pomodoro", "Work time is over! Take a short break.")
                    stg.remaining_time = stg.short_break_time
                stg.is_working = False
            else:
                show_message("Pomodoro", "Break is over! Back to work.")
                stg.is_working = True
                stg.remaining_time = stg.work_time
            update_time_display(stg)
            stg.root.after(1000, run)
    if stg.is_running:
        run()

def input_fields(stg: Settings, state):
    stg.work_hours_entry.config(state=state)
    stg.work_minutes_entry.config(state=state)
    stg.break_hours_entry.config(state=state)
    stg.break_minutes_entry.config(state=state)
    stg.long_break_hours_entry.config(state=state)
    stg.long_break_minutes_entry.config(state=state)

def toggle_pause_resume(stg: Settings):
    # Pauses or resumes the timer
    if stg.is_running:
        stg.is_running = False
        stg.start_button.config(text="Resume", bg="#ffc107")
        # Activate input fields
        input_fields(stg, "normal")
    else:
        stg.is_running = True
        pomodoro_timer(stg)
        stg.start_button.config(text="Pause", bg="#dc3545")
        # Deactivate input fields
        input_fields(stg, "disabled")

def reset_timer(stg: Settings):
    # Resets the timer to the working or break time
    stg.is_running = False
    stg.start_button.config(text="Pause", bg="#dc3545")
    stg.remaining_time = stg.work_time if stg.is_working else stg.short_break_time
    update_time_display(stg)
    input_fields(stg, "normal")

def apply_settings(stg: Settings):
    # Applies the parameters entered by the user
    try:
        work_hours = int(stg.work_hours_entry.get() or 0)
        work_minutes = int(stg.work_minutes_entry.get() or 0)
        break_hours = int(stg.break_hours_entry.get() or 0)
        break_minutes = int(stg.break_minutes_entry.get() or 0)
        long_break_hours = int(stg.long_break_hours_entry.get() or 0)
        long_break_minutes = int(stg.long_break_minutes_entry.get() or 0)

        stg.work_time = work_hours * 3600 + work_minutes * 60
        stg.short_break_time = break_hours * 3600 + break_minutes * 60
        stg.long_break_time = long_break_hours * 3600 + long_break_minutes * 60

        save_settings(stg)
        reset_timer(stg)
    except ValueError:
        show_message("Erreur", "Veuillez entrer des valeurs valides.")

def populate_settings_entries(stg: Settings):
    # Fills the input fields with the current parameter values
    work_hours, work_minutes = divmod(stg.work_time, 3600)
    work_minutes //= 60  # Convert remaining seconds to minutes

    short_break_hours, short_break_minutes = divmod(stg.short_break_time, 3600)
    short_break_minutes //= 60  # Convert remaining seconds to minutes

    long_break_hours, long_break_minutes = divmod(stg.long_break_time, 3600)
    long_break_minutes //= 60  # Convert remaining seconds to minutes

    # Populate work time fields
    stg.work_hours_entry.delete(0, tk.END)
    stg.work_hours_entry.insert(0, str(work_hours))
    stg.work_minutes_entry.delete(0, tk.END)
    stg.work_minutes_entry.insert(0, str(work_minutes))

    # Populate short break fields
    stg.break_hours_entry.delete(0, tk.END)
    stg.break_hours_entry.insert(0, str(short_break_hours))
    stg.break_minutes_entry.delete(0, tk.END)
    stg.break_minutes_entry.insert(0, str(short_break_minutes))

    # Populate long break fields
    stg.long_break_hours_entry.delete(0, tk.END)
    stg.long_break_hours_entry.insert(0, str(long_break_hours))
    stg.long_break_minutes_entry.delete(0, tk.END)
    stg.long_break_minutes_entry.insert(0, str(long_break_minutes))