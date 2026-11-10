"""
=============================================================================
ANIMACIÓN MANIM CE: RESOLUCIÓN COMPLETA DE PROBLEMA DE ESPACIOS AFINES
Curso: Geometría Lineal / Geometría Afín y Proyectiva
=============================================================================

Problema:
En el espacio afín tridimensional A^3(R), se consideran los puntos no colineales:
    P0 = (1, 2, 0),   P1 = (3, 2, 1),   P2 = (0, 4, 1)

1. Determine las ecuaciones paramétricas e implícitas del plano afín Pi
   que contiene a {P0, P1, P2}.
2. Verifique si el punto Q = (4, 4, 3) pertenece al plano Pi.
3. En caso afirmativo, calcule las coordenadas afines de Q respecto al marco
   afín {P0; v1, v2} y determine sus coordenadas baricéntricas con respecto
   al símplice de referencia {P0, P1, P2}.

-----------------------------------------------------------------------------
AJUSTES:
  - 3 segundos de pausa garantizados después de cada ecuación y resultado clave.
  - Corrección de recuadros (SurroundingRectangle) para enmarcar con precisión
    milimétrica cada resultado sin desalineaciones.
-----------------------------------------------------------------------------
"""

from manim import *
import numpy as np

# =============================================================================
# CONFIGURACIÓN GLOBAL DE VELOCIDAD
# =============================================================================
FACTOR_DURACION = 1.0


class BaseEscena(Scene):
    """Escena base que escala automáticamente la velocidad de todas las animaciones."""
    def play(self, *args, **kwargs):
        if "run_time" in kwargs:
            kwargs["run_time"] *= FACTOR_DURACION
        else:
            kwargs["run_time"] = 1.0 * FACTOR_DURACION
        super().play(*args, **kwargs)

    def wait(self, duration=1.0, **kwargs):
        super().wait(duration * FACTOR_DURACION, **kwargs)


