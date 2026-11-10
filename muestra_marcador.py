"""
=============================================================================
MUESTRA: ESCRITURA EN PIZARRA CON MARCADOR ANIMADO EN TIEMPO REAL
Curso: Geometría Lineal / Geometría Afín
=============================================================================
Este script demuestra la simulación completa de escritura a mano:
  - Fondo de pizarra escolar verde oscura (#182c1f).
  - Marcador vectorial realista (punta blanca, cuerpo amarillo, tapa).
  - El marcador sigue la punta del trazo milimétricamente en cada fotograma.
  - El marcador se "levanta" de la pizarra entre palabras y traza recuadros.
  - 100% libre de errores de LaTeX (utiliza Text de Manim).

Para compilar y ver el resultado:
  python -m manim -pql muestra_marcador.py EscrituraConMarcador
=============================================================================
"""

from manim import *
import numpy as np


def crear_marcador():
    """
    Construye un marcador vectorial realista orientado a 45 grados,
    con su punta de escritura en el vértice inferior izquierdo.
    """
    # 1. Punta de fieltro biselada (blanca/tiza)
    punta = Polygon(
        [-0.03, 0.03, 0], [0.03, -0.03, 0], [-0.10, -0.10, 0],
        fill_color=WHITE, fill_opacity=1.0, stroke_width=0
    )
    # 2. Cuello / soporte de la punta
    cuello = Polygon(
        [-0.03, 0.03, 0], [0.05, 0.11, 0], [0.11, 0.05, 0], [0.03, -0.03, 0],
        fill_color=DARK_GRAY, fill_opacity=1.0, stroke_width=0.5, stroke_color=BLACK
    )
    # 3. Cuerpo cilíndrico del marcador (inclinado a 45°)
    cuerpo = Polygon(
        [0.05, 0.11, 0], [0.35, 0.71, 0], [0.55, 0.61, 0], [0.11, 0.05, 0],
        fill_color=YELLOW_D, fill_opacity=1.0, stroke_width=0.8, stroke_color=DARK_GRAY
    )
    # 4. Franja de marca en el cuerpo
    franja = Polygon(
        [0.15, 0.31, 0], [0.23, 0.47, 0], [0.43, 0.37, 0], [0.35, 0.21, 0],
        fill_color=RED_C, fill_opacity=1.0, stroke_width=0.5, stroke_color=BLACK
    )
    # 5. Tapa trasera
    tapa = Polygon(
        [0.35, 0.71, 0], [0.43, 0.87, 0], [0.63, 0.77, 0], [0.55, 0.61, 0],
        fill_color=GRAY_D, fill_opacity=1.0, stroke_width=0.8, stroke_color=BLACK
    )
    marcador = VGroup(punta, cuello, cuerpo, franja, tapa)
    return marcador


class EscrituraConMarcador(Scene):
    def construct(self):
        # 1. Fondo de pizarra verde escolar tradicional
        self.camera.background_color = "#162a1d"

        # 2. Instanciamos el marcador
        marcador = crear_marcador()
        marcador.shift(DOWN * 4)  # Empieza fuera de pantalla

        def trazar(objeto, duracion=2.5, es_figura=False):
            """
            Función auxiliar que mueve el marcador al inicio del objeto,
            lo hace seguir cada curva Bézier en tiempo real y luego levanta la punta.
            """
            # Función para que el marcador siga la punta del trazo
            def seguir_trazo(m):
                pts = objeto.get_points()
                if len(pts) > 0:
                    # Posiciona la punta del marcador (esquina inferior izquierda) en el trazo
                    m.move_to(pts[-1], aligned_edge=DL)

            # Acercamos el marcador al inicio del trazo si es visible
            pts_objeto = objeto.get_points()
            if len(pts_objeto) > 0 and marcador in self.mobjects:
                self.play(
                    marcador.animate.move_to(pts_objeto[0], aligned_edge=DL),
                    run_time=0.35,
                    rate_func=smooth
                )

            # Activamos el seguimiento continuo por fotograma
            marcador.add_updater(seguir_trazo)
            if marcador not in self.mobjects:
                self.add(marcador)

            # Animamos el trazo (escribir texto o crear contorno geométrico)
            if es_figura:
                self.play(Create(objeto), run_time=duracion, rate_func=linear)
            else:
                self.play(Write(objeto), run_time=duracion, rate_func=linear)

            # Desactivamos el updater y "levantamos" el marcador ligeramente
            marcador.remove_updater(seguir_trazo)
            self.play(marcador.animate.shift(UR * 0.25), run_time=0.2)

        # -------------------------------------------------------------------
        # ANIMACIÓN 1: El marcador entra y escribe el título
        # -------------------------------------------------------------------
        titulo = Text("Geometría Afín: Ecuación y Pertenencia", font_size=28, color=YELLOW_A)
        titulo.to_edge(UP, buff=0.55)

        linea_sub = Line(LEFT * 5.6, RIGHT * 5.6, color=GREEN_D, stroke_width=2)
        linea_sub.next_to(titulo, DOWN, buff=0.15)

        # Entrada del marcador a la pizarra
        self.play(FadeIn(marcador, shift=UR * 0.8), run_time=0.6)
        trazar(titulo, duracion=2.4)
        trazar(linea_sub, duracion=1.0, es_figura=True)
        self.wait(0.8)

        # -------------------------------------------------------------------
        # ANIMACIÓN 2: Puntos dados
        # -------------------------------------------------------------------
        txt_puntos = Text(
            "Puntos dados:  P₀(1, 2, 0),   P₁(3, 2, 1),   P₂(0, 4, 1)",
            font_size=21,
            color=WHITE
        ).shift(UP * 1.5)

        trazar(txt_puntos, duracion=2.5)
        self.wait(1.0)

        # -------------------------------------------------------------------
        # ANIMACIÓN 3: Ecuación implícita de Pi y recuadro dibujado con marcador
        # -------------------------------------------------------------------
        eq_plano = Text(
            "Π:  2x + 3y - 4z - 8 = 0",
            font_size=28,
            color=YELLOW_C
        ).shift(UP * 0.3)

        caja_eq = SurroundingRectangle(
            eq_plano,
            color=YELLOW_C,
            buff=0.25,
            stroke_width=2.5,
            corner_radius=0.1
        )

        trazar(eq_plano, duracion=2.2)
        # El marcador recorre todo el perímetro del recuadro
        trazar(caja_eq, duracion=1.8, es_figura=True)
        self.wait(1.5)

        # -------------------------------------------------------------------
        # ANIMACIÓN 4: Comprobación del punto Q
        # -------------------------------------------------------------------
        sust_txt = Text(
            "Evaluando Q(4, 4, 3):   2(4) + 3(4) - 4(3) - 8 = 0",
            font_size=21,
            color=WHITE
        ).next_to(caja_eq, DOWN, buff=0.6)

        trazar(sust_txt, duracion=2.6)
        self.wait(0.8)

        # Conclusión final destacada
        concl_txt = Text(
            "✓ 0 = 0  ==>  Q ∈ Π  (Pertenencia confirmada)",
            font_size=23,
            color=GREEN_B
        ).next_to(sust_txt, DOWN, buff=0.45)

        trazar(concl_txt, duracion=2.2)

        # -------------------------------------------------------------------
        # SALIDA DEL MARCADOR
        # -------------------------------------------------------------------
        self.play(FadeOut(marcador, shift=DR * 1.5), run_time=0.8)

        # Pausa final para apreciar la pizarra completa
        self.wait(3.5)
