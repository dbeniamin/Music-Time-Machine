import flet as ft
from .components import status_card, creds_card, create_card

def build_layout(app):
    date_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Select Date", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Choose a date to get Billboard Hot 100", size=14,
                        color=ft.Colors.ON_SURFACE_VARIANT),
                ft.Text("YYYY-MM-DD format", size=14,
                        color=ft.Colors.ON_SURFACE_VARIANT),
                app.date_field,
            ]),
            padding=20,
            expand=True,
        )
    )

    return ft.Container(
        content=ft.Column([
            date_card,
            ft.Container(creds_card(app.creds_status, app.config_button), expand=True),  # wrap with expand
            ft.Container(create_card(app.create_button, app.progress_ring), expand=True),
            ft.Container(status_card(app.status_column), expand=True),
        ],
            spacing=20,
            # alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        ),
        padding=20,
        expand=True,
    )