# ---------------------------------------------------------------------------
# ESCENA 1: Presentación del Problema y No Colinealidad
# ---------------------------------------------------------------------------
class Escena1_Enunciado(BaseEscena):
    def construct(self):
        # Encabezado
        badge = Tex(r"\textbf{GEOMETRÍA LINEAL} $\cdot$ Espacios Afines", font_size=20, color=BLUE_C)
        badge.to_corner(UL, buff=0.4)

        titulo = Title(
            r"Plano Afín en $\mathbb{A}^3(\mathbb{R})$: Ecuaciones y Coordenadas",
            font_size=34,
            color=BLUE_B
        )
        self.play(FadeIn(badge), Write(titulo))
        self.wait(0.5)

        # Contenido del enunciado
        txt_intro = Text(
            "Sean los puntos dados en el espacio afín tridimensional:",
            font_size=22,
            color=YELLOW_C
        )
        formula_puntos = MathTex(
            r"P_0 = (1, 2, 0), \quad P_1 = (3, 2, 1), \quad P_2 = (0, 4, 1)",
            font_size=30,
            color=WHITE
        )
        enunciado_content = VGroup(txt_intro, formula_puntos).arrange(DOWN, buff=0.25)
        enunciado_box = SurroundingRectangle(
            enunciado_content,
            color=BLUE_D,
            buff=0.35,
            stroke_width=2.0,
            corner_radius=0.15
        )
        grupo_enun = VGroup(enunciado_content, enunciado_box).shift(UP * 0.9)

        self.play(Create(enunciado_box), FadeIn(enunciado_content, shift=UP * 0.2))
        self.wait(1.5)

        # Deducción de vectores directores
        sub_vec = Text("1. Subespacio director del plano afín:", font_size=22, color=GREEN_C)

        v1_tex = MathTex(
            r"v_1 = \vec{P_0 P_1} = P_1 - P_0 = (3-1, \, 2-2, \, 1-0) = (2, 0, 1)",
            font_size=25,
            color=TEAL_C
        )
        v2_tex = MathTex(
            r"v_2 = \vec{P_0 P_2} = P_2 - P_0 = (0-1, \, 4-2, \, 1-0) = (-1, 2, 1)",
            font_size=25,
            color=ORANGE
        )

        indep_tex = MathTex(
            r"\operatorname{rg}\begin{pmatrix} 2 & 0 & 1 \\ -1 & 2 & 1 \end{pmatrix} = 2"
            r"\implies \{v_1, v_2\} \text{ son linealmente independientes}",
            font_size=25,
            color=YELLOW_B
        )
        conclusion_colineal = Tex(
            r"Por tanto, $\{P_0, P_1, P_2\}$ son no colineales y determinan de forma única un plano afín $\Pi$.",
            font_size=22,
            color=GRAY_A
        )

        grupo_vectores = VGroup(
            sub_vec, v1_tex, v2_tex, indep_tex, conclusion_colineal
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(grupo_enun, DOWN, buff=0.35).align_to(grupo_enun, LEFT)

        self.play(FadeIn(sub_vec))
        self.play(Write(v1_tex))
        self.play(Write(v2_tex))
        self.play(Write(indep_tex))
        self.play(FadeIn(conclusion_colineal))
        # Pausa de 3 segundos tras calcular los vectores e independencia afín
        self.wait(3.0)

        self.play(FadeOut(Group(*self.mobjects)))


# ---------------------------------------------------------------------------
# ESCENA 2: Ecuaciones Paramétricas e Implícitas
# ---------------------------------------------------------------------------
class Escena2_EcuacionesPlano(BaseEscena):
    def construct(self):
        titulo = Title(
            r"1. Ecuaciones del Plano Afín $\Pi = P_0 + \langle v_1, v_2 \rangle$",
            font_size=32,
            color=BLUE_B
        )
        self.play(Write(titulo))

        # Panel Izquierdo: Paramétricas (se posiciona antes de crear el recuadro)
        lbl_param = Text("Ecuaciones Paramétricas", font_size=21, color=YELLOW_C)
        def_param = MathTex(
            r"X = P_0 + \lambda v_1 + \mu v_2, \quad (\lambda, \mu \in \mathbb{R})",
            font_size=23
        )
        vec_param = MathTex(
            r"\begin{pmatrix} x \\ y \\ z \end{pmatrix} ="
            r"\begin{pmatrix} 1 \\ 2 \\ 0 \end{pmatrix} +"
            r"\lambda \begin{pmatrix} 2 \\ 0 \\ 1 \end{pmatrix} +"
            r"\mu \begin{pmatrix} -1 \\ 2 \\ 1 \end{pmatrix}",
            font_size=23,
            color=TEAL_B
        )
        sis_param = MathTex(
            r"\Pi:\ \begin{cases}"
            r"x = 1 + 2\lambda - \mu \\"
            r"y = 2 + 2\mu \\"
            r"z = \lambda + \mu"
            r"\end{cases}",
            font_size=26,
            color=WHITE
        )

        col_izq = VGroup(
            lbl_param, def_param, vec_param, sis_param
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(LEFT, buff=0.8).shift(DOWN * 0.25)

        # Recuadro creado exactamente sobre sis_param ya posicionado
        box_param = SurroundingRectangle(sis_param, color=GREEN_C, buff=0.18, stroke_width=2.5)

        # Panel Derecho: Implícita (se posiciona antes de crear el recuadro)
        lbl_imp = Text("Ecuación Implícita / Cartesiana", font_size=21, color=YELLOW_C)
        def_imp = MathTex(
            r"\operatorname{rg}\begin{pmatrix} x-1 & y-2 & z \\ 2 & 0 & 1 \\ -1 & 2 & 1 \end{pmatrix} = 2"
            r"\iff \det(\dots) = 0",
            font_size=21
        )
        det_imp = MathTex(
            r"\begin{vmatrix}"
            r"x-1 & y-2 & z \\"
            r"2 & 0 & 1 \\"
            r"-1 & 2 & 1"
            r"\end{vmatrix} = 0",
            font_size=24,
            color=ORANGE
        )
        desarr_det = MathTex(
            r"-2(x-1) - 3(y-2) + 4z &= 0 \\"
            r"-2x - 3y + 4z + 8 &= 0",
            font_size=23
        )
        eq_final = MathTex(
            r"\Pi:\ 2x + 3y - 4z - 8 = 0",
            font_size=26,
            color=YELLOW_C
        )

        col_der = VGroup(
            lbl_imp, def_imp, det_imp, desarr_det, eq_final
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.25)

        # Recuadro creado exactamente sobre eq_final ya posicionado
        box_imp = SurroundingRectangle(eq_final, color=YELLOW_C, buff=0.18, stroke_width=2.5)

        # Divisor vertical
        linea_div = DashedLine(UP * 2.3, DOWN * 3.2, color=GRAY_D)

        # Animación Izquierda (Paramétricas)
        self.play(FadeIn(lbl_param), Write(def_param))
        self.play(Write(vec_param))
        self.play(Write(sis_param))
        self.play(Create(box_param))
        # Pausa de 3 segundos tras mostrar las ecuaciones paramétricas
        self.wait(3.0)

        self.play(Create(linea_div))

        # Animación Derecha (Implícita)
        self.play(FadeIn(lbl_imp), Write(def_imp))
        self.play(Write(det_imp))
        self.play(Write(desarr_det))
        self.play(Write(eq_final))
        self.play(Create(box_imp))
        # Pausa de 3 segundos tras mostrar la ecuación implícita
        self.wait(3.0)

        self.play(FadeOut(Group(*self.mobjects)))


# ---------------------------------------------------------------------------
# ESCENA 3: Pertenencia del Punto Q
# ---------------------------------------------------------------------------
class Escena3_PertenenciaQ(BaseEscena):
    def construct(self):
        titulo = Title(
            r"2. Verificación de Pertenencia del Punto $Q = (4, 4, 3)$",
            font_size=32,
            color=BLUE_B
        )
        self.play(Write(titulo))

        txt_criterio = Text(
            "Un punto pertenece al plano afín si satisface su ecuación implícita:",
            font_size=22,
            color=GRAY_B
        ).shift(UP * 2.0)

        eq_plano = MathTex(
            r"\Pi:\quad 2x + 3y - 4z - 8 = 0",
            font_size=28,
            color=BLUE_C
        ).next_to(txt_criterio, DOWN, buff=0.35)

        self.play(FadeIn(txt_criterio), Write(eq_plano))
        self.wait(1.0)

        eval_tex = MathTex(
            r"\text{Sustituyendo } x=4,\; y=4,\; z=3:",
            font_size=24,
            color=YELLOW_C
        ).next_to(eq_plano, DOWN, buff=0.5)

        calc_pasos = MathTex(
            r"2(4) + 3(4) - 4(3) - 8 &= 8 + 12 - 12 - 8 \\"
            r"&= 20 - 20 \\"
            r"&= 0",
            font_size=28,
            color=WHITE
        ).next_to(eval_tex, DOWN, buff=0.35)

        self.play(Write(eval_tex))
        self.play(Write(calc_pasos))
        self.wait(1.5)

        concl_tex = MathTex(
            r"0 = 0 \quad \Longrightarrow \quad Q = (4, 4, 3) \in \Pi \quad \text{\textbf{(Afirmativo)}}",
            font_size=28,
            color=GREEN_C
        ).next_to(calc_pasos, DOWN, buff=0.6)

        # Recuadro ajustado perfectamente sobre concl_tex
        box_conc = SurroundingRectangle(concl_tex, color=GREEN_C, buff=0.22, stroke_width=2.5, corner_radius=0.12)

        self.play(Write(concl_tex), Create(box_conc))
        self.play(Indicate(concl_tex, color=GREEN_A))
        # Pausa de 3 segundos tras verificar la pertenencia
        self.wait(3.0)

        self.play(FadeOut(Group(*self.mobjects)))


# ---------------------------------------------------------------------------
# ESCENA 4: Coordenadas Afines y Baricéntricas
# ---------------------------------------------------------------------------
class Escena4_Coordenadas(BaseEscena):
    def construct(self):
        titulo = Title(
            r"3. Coordenadas Afines y Baricéntricas de $Q$",
            font_size=32,
            color=BLUE_B
        )
        self.play(Write(titulo))

        # 3.1 Marco Afín
        sec1 = Text("3.1 Marco afín de referencia {P0; v1, v2}:", font_size=21, color=YELLOW_C)
        sec1.to_edge(LEFT, buff=0.8).shift(UP * 2.2)

        p0q_tex = MathTex(
            r"\vec{P_0 Q} = Q - P_0 = (4-1, \, 4-2, \, 3-0) = (3, 2, 3)",
            font_size=24,
            color=TEAL_C
        ).next_to(sec1, DOWN, buff=0.2, aligned_edge=LEFT)

        sis_afin = MathTex(
            r"\alpha_1 v_1 + \alpha_2 v_2 = \vec{P_0 Q} \iff "
            r"\alpha_1 \begin{pmatrix} 2 \\ 0 \\ 1 \end{pmatrix} + "
            r"\alpha_2 \begin{pmatrix} -1 \\ 2 \\ 1 \end{pmatrix} = "
            r"\begin{pmatrix} 3 \\ 2 \\ 3 \end{pmatrix}",
            font_size=23
        ).next_to(p0q_tex, DOWN, buff=0.2, aligned_edge=LEFT)

        sol_afin = MathTex(
            r"\begin{cases}"
            r"2\alpha_1 - \alpha_2 = 3 \\"
            r"2\alpha_2 = 2 \implies \boldsymbol{\alpha_2 = 1} \\"
            r"\alpha_1 + \alpha_2 = 3 \implies \boldsymbol{\alpha_1 = 2}"
            r"\end{cases}"
            r"\quad \Longrightarrow \quad [Q]_{\{P_0; v_1, v_2\}} = (2, 1)",
            font_size=24,
            color=GREEN_C
        ).next_to(sis_afin, DOWN, buff=0.2, aligned_edge=LEFT)

        # Recuadro ajustado a sol_afin
        box_afin = SurroundingRectangle(sol_afin, color=GREEN_C, buff=0.18, stroke_width=2.5)

        self.play(FadeIn(sec1), Write(p0q_tex))
        self.play(Write(sis_afin))
        self.play(Write(sol_afin), Create(box_afin))
        # Pausa de 3 segundos tras calcular coordenadas afines
        self.wait(3.0)

        # 3.2 Coordenadas Baricéntricas
        sec2 = Text("3.2 Coordenadas baricéntricas respecto al símplice {P0, P1, P2}:", font_size=21, color=YELLOW_C)
        sec2.next_to(box_afin, DOWN, buff=0.35, aligned_edge=LEFT)

        def_bari = MathTex(
            r"Q = \lambda_0 P_0 + \lambda_1 P_1 + \lambda_2 P_2 \quad \text{con} \quad \lambda_0 + \lambda_1 + \lambda_2 = 1",
            font_size=23
        ).next_to(sec2, DOWN, buff=0.2, aligned_edge=LEFT)

        relacion_bari = MathTex(
            r"Q = P_0 + \alpha_1(P_1 - P_0) + \alpha_2(P_2 - P_0) = (1 - \alpha_1 - \alpha_2)P_0 + \alpha_1 P_1 + \alpha_2 P_2",
            font_size=22,
            color=ORANGE
        ).next_to(def_bari, DOWN, buff=0.2, aligned_edge=LEFT)

        sol_bari = MathTex(
            r"\lambda_1 = \alpha_1 = 2, \quad \lambda_2 = \alpha_2 = 1, \quad "
            r"\lambda_0 = 1 - 2 - 1 = -2"
            r"\quad \Longrightarrow \quad (\lambda_0, \lambda_1, \lambda_2) = (-2, 2, 1)",
            font_size=24,
            color=YELLOW_C
        ).next_to(relacion_bari, DOWN, buff=0.2, aligned_edge=LEFT)

        # Recuadro ajustado a sol_bari
        box_bari = SurroundingRectangle(sol_bari, color=YELLOW_C, buff=0.18, stroke_width=2.5)

        self.play(FadeIn(sec2), Write(def_bari))
        self.play(Write(relacion_bari))
        self.play(Write(sol_bari))
        self.play(Create(box_bari))
        # Pausa de 3 segundos tras calcular coordenadas baricéntricas
        self.wait(3.0)

        self.play(FadeOut(Group(*self.mobjects)))


# ---------------------------------------------------------------------------
# ESCENA 5: Visualización Geométrica en 3D
# ---------------------------------------------------------------------------
class Escena5_Visualizacion3D(ThreeDScene):
    def construct(self):
        # Orientación de cámara 3D
        self.set_camera_orientation(phi=68 * DEGREES, theta=-55 * DEGREES, zoom=0.85)

        # Título fijado en pantalla (HUD 2D)
        titulo_3d = Title(
            r"Interpretación Geométrica en el Espacio Afín $\mathbb{A}^3(\mathbb{R})$",
            font_size=30,
            color=BLUE_B
        )
        self.add_fixed_in_frame_mobjects(titulo_3d)

        # Sistema de Ejes 3D
        axes = ThreeDAxes(
            x_range=[-1, 6, 1],
            y_range=[-1, 6, 1],
            z_range=[-1, 5, 1],
            x_length=7,
            y_length=7,
            z_length=6
        )
        x_label = axes.get_x_axis_label(MathTex("x", font_size=22))
        y_label = axes.get_y_axis_label(MathTex("y", font_size=22))
        z_label = axes.get_z_axis_label(MathTex("z", font_size=22))

        self.play(Create(axes), Write(x_label), Write(y_label), Write(z_label))

        # Puntos en coordenadas del espacio
        p0_coords = np.array([1.0, 2.0, 0.0])
        p1_coords = np.array([3.0, 2.0, 1.0])
        p2_coords = np.array([0.0, 4.0, 1.0])
        q_coords  = np.array([4.0, 4.0, 3.0])

        p0_pt = axes.c2p(*p0_coords)
        p1_pt = axes.c2p(*p1_coords)
        p2_pt = axes.c2p(*p2_coords)
        q_pt  = axes.c2p(*q_coords)

        # Puntos 3D
        dot_p0 = Dot3D(point=p0_pt, radius=0.10, color=BLUE_C)
        dot_p1 = Dot3D(point=p1_pt, radius=0.10, color=TEAL_C)
        dot_p2 = Dot3D(point=p2_pt, radius=0.10, color=ORANGE)
        dot_q  = Dot3D(point=q_pt,  radius=0.12, color=YELLOW_C)

        lbl_p0 = MathTex(r"P_0(1,2,0)", font_size=20, color=BLUE_C).next_to(dot_p0, DOWN + LEFT, buff=0.1)
        lbl_p1 = MathTex(r"P_1(3,2,1)", font_size=20, color=TEAL_C).next_to(dot_p1, RIGHT, buff=0.1)
        lbl_p2 = MathTex(r"P_2(0,4,1)", font_size=20, color=ORANGE).next_to(dot_p2, LEFT, buff=0.1)
        lbl_q  = MathTex(r"Q(4,4,3)",   font_size=22, color=YELLOW_C).next_to(dot_q, UP + RIGHT, buff=0.1)

        self.play(FadeIn(dot_p0), Write(lbl_p0))
        self.play(FadeIn(dot_p1), Write(lbl_p1))
        self.play(FadeIn(dot_p2), Write(lbl_p2))
        self.wait(1.0)

        # Vectores directores v1 y v2
        vec_v1 = Arrow3D(start=p0_pt, end=p1_pt, color=TEAL_C, thickness=0.03)
        vec_v2 = Arrow3D(start=p0_pt, end=p2_pt, color=ORANGE, thickness=0.03)

        self.play(Create(vec_v1), Create(vec_v2))
        self.wait(1.5)

        # Superficie del plano afín Pi
        v1 = p1_coords - p0_coords  # (2, 0, 1)
        v2 = p2_coords - p0_coords  # (-1, 2, 1)

        c1 = axes.c2p(*(p0_coords - 0.6 * v1 - 0.4 * v2))
        c2 = axes.c2p(*(p0_coords + 2.4 * v1 - 0.4 * v2))
        c3 = axes.c2p(*(p0_coords + 2.4 * v1 + 1.6 * v2))
        c4 = axes.c2p(*(p0_coords - 0.6 * v1 + 1.6 * v2))

        plano_superficie = Polygon(
            c1, c2, c3, c4,
            fill_color=BLUE_E,
            fill_opacity=0.35,
            stroke_color=BLUE_B,
            stroke_width=2
        )

        lbl_plano = MathTex(r"\Pi: 2x+3y-4z-8=0", font_size=22, color=BLUE_B)
        lbl_plano.move_to(axes.c2p(1.5, 4.5, 2.0))

        self.play(Create(plano_superficie), Write(lbl_plano))
        self.wait(1.5)

        # Punto Q y vector P0Q
        vec_p0q = Arrow3D(start=p0_pt, end=q_pt, color=YELLOW_C, thickness=0.04)

        # Descomposición afín: P0 -> P0 + 2*v1 -> Q
        pt_intermedio = axes.c2p(*(p0_coords + 2.0 * v1))
        vec_comp1 = Arrow3D(start=p0_pt, end=pt_intermedio, color=GREEN_C, thickness=0.03)
        vec_comp2 = Arrow3D(start=pt_intermedio, end=q_pt, color=GREEN_B, thickness=0.03)

        lbl_hud = MathTex(
            r"\vec{P_0 Q} = 2v_1 + 1v_2 \quad \implies [Q] = (2, 1)",
            font_size=22,
            color=YELLOW_C
        )
        self.add_fixed_in_frame_mobjects(lbl_hud)
        lbl_hud.to_corner(DR, buff=0.6)

        self.play(FadeIn(dot_q), Write(lbl_q))
        self.play(Create(vec_p0q))
        self.play(Write(lbl_hud))
        self.wait(1.5)

        self.play(Create(vec_comp1), Create(vec_comp2))
        self.wait(1.5)

        # Rotación orbital fluida de la cámara en 3D
        self.begin_ambient_camera_rotation(rate=0.20)
        self.wait(6.0)
        self.stop_ambient_camera_rotation()

        # Limpieza de escena
        self.play(
            FadeOut(lbl_hud),
            FadeOut(titulo_3d),
            FadeOut(axes), FadeOut(x_label), FadeOut(y_label), FadeOut(z_label),
            FadeOut(dot_p0), FadeOut(dot_p1), FadeOut(dot_p2), FadeOut(dot_q),
            FadeOut(lbl_p0), FadeOut(lbl_p1), FadeOut(lbl_p2), FadeOut(lbl_q),
            FadeOut(vec_v1), FadeOut(vec_v2), FadeOut(vec_p0q),
            FadeOut(vec_comp1), FadeOut(vec_comp2),
            FadeOut(plano_superficie), FadeOut(lbl_plano)
        )
        self.wait(0.5)


# ---------------------------------------------------------------------------
# ESCENA 6: Resumen Ejecutivo y Conclusiones
# ---------------------------------------------------------------------------
class Escena6_Resumen(BaseEscena):
    def construct(self):
        titulo = Title(r"Resumen Final de Solución", font_size=34, color=BLUE_B)
        self.play(Write(titulo))

        t1 = Text("1. Ecuaciones del plano afín Pi:", font_size=21, color=YELLOW_C)
        r1_param = MathTex(
            r"\text{Paramétricas: } \begin{cases} x = 1 + 2\lambda - \mu \\ y = 2 + 2\mu \\ z = \lambda + \mu \end{cases}",
            font_size=22
        )
        r1_imp = MathTex(
            r"\text{Implícita: } 2x + 3y - 4z - 8 = 0",
            font_size=22,
            color=GREEN_C
        )

        t2 = Text("2. Pertenencia de Q = (4, 4, 3):", font_size=21, color=YELLOW_C)
        r2 = MathTex(
            r"2(4) + 3(4) - 4(3) - 8 = 0 \iff 0 = 0 \implies Q \in \Pi \quad \text{\textbf{(Sí pertenece)}}",
            font_size=22,
            color=GREEN_C
        )

        t3 = Text("3. Coordenadas de Q en el plano afín:", font_size=21, color=YELLOW_C)
        r3_afin = MathTex(
            r"\text{Coordenadas afines respecto a } \{P_0; v_1, v_2\}: \quad [Q] = (2, 1)",
            font_size=22,
            color=TEAL_C
        )
        r3_bari = MathTex(
            r"\text{Coordenadas baricéntricas respecto a } \{P_0, P_1, P_2\}: \quad (\lambda_0, \lambda_1, \lambda_2) = (-2, 2, 1)",
            font_size=22,
            color=ORANGE
        )

        contenido = VGroup(
            t1, r1_param, r1_imp,
            t2, r2,
            t3, r3_afin, r3_bari
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).shift(DOWN * 0.2)

        # Recuadro ajustado exactamente sobre el bloque de contenido
        panel = SurroundingRectangle(contenido, color=BLUE_D, buff=0.35, stroke_width=2.5, corner_radius=0.15)

        self.play(Create(panel))
        self.play(FadeIn(t1), Write(r1_param), Write(r1_imp))
        self.play(FadeIn(t2), Write(r2))
        self.play(FadeIn(t3), Write(r3_afin), Write(r3_bari))
        # Pausa de 3.5 segundos en la pantalla de resumen
        self.wait(3.5)


# ---------------------------------------------------------------------------
# ESCENA MASTER: VideoCompleto (2D)
# ---------------------------------------------------------------------------
class VideoCompleto(BaseEscena):
    def construct(self):
        Escena1_Enunciado.construct(self)
        Escena2_EcuacionesPlano.construct(self)
        Escena3_PertenenciaQ.construct(self)
        Escena4_Coordenadas.construct(self)
        Escena6_Resumen.construct(self)


# ---------------------------------------------------------------------------
# ESCENA MASTER INTEGRADA (2D + MODELO 3D EN UN SOLO VIDEO)
# ---------------------------------------------------------------------------
class PresentacionMaestra3D(ThreeDScene):
    def construct(self):
        Escena1_Enunciado.construct(self)
        Escena2_EcuacionesPlano.construct(self)
        Escena3_PertenenciaQ.construct(self)
        Escena4_Coordenadas.construct(self)
        Escena5_Visualizacion3D.construct(self)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        Escena6_Resumen.construct(self)
