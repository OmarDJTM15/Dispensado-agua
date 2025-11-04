import flet as ft

class PantallaPrincipal(ft.Column):
    """Pantalla inicial de selección de cantidad de agua."""
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.alignment = "center"
        self.horizontal_alignment = "center"
        self.spacing = 25
        self.build_ui()

    def build_ui(self):
        self.logo = ft.Image(src="../assets/logo.png", width=120, height=120)
        self.titulo = ft.Text(
            "SELECT YOUR WATER AMOUNT\nSELECCIONE LA CANTIDAD DE AGUA",
            size=22,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
            color="white"
        )

        self.boton_5 = ft.ElevatedButton("5 L / $5", width=200)
        self.boton_10 = ft.ElevatedButton("10 L / $10", width=200)
        self.boton_20 = ft.ElevatedButton("20 L / $20", width=200)

        self.controls = [
            self.logo,
            self.titulo,
            ft.Row([self.boton_5, self.boton_10, self.boton_20], alignment="center")
        ]
