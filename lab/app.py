"""
Laboratorio Interactivo de Geometría de Posgrado.
Cubre:
- Parte I: Espacios Afines y Euclidianos (Módulos 1 al 5)
- Parte II: Teoría de las Curvas (Módulos 6 al 8)
Renderizado Vectorial SVG Nítido y de Alto Rendimiento (2D y Proyección Isométrica 3D).
"""

import sys
import os
import numpy as np
import streamlit as st

# Incorporar 'src' y 'lab' al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from geometria_lineal.affine_space import AffinePoint, Vector
from geometria_lineal.barycentric import Simplex
from geometria_lineal.affine_group import AffineTransform
from geometria_lineal.isometries import EuclideanIsometry, classify_isometry_2d, cartan_dieudonne_decomposition
from geometria_lineal.svd_geometry import GeometricSVD
from teoria_curvas.curve import ParametricCurve, HelixCurve, VivianiCurve, Circle2D
from teoria_curvas.frenet_serret import compute_frenet_apparatus
from teoria_curvas.fundamental_theorem import reconstruct_curve_from_intrinsic, local_canonical_expansion
from teoria_curvas.involutes_evolutes import compute_involute, compute_evolute_2d, OsculatingCircle
from svg_plotter import SVGPlotter


st.set_page_config(
    page_title="Laboratorio de Geometría Diferencial y Lineal",
    page_icon="📐",
    layout="wide"
)

st.title("🏛️ Laboratorio Interactivo de Geometría de Posgrado")
st.caption("Espacios Afines, Euclidianos y Teoría de las Curvas • Antigravity Ecosystem")

tema_general = st.sidebar.radio(
    "Seleccione Área Temática:",
    ["Parte I: Espacios Afines y Euclidianos", "Parte II: Teoría de las Curvas"]
)

if tema_general == "Parte I: Espacios Afines y Euclidianos":
    modulo = st.sidebar.selectbox(
        "Seleccione Módulo de Exploración:",
        [
            "1. Estructura de Espacio Afín",
            "2. Coordenadas Baricéntricas y Símplices",
            "3. Grupo Afín y Coordenadas Homogéneas",
            "4. Isometrías y Teorema de Cartan-Dieudonné",
            "5. SVD y Transformaciones Geométricas"
        ]
    )
else:
    modulo = st.sidebar.selectbox(
        "Seleccione Módulo de Curvas:",
        [
            "6. Curvas Regulares y Longitud de Arco",
            "7. Curvatura, Torsión y Triedro de Frenet",
            "8. Teorema Fundamental, Forma Canónica y Evolutas"
        ]
    )

