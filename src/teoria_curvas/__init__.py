"""
Biblioteca de Teoría de Curvas en R^2 y R^3 para Nivel de Posgrado.
Incluye:
- Parametrizaciones regulares y longitud de arco.
- Aparato de Frenet-Serret (T, N, B), curvatura, torsión y planos asociados.
- Teorema fundamental de existencia y unicidad (integrador ODE de ecuaciones intrínsecas).
- Círculo osculador, esfera osculatriz, involutas y evolutas.
"""

from .curve import ParametricCurve, HelixCurve, VivianiCurve, Circle2D
from .frenet_serret import FrenetFrame, FrenetApparatus, compute_frenet_apparatus
from .fundamental_theorem import reconstruct_curve_from_intrinsic, local_canonical_expansion
from .involutes_evolutes import compute_involute, compute_evolute_2d, OsculatingCircle

__all__ = [
    "ParametricCurve",
    "HelixCurve",
    "VivianiCurve",
    "Circle2D",
    "FrenetFrame",
    "FrenetApparatus",
    "compute_frenet_apparatus",
    "reconstruct_curve_from_intrinsic",
    "local_canonical_expansion",
    "compute_involute",
    "compute_evolute_2d",
    "OsculatingCircle",
]

