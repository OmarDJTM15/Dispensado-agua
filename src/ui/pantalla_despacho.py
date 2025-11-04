import flet as ft
import time
import threading
import random
from utils.config import RUTA_ASSETS
from utils.logger import registrar_despacho



class PantallaDespacho(ft.Container):
    """Pantalla que simula el llenado de agua con animación visual."""

    def __init__(self, page: ft.Page, litros: float, regresar_callback):
        super().__init__()
        self.page = page
        self.litros_total = litros
        self.litros_actual = 0
        self.regresar_callback = regresar_callback
        self.despachando = True

        # --- Fondo tipo agua ---
        self.bgcolor = ft.LinearGradient(
            colors=["#0099ff", "#00ccff", "#e0f7fa"],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
        )
        self.expand = True
        self.alignment = ft.alignment.center

        # --- Stack principal (para gotas animadas y contenido centrado) ---
        self.stack = ft.Stack(expand=True)

        # --- Gotas animadas (dentro del Stack) ---
        self.gotas = []
        for _ in range(8):
            drop = ft.Container(
                content=ft.Icon(
                    ft.Icons.WATER_DROP,
                    color="#ffffff88",
                    size=random.randint(18, 28),
                ),
                top=random.randint(100, 400),
                left=random.randint(50, 600),
            )
            self.gotas.append(drop)

        # --- Texto principal ---
        self.titulo = ft.Text(
            f"DESPACHANDO {self.litros_total} LITROS\nDISPENSING {self.litros_total} LITERS",
            size=22,
            weight="bold",
            text_align="center",
            color="white",
        )

        # --- Progreso ---
        self.progreso = ft.ProgressBar(
            width=400, height=25, bgcolor="#ffffff55", color="#00b0ff"
        )
        self.texto_estado = ft.Text("Iniciando despacho...", size=18, color="white")

        # --- Imagen del garrafón (usa page.assets_dir para mostrarla correctamente) ---
        self.garrafon_img = ft.Image(
            src=ft.Image(src=f"{RUTA_ASSETS}\\garrafon_lleno.png"),
            width=240,
            height=260,
            fit=ft.ImageFit.CONTAIN,
        )

        # --- Botón cancelar ---
        self.boton_cancelar = ft.ElevatedButton(
            "⏹️ CANCELAR",
            bgcolor="#ef5350",
            color="white",
            width=200,
            on_click=lambda _: self.cancelar(),
        )

        # --- Contenedor central ---
        self.columna_central = ft.Column(
            [
                self.titulo,
                self.garrafon_img,
                self.progreso,
                self.texto_estado,
                self.boton_cancelar,
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=25,
        )

        # --- Centrar toda la columna en pantalla ---
        self.contenedor_central = ft.Container(
            content=self.columna_central,
            alignment=ft.alignment.center,
            expand=True,
        )

        # --- Armar estructura del Stack ---
        self.stack.controls = [*self.gotas, self.contenedor_central]
        self.content = self.stack

        # Iniciar animaciones
        threading.Thread(target=self.iniciar_animaciones, daemon=True).start()

    def iniciar_animaciones(self):
        """Retraso inicial para asegurar que la UI se haya renderizado."""
        time.sleep(1)
        threading.Thread(target=self.simular_despacho, daemon=True).start()
        threading.Thread(target=self.animar_gotas, daemon=True).start()

    def cancelar(self):
        self.despachando = False
        self.regresar_callback()

    def simular_despacho(self):
        snackbar = ft.SnackBar(
                        content=ft.Text(
                            "✅ Registro guardado correctamente / Record saved successfully",
                            color="white"
                        ),
                        bgcolor="#004c8c",
                        duration=2000,  # milisegundos (2 segundos)
                        show_close_icon=True,
                        open=True,
                    )
        """Simula el llenado del garrafón."""
        while self.litros_actual < self.litros_total and self.despachando:
            time.sleep(0.3)
            self.litros_actual += 0.5
            progreso = self.litros_actual / self.litros_total
            self.progreso.value = progreso
            self.texto_estado.value = (
                f"Despachando... {self.litros_actual:.1f} L / {self.litros_total} L"
            )
            self.page.update()

        if self.despachando:
            self.texto_estado.value = "✅ Llenado completo / Filling complete"
            self.page.update()

            # 💾 Registrar datos según el tipo de acción
            if self.litros_total == 0:
                # Modo lavado (no hay litros pero sí costo de servicio)
                registrar_despacho(0, 5)
            else:
                # Modo llenado normal
                precio_por_litro = 0.5
                monto = self.litros_total * precio_por_litro
                registrar_despacho(self.litros_total, monto)

            # ✅ Mostrar notificación visual (toast)
            snackbar = ft.SnackBar(
                content=ft.Text(
                    "✅ Registro guardado correctamente / Record saved successfully",
                    color="white"
                ),
                bgcolor="#004c8c",
                duration=2000,
                show_close_icon=True,
                open=True,
            )

            # Agregar y actualizar
            self.page.overlay.append(snackbar)
            self.page.update()

            time.sleep(1.5)
            self.regresar_callback()

            time.sleep(1.5)
            self.regresar_callback()

    def animar_gotas(self):
        """Efecto de gotas que caen mientras se llena."""
        while self.despachando:
            for drop in self.gotas:
                drop.top += 8
                if drop.top > 500:
                    drop.top = random.randint(50, 150)
                    drop.left = random.randint(50, 600)
            self.page.update()
            time.sleep(0.05)
