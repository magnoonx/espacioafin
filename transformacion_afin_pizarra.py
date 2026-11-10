"""
=============================================================================
ANIMACIÓN CON MARCADOR SOBRE PIZARRA BLANCA (WHITEBOARD STYLE)
Curso: Geometría Lineal / Robótica Cinemática y Visión por Computador
=============================================================================
Problema:
Transformación afín f : A³ -> A³ compuesta por:
  - Rotación θ = π/2 alrededor del eje Z
  - Traslación por b = (2, -1, 3)ᵀ

1. Matriz T ∈ Aff(3) ⊂ GL(4, R) en coordenadas homogéneas.
2. Imagen del punto afín P = (1, 2, 4)ᵀ e imagen del vector libre v = (1, 2, 4)ᵀ.
3. Explicación axiomática de la componente homogénea w ∈ {0, 1}.

Características de la animación:
  - Fondo de pizarra blanca moderna (#f8fafc).
  - Marcador de borrado en seco (tinta azul marino y toques en verde/rojo).
  - Trazado en tiempo real con levante de marcador entre trazos.
  - Pausas generosas (3.5s - 4.5s) en cada ecuación clave.
  - 100% libre de dependencias LaTeX (utiliza Text de Manim).

Para compilar:
  python -m manim -pql transformacion_afin_pizarra.py TransformacionAfinPizarra
=============================================================================
"""

from manim import *
import numpy as np


def crear_marcador_pizarra_blanca(color_tinta="#1e3a8a"):
    """
    Construye un marcador de borrado en seco para pizarra blanca:
    punta biselada del color de la tinta, cuerpo blanco/plateado con franja azul y tapa.
    """
    # 1. Punta de fieltro biselada (color de tinta)
    punta = Polygon(
        [-0.03, 0.03, 0], [0.03, -0.03, 0], [-0.10, -0.10, 0],
        fill_color=color_tinta, fill_opacity=1.0, stroke_width=0
    )
    # 2. Soporte negro de la punta
    cuello = Polygon(
        [-0.03, 0.03, 0], [0.05, 0.11, 0], [0.11, 0.05, 0], [0.03, -0.03, 0],
        fill_color="#334155", fill_opacity=1.0, stroke_width=0.5, stroke_color=BLACK
    )
    # 3. Cuerpo blanco cilíndrico del marcador de pizarra
    cuerpo = Polygon(
        [0.05, 0.11, 0], [0.35, 0.71, 0], [0.55, 0.61, 0], [0.11, 0.05, 0],
        fill_color="#f1f5f9", fill_opacity=1.0, stroke_width=0.8, stroke_color="#64748b"
    )
    # 4. Franja identificadora con el color de la tinta
    franja = Polygon(
        [0.15, 0.31, 0], [0.23, 0.47, 0], [0.43, 0.37, 0], [0.35, 0.21, 0],
        fill_color=color_tinta, fill_opacity=1.0, stroke_width=0.5, stroke_color="#475569"
    )
    # 5. Tapa trasera
    tapa = Polygon(
        [0.35, 0.71, 0], [0.43, 0.87, 0], [0.63, 0.77, 0], [0.55, 0.61, 0],
        fill_color=color_tinta, fill_opacity=1.0, stroke_width=0.8, stroke_color=BLACK
    )
    marcador = VGroup(punta, cuello, cuerpo, franja, tapa)
    return marcador


