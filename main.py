import flet as ft
from App_oop.app import SpotifyTimeMachineApp

def main():
    app = SpotifyTimeMachineApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()
