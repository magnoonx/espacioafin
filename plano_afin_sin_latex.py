"""
=============================================================================
ANIMACIÓN MANIM CE: PRESENTACIÓN DIDÁCTICA COMPLETA (2D + 3D)
Curso: Geometría Lineal / Geometría Afín
=============================================================================
Versión 100% libre de dependencias LaTeX (utiliza Text y Pango).
Ritmo pausado y pedagógico:
  - Fórmulas escritas a velocidad natural (run_time de 1.8s a 2.5s).
  - Pausas generosas de 4 a 5 segundos en cada ecuación y conclusión clave.
  - Integración completa del modelo 3D con rotación orbital de cámara.
=============================================================================
"""

from manim import *
import numpy as np

# =============================================================================
# CONFIGURACIÓN GLOBAL DE VELOCIDAD
# =============================================================================
FACTOR_DURACION = 1.0  # Puedes aumentar a 1.2 o 1.3 si deseas aún más tiempo


class TextTitle(VGroup):
    """Título elegante 100% basado en Text y Line (sin ninguna llamada a LaTeX)."""
    def __init__(self, text, font_size=28, color=BLUE_B, **kwargs):
        super().__init__(**kwargs)
        self.text_obj = Text(text, font_size=font_size, color=color)
        self.text_obj.to_edge(UP, buff=0.45)
        self.line = Line(
            start=np.array([-6.2, self.text_obj.get_bottom()[1] - 0.15, 0]),
            end=np.array([6.2, self.text_obj.get_bottom()[1] - 0.15, 0]),
            color=BLUE_D,
            stroke_width=1.5
        )
        self.add(self.text_obj, self.line)


class BaseEscena(Scene):
    """Escena base que escala automáticamente la velocidad de todas las animaciones."""
    def play(self, *args, **kwargs):
        if "run_time" in kwargs:
            kwargs["run_time"] *= FACTOR_DURACION
        else:
            kwargs["run_time"] = 1.5 * FACTOR_DURACION  # Escritura más pausada por defecto
        super().play(*args, **kwargs)

    def wait(self, duration=1.0, **kwargs):
        super().wait(duration * FACTOR_DURACION, **kwargs)


class Escena1_EnunciadoSinLatex(BaseEscena):
    def construct(self):
        titulo = TextTitle("Plano Afín en A³(R): Ecuaciones y Coordenadas", font_size=28, color=BLUE_B)
        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=1.5)
        self.wait(1.5)

        t1 = Text("Puntos dados en el espacio afín tridimensional:", font_size=20, color=YELLOW_C)
        t_pts = Text("P₀ = (1, 2, 0),    P₁ = (3, 2, 1),    P₂ = (0, 4, 1)", font_size=24, color=WHITE)
        enun = VGroup(t1, t_pts).arrange(DOWN, buff=0.25)
        caja = SurroundingRectangle(enun, color=BLUE_D, buff=0.3, stroke_width=2.0, corner_radius=0.15)
        grupo_enun = VGroup(enun, caja).shift(UP * 0.9)

        self.play(Create(caja), FadeIn(enun, shift=UP * 0.2), run_time=2.0)
        self.wait(2.5)

        v_sub = Text("Vectores directores del plano afín:", font_size=20, color=GREEN_C)
        v1_t = Text("v₁ = P₀P₁ = P₁ - P₀ = (3-1, 2-2, 1-0) = (2, 0, 1)", font_size=20, color=TEAL_C)
        v2_t = Text("v₂ = P₀P₂ = P₂ - P₀ = (0-1, 4-2, 1-0) = (-1, 2, 1)", font_size=20, color=ORANGE)
        ind_t = Text("Rango de la matriz de vectores = 2  ==>  {v₁, v₂} son l.i.", font_size=20, color=YELLOW_B)
        concl = Text("Por tanto, {P₀, P₁, P₂} no son colineales y definen el plano afín Π.", font_size=18, color=GRAY_A)

        grp = VGroup(v_sub, v1_t, v2_t, ind_t, concl).arrange(
            DOWN, buff=0.22, aligned_edge=LEFT
        ).next_to(grupo_enun, DOWN, buff=0.35).align_to(grupo_enun, LEFT)

        self.play(FadeIn(v_sub), run_time=1.2)
        self.play(Write(v1_t), run_time=1.8)
        self.wait(1.0)
        self.play(Write(v2_t), run_time=1.8)
        self.wait(1.5)
        self.play(Write(ind_t), run_time=2.0)
        self.play(FadeIn(concl), run_time=1.5)

        # Pausa generosa para asimilar la independencia afín
        self.wait(4.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.2)


