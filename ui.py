import settings as stg
import tkinter as tk
import toml
from timer import populate_settings_entries, update_time_display, reset_timer, pomodoro_timer, toggle_pause_resume, apply_settings

def get_version_from_pyproject():
    try:
        with open("pyproject.toml", "r") as file:
            pyproject = toml.load(file)
            return pyproject.get("project", {}).get("version", "Unknown")
    except FileNotFoundError:
        return "Unknown"

def validate_input(P, max_value):
    # Validates whether the user input is an integer or empty
    if P == "":
        return True
    if P.isdigit():
        value = int(P)
        return 0 <= value <= max_value
    return False

def ui(settings: stg.Settings):
    # Initialise UI
    stg.load_settings(settings)

    # Tkinter UI setup
    root = tk.Tk()
    root.title(f"Pomodoro Timer")
    root.resizable(False, False)
    root.config(bg="#FF6347")

    # UI elements
    font_style = ("Helvetica", 14)

    time_label = tk.Label(root, text="Pomodoro Timer", font=("Helvetica", 20, "bold"), bg="#FF6347", fg="white")
    time_label.pack(pady=10)

    # Settings table
    settings_frame = tk.Frame(root, bg="#FF6347")
    settings_frame.pack(pady=10)

    # Table headers
    tk.Label(settings_frame, text="", font=font_style, bg="#FF6347", fg="white").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(settings_frame, text="Hours", font=font_style, bg="#FF6347", fg="white").grid(row=0, column=1, padx=10, pady=5)
    tk.Label(settings_frame, text="Minutes", font=font_style, bg="#FF6347", fg="white").grid(row=0, column=2, padx=10, pady=5)

    # Work time row
    tk.Label(settings_frame, text="Work", font=font_style, bg="#FF6347", fg="white").grid(row=1, column=0, padx=10, pady=5)
    work_hours_entry = tk.Entry(settings_frame, font=font_style, width=5, validate="key", validatecommand=(root.register(lambda P: validate_input(P, 23)), "%P"))
    work_hours_entry.grid(row=1, column=1, padx=10, pady=5)
    work_minutes_entry = tk.Entry(settings_frame, font=font_style, width=5, validate="key", validatecommand=(root.register(lambda P: validate_input(P, 59)), "%P"))
    work_minutes_entry.grid(row=1, column=2, padx=10, pady=5)

    # Short break row
    tk.Label(settings_frame, text="Short Pause", font=font_style, bg="#FF6347", fg="white").grid(row=2, column=0, padx=10, pady=5)
    break_hours_entry = tk.Entry(settings_frame, font=font_style, width=5, validate="key", validatecommand=(root.register(lambda P: validate_input(P, 23)), "%P"))
    break_hours_entry.grid(row=2, column=1, padx=10, pady=5)
    break_minutes_entry = tk.Entry(settings_frame, font=font_style, width=5, validate="key", validatecommand=(root.register(lambda P: validate_input(P, 59)), "%P"))
    break_minutes_entry.grid(row=2, column=2, padx=10, pady=5)

    # Long break row
    tk.Label(settings_frame, text="Long Pause", font=font_style, bg="#FF6347", fg="white").grid(row=3, column=0, padx=10, pady=5)
    long_break_hours_entry = tk.Entry(settings_frame, font=font_style, width=5, validate="key", validatecommand=(root.register(lambda P: validate_input(P, 23)), "%P"))
    long_break_hours_entry.grid(row=3, column=1, padx=10, pady=5)
    long_break_minutes_entry = tk.Entry(settings_frame, font=font_style, width=5, validate="key", validatecommand=(root.register(lambda P: validate_input(P, 59)), "%P"))
    long_break_minutes_entry.grid(row=3, column=2, padx=10, pady=5)

    # Version label
    version = get_version_from_pyproject()
    version_label = tk.Label(root, text=f"Version {version}", font=("Helvetica", 10), bg="#FF6347", fg="white", anchor="e")
    version_label.pack(side="bottom", anchor="se", padx=10, pady=5)

    # Buttons
    button_frame = tk.Frame(root, bg="#FF6347")
    button_frame.pack(pady=10)

    start_button = tk.Button(button_frame, text="Pause", command=lambda: toggle_pause_resume(settings), font=("Helvetica", 16), bg="#dc3545", fg="white", relief="raised", bd=5)
    start_button.grid(row=0, column=0, padx=10, pady=5)

    reset_button = tk.Button(button_frame, text="Reset", command=lambda: reset_timer(settings), font=("Helvetica", 16), bg="#6c757d", fg="white", relief="raised", bd=5)
    reset_button.grid(row=0, column=1, padx=10, pady=5)

    apply_button = tk.Button(button_frame, text="Apply", command=lambda: apply_settings(settings), font=("Helvetica", 16), bg="#007bff", fg="white", relief="raised", bd=5)
    apply_button.grid(row=0, column=2, padx=10, pady=5)

    # Assign entries to settings
    settings.root = root
    settings.time_label = time_label
    settings.work_hours_entry = work_hours_entry
    settings.work_minutes_entry = work_minutes_entry
    settings.break_hours_entry = break_hours_entry
    settings.break_minutes_entry = break_minutes_entry
    settings.long_break_hours_entry = long_break_hours_entry
    settings.long_break_minutes_entry = long_break_minutes_entry
    settings.start_button = start_button

    # Populate and start
    populate_settings_entries(settings)
    update_time_display(settings)
    settings.is_working = True
    reset_timer(settings)
    settings.is_running = True
    pomodoro_timer(settings)
    root.mainloop()