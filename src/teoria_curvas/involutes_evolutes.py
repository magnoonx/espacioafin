"""
Módulo de Involutas (Evolventes), Evolutas y Teoría del Contacto.

Cubre:
- Involuta de una curva: gamma_inv(s) = gamma(s) + (c - s) * T(s).
  Generada al desenrollar una cuerda inextensible tensada sobre la curva.
  Propiedad: La tangente a gamma es la normal a gamma_inv.
- Evoluta: Lugar geométrico de los centros de curvatura C(s) = gamma(s) + rho(s) * N(s).
  Cúspides de la evoluta corresponden a los vértices de la curva (donde d_kappa/ds = 0).
- Círculo osculador y orden de contacto (contacto de orden >= 2).
"""

from __future__ import annotations
from typing import Sequence, Tuple, Optional
import numpy as np
from .curve import ParametricCurve
from .frenet_serret import compute_frenet_apparatus, FrenetFrame


class OsculatingCircle:
    """Círculo osculador en un punto de la curva (contacto de orden 2)."""

    def __init__(self, frame: FrenetFrame):
        self.frame = frame
        self.center = frame.center_of_curvature
        self.radius = frame.radius_of_curvature
        self.plane_normal = frame.B # Yace en el plano osculador span{T, N}

    def generate_circle_points(self, num_points: int = 100) -> np.ndarray:
        """Genera puntos 3D que describen la circunferencia osculatriz en el plano osculador."""
        if np.isinf(self.radius) or self.radius > 1e4:
            # Línea recta tangente
            ts = np.linspace(-3, 3, num_points)
            return np.array([self.frame.point + t * self.frame.T for t in ts])

        thetas = np.linspace(0, 2 * np.pi, num_points)
        # La circunferencia está parametrizada en el plano osculador por C + R*(cos*T + sin*N)
        circle_pts = []
        for th in thetas:
            pt = self.center + self.radius * (np.cos(th) * (-self.frame.N) + np.sin(th) * self.frame.T)
            circle_pts.append(pt)
        return np.array(circle_pts)


def compute_involute(curve: ParametricCurve, c_const: float = 0.0, num_points: int = 150) -> np.ndarray:
    """
    Calcula la involuta (evolvente) de la curva para una longitud de hilo c_const:
      gamma_inv(t) = gamma(t) + (c_const - s(t)) * T(t)
    """
    ts = np.linspace(curve.t_min, curve.t_max, num_points)
    involute_pts = []

    for t in ts:
        p = curve(t)
        v = curve.velocity(t)
        sp = np.linalg.norm(v)
        if sp < 1e-7:
            continue
        T = v / sp
        s = curve.arc_length(curve.t_min, t)
        inv_p = p + (c_const - s) * T
        involute_pts.append(inv_p)

    return np.array(involute_pts)


def compute_evolute_2d(curve: ParametricCurve, num_points: int = 150) -> np.ndarray:
    """
    Calcula la evoluta (lugar geométrico de centros de curvatura) para una curva plana:
      gamma_evo(t) = gamma(t) + (1 / kappa(t)) * N(t)
    """
    ts = np.linspace(curve.t_min, curve.t_max, num_points)
    evolute_pts = []

    for t in ts:
        frame = compute_frenet_apparatus(curve, t)
        if frame.curvature > 1e-6:
            c = frame.center_of_curvature
            evolute_pts.append(c)

    return np.array(evolute_pts)