class Escena2_EcuacionesSinLatex(BaseEscena):
    def construct(self):
        titulo = TextTitle("1. Ecuaciones del Plano Afín Π = P₀ + <v₁, v₂>", font_size=28, color=BLUE_B)
        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=1.5)
        self.wait(1.0)

        # Panel Izquierdo: Paramétricas
        lbl_p = Text("Ecuaciones Paramétricas", font_size=20, color=YELLOW_C)
        def_p = Text("X = P₀ + λ·v₁ + μ·v₂,   (λ, μ ∈ R)", font_size=18, color=GRAY_B)
        sis_p = Text(
            "Π: {\n"
            "  x = 1 + 2λ - μ\n"
            "  y = 2 + 2μ\n"
            "  z = λ + μ",
            font_size=22,
            line_spacing=0.8,
            color=WHITE
        )

        col_izq = VGroup(lbl_p, def_p, sis_p).arrange(
            DOWN, buff=0.28, aligned_edge=LEFT
        ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)

        box_p = SurroundingRectangle(sis_p, color=GREEN_C, buff=0.2, stroke_width=2.5)

        # Panel Derecho: Implícita
        lbl_i = Text("Ecuación Implícita (Cartesiana)", font_size=20, color=YELLOW_C)
        det_i = Text(
            "det | x-1   y-2   z |\n"
            "    |   2     0   1 | = 0\n"
            "    |  -1     2   1 |",
            font_size=19,
            line_spacing=0.8,
            color=ORANGE
        )
        des_i = Text("-2(x - 1) - 3(y - 2) + 4z = 0\n-2x - 3y + 4z + 8 = 0", font_size=18, line_spacing=0.7)
        eq_f = Text("Π:  2x + 3y - 4z - 8 = 0", font_size=22, color=YELLOW_C)

        col_der = VGroup(lbl_i, det_i, des_i, eq_f).arrange(
            DOWN, buff=0.24, aligned_edge=LEFT
        ).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.2)

        box_i = SurroundingRectangle(eq_f, color=YELLOW_C, buff=0.2, stroke_width=2.5)

        linea = DashedLine(UP * 2.3, DOWN * 3.0, color=GRAY_D)

        # Animación Izquierda (Paramétricas)
        self.play(FadeIn(lbl_p), Write(def_p), run_time=1.8)
        self.wait(1.0)
        self.play(Write(sis_p), run_time=2.5)
        self.play(Create(box_p), run_time=1.2)
        # Pausa de 4.5 segundos tras mostrar las ecuaciones paramétricas
        self.wait(4.5)

        self.play(Create(linea), run_time=1.0)

        # Animación Derecha (Implícita)
        self.play(FadeIn(lbl_i), Write(det_i), run_time=2.2)
        self.wait(1.5)
        self.play(Write(des_i), run_time=2.2)
        self.wait(1.5)
        self.play(Write(eq_f), run_time=2.0)
        self.play(Create(box_i), run_time=1.2)
        # Pausa de 4.5 segundos tras mostrar la ecuación implícita
        self.wait(4.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.2)


class Escena3_PertenenciaSinLatex(BaseEscena):
    def construct(self):
        titulo = TextTitle("2. Verificación de Pertenencia de Q = (4, 4, 3)", font_size=28, color=BLUE_B)
        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=1.5)
        self.wait(1.0)

        eq = Text("Ecuación de Π:  2x + 3y - 4z - 8 = 0", font_size=22, color=BLUE_C).shift(UP * 1.8)
        self.play(Write(eq), run_time=1.8)
        self.wait(1.5)

        sust = Text("Sustituyendo x=4, y=4, z=3:", font_size=20, color=YELLOW_C).next_to(eq, DOWN, buff=0.5)
        calc = Text(
            "2(4) + 3(4) - 4(3) - 8\n"
            "= 8 + 12 - 12 - 8\n"
            "= 20 - 20 = 0",
            font_size=22,
            line_spacing=0.8
        ).next_to(sust, DOWN, buff=0.35)

        self.play(FadeIn(sust), run_time=1.2)
        self.play(Write(calc), run_time=2.5)
        self.wait(2.0)

        res_txt = Text(
            "0 = 0  ==>  Q = (4, 4, 3) ∈ Π  (Sí pertenece)",
            font_size=22,
            color=GREEN_C
        ).next_to(calc, DOWN, buff=0.6)

        box_res = SurroundingRectangle(res_txt, color=GREEN_C, buff=0.25, stroke_width=2.5, corner_radius=0.12)

        self.play(Write(res_txt), Create(box_res), run_time=2.0)
        self.play(Indicate(res_txt, color=GREEN_A), run_time=1.5)
        # Pausa de 4.5 segundos tras comprobar pertenencia
        self.wait(4.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.2)


