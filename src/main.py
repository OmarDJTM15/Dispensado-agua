import flet as ft
import ui.pantalla_principal as PP

def main(page: ft.Page):
    """Punto de entrada principal de la app."""
    page.title = "Dispensador de Agua Inteligente"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.add(PP.PantallaPrincipal(page))

ft.app(target=main)
