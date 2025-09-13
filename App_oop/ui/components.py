import flet as ft

def status_card(status_column):
    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Status", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=status_column,
                    height=300,
                    padding=10,
                    bgcolor=ft.Colors.ON_SURFACE_VARIANT,
                    border_radius=8,
                    expand=True,
                )
            ]),
            padding=20,
            expand=True,
        )
    )

def creds_card(creds_status, config_button):
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Spotify Credentials", size=18, weight=ft.FontWeight.BOLD),
                    creds_status,
                    config_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,  # This is the key change
            ),
            padding=20,
        ),
        expand=True,
    )

def create_card(create_button, progress_ring):
    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Create Your Playlist", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("This will create a private Spotify playlist with songs from Billboard Hot 100",
                        size=14, color=ft.Colors.ON_SURFACE_VARIANT),
                ft.Row([create_button, progress_ring], alignment=ft.MainAxisAlignment.CENTER),
            ]),
            padding=20,
            expand=True,
        )
    )