class Escena4_CoordenadasSinLatex(BaseEscena):
    def construct(self):
        titulo = TextTitle("3. Coordenadas Afines y Baricéntricas de Q", font_size=28, color=BLUE_B)
        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=1.5)
        self.wait(1.0)

        # 3.1 Marco Afín
        s1 = Text("3.1 Marco afín {P₀; v₁, v₂}:", font_size=20, color=YELLOW_C).to_edge(LEFT, buff=0.8).shift(UP * 2.2)
        pq = Text("Vector P₀Q = Q - P₀ = (4-1, 4-2, 3-0) = (3, 2, 3)", font_size=19, color=TEAL_C).next_to(s1, DOWN, buff=0.2, aligned_edge=LEFT)
        def_af = Text("α₁·v₁ + α₂·v₂ = P₀Q  ==>  α₁(2, 0, 1) + α₂(-1, 2, 1) = (3, 2, 3)", font_size=18).next_to(pq, DOWN, buff=0.2, aligned_edge=LEFT)
        sol_af = Text("De la 2da fila: 2α₂ = 2 ==> α₂ = 1\nDe la 3ra fila: α₁ + 1 = 3 ==> α₁ = 2\n==> Coordenadas afines: [Q] = (2, 1)", font_size=19, line_spacing=0.8, color=GREEN_C).next_to(def_af, DOWN, buff=0.2, aligned_edge=LEFT)

        box_af = SurroundingRectangle(sol_af, color=GREEN_C, buff=0.18, stroke_width=2.5)

        self.play(FadeIn(s1), Write(pq), run_time=2.0)
        self.wait(1.5)
        self.play(Write(def_af), run_time=2.2)
        self.wait(1.5)
        self.play(Write(sol_af), Create(box_af), run_time=2.5)
        # Pausa de 4.5 segundos tras obtener coordenadas afines
        self.wait(4.5)

        # 3.2 Símplice y Baricéntricas
        s2 = Text("3.2 Coordenadas baricéntricas respecto al símplice {P₀, P₁, P₂}:", font_size=20, color=YELLOW_C).next_to(box_af, DOWN, buff=0.35, aligned_edge=LEFT)
        rel = Text("Q = (1 - α₁ - α₂)P₀ + α₁P₁ + α₂P₂  con  λ₀ + λ₁ + λ₂ = 1", font_size=18, color=ORANGE).next_to(s2, DOWN, buff=0.2, aligned_edge=LEFT)
        sol_ba = Text("λ₁ = 2,   λ₂ = 1,   λ₀ = 1 - 2 - 1 = -2\n==> Coordenadas baricéntricas: (λ₀, λ₁, λ₂) = (-2, 2, 1)", font_size=19, line_spacing=0.8, color=YELLOW_C).next_to(rel, DOWN, buff=0.2, aligned_edge=LEFT)

        box_ba = SurroundingRectangle(sol_ba, color=YELLOW_C, buff=0.18, stroke_width=2.5)

        self.play(FadeIn(s2), Write(rel), run_time=2.2)
        self.wait(1.5)
        self.play(Write(sol_ba), run_time=2.5)
        self.play(Create(box_ba), run_time=1.2)
        # Pausa de 4.5 segundos tras obtener coordenadas baricéntricas
        self.wait(4.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.2)