class TransformacionAfinPizarra(Scene):
    def construct(self):
        # 1. Pizarra blanca moderna con contraste suave y elegante
        self.camera.background_color = "#f8fafc"

        # Colores de marcador sobre pizarra blanca
        COLOR_TITULO   = "#0f172a"  # Negro pizarra profundo
        COLOR_TEXTO    = "#1e293b"  # Carbón oscuro
        COLOR_MATRIZ   = "#1d4ed8"  # Azul marcador clásico
        COLOR_PUNTO    = "#b91c1c"  # Rojo marcador para puntos
        COLOR_VECTOR   = "#047857"  # Verde marcador para vectores
        COLOR_RECUADRO = "#0284c7"  # Azul cian para recuadros

        marcador = crear_marcador_pizarra_blanca(color_tinta=COLOR_MATRIZ)

        def trazar(objeto, duracion=2.2, es_figura=False):
            """Mueve el marcador y sigue el trazo en tiempo real."""
            def seguir_trazo(m):
                pts = objeto.get_points()
                if len(pts) > 0:
                    m.move_to(pts[-1], aligned_edge=DL)

            pts_objeto = objeto.get_points()
            if len(pts_objeto) > 0 and marcador in self.mobjects:
                self.play(
                    marcador.animate.move_to(pts_objeto[0], aligned_edge=DL),
                    run_time=0.35,
                    rate_func=smooth
                )

            marcador.add_updater(seguir_trazo)
            if marcador not in self.mobjects:
                self.add(marcador)

            if es_figura:
                self.play(Create(objeto), run_time=duracion, rate_func=linear)
            else:
                self.play(Write(objeto), run_time=duracion, rate_func=linear)

            marcador.remove_updater(seguir_trazo)
            self.play(marcador.animate.shift(UR * 0.25), run_time=0.2)

        # ===================================================================
        # PARTE 1: TÍTULO Y CONSTRUCCIÓN DE LA MATRIZ HOMOGÉNEA T
        # ===================================================================
        titulo = Text("Robótica y Visión: Transformación Afín en A³", font_size=26, color=COLOR_TITULO)
        titulo.to_edge(UP, buff=0.5)

        linea_tit = Line(LEFT * 6.0, RIGHT * 6.0, color="#94a3b8", stroke_width=2.0)
        linea_tit.next_to(titulo, DOWN, buff=0.15)

        self.play(FadeIn(marcador, shift=UR * 0.8), run_time=0.6)
        trazar(titulo, duracion=2.2)
        trazar(linea_tit, duracion=0.9, es_figura=True)
        self.wait(1.0)

        # Datos de la transformación
        txt_datos = Text(
            "Rotación: Rz(π/2) alrededor de Z   |   Traslación: b = (2, -1, 3)ᵀ",
            font_size=19,
            color=COLOR_TEXTO
        ).shift(UP * 1.7)
        trazar(txt_datos, duracion=2.2)
        self.wait(1.0)

        # Panel izquierdo: Rotación y traslación
        txt_sub1 = Text("1. Matriz de Rotación Rz(π/2) y Vector b:", font_size=18, color=COLOR_MATRIZ)
        txt_sub1.to_edge(LEFT, buff=0.8).shift(UP * 0.9)

        r_matrix = Text(
            "Rz(π/2) = [  0  -1   0 ]\n"
            "          [  1   0   0 ]\n"
            "          [  0   0   1 ]",
            font_size=19,
            line_spacing=0.75,
            color=COLOR_TEXTO
        ).next_to(txt_sub1, DOWN, buff=0.25, aligned_edge=LEFT)

        col_izq = VGroup(txt_sub1, r_matrix)
        trazar(txt_sub1, duracion=1.8)
        trazar(r_matrix, duracion=2.5)
        self.wait(1.0)

        # Panel derecho: Matriz homogénea T en Aff(3)
        txt_sub2 = Text("Matriz Homogénea T ∈ Aff(3) ⊂ GL(4, R):", font_size=18, color=COLOR_MATRIZ)
        txt_sub2.to_edge(RIGHT, buff=0.8).shift(UP * 0.9)

        t_matrix = Text(
            "T = [  0  -1   0 |  2 ]\n"
            "    [  1   0   0 | -1 ]\n"
            "    [  0   0   1 |  3 ]\n"
            "    [------------+----]\n"
            "    [  0   0   0 |  1 ]",
            font_size=20,
            line_spacing=0.75,
            color=COLOR_MATRIZ
        ).next_to(txt_sub2, DOWN, buff=0.25, aligned_edge=LEFT)

        box_t = SurroundingRectangle(t_matrix, color=COLOR_RECUADRO, buff=0.2, stroke_width=2.5, corner_radius=0.1)

        trazar(txt_sub2, duracion=2.0)
        trazar(t_matrix, duracion=2.8)
        trazar(box_t, duracion=1.8, es_figura=True)
        # Pausa generosa de 4.5 segundos para asimilar la matriz T
        self.wait(4.5)

        # Limpiar escena para la Parte 2
        self.play(
            FadeOut(txt_datos), FadeOut(col_izq),
            FadeOut(txt_sub2), FadeOut(t_matrix), FadeOut(box_t),
            run_time=1.0
        )
        self.wait(0.5)

        # ===================================================================
        # PARTE 2: IMAGEN DEL PUNTO AFÍN P (w=1) VS VECTOR LIBRE v (w=0)
        # ===================================================================
        txt_sec2 = Text(
            "2. Transformación: Punto Afín P (w = 1)  vs  Vector Libre v (w = 0)",
            font_size=20,
            color=COLOR_TITULO
        ).shift(UP * 1.8)
        trazar(txt_sec2, duracion=2.4)
        self.wait(1.0)

        # Columna Izquierda: Punto P (w=1)
        lbl_p = Text("A) Punto Afín P = (1, 2, 4)ᵀ  ==>  w = 1", font_size=19, color=COLOR_PUNTO)
        calc_p = Text(
            "T · P_hom = [  0  -1   0   2 ] [ 1 ]   [ -2 + 2 ]   [ 0 ]\n"
            "            [  1   0   0  -1 ] [ 2 ] = [  1 - 1 ] = [ 0 ]\n"
            "            [  0   0   1   3 ] [ 4 ]   [  4 + 3 ]   [ 7 ]\n"
            "            [  0   0   0   1 ] [ 1 ]   [    1   ]   [ 1 ]",
            font_size=18,
            line_spacing=0.75,
            color=COLOR_TEXTO
        )
        res_p = Text("==> Imagen: f(P) = (0, 0, 7)ᵀ", font_size=20, color=COLOR_PUNTO)
        box_p = SurroundingRectangle(res_p, color=COLOR_PUNTO, buff=0.18, stroke_width=2.5, corner_radius=0.1)

        grupo_p = VGroup(lbl_p, calc_p, res_p).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        grupo_p.to_edge(LEFT, buff=0.8).shift(DOWN * 0.4)
        box_p.move_to(res_p)

        trazar(lbl_p, duracion=2.0)
        trazar(calc_p, duracion=3.0)
        trazar(res_p, duracion=1.8)
        trazar(box_p, duracion=1.5, es_figura=True)
        # Pausa de 4.0 segundos para el punto P
        self.wait(4.0)

        # Columna Derecha: Vector v (w=0)
        lbl_v = Text("B) Vector Libre v = (1, 2, 4)ᵀ  ==>  w = 0", font_size=19, color=COLOR_VECTOR)
        calc_v = Text(
            "T · v_hom = [  0  -1   0   2 ] [ 1 ]   [ -2 + 0 ]   [ -2 ]\n"
            "            [  1   0   0  -1 ] [ 2 ] = [  1 - 0 ] = [  1 ]\n"
            "            [  0   0   1   3 ] [ 4 ]   [  4 + 0 ]   [  4 ]\n"
            "            [  0   0   0   1 ] [ 0 ]   [    0   ]   [  0 ]",
            font_size=18,
            line_spacing=0.75,
            color=COLOR_TEXTO
        )
        res_v = Text("==> Imagen: f_vec(v) = (-2, 1, 4)ᵀ", font_size=20, color=COLOR_VECTOR)
        box_v = SurroundingRectangle(res_v, color=COLOR_VECTOR, buff=0.18, stroke_width=2.5, corner_radius=0.1)

        grupo_v = VGroup(lbl_v, calc_v, res_v).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        grupo_v.to_edge(RIGHT, buff=0.8).shift(DOWN * 0.4)
        box_v.move_to(res_v)

        trazar(lbl_v, duracion=2.0)
        trazar(calc_v, duracion=3.0)
        trazar(res_v, duracion=1.8)
        trazar(box_v, duracion=1.5, es_figura=True)
        # Pausa de 4.5 segundos para contrastar punto vs vector
        self.wait(4.5)

        # Limpiar escena para la Parte 3
        self.play(
            FadeOut(txt_sec2), FadeOut(grupo_p), FadeOut(box_p),
            FadeOut(grupo_v), FadeOut(box_v),
            run_time=1.0
        )
        self.wait(0.5)

        # ===================================================================
        # PARTE 3: DISTINCIÓN AXIOMÁTICA ENTRE PUNTOS Y VECTORES (w ∈ {0, 1})
        # ===================================================================
        txt_sec3 = Text("3. Justificación Axiomática de la Componente Homogénea w:", font_size=20, color=COLOR_TITULO)
        txt_sec3.shift(UP * 1.8)
        trazar(txt_sec3, duracion=2.4)
        self.wait(1.0)

        ax1 = Text(
            "• Para PUNTOS (w = 1):  T · [ P , 1 ]ᵀ = [ R·P + b·(1) , 1 ]ᵀ\n"
            "  -> La traslación se activa (+b). Los puntos tienen posición fija en el espacio.",
            font_size=18,
            line_spacing=0.7,
            color=COLOR_PUNTO
        )
        ax2 = Text(
            "• Para VECTORES (w = 0): T · [ v , 0 ]ᵀ = [ R·v + b·(0) , 0 ]ᵀ = [ R·v , 0 ]ᵀ\n"
            "  -> La traslación se anula. Un vector libre representa desplazamiento puro, sin origen.",
            font_size=18,
            line_spacing=0.7,
            color=COLOR_VECTOR
        )
        ax3 = Text(
            "• Álgebra afín preservada exactamente:\n"
            "  - Punto - Punto = Vector :  w = 1 - 1 = 0  (diferencia de posiciones es un vector)\n"
            "  - Punto + Vector = Punto  :  w = 1 + 0 = 1  (trasladar un punto da otro punto)\n"
            "  - Vector + Vector = Vector:  w = 0 + 0 = 0  (suma de desplazamientos)\n"
            "  - Punto + Punto = Prohibido: w = 1 + 1 = 2 ∉ {0, 1} (operación no afín)",
            font_size=17,
            line_spacing=0.75,
            color=COLOR_TEXTO
        )

        bloque_ax = VGroup(ax1, ax2, ax3).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        bloque_ax.shift(DOWN * 0.45)
        caja_ax = SurroundingRectangle(bloque_ax, color=COLOR_RECUADRO, buff=0.25, stroke_width=2.5, corner_radius=0.15)

        trazar(ax1, duracion=3.0)
        self.wait(1.5)
        trazar(ax2, duracion=3.0)
        self.wait(1.5)
        trazar(ax3, duracion=3.8)
        trazar(caja_ax, duracion=2.0, es_figura=True)
        # Pausa generosa de 5.0 segundos para leer la justificación axiomática
        self.wait(5.0)

        # -------------------------------------------------------------------
        # RETIRADA DEL MARCADOR Y FINAL
        # -------------------------------------------------------------------
        self.play(FadeOut(marcador, shift=DR * 1.5), run_time=0.8)
        self.wait(3.0)

