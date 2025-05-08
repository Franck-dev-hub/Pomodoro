import json

SETTINGS_FILE = "settings.json"

class Settings:
    # Class for managing application parameters
    def __init__(self):
        self.work_time = 25 * 60  # Default working time in seconds
        self.short_break_time = 5 * 60  # Default short pause time in seconds
        self.long_break_time = 15 * 60 # Default long pause time in seconds
        self.remaining_time = 0
        self.is_working = False
        self.is_running = False
        self.long_break_cycle = 3
        self.cycle_count = 0
        self.root = None
        self.time_label = None
        self.work_hours_entry = None
        self.work_minutes_entry = None
        self.break_hours_entry = None
        self.break_minutes_entry = None
        self.start_button = None


def load_settings(stg: Settings):
    # Load parameters from a JSON file
    # If the file does not exist or is corrupt, use the default values
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
            stg.work_time = max(0, settings.get("work_time", 25 * 60))
            stg.short_break_time = max(0, settings.get("short_break_time", 5 * 60))
            stg.long_break_time = max(0, settings.get("long_break_time", 15 * 60))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erreur lors du chargement des paramètres : {e}")
        save_settings(stg)


def save_settings(stg: Settings):
    # Saves the parameters in a JSON file
    settings = {
        "work_time": stg.work_time,
        "short_break_time": stg.short_break_time,
        "long_break_time": stg.long_break_time,
    }
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
    except IOError as e:
        print(f"Erreur lors de la sauvegarde des paramètres : {e}")