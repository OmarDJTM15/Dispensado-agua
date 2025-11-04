import flet as ft
import threading
import time


class PantallaSplash(ft.Container):
    """Pantalla inicial con logo animado y transición suave."""

    def __init__(self, page: ft.Page, continuar_callback):
        super().__init__()
        self.page = page
        self.continuar_callback = continuar_callback

        # --- Fondo ---
        self.bgcolor = ft.LinearGradient(
            colors=["#0099ff", "#00ccff", "#e0f7fa"],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
        )
        self.expand = True
        self.alignment = ft.alignment.center

        # --- Logo ---
        self.logo = ft.Image(
            src="C:/dispensador_agua/assets/logo.png",  # 🔧 cambia esta ruta si es necesario
            width=220,
            height=220,
            opacity=0.0,
        )

        # --- Texto ---
        self.texto = ft.Text(
            "Osmopurificadora Puebla",
            size=24,
            color="white",
            weight="bold",
            opacity=0.0,
        )

        # --- Contenedor principal ---
        self.content = ft.Column(
            [self.logo, self.texto],
            alignment="center",
            horizontal_alignment="center",
            spacing=15,
        )

        # Inicia la animación al cargar
        threading.Thread(target=self.animar, daemon=True).start()

    def animar(self):
        """Animación de fade-in y transición al menú principal."""
        # Fade in
        for i in range(11):
            self.logo.opacity = i / 10
            self.texto.opacity = i / 10
            self.page.update()
            time.sleep(0.08)

        # Espera unos segundos mostrando el logo
        time.sleep(1.8)

        # Fade out
        for i in range(10, -1, -1):
            self.logo.opacity = i / 10
            self.texto.opacity = i / 10
            self.page.update()
            time.sleep(0.05)

        # Transición a la pantalla principal
        self.continuar_callback()
