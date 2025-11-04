import flet as ft
import pandas as pd
import os
import plotly.express as px
import plotly.io as pio
import base64
from utils.config import RUTA_CSV, ADMIN_PASSWORD



class PantallaDashboard(ft.Container):
    """Panel administrativo con autenticación y dashboard."""

    def __init__(self, page: ft.Page, regresar_callback):
        super().__init__()
        self.page = page
        self.regresar_callback = regresar_callback
        self.expand = True
        self.bgcolor = ft.LinearGradient(
            colors=["#0099ff", "#00ccff", "#e0f7fa"],
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
        )
        self.alignment = ft.alignment.center

        # Mostrar fondo base inicial
        self.mensaje = ft.Text(
            "🔒 Acceso restringido. Ingrese la contraseña de administrador.",
            size=18,
            color="white",
            text_align="center",
        )
        self.content = ft.Column(
            [self.mensaje],
            alignment="center",
            horizontal_alignment="center",
        )

        # Lanzar el cuadro de diálogo inmediatamente
        self.page.add(self)
        self.page.update()
        self.password_dialog()  # 🔑 se ejecuta de forma síncrona (funciona en Flet 0.22+)

    # ----------------------------------------------------------------------
    # 🔐 Diálogo de contraseña
    # ----------------------------------------------------------------------
    def password_dialog(self):
        """Muestra el cuadro de diálogo para autenticación."""

        password_input = ft.TextField(
            label="Contraseña / Password",
            password=True,
            can_reveal_password=True,
            autofocus=True,
            width=250,
        )

        def verificar_contraseña(e):
            if password_input.value == ADMIN_PASSWORD:
                dlg.open = False
                self.page.update()
                self.build_dashboard()
            else:
                password_input.error_text = "Contraseña incorrecta / Wrong password"
                self.page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("🔒 Acceso administrativo"),
            content=ft.Column(
                [
                    ft.Text("Ingrese la contraseña para acceder al panel."),
                    password_input,
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.regresar_callback()),
                ft.TextButton("Entrar", on_click=verificar_contraseña),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(dlg)
        self.page.update()

    # ----------------------------------------------------------------------
    # 📊 Dashboard
    # ----------------------------------------------------------------------
    def build_dashboard(self):
        """Carga los datos del CSV y muestra las gráficas y métricas."""
        titulo = ft.Text(
            "📊 PANEL ADMINISTRATIVO / DASHBOARD",
            size=26,
            weight="bold",
            color="white",
            text_align="center",
        )

        # --- Leer CSV ---
        if not os.path.exists(RUTA_CSV):
            df = pd.DataFrame(columns=["fecha", "litros", "monto"])
        else:
            df = pd.read_csv(RUTA_CSV)

        if not df.empty:
            df["fecha"] = pd.to_datetime(df["fecha"])
            total_litros = df["litros"].sum()
            total_monto = df["monto"].sum()
            promedio = df["litros"].mean().round(2)

            df["hora"] = df["fecha"].dt.strftime("%H:%M")
            fig = px.bar(
                df,
                x="hora",
                y="litros",
                title="Litros despachados por hora",
                color_discrete_sequence=["#00b0ff"],
            )

            # Convertir a imagen PNG
            img_bytes = pio.to_image(fig, format="png")
            img_b64 = base64.b64encode(img_bytes).decode("utf-8")

            grafica = ft.Image(
                src_base64=img_b64,
                width=700,
                height=400,
                fit=ft.ImageFit.CONTAIN,
            )
        else:
            total_litros, total_monto, promedio = 0, 0, 0
            grafica = ft.Text("📭 No hay datos registrados aún.", color="white")

        # Tarjetas métricas
        tarjetas = ft.Row(
            [
                self.metric_card("💧 Litros totales", f"{total_litros:.1f} L"),
                self.metric_card("💵 Monto total", f"${total_monto:.2f}"),
                self.metric_card("📏 Promedio por llenado", f"{promedio:.1f} L"),
            ],
            alignment="center",
            spacing=30,
        )

        # Botón volver
        boton_volver = ft.ElevatedButton(
            "⬅️ Volver al menú principal",
            width=250,
            bgcolor="#004c8c",
            color="white",
            on_click=lambda _: self.regresar_callback(),
        )

        # Reemplazar contenido principal
        self.content = ft.Column(
            [
                titulo,
                ft.Divider(height=15, color="transparent"),
                tarjetas,
                ft.Divider(height=20, color="transparent"),
                grafica,
                ft.Divider(height=30, color="transparent"),
                boton_volver,
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=20,
        )
        self.page.update()

    # ----------------------------------------------------------------------
    # 📋 Tarjeta de métrica
    # ----------------------------------------------------------------------
    def metric_card(self, titulo, valor):
        """Crea una tarjeta con un valor destacado."""
        return ft.Container(
            width=220,
            height=110,
            bgcolor="white",
            border_radius=15,
            padding=10,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(blur_radius=10, color="#00000040"),
            content=ft.Column(
                [
                    ft.Text(titulo, size=14, color="#0077c2", text_align="center"),
                    ft.Text(valor, size=22, weight="bold", color="#004c8c", text_align="center"),
                ],
                alignment="center",
                horizontal_alignment="center",
            ),
        )