# -----------------------------------------------------------------------------
# MÓDULO 1: ESTRUCTURA DE ESPACIO AFÍN
# -----------------------------------------------------------------------------
if modulo.startswith("1."):
    st.header("1. Estructura Axiomática de Espacio Afín")
    st.markdown("""
    En un espacio afín $(A, V, +)$, los **puntos** carecen de origen intrínseco.
    - La diferencia de puntos engendra vectores libres: $Q - P = \\mathbf{v} \\in V$.
    - La suma de puntos $P + Q$ carece de significado geométrico.
    - Fijar un marco afín $\\mathcal{R} = (O; \\mathbf{e}_1, \\mathbf{e}_2)$ permite asignar coordenadas a cada punto:
      $$P = O + x_1 \\mathbf{e}_1 + x_2 \\mathbf{e}_2$$
    """)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Parámetros del Marco y Puntos")
        ox = st.slider("Origen Ox", -3.0, 3.0, 0.0, 0.25)
        oy = st.slider("Origen Oy", -3.0, 3.0, 0.0, 0.25)
        px = st.slider("Punto P (x)", -4.0, 4.0, 1.0, 0.25)
        py = st.slider("Punto P (y)", -4.0, 4.0, 1.0, 0.25)
        qx = st.slider("Punto Q (x)", -4.0, 4.0, -2.0, 0.25)
        qy = st.slider("Punto Q (y)", -4.0, 4.0, 2.5, 0.25)

        p = AffinePoint([px, py])
        q = AffinePoint([qx, qy])
        v_diff = q - p

        st.info(f"**Vector de Chasles:** $\\mathbf{{v}} = Q - P = ({v_diff[0]:.2f}, {v_diff[1]:.2f})$\n\n"
                f"**Norma Euclidiana:** $\\|\\mathbf{{v}}\\| = {v_diff.norm():.3f}$")

    with col2:
        plotter = SVGPlotter(width=620, height=520, xlim=(-5.5, 5.5), ylim=(-5.5, 5.5))
        plotter.draw_grid_and_axes()
        plotter.draw_point(ox, oy, color="#ef4444", radius=7.0, label=f"O({ox},{oy})")
        plotter.draw_arrow(ox, oy, ox + 1.2, oy, color="#22c55e", width=2.5, label="e1")
        plotter.draw_arrow(ox, oy, ox, oy + 1.2, color="#f97316", width=2.5, label="e2")
        plotter.draw_point(px, py, color="#38bdf8", radius=6.5, label="P")
        plotter.draw_point(qx, qy, color="#a855f7", radius=6.5, label="Q")
        plotter.draw_line(ox, oy, px, py, color="#38bdf8", width=1.5, dashed=True)
        plotter.draw_line(ox, oy, qx, qy, color="#a855f7", width=1.5, dashed=True)
        plotter.draw_arrow(px, py, qx, qy, color="#eab308", width=3.0, label="v = Q - P")
        st.markdown(plotter.render(), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MÓDULO 2: COORDENADAS BARICÉNTRICAS Y SÍMPLICES
# -----------------------------------------------------------------------------
elif modulo.startswith("2."):
    st.header("2. Coordenadas Baricéntricas y Combinaciones Convexas")
    st.markdown("""
    Un $n$-símplice $\\Delta$ en $\\mathbb{R}^n$ se define por $n+1$ vértices afínmente independientes.
    Todo punto $P$ se expresa como combinación baricéntrica única:
    $$P = \\sum_{i=0}^n \\lambda_i P_i, \\quad \\sum_{i=0}^n \\lambda_i = 1$$
    """)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Posición del Punto de Prueba")
        test_x = st.slider("Coordenada X del Punto P", -4.0, 4.0, 0.0, 0.1)
        test_y = st.slider("Coordenada Y del Punto P", -3.0, 4.0, 0.5, 0.1)

        v0 = AffinePoint([-2.5, -1.5])
        v1 = AffinePoint([2.5, -1.5])
        v2 = AffinePoint([0.0, 2.5])
        tri = Simplex([v0, v1, v2])

        p_test = AffinePoint([test_x, test_y])
        bcoords = tri.to_barycentric(p_test)
        l0, l1, l2 = bcoords[0], bcoords[1], bcoords[2]

        st.markdown(f"### Pesos Baricéntricos:")
        st.write(f"- $\\lambda_0$: `{l0:.4f}`")
        st.write(f"- $\\lambda_1$: `{l1:.4f}`")
        st.write(f"- $\\lambda_2$: `{l2:.4f}`")

        if bcoords.is_interior():
            st.success("🟢 Punto en el **INTERIOR**.")
        elif bcoords.is_boundary():
            st.warning("🟡 Punto en la **FRONTERA**.")
        else:
            st.error("🔴 Punto **EXTERIOR** (No convexo).")

        st.metric("Área del Símplice", f"{tri.measure():.3f}")

    with col2:
        plotter = SVGPlotter(width=620, height=520, xlim=(-4.5, 4.5), ylim=(-3.5, 4.5))
        plotter.draw_grid_and_axes()
        pts = [v0.coordinates, v1.coordinates, v2.coordinates]
        plotter.draw_polygon(pts, fill="rgba(45, 212, 191, 0.2)", stroke="#14b8a6", width=2.5, label="2-Símplice Δ")
        plotter.draw_point(v0[0], v0[1], color="#ef4444", radius=6.0, label="P0")
        plotter.draw_point(v1[0], v1[1], color="#22c55e", radius=6.0, label="P1")
        plotter.draw_point(v2[0], v2[1], color="#38bdf8", radius=6.0, label="P2")
        pt_col = "#22c55e" if bcoords.is_convex() else "#ef4444"
        plotter.draw_point(test_x, test_y, color=pt_col, radius=8.0, label=f"P ({l0:.2f}, {l1:.2f}, {l2:.2f})")
        st.markdown(plotter.render(), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MÓDULO 3: GRUPO AFÍN Y COORDENADAS HOMOGÉNEAS
# -----------------------------------------------------------------------------
elif modulo.startswith("3."):
    st.header("3. El Grupo Afín $\\mathrm{Aff}(E)$ y Coordenadas Homogéneas")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Parámetros")
        theta_deg = st.slider("Rotación (°)", -180.0, 180.0, 30.0, 5.0)
        sx = st.slider("Escalado X", 0.2, 2.5, 1.2, 0.1)
        sy = st.slider("Escalado Y", 0.2, 2.5, 0.8, 0.1)
        shear_k = st.slider("Cizalladura", -2.0, 2.0, 0.4, 0.1)
        tx = st.slider("Traslación X", -3.0, 3.0, 1.0, 0.25)
        ty = st.slider("Traslación Y", -3.0, 3.0, -0.5, 0.25)

        theta = np.radians(theta_deg)
        R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        S = np.diag([sx, sy])
        Sh = np.array([[1.0, shear_k], [0.0, 1.0]])
        A = R @ S @ Sh
        b = np.array([tx, ty])
        t_affine = AffineTransform(A, b)

        st.write("Matriz Homogénea:", t_affine.homogeneous_matrix)
        st.metric("Determinante (Área)", f"{t_affine.determinant:.4f}")

    with col2:
        plotter = SVGPlotter(width=620, height=520, xlim=(-5.0, 6.0), ylim=(-5.0, 6.0))
        plotter.draw_grid_and_axes()
        shape_orig = np.array([[0, 0], [1.5, 0], [1.5, 0.4], [0.4, 0.4], [0.4, 1.5], [0, 1.5]])
        plotter.draw_polygon(shape_orig, fill="rgba(148, 163, 184, 0.3)", stroke="#94a3b8", width=1.5, label="Original")
        shape_trans = (A @ shape_orig.T).T + b
        plotter.draw_polygon(shape_trans, fill="rgba(250, 204, 21, 0.4)", stroke="#facc15", width=2.5, label="f(P)")
        st.markdown(plotter.render(), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MÓDULO 4: ISOMETRÍAS Y CARTAN-DIEUDONNÉ
# -----------------------------------------------------------------------------
elif modulo.startswith("4."):
    st.header("4. Isometrías y Teorema de Cartan-Dieudonné")
    col1, col2 = st.columns([1, 2])
    with col1:
        iso_type = st.radio("Tipo:", ["Rotación", "Traslación", "Reflexión con Deslizamiento"])
        if iso_type == "Rotación":
            angle = st.slider("Ángulo", -180.0, 180.0, 60.0, 5.0)
            rot = AffineTransform.rotation_2d(np.radians(angle), center=AffinePoint([0.0, 0.0]))
            iso = EuclideanIsometry(rot.A, rot.b)
        elif iso_type == "Traslación":
            bx = st.slider("bx", -3.0, 3.0, 2.0, 0.25)
            by = st.slider("by", -3.0, 3.0, 1.5, 0.25)
            iso = EuclideanIsometry(np.eye(2), [bx, by])
        else:
            angle_axis = st.slider("Eje (°)", -90.0, 90.0, 30.0, 5.0)
            glide = st.slider("Deslizamiento", -3.0, 3.0, 1.8, 0.2)
            rad = np.radians(angle_axis)
            n_norm = np.array([-np.sin(rad), np.cos(rad)])
            v_dir = np.array([np.cos(rad), np.sin(rad)])
            iso = EuclideanIsometry(np.eye(2) - 2.0 * np.outer(n_norm, n_norm), glide * v_dir)

        reflections = cartan_dieudonne_decomposition(iso)
        st.success(f"Descomposición: {len(reflections)} reflexiones hiperplanas.")

    with col2:
        plotter = SVGPlotter(width=620, height=520, xlim=(-5.0, 5.0), ylim=(-5.0, 5.0))
        plotter.draw_grid_and_axes()
        shape = np.array([[-0.5, -0.5], [1.2, -0.5], [0.3, 1.0]])
        plotter.draw_polygon(shape, fill="rgba(148, 163, 184, 0.3)", stroke="#94a3b8", width=1.5, label="F0")
        shape_iso = (iso.A @ shape.T).T + iso.b
        plotter.draw_polygon(shape_iso, fill="rgba(34, 197, 94, 0.4)", stroke="#22c55e", width=2.5, label="f(F0)")
        for idx, refl in enumerate(reflections):
            p0 = refl.p0.coordinates
            normal = refl.n.data
            tangent = np.array([-normal[1], normal[0]])
            plotter.draw_line(p0[0] - tangent[0]*7, p0[1] - tangent[1]*7, p0[0] + tangent[0]*7, p0[1] + tangent[1]*7,
                              color="#f43f5e", width=2.0, dashed=True)
        st.markdown(plotter.render(), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MÓDULO 5: SVD GEOMÉTRICA
# -----------------------------------------------------------------------------
elif modulo.startswith("5."):
    st.header("5. SVD y Transformaciones Geométricas")
    col1, col2 = st.columns([1, 2])
    with col1:
        a11 = st.slider("a11", -3.0, 3.0, 1.8, 0.1)
        a12 = st.slider("a12", -3.0, 3.0, 0.6, 0.1)
        a21 = st.slider("a21", -3.0, 3.0, 0.4, 0.1)
        a22 = st.slider("a22", -3.0, 3.0, 1.2, 0.1)
        A_mat = np.array([[a11, a12], [a21, a22]])
        gsvd = GeometricSVD(A_mat)
        axes_info = gsvd.principal_axes_2d()
        st.metric("σ1 (Semieje Mayor)", f"{axes_info['sigma1']:.4f}")
        st.metric("σ2 (Semieje Menor)", f"{axes_info['sigma2']:.4f}")

    with col2:
        plotter = SVGPlotter(width=620, height=520, xlim=(-4.0, 4.0), ylim=(-4.0, 4.0))
        plotter.draw_grid_and_axes()
        thetas = np.linspace(0, 2 * np.pi, 80)
        c_pts = np.column_stack([np.cos(thetas), np.sin(thetas)])
        plotter.draw_polyline(c_pts, stroke="#38bdf8", width=1.5, dashed=True)
        e_pts = (A_mat @ c_pts.T).T
        plotter.draw_polyline(e_pts, stroke="#c084fc", width=2.8)
        st.markdown(plotter.render(), unsafe_allow_html=True)

# =============================================================================
# PARTE II: TEORÍA DE LAS CURVAS
# =============================================================================

# -----------------------------------------------------------------------------
# MÓDULO 6: CURVAS REGULARES Y LONGITUD DE ARCO
# -----------------------------------------------------------------------------
elif modulo.startswith("6."):
    st.header("I.1. Concepto de Curva, Regularidad y Longitud de Arco")
    st.markdown("""
    Una curva $\\gamma: [a, b] \\to \\mathbb{R}^3$ es **regular** si su velocidad nunca se anula:
    $$\\gamma'(t) \\neq \\mathbf{0}, \\quad \\forall t \\in [a, b]$$
    La **longitud de arco** acumulada es $s(t) = \\int_a^t \\|\\gamma'(u)\\| du$, permitiendo la
    **reparametrización natural** donde la rapidez es constantemente unitaria: $\\|\\gamma'(s)\\| = 1$.
    """)

    col1, col2 = st.columns([1, 2])
    with col1:
        curva_tipo = st.selectbox("Seleccione Curva de Prueba:", ["Hélice Circular 3D", "Curva Plana Sinuosa", "Curva de Viviani"])

        if curva_tipo == "Hélice Circular 3D":
            radio = st.slider("Radio a", 0.5, 3.0, 1.8, 0.1)
            paso = st.slider("Paso b", 0.1, 1.5, 0.4, 0.05)
            t_eval = st.slider("Parámetro t", 0.0, float(4 * np.pi), float(np.pi), 0.1)
            curve = HelixCurve(a=radio, b=paso, t_range=(0.0, 4 * np.pi))

        elif curva_tipo == "Curva Plana Sinuosa":
            amp = st.slider("Amplitud", 0.5, 2.5, 1.2, 0.1)
            freq = st.slider("Frecuencia", 0.5, 2.5, 1.0, 0.1)
            t_eval = st.slider("Parámetro t", -3.0, 3.0, 0.5, 0.1)
            def f_sin(t):
                return np.array([t, amp * np.sin(freq * t), 0.0])
            curve = ParametricCurve(f_sin, (-3.0, 3.0), name="Sinuosa 2D")

        else: # Viviani
            a_viv = st.slider("Parámetro a", 0.5, 2.5, 1.5, 0.1)
            t_eval = st.slider("Parámetro t", float(-2 * np.pi), float(2 * np.pi), 1.0, 0.1)
            curve = VivianiCurve(a=a_viv)

        es_reg, t_sing = curve.is_regular()
        if es_reg:
            st.success("✅ La curva es **REGULAR** en todo el dominio.")
        else:
            st.error(f"❌ Singularidad detectada en t = {t_sing:.3f}")

        vel = curve.velocity(t_eval)
        rapidez = curve.speed(t_eval)
        s_val = curve.arc_length(curve.t_min, t_eval)
        s_total = curve.arc_length()

        st.metric("Vector Velocidad γ'(t)", f"({vel[0]:.2f}, {vel[1]:.2f}, {vel[2]:.2f})")
        st.metric("Rapidez Escalar ||γ'(t)||", f"{rapidez:.4f}")
        st.metric("Longitud de Arco s(t)", f"{s_val:.4f} / {s_total:.4f}")

    with col2:
        pts = curve.evaluate_points(180)
        p_curr = curve(t_eval)

        if curva_tipo == "Curva Plana Sinuosa":
            plotter = SVGPlotter(width=620, height=520, xlim=(-4.0, 4.0), ylim=(-3.0, 3.0))
            plotter.draw_grid_and_axes()
            plotter.draw_polyline(pts[:, :2], stroke="#2dd4bf", width=3.0)
            plotter.draw_point(p_curr[0], p_curr[1], color="#fbbf24", radius=7.0, label="γ(t)")
            plotter.draw_arrow(p_curr[0], p_curr[1], p_curr[0] + vel[0]*0.5, p_curr[1] + vel[1]*0.5,
                               color="#f97316", width=2.8, label="γ'(t)")
        else:
            plotter = SVGPlotter(width=620, height=520, xlim=(-5.0, 5.0), ylim=(-4.5, 5.5))
            plotter.draw_axes_3d(length=3.5, scale=0.85)
            plotter.draw_curve_3d(pts, stroke="#2dd4bf", width=3.0, scale=0.85)
            plotter.draw_point_3d(p_curr, color="#fbbf24", radius=6.5, label="γ(t)", scale=0.85)
            plotter.draw_vector_3d(p_curr, vel * (0.8 / rapidez), color="#f97316", width=2.8, label="T", scale=0.85)

        st.markdown(plotter.render(), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MÓDULO 7: CURVATURA, TORSIÓN Y TRIEDRO DE FRENET
# -----------------------------------------------------------------------------
elif modulo.startswith("7."):
    st.header("I.2. Curvatura, Torsión y Triedro Móvil de Frenet-Serret")
    st.markdown("""
    En cada punto regular con aceleración no colineal, existe una base ortonormal $\{\\mathbf{T}, \\mathbf{N}, \\mathbf{B}\} \\in \\mathrm{SO}(3)$:
    - **Tangente:** $\\mathbf{T} = \\gamma' / \\|\\gamma'\\|$
    - **Binormal:** $\\mathbf{B} = (\\gamma' \\times \\gamma'') / \\|\\gamma' \\times \\gamma''\\|$
    - **Normal Principal:** $\\mathbf{N} = \\mathbf{B} \\times \\mathbf{T}$
    - **Curvatura:** $\\kappa = \\|\\gamma' \\times \\gamma''\\| / \\|\\gamma'\\|^3$ (Tasa de giro de $\\mathbf{T}$)
    - **Torsión:** $\\tau = \\frac{(\\gamma' \\times \\gamma'') \\cdot \\gamma'''}{\\|\\gamma' \\times \\gamma''\\|^2}$ (Salida del plano osculador)
    """)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Parámetros de la Hélice 3D")
        a_h = st.slider("Radio a (Hélice)", 0.8, 3.0, 1.8, 0.1)
        b_h = st.slider("Paso b (Hélice)", 0.1, 1.5, 0.5, 0.05)
        t_param = st.slider("Posición t en la curva", 0.0, float(3 * np.pi), float(1.2 * np.pi), 0.1)

        helix = HelixCurve(a=a_h, b=b_h, t_range=(0.0, 3 * np.pi))
        frame = compute_frenet_apparatus(helix, t_param)

        st.markdown("### Magnitudes Intrínsecas:")
        st.metric("Curvatura κ", f"{frame.curvature:.4f}", help="κ = a / (a^2 + b^2)")
        st.metric("Radio de Curvatura ρ = 1/κ", f"{frame.radius_of_curvature:.4f}")
        st.metric("Torsión τ", f"{frame.torsion:.4f}", help="τ = b / (a^2 + b^2)")

        st.markdown("### Vectores del Triedro Móvil:")
        st.write(f"- **T (Rojo):** `[{frame.T[0]:.3f}, {frame.T[1]:.3f}, {frame.T[2]:.3f}]`")
        st.write(f"- **N (Verde):** `[{frame.N[0]:.3f}, {frame.N[1]:.3f}, {frame.N[2]:.3f}]`")
        st.write(f"- **B (Azul):** `[{frame.B[0]:.3f}, {frame.B[1]:.3f}, {frame.B[2]:.3f}]`")

        osculating = OsculatingCircle(frame)

    with col2:
        plotter = SVGPlotter(width=620, height=520, xlim=(-5.5, 5.5), ylim=(-4.5, 5.5))
        plotter.draw_axes_3d(length=3.5, scale=0.85)

        # Curva 3D
        h_pts = helix.evaluate_points(150)
        plotter.draw_curve_3d(h_pts, stroke="#2dd4bf", width=2.5, scale=0.85)

        # Punto P
        p_pt = frame.point
        plotter.draw_point_3d(p_pt, color="#fbbf24", radius=6.5, label="P", scale=0.85)

        # Vectores T, N, B
        vec_len = 1.6
        plotter.draw_vector_3d(p_pt, frame.T * vec_len, color="#ef4444", width=3.0, label="T", scale=0.85)
        plotter.draw_vector_3d(p_pt, frame.N * vec_len, color="#22c55e", width=3.0, label="N", scale=0.85)
        plotter.draw_vector_3d(p_pt, frame.B * vec_len, color="#38bdf8", width=3.0, label="B", scale=0.85)

        # Círculo Osculador
        circle_pts = osculating.generate_circle_points(80)
        plotter.draw_curve_3d(circle_pts, stroke="#c084fc", width=2.0, scale=0.85)
        plotter.draw_point_3d(frame.center_of_curvature, color="#c084fc", radius=4.5, label="C", scale=0.85)

        st.markdown(plotter.render(), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MÓDULO 8: TEOREMA FUNDAMENTAL, FORMA CANÓNICA Y EVOLUTAS
# -----------------------------------------------------------------------------
elif modulo.startswith("8."):
    st.header("I.3. Teorema Fundamental, Forma Canónica y Evolutas")
    st.markdown("""
    - **Teorema Fundamental:** Dadas $\\kappa(s) > 0$ y $\\tau(s)$, existe una única curva espacial módulo isometrías en $\\mathrm{SE}(3)$.
    - **Forma Canónica Local:** Desarrollo de Taylor de orden 3 en el triedro local:
      $$x(s) \\approx s - \\frac{\\kappa_0^2}{6}s^3, \\quad y(s) \\approx \\frac{\\kappa_0}{2}s^2, \\quad z(s) \\approx \\frac{\\kappa_0 \\tau_0}{6}s^3$$
    - **Evoluta:** Lugar geométrico de los centros de curvatura $C(t) = \\gamma(t) + \\rho(t) \\mathbf{N}(t)$.
    """)

    sub_tab = st.radio("Herramienta de Exploración:", ["Integrador de Frenet (Teorema Fundamental)", "Forma Canónica Local", "Evoluta y Cúspides"])

    if sub_tab.startswith("Integrador"):
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("Ecuaciones Intrínsecas κ(s) y τ(s)")
            k_const = st.slider("Curvatura Constante κ", 0.1, 2.0, 0.6, 0.1)
            t_const = st.slider("Torsión Constante τ", -1.5, 1.5, 0.3, 0.1)
            s_max = st.slider("Longitud de Arco Total L", 2.0, 15.0, 8.0, 0.5)

            sol = reconstruct_curve_from_intrinsic(
                kappa_func=lambda s: k_const,
                tau_func=lambda s: t_const,
                s_span=(0.0, s_max),
                num_points=160
            )
            st.info("La curva 3D es reconstruida numéricamente integrando las 12 EDOs de Frenet-Serret con RK45.")

        with col2:
            plotter = SVGPlotter(width=620, height=520, xlim=(-5.5, 5.5), ylim=(-4.5, 5.5))
            plotter.draw_axes_3d(length=3.5, scale=0.85)
            plotter.draw_curve_3d(sol["points"], stroke="#eab308", width=3.0, scale=0.85)
            plotter.draw_point_3d(sol["points"][0], color="#22c55e", radius=5.0, label="s=0", scale=0.85)
            plotter.draw_point_3d(sol["points"][-1], color="#ef4444", radius=5.0, label=f"s={s_max}", scale=0.85)
            st.markdown(plotter.render(), unsafe_allow_html=True)

    elif sub_tab.startswith("Forma"):
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("Parámetros Locales en s = 0")
            k0 = st.slider("Curvatura κ_0", 0.2, 3.0, 1.2, 0.1)
            t0 = st.slider("Torsión τ_0", -2.0, 2.0, 0.8, 0.1)
            expansion = local_canonical_expansion(kappa0=k0, tau0=t0, s_range=(-0.8, 0.8), num_points=120)

            st.markdown("""
            **Tres Proyecciones Características:**
            1. **Plano Osculador (T, N):** $y \\approx \\frac{\\kappa}{2} x^2$ (Parábola osculatriz).
            2. **Plano Rectificante (T, B):** $z \\approx \\frac{\\kappa \\tau}{6} x^3$ (Cúbica con inflexión).
            3. **Plano Normal (N, B):** $z^2 \\propto y^3$ (Cúspide Neiliana).
            """)

        with col2:
            plotter = SVGPlotter(width=620, height=520, xlim=(-2.0, 2.0), ylim=(-1.5, 1.5))
            plotter.draw_grid_and_axes()
            # Plano osculador: x vs y
            pts_xy = np.column_stack([expansion["x"], expansion["y"]])
            plotter.draw_polyline(pts_xy, stroke="#38bdf8", width=2.8)
            plotter.draw_point(0, 0, color="#ef4444", radius=6.0, label="s=0")
            st.caption("Proyección en Plano Osculador (Eje X: Tangente, Eje Y: Normal)")
            st.markdown(plotter.render(), unsafe_allow_html=True)

    else: # Evoluta
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("Evoluta de una Elipse")
            a_el = st.slider("Semieje Mayor a", 1.5, 3.5, 2.5, 0.1)
            b_el = st.slider("Semieje Menor b", 0.5, 2.0, 1.2, 0.1)

            def f_ellipse(t):
                return np.array([a_el * np.cos(t), b_el * np.sin(t), 0.0])

            curva_el = ParametricCurve(f_ellipse, (0.0, 2 * np.pi), name="Elipse")
            evo_pts = compute_evolute_2d(curva_el, num_points=160)

            st.info("""
            La evoluta de una elipse es un **astroide** (hipocicloide de 4 cúspides).
            Las 4 cúspides corresponden a los 4 vértices de la elipse donde $\\kappa'(s) = 0$.
            """)

        with col2:
            plotter = SVGPlotter(width=620, height=520, xlim=(-4.0, 4.0), ylim=(-4.0, 4.0))
            plotter.draw_grid_and_axes()
            el_pts = curva_el.evaluate_points(120)
            plotter.draw_polyline(el_pts[:, :2], stroke="#2dd4bf", width=2.5)
            plotter.draw_polyline(evo_pts[:, :2], stroke="#f43f5e", width=2.8)
            plotter.draw_point(0, 0, color="#ffffff", radius=4.0, label="Centro")
            st.caption("Curva original (Verde) y su Evoluta / Astroide (Rojo)")
            st.markdown(plotter.render(), unsafe_allow_html=True)
