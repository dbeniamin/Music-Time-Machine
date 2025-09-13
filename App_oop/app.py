import flet as ft
from datetime import datetime
import threading
import webbrowser
from App_oop.config.settings import load_config, save_config
from App_oop.logic.spotify import SpotifyClient
from .ui.layout import build_layout


class SpotifyTimeMachineApp:
    def __init__(self):
        self.page = None

        # Credentials
        self.spotify_id = None
        self.spotify_secret = None

        # UI refs
        self.date_field = None
        self.creds_status = None
        self.config_button = None
        self.create_button = None
        self.progress_ring = None
        self.status_column = None

    # ----------------------------
    # Setup
    # ----------------------------
    def main(self, page: ft.Page):
        self.page = page
        page.title = "🎵 Music Time Machine"
        page.window_width = 800
        page.window_height = 900
        page.scroll = ft.ScrollMode.AUTO

        # App Title UI
        app_title = ft.Text(
            "🎵Music Time Machine🎵",
            size=30,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.PRIMARY
        )
        centered_title = ft.Row([app_title], alignment=ft.MainAxisAlignment.CENTER)

        # UI refs
        self.date_field = ft.TextField(
            label="Date",
            hint_text="YYYY-MM-DD",
            value=datetime.now().strftime("%Y-%m-%d"),
            prefix_icon=ft.Icons.DATE_RANGE,
        )
        self.creds_status = ft.Text("❌ Not configured", color=ft.Colors.RED, size=16)
        self.config_button = ft.ElevatedButton(
            text="Configure Spotify API",
            icon=ft.Icons.SETTINGS,
            on_click=self.show_credentials_dialog,
        )
        self.create_button = ft.ElevatedButton(
            text="🎶 Create Playlist",
            icon=ft.Icons.PLAYLIST_ADD,
            on_click=self.create_playlist_clicked,
            disabled=True,
            width=200,
            height=50
        )
        self.progress_ring = ft.ProgressRing(visible=False)
        self.status_column = ft.Column(scroll=ft.ScrollMode.AUTO)

        # Main page layout
        page_content = ft.Column(
            [
                centered_title,
                build_layout(self)
            ],
            expand=True
        )
        page.add(page_content)

        # Load configuration
        config = load_config()
        self.spotify_id = config.get("spotify_id")
        self.spotify_secret = config.get("spotify_secret")
        if self.spotify_id and self.spotify_secret:
            self.update_creds_status(True)
            self.log_message("Configuration loaded successfully!", "success")
        else:
            self.log_message("No configuration found. Please set up your Spotify credentials.", "info")

    # ----------------------------
    # Helpers
    # ----------------------------
    def log_message(self, message, type="info"):
        colors = {
            "info": ft.Colors.BLUE,
            "success": ft.Colors.GREEN,
            "error": ft.Colors.RED,
            "warning": ft.Colors.ORANGE,
        }
        icons = {
            "info": ft.Icons.INFO,
            "success": ft.Icons.CHECK_CIRCLE,
            "error": ft.Icons.ERROR,
            "warning": ft.Icons.WARNING,
        }
        self.status_column.controls.append(
            ft.Row([
                ft.Icon(name=icons[type], color=colors[type], size=16),
                ft.Text(message, size=14, color=colors[type])
            ])
        )
        if len(self.status_column.controls) > 10:
            self.status_column.controls.pop(0)
        self.page.update()

    def update_creds_status(self, configured=False):
        if configured:
            self.creds_status.value = "✅ Configured"
            self.creds_status.color = ft.Colors.GREEN
            self.create_button.disabled = False
        else:
            self.creds_status.value = "❌ Not configured"
            self.creds_status.color = ft.Colors.RED
            self.create_button.disabled = True
        self.page.update()

    # ----------------------------
    # Credentials dialog
    # ----------------------------
    def show_credentials_dialog(self, e=None):
        client_id_field = ft.TextField(
            label="Spotify Client ID",
            hint_text="Enter your Spotify Client ID",
            value=self.spotify_id or "",
        )
        client_secret_field = ft.TextField(
            label="Spotify Client Secret",
            hint_text="Enter your Spotify Client Secret",
            value=self.spotify_secret or "",
            password=True,
        )

        warning_text = ft.Text("", color=ft.Colors.RED, size=14)

        instructions = ft.Column([
            ft.Text("To use this app, you need Spotify API credentials:", size=14),
            ft.Text("1. Go to ", size=14),
            ft.TextButton(
                text="https://developer.spotify.com/dashboard",
                on_click=lambda e: webbrowser.open("https://developer.spotify.com/dashboard"),
            ),
            ft.Text("2. Log in with your Spotify account", size=14),
            ft.Text("3. Create an App and set the redirect URI to:", size=14),
            ft.Text("https://example.com/callback", size=14, color=ft.Colors.BLUE),
        ], spacing=4)

        def save_credentials(ev=None):
            if client_id_field.value.strip() and client_secret_field.value.strip():
                self.spotify_id = client_id_field.value.strip()
                self.spotify_secret = client_secret_field.value.strip()
                save_config({"spotify_id": self.spotify_id, "spotify_secret": self.spotify_secret})
                self.update_creds_status(True)
                self.log_message("Spotify credentials saved successfully!", "success")
                dialog.open = False
                self.page.update()
            else:
                warning_text.value = "❌ Both fields are required!"
                dialog.update()

        def cancel(ev=None):
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Spotify API Configuration"),
            content=ft.Column([
                instructions,
                ft.Divider(),
                client_id_field,
                client_secret_field,
                warning_text
            ], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=cancel),
                ft.ElevatedButton("Save", on_click=save_credentials),
            ],
        )

        self.page.open(dialog)


    # ----------------------------
    # OAuth dialog for copy-paste
    # ----------------------------
    def get_oauth_url_from_user(self, auth_url):
        done = threading.Event()
        self.redirect_input = ft.TextField(
            label="Paste Spotify redirect URL here", width=500
        )

        def submit(e):
            self.redirect_response = self.redirect_input.value
            done.set()
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Spotify Login"),
            content=ft.Column([
                ft.Text("1. Log in via the browser window."),
                ft.Text("2. Approve access."),
                ft.Text("3. Copy the full URL you are redirected to."),
                self.redirect_input
            ]),
            actions=[ft.ElevatedButton("Submit", on_click=submit)]
        )

        self.page.open(dialog)
        self.page.update()
        done.wait()  # wait until user submits
        return self.redirect_response

    # ----------------------------
    # Playlist creation
    # ----------------------------
    def create_playlist_clicked(self, e):
        threading.Thread(target=self.create_playlist, daemon=True).start()

    def create_playlist(self):
        try:
            date = self.date_field.value.strip()
            if not date:
                snackbar = ft.SnackBar(content=ft.Text("Please enter a date"))
                self.page.overlay.append(snackbar)
                snackbar.open = True
                self.page.update()
                return

            self.progress_ring.visible = True
            self.create_button.disabled = True
            self.page.update()

            client = SpotifyClient(self.spotify_id, self.spotify_secret, app_instance=self)
            count = client.create_playlist_from_billboard(date)

            self.log_message(f"Playlist created with {count} songs", "success")
            snackbar = ft.SnackBar(content=ft.Text(f"✅ Playlist created with {count} songs!"),
                                   bgcolor=ft.Colors.GREEN)
            self.page.overlay.append(snackbar)
            snackbar.open = True
            self.page.update()
        except Exception as e:
            msg = f"Error: {str(e)}"
            self.log_message(msg, "error")
            snackbar = ft.SnackBar(content=ft.Text(f"❌ {msg}"), bgcolor=ft.Colors.RED)
            self.page.overlay.append(snackbar)
            snackbar.open = True
            self.page.update()
        finally:
            self.progress_ring.visible = False
            self.create_button.disabled = False
            self.page.update()
