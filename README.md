# Geometría Diferencial y Álgebra Lineal Geométrica: Infraestructura Computacional e Instruccional de Posgrado

Repositorio integral con el ecosistema de software, animaciones cinemáticas con **Manim**, laboratorio interactivo con **Streamlit** y biblioteca matemática para el curso de posgrado que articula:

1. **Parte I: Espacios Afines y Euclidianos:**
   > *"Estructura de espacio afín, coordenadas baricéntricas, combinaciones convexas, grupo afín, isometrías y descomposición en valores singulares orientada a transformaciones geométricas."*
2. **Parte II: Teoría de las Curvas:**
   > *"Concepto de curva (regularidad, longitud de arco, proyecciones), Curvatura y Torsión (triedro de Frenet-Serret, planos fundamentales, círculo osculador) y Teoría de Curvas (fórmulas de Frenet, teorema fundamental de existencia/unicidad, forma canónica, involutas, evolutas y contacto)."*

---

## 🏛️ Arquitectura del Repositorio

```text
CursoGeometriaLineal/
├── animations/                       # 🎬 Suite de Animaciones Vectoriales con Manim
│   ├── manim_utils.py                # Utilidades de layout con zonas protegidas (sin solapamiento)
│   ├── scene_01_affine_space.py      # Escena 1: Axiomas, Puntos vs Vectores y Marco Afín
│   ├── scene_02_barycentric.py       # Escena 2: Coordenadas Baricéntricas y Símplices
│   ├── scene_03_affine_group.py      # Escena 3: Grupo Afín y Coordenadas Homogéneas
│   ├── scene_04_isometries.py        # Escena 4: Isometrías y Teorema de Cartan-Dieudonné
│   ├── scene_05_svd_geometry.py      # Escena 5: Geometría SVD (Esfera -> Elipsoide)
│   ├── scene_06_regular_curves_arclength.py # Escena 6: Regularidad y Longitud de Arco (I.1)
│   ├── scene_07_frenet_trihedron.py         # Escena 7: Triedro de Frenet {T, N, B} en 3D (I.2)
│   └── scene_08_fundamental_theorem_canonical.py # Escena 8: Teorema Fundamental y Evolutas (I.3)
├── docs/                             # 📚 Documentación Pedagógica y Curricular
│   ├── SYLLABUS.md                   # Programa de posgrado, fundamentación y bibliografía
│   └── GUIA_DOCENTE.md               # Metodología de enseñanza y planificación sesión por sesión
├── lab/                              # 🧪 Laboratorio Interactivo Web (Streamlit)
│   ├── app.py                        # Aplicación interactiva con navegación completa de 8 módulos
│   └── svg_plotter.py                # Motor vectorial SVG 2D y proyección isométrica 3D
├── notebooks/                        # 📓 Cuadernos para Estudiantes e Investigadores
│   └── laboratorio_posgrado_geometria.ipynb
├── src/                              # ⚙️ Motores Matemáticos y Computacionales
│   ├── geometria_lineal/             # Parte I: Espacios Afines y Euclidianos
│   │   ├── affine_space.py           # Puntos, Vectores, Axiomática y Marcos
│   │   ├── barycentric.py            # Símplices, Coordenadas Baricéntricas y Convexidad
│   │   ├── affine_group.py           # Grupo Aff(n), Coordenadas Homogéneas y Puntos Fijos
│   │   ├── isometries.py             # E(n), Reflexiones y Descomposición Cartan-Dieudonné
│   │   └── svd_geometry.py           # SVD geométrica, Elipsoides y Factorización Polar
│   └── teoria_curvas/                # Parte II: Teoría de las Curvas
│       ├── curve.py                  # Curvas regulares, derivadas C^m y longitud de arco
│       ├── frenet_serret.py          # Aparato de Frenet {T, N, B}, curvatura κ, torsión τ
│       ├── fundamental_theorem.py    # Integrador ODE de Frenet y forma canónica local
│       └── involutes_evolutes.py     # Involutas, evolutas 2D/3D y círculos osculadores
├── tests/                            # 🔬 Suites de Pruebas Unitarias Numéricas
│   ├── test_all.py                   # Pruebas de álgebra afín y euclidiana (5 tests OK)
│   └── test_curvas.py                # Pruebas de teoría de curvas y Frenet (5 tests OK)
├── cli.py                            # 🛠️ CLI Unificado de Automatización Docente
├── requirements.txt                  # Dependencias del proyecto
└── README.md                         # Documentación general del repositorio
```

