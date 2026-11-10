"""
=============================================================================
MUESTRA INDEPENDIENTE: ESTILO PIZARRA Y TRAZO A MANO (DOODLE STYLE)
Curso: Geometría Lineal / Geometría Afín
=============================================================================
Archivo de muestra completamente independiente (no modifica nada del proyecto).
Características demostradas:
  1. Fondo de pizarra verde académica (#1a3323).
  2. Marcador/tiza animado que sigue el trazo en tiempo real al escribir.
  3. Formas geométricas con trazo imperfecto/boceto a mano alzada (estilo doodle).
  4. 100% libre de dependencias LaTeX (utiliza fuentes del sistema con Text).

Para ejecutar y visualizar esta muestra:
  python -m manim -pql muestra_doodle_pizarra.py MuestraDoodlePizarra
=============================================================================
"""

from manim import *
import numpy as np


def crear_marcador():
    """
    Construye un marcador vectorial con punta, cuerpo cilíndrico y tapa,
    orientado naturalmente a ~45 grados.
    """
    # Punta de fieltro/tiza blanca
    punta = Polygon(
        [-0.04, 0.04, 0], [0.04, -0.04, 0], [-0.12, -0.12, 0],
        fill_color=WHITE, fill_opacity=1.0, stroke_width=0
    )
    # Cuerpo del marcador (color llamativo)
    cuerpo = Polygon(
        [-0.04, 0.04, 0], [0.20, 0.60, 0], [0.42, 0.48, 0], [0.04, -0.04, 0],
        fill_color=YELLOW_D, fill_opacity=0.95, stroke_width=1.0, stroke_color=DARK_GRAY
    )
    # Tapa superior
    tapa = Polygon(
        [0.20, 0.60, 0], [0.28, 0.74, 0], [0.50, 0.62, 0], [0.42, 0.48, 0],
        fill_color=GRAY_D, fill_opacity=1.0, stroke_width=1.0, stroke_color=BLACK
    )
    marcador = VGroup(punta, cuerpo, tapa)
    return marcador


def animar_con_marcador(scene, target, marcador, run_time=2.2, es_trazo_linea=False):
    """
    Vincula dinámicamente la punta del marcador al último vértice
    dibujado en cada fotograma.
    """
    def seguir_punta(m):
        puntos = target.get_points()
        if len(puntos) > 0:
            m.move_to(puntos[-1], aligned_edge=DL)

    marcador.add_updater(seguir_punta)
    scene.add(marcador)

    if es_trazo_linea:
        scene.play(Create(target), run_time=run_time, rate_func=linear)
    else:
        scene.play(Write(target), run_time=run_time, rate_func=linear)

    marcador.remove_updater(seguir_punta)


def aplicar_estilo_doodle(mobject, subdivisiones=25, factor_ruido=0.035):
    """
    Subdivide las aristas rectas e introduce una perturbación aleatoria suave
    para simular el pulso humano de mano alzada (estilo Excalidraw / Doodle).
    """
    mobject.insert_n_curves(subdivisiones)
    puntos = mobject.get_points()
    ruido = np.random.normal(0, factor_ruido, puntos.shape)
    ruido[:, 2] = 0.0  # Mantener estrictamente en el plano XY
    mobject.set_points(puntos + ruido)
    return mobject


