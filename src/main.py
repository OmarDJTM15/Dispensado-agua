import flet as ft
from ui.pantalla_splash import PantallaSplash
import ui.pantalla_principal as PP

def main(page: ft.Page):
    """Punto de entrada principal de la app."""
    page.title = "Dispensador de Agua Inteligente"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    def ir_a_principal():
        page.clean()
        page.add(PP.PantallaPrincipal(page))
        
    page.add(PantallaSplash(page, continuar_callback=ir_a_principal))

ft.app(target=main)