---

## 🚀 Inicio Rápido

### 1. Requisitos
- Python 3.10 o superior (compatible con Python 3.13 y NumPy 2.x).
- Dependencias: `numpy`, `scipy`, `sympy`, `streamlit`, `manim`.

### 2. Auditar el Estado de los Módulos
```bash
python cli.py status
```

### 3. Ejecutar Pruebas Matemáticas Unitarias (10 Tests)
```bash
python cli.py test
```

### 4. Lanzar el Laboratorio Interactivo Web
```bash
python cli.py lab
```
*O directamente con Streamlit:*
```bash
streamlit run lab/app.py
```

### 5. Renderizar Animaciones con Manim
El CLI soporta renderizado individual o por lotes en calidades `l` (480p), `m` (720p) y `h` (1080p):
```bash
# Renderizar la animación del Triedro de Frenet en 3D
python cli.py render frenet -q m

# Renderizar el Teorema Fundamental y las Evolutas
python cli.py render fundamental -q m

# Renderizar las 8 escenas del curso en lote
python cli.py render all -q m
```

---

## 📚 Mapa Curricular Completo (8 Unidades)

| Unidad | Núcleo Temático | Motor de Código (`src`) | Animación Manim (`animations`) | Laboratorio Web (`lab`) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Espacio Afín** | $(A,V,+)$, $Q-P=\mathbf{v}$, Chasles, Marcos $(O;e_i)$ | `geometria_lineal/affine_space.py` | `scene_01_affine_space.py` | Módulo 1: Puntos vs Vectores |
| **2. Baricentros** | Símplices, $\sum \lambda_i = 1$, Convexidad, Áreas | `geometria_lineal/barycentric.py` | `scene_02_barycentric.py` | Módulo 2: Símplices y Pesos |
| **3. Grupo Afín** | $\mathbb{R}^n \rtimes \mathrm{GL}(n)$, Matrices Homogéneas | `geometria_lineal/affine_group.py` | `scene_03_affine_group.py` | Módulo 3: Deformación y Puntos Fijos |
| **4. Isometrías** | $\mathrm{E}(n)$, Reflexiones, Cartan-Dieudonné | `geometria_lineal/isometries.py` | `scene_04_isometries.py` | Módulo 4: Descomposición en Espejos |
| **5. SVD Geométrica** | $A = U\Sigma V^T$, Elipsoides, Factorización Polar | `geometria_lineal/svd_geometry.py` | `scene_05_svd_geometry.py` | Módulo 5: Esfera a Elipsoide y SVD |
| **6. Curvas Regulares** | $\gamma'(t) \neq \mathbf{0}$, Longitud de Arco $s(t)$, Reparametrización Natural | `teoria_curvas/curve.py` | `scene_06_regular_curves_arclength.py` | Módulo 6: Regularidad y Longitud $s$ |
| **7. Frenet-Serret** | $\{\mathbf{T}, \mathbf{N}, \mathbf{B}\}$, Curvatura $\kappa$, Torsión $\tau$, Planos | `teoria_curvas/frenet_serret.py` | `scene_07_frenet_trihedron.py` | Módulo 7: Triedro Móvil 3D y Círculo |
| **8. Teorema Fundamental** | Integrador ODE $\kappa(s),\tau(s)$, Expansión Canónica, Evolutas | `teoria_curvas/fundamental_theorem.py` | `scene_08_fundamental_theorem_canonical.py` | Módulo 8: Integrador de Curvas y Astroide |