class MuestraDoodlePizarra(Scene):
    def construct(self):
        # 1. Configurar color de pizarra verde escolar tradicional
        self.camera.background_color = "#162b1e"

        marcador = crear_marcador()

        # 2. Título escrito a mano con el marcador
        titulo = Text("Demostración: Estilo Pizarra y Boceto a Mano", font_size=26, color=YELLOW_A)
        titulo.to_edge(UP, buff=0.45)
        linea_titulo = Line(LEFT * 5.8, RIGHT * 5.8, color=GREEN_E, stroke_width=1.5)
        aplicar_estilo_doodle(linea_titulo, subdivisiones=20, factor_ruido=0.03)
        linea_titulo.next_to(titulo, DOWN, buff=0.15)

        self.play(FadeIn(marcador, shift=DR * 0.5), run_time=0.8)
        animar_con_marcador(self, titulo, marcador, run_time=2.2)
        animar_con_marcador(self, linea_titulo, marcador, run_time=1.0, es_trazo_linea=True)
        self.wait(1.0)

        # 3. Dibujar triángulo afín {P0, P1, P2} con estilo boceto (doodle)
        pt_p0 = np.array([-4.0, -0.6, 0])
        pt_p1 = np.array([-1.0, -0.6, 0])
        pt_p2 = np.array([-2.5, 1.8, 0])

        triangulo_base = Polygon(
            pt_p0, pt_p1, pt_p2,
            stroke_color=TEAL_C,
            stroke_width=3.5,
            fill_color=TEAL_E,
            fill_opacity=0.25
        )
        aplicar_estilo_doodle(triangulo_base, subdivisiones=30, factor_ruido=0.04)

        lbl_tri = Text("Símplice {P₀, P₁, P₂}", font_size=18, color=TEAL_B).next_to(pt_p2, UP, buff=0.15)
        lbl_p0 = Text("P₀", font_size=18, color=WHITE).next_to(pt_p0, DOWN + LEFT, buff=0.1)
        lbl_p1 = Text("P₁", font_size=18, color=WHITE).next_to(pt_p1, DOWN + RIGHT, buff=0.1)
        lbl_p2 = Text("P₂", font_size=18, color=WHITE).next_to(pt_p2, LEFT, buff=0.1)

        animar_con_marcador(self, triangulo_base, marcador, run_time=2.5, es_trazo_linea=True)
        self.play(Write(lbl_p0), Write(lbl_p1), Write(lbl_p2), Write(lbl_tri), run_time=1.2)
        self.wait(1.2)

        # 4. Punto exterior Q(4, 4, 3) con coordenadas baricéntricas
        pt_q = np.array([-0.3, -2.0, 0])
        dot_q = Dot(pt_q, radius=0.09, color=YELLOW_B)
        lbl_q = Text("Q(4, 4, 3)", font_size=19, color=YELLOW_B).next_to(dot_q, RIGHT, buff=0.15)
        nota_q = Text("λ₀ = -2 < 0 (Exterior)", font_size=15, color=ORANGE).next_to(lbl_q, DOWN, buff=0.1)

        self.play(FadeIn(dot_q), run_time=0.6)
        animar_con_marcador(self, lbl_q, marcador, run_time=1.4)
        self.play(FadeIn(nota_q), run_time=0.8)
        self.wait(1.0)

        # 5. Panel derecho: Ecuación implícita enmarcada con trazo a mano alzada
        txt_plano_lbl = Text("Ecuación Implícita del Plano:", font_size=20, color=YELLOW_C)
        txt_plano_lbl.move_to(np.array([2.8, 1.2, 0]))

        eq_plano = Text("Π: 2x + 3y - 4z - 8 = 0", font_size=23, color=WHITE)
        eq_plano.next_to(txt_plano_lbl, DOWN, buff=0.3)

        # Caja rectangular imperfecta a mano alzada (estilo boceto)
        caja_doodle = Rectangle(width=5.0, height=1.3, stroke_color=YELLOW_C, stroke_width=3.0)
        caja_doodle.move_to(eq_plano)
        aplicar_estilo_doodle(caja_doodle, subdivisiones=32, factor_ruido=0.038)

        animar_con_marcador(self, txt_plano_lbl, marcador, run_time=1.8)
        animar_con_marcador(self, eq_plano, marcador, run_time=2.2)
        animar_con_marcador(self, caja_doodle, marcador, run_time=1.8, es_trazo_linea=True)
        self.wait(1.2)

        # 6. Flecha y conclusión trazada a mano
        concl_txt = Text("✓ Pertenencia comprobada: 0 = 0", font_size=18, color=GREEN_B)
        concl_txt.next_to(caja_doodle, DOWN, buff=0.55)

        flecha_mano = Arrow(
            start=concl_txt.get_left() + LEFT * 0.2,
            end=pt_q + RIGHT * 1.8,
            color=GREEN_C,
            stroke_width=2.5,
            tip_length=0.2
        )
        aplicar_estilo_doodle(flecha_mano, subdivisiones=15, factor_ruido=0.03)

        animar_con_marcador(self, concl_txt, marcador, run_time=1.8)
        self.play(Create(flecha_mano), run_time=1.2)

        # 7. Retirar el marcador elegantemente
        self.play(FadeOut(marcador, shift=DR * 0.8), run_time=0.8)

        # Pausa final para contemplar el resultado
        self.wait(4.0)