class Escena3D_SinLatex(ThreeDScene):
    """
    Visualización geométrica en 3D con cámara orbital, 100% libre de dependencias LaTeX.
    """
    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-55 * DEGREES, zoom=0.85)

        titulo_3d = TextTitle("Visualización Geométrica 3D en A³(R)", font_size=26, color=BLUE_B)
        self.add_fixed_in_frame_mobjects(titulo_3d)

        axes = ThreeDAxes(
            x_range=[-1, 6, 1],
            y_range=[-1, 6, 1],
            z_range=[-1, 5, 1],
            x_length=7,
            y_length=7,
            z_length=6
        )
        x_label = axes.get_x_axis_label(Text("x", font_size=18))
        y_label = axes.get_y_axis_label(Text("y", font_size=18))
        z_label = axes.get_z_axis_label(Text("z", font_size=18))

        self.play(Create(axes), Write(x_label), Write(y_label), Write(z_label), run_time=2.0)

        p0_coords = np.array([1.0, 2.0, 0.0])
        p1_coords = np.array([3.0, 2.0, 1.0])
        p2_coords = np.array([0.0, 4.0, 1.0])
        q_coords  = np.array([4.0, 4.0, 3.0])

        p0_pt = axes.c2p(*p0_coords)
        p1_pt = axes.c2p(*p1_coords)
        p2_pt = axes.c2p(*p2_coords)
        q_pt  = axes.c2p(*q_coords)

        dot_p0 = Dot3D(point=p0_pt, radius=0.10, color=BLUE_C)
        dot_p1 = Dot3D(point=p1_pt, radius=0.10, color=TEAL_C)
        dot_p2 = Dot3D(point=p2_pt, radius=0.10, color=ORANGE)
        dot_q  = Dot3D(point=q_pt,  radius=0.12, color=YELLOW_C)

        lbl_p0 = Text("P₀(1,2,0)", font_size=16, color=BLUE_C).next_to(dot_p0, DOWN + LEFT, buff=0.1)
        lbl_p1 = Text("P₁(3,2,1)", font_size=16, color=TEAL_C).next_to(dot_p1, RIGHT, buff=0.1)
        lbl_p2 = Text("P₂(0,4,1)", font_size=16, color=ORANGE).next_to(dot_p2, LEFT, buff=0.1)
        lbl_q  = Text("Q(4,4,3)",   font_size=18, color=YELLOW_C).next_to(dot_q, UP + RIGHT, buff=0.1)

        self.play(FadeIn(dot_p0), Write(lbl_p0), run_time=1.5)
        self.play(FadeIn(dot_p1), Write(lbl_p1), run_time=1.5)
        self.play(FadeIn(dot_p2), Write(lbl_p2), run_time=1.5)
        self.wait(2.0)

        vec_v1 = Arrow3D(start=p0_pt, end=p1_pt, color=TEAL_C, thickness=0.03)
        vec_v2 = Arrow3D(start=p0_pt, end=p2_pt, color=ORANGE, thickness=0.03)

        self.play(Create(vec_v1), Create(vec_v2), run_time=2.0)
        self.wait(2.0)

        v1 = p1_coords - p0_coords
        v2 = p2_coords - p0_coords

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

        lbl_plano = Text("Π: 2x+3y-4z-8=0", font_size=18, color=BLUE_B)
        lbl_plano.move_to(axes.c2p(1.5, 4.5, 2.0))

        self.play(Create(plano_superficie), Write(lbl_plano), run_time=2.5)
        self.wait(2.5)

        vec_p0q = Arrow3D(start=p0_pt, end=q_pt, color=YELLOW_C, thickness=0.04)

        pt_intermedio = axes.c2p(*(p0_coords + 2.0 * v1))
        vec_comp1 = Arrow3D(start=p0_pt, end=pt_intermedio, color=GREEN_C, thickness=0.03)
        vec_comp2 = Arrow3D(start=pt_intermedio, end=q_pt, color=GREEN_B, thickness=0.03)

        lbl_hud = Text(
            "P₀Q = 2·v₁ + 1·v₂  ==>  [Q] = (2, 1)",
            font_size=18,
            color=YELLOW_C
        )
        self.add_fixed_in_frame_mobjects(lbl_hud)
        lbl_hud.to_corner(DR, buff=0.6)

        self.play(FadeIn(dot_q), Write(lbl_q), run_time=1.5)
        self.play(Create(vec_p0q), Write(lbl_hud), run_time=2.0)
        self.wait(2.0)

        self.play(Create(vec_comp1), Create(vec_comp2), run_time=2.2)
        self.wait(2.5)

        # Rotación orbital fluida y pausada (8 segundos de giro para apreciar el plano en 3D)
        self.begin_ambient_camera_rotation(rate=0.18)
        self.wait(8.0)
        self.stop_ambient_camera_rotation()

        self.play(
            FadeOut(lbl_hud),
            FadeOut(titulo_3d),
            FadeOut(axes), FadeOut(x_label), FadeOut(y_label), FadeOut(z_label),
            FadeOut(dot_p0), FadeOut(dot_p1), FadeOut(dot_p2), FadeOut(dot_q),
            FadeOut(lbl_p0), FadeOut(lbl_p1), FadeOut(lbl_p2), FadeOut(lbl_q),
            FadeOut(vec_v1), FadeOut(vec_v2), FadeOut(vec_p0q),
            FadeOut(vec_comp1), FadeOut(vec_comp2),
            FadeOut(plano_superficie), FadeOut(lbl_plano),
            run_time=1.5
        )
        self.wait(1.0)


