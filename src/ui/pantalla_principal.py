import flet as ft
from ui.pantalla_despacho import PantallaDespacho
from ui.pantalla_dashboard import PantallaDashboard
import os

# Ruta estática de tus imágenes
RUTA_ASSETS = r"C:\dispensador_agua\assets"  # 👈 cambia si usas otra ruta


class PantallaPrincipal(ft.Container):
    """Pantalla de selección de cantidad de agua (principal)."""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.bgcolor = ft.LinearGradient(
            colors=["#0099ff", "#00ccff", "#e0f7fa"],
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
        )
        self.alignment = ft.alignment.center

        self.build_ui()

    def build_ui(self):
        # --- Título ---
        titulo = ft.Text(
            "SELECCIONE SU OPCIÓN / SELECT YOUR OPTION",
            size=24,
            weight="bold",
            color="white",
            text_align="center",
        )

        subtitulo = ft.Text(
            "Elija el tipo de llenado que desea\nChoose the type of filling you want",
            size=16,
            color="white",
            text_align="center",
        )

        # --- Opciones de garrafones ---
        opcion_5L = self.crear_opcion(
            img="garrafon_medio.png",
            titulo="5 LITROS",
            subtitulo="HALF BOTTLE",
            precio="$5",
            litros=5,
        )

        opcion_10L = self.crear_opcion(
            img="garrafon_lleno.png",
            titulo="20 LITROS",
            subtitulo="FULL BOTTLE",
            precio="$10",
            litros=20,
        )

        opcion_lavado = self.crear_opcion(
            img="garrafon_lavado.png",
            titulo="LAVADO",
            subtitulo="CLEANING",
            precio="$5",
            litros=0,
        )

        fila_opciones = ft.Row(
            [opcion_5L, opcion_10L, opcion_lavado],
            alignment="center",
            spacing=50,
        )

        # --- Contenedor principal ---
        self.content = ft.Column(
                    [
                        titulo,
                        subtitulo,
                        fila_opciones,
                    ],
                    alignment="center",
                    horizontal_alignment="center",
                    spacing=30,
                )
            # --- Botón administrador ---
        boton_admin = ft.ElevatedButton(
            "🔒 ADMINISTRADOR / ADMIN",
            bgcolor="#004c8c",
            color="white",
            width=250,
            on_click=lambda _: self.ir_a_dashboard(),
        )

        self.content = ft.Column(
            [
                titulo,
                subtitulo,
                fila_opciones,
                ft.Divider(height=30, color="transparent"),
                boton_admin,
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=30,
        )


    # --------------------------------------------------------
    # FUNCIÓN PARA CREAR UNA TARJETA DE OPCIÓN
    # --------------------------------------------------------
    def crear_opcion(self, img, titulo, subtitulo, precio, litros):
        """Crea una tarjeta visual para cada opción."""
        ruta_img = os.path.join(RUTA_ASSETS, img)

        imagen = ft.Image(
            src=ruta_img,
            width=180,
            height=200,
            fit=ft.ImageFit.CONTAIN,
        )

        texto_titulo = ft.Text(titulo, size=20, weight="bold", color="#004c8c")
        texto_subtitulo = ft.Text(subtitulo, size=16, color="#0077c2")
        texto_precio = ft.Text(precio, size=18, color="#004c8c")

        card = ft.Container(
            content=ft.Column(
                [imagen, texto_titulo, texto_subtitulo, texto_precio],
                alignment="center",
                horizontal_alignment="center",
                spacing=5,
            ),
            width=220,
            height=320,
            bgcolor="white",
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=10, color="#00000040"),
            alignment=ft.alignment.center,
            on_click=lambda _: self.ir_a_despacho(litros),
        )

        return card

    # --------------------------------------------------------
    # NAVEGACIÓN HACIA LA PANTALLA DE DESPACHO
    # --------------------------------------------------------
    def ir_a_despacho(self, litros):
        self.page.clean()
        self.page.add(
            PantallaDespacho(
                self.page, litros, regresar_callback=lambda: self.regresar_menu()
            )
        )

    def regresar_menu(self):
        self.page.clean()
        self.page.add(PantallaPrincipal(self.page))
        self.page
        
    def ir_a_dashboard(self):
        self.page.clean()
        self.page.add(PantallaDashboard(self.page, regresar_callback=lambda: self.regresar_menu()))
