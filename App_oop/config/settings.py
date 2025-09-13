import json, os, sys
from pathlib import Path

def get_app_data_dir():
    if sys.platform == "win32":
        app_data = os.environ.get("APPDATA", os.path.expanduser("~"))
        app_dir = Path(app_data) / "SpotifyTimeMachine"
    else:
        app_dir = Path.home() / ".spotify_time_machine"
    app_dir.mkdir(exist_ok=True)
    return app_dir

def load_config():
    config_file = get_app_data_dir() / "config.json"
    if config_file.exists():
        with open(config_file, "r") as f:
            return json.load(f)
    return {}

def save_config(config: dict):
    config_file = get_app_data_dir() / "config.json"
    with open(config_file, "w") as f:
        json.dump(config, f)