class Escena5_ResumenSinLatex(BaseEscena):
    def construct(self):
        titulo = TextTitle("Resumen Final de Solución", font_size=28, color=BLUE_B)
        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=1.5)
        self.wait(1.0)

        t1 = Text("1. Ecuaciones del plano afín Π:", font_size=19, color=YELLOW_C)
        e1 = Text("   Paramétricas: x = 1+2λ-μ,  y = 2+2μ,  z = λ+μ\n   Implícita:    2x + 3y - 4z - 8 = 0", font_size=18, line_spacing=0.7)

        t2 = Text("2. Pertenencia de Q(4, 4, 3):", font_size=19, color=YELLOW_C)
        e2 = Text("   2(4) + 3(4) - 4(3) - 8 = 0  ==>  Q ∈ Π  (Sí pertenece)", font_size=18, color=GREEN_C)

        t3 = Text("3. Coordenadas de Q:", font_size=19, color=YELLOW_C)
        e3 = Text("   Marco afín {P₀; v₁, v₂}:           [Q] = (2, 1)\n   Símplice afín {P₀, P₁, P₂}:        (λ₀, λ₁, λ₂) = (-2, 2, 1)", font_size=18, line_spacing=0.7, color=TEAL_C)

        cont = VGroup(t1, e1, t2, e2, t3, e3).arrange(DOWN, buff=0.25, aligned_edge=LEFT).shift(DOWN * 0.2)
        panel = SurroundingRectangle(cont, color=BLUE_D, buff=0.35, stroke_width=2.5, corner_radius=0.15)

        self.play(Create(panel), run_time=1.5)
        self.play(FadeIn(cont), run_time=2.5)
        # Pausa de 6.0 segundos en la pantalla de resumen final
        self.wait(6.0)


# =============================================================================
# ESCENA MAESTRA (POR DEFECTO): 2D ÁLGEBRA + MODELO 3D + RESUMEN FINAL
# =============================================================================
class PresentacionMaestraSinLatex(ThreeDScene):
    """
    Video maestro completo que unifica:
      1. Planteamiento e independencia afín (2D)
      2. Ecuaciones paramétricas e implícita (2D)
      3. Verificación de pertenencia de Q (2D)
      4. Coordenadas afines y baricéntricas (2D)
      5. Modelo geométrico tridimensional con rotación (3D)
      6. Resumen ejecutivo final (2D)
    Duración total estimada: ~2 minutos y 45 segundos.
    """
    def construct(self):
        Escena1_EnunciadoSinLatex.construct(self)
        Escena2_EcuacionesSinLatex.construct(self)
        Escena3_PertenenciaSinLatex.construct(self)
        Escena4_CoordenadasSinLatex.construct(self)
        Escena3D_SinLatex.construct(self)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        Escena5_ResumenSinLatex.construct(self)


class VideoCompletoSinLatex(BaseEscena):
    """Secuencia exclusiva en 2D (deducciones y álgebra)."""
    def construct(self):
        Escena1_EnunciadoSinLatex.construct(self)
        Escena2_EcuacionesSinLatex.construct(self)
        Escena3_PertenenciaSinLatex.construct(self)
        Escena4_CoordenadasSinLatex.construct(self)
        Escena5_ResumenSinLatex.construct(self)
