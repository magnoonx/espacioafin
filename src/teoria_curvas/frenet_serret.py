"""
Módulo del Aparato de Frenet-Serret, Curvatura y Torsión.

Define para cualquier curva en R^3:
- Triedro móvil de Frenet-Serret: {T, N, B}
  - T: Vector Tangente Unitario
  - N: Vector Normal Principal Unitario
  - B: Vector Binormal Unitario (B = T x N)
- Escalares intrínsecos:
  - Curvatura: kappa(t) = ||gamma' x gamma''|| / ||gamma'||^3
  - Torsión:   tau(t)   = (gamma' x gamma'' . gamma''') / ||gamma' x gamma''||^2
- Planos fundamentales asociados:
  - Plano Osculador:   <X - P, B> = 0 (span{T, N})
  - Plano Normal:      <X - P, T> = 0 (span{N, B})
  - Plano Rectificante:<X - P, N> = 0 (span{T, B})
- Elementos osculadores:
  - Círculo Osculador: Centro C = P + (1/kappa) * N, Radio rho = 1/kappa
"""

from __future__ import annotations
from typing import Sequence, Dict, Any, Optional
import numpy as np
from .curve import ParametricCurve


class FrenetFrame:
    """
    Representa el triedro móvil de Frenet-Serret y sus magnitudes geométricas
    en un punto específico de la curva.
    """

    def __init__(
        self,
        point: np.ndarray,
        tangent: np.ndarray,
        normal: np.ndarray,
        binormal: np.ndarray,
        curvature: float,
        torsion: float,
        t_param: float
    ):
        self.point = point
        self.T = tangent
        self.N = normal
        self.B = binormal
        self.curvature = curvature
        self.torsion = torsion
        self.t = t_param

    @property
    def radius_of_curvature(self) -> float:
        """Radio de curvatura rho = 1 / kappa."""
        if self.curvature < 1e-9:
            return float("inf")
        return 1.0 / self.curvature

    @property
    def center_of_curvature(self) -> np.ndarray:
        """Centro de curvatura C = P + (1 / kappa) * N."""
        if self.curvature < 1e-9:
            return self.point + self.N * 1e6
        return self.point + self.radius_of_curvature * self.N

    def is_orthonormal(self, tol: float = 1e-4) -> bool:
        """Comprueba que {T, N, B} forma una base ortonormal orientada positivamente en SO(3)."""
        M = np.column_stack([self.T, self.N, self.B])
        is_ortho = np.allclose(M.T @ M, np.eye(3), atol=tol)
        is_direct = np.isclose(np.linalg.det(M), 1.0, atol=tol)
        return is_ortho and is_direct

    def osculating_plane_equation(self) -> Tuple[np.ndarray, float]:
        """Ecuación del plano osculador: <B, X> + d = 0, donde d = - <B, P>."""
        d = -float(np.dot(self.B, self.point))
        return self.B, d

    def normal_plane_equation(self) -> Tuple[np.ndarray, float]:
        """Ecuación del plano normal: <T, X> + d = 0, donde d = - <T, P>."""
        d = -float(np.dot(self.T, self.point))
        return self.T, d

    def rectifying_plane_equation(self) -> Tuple[np.ndarray, float]:
        """Ecuación del plano rectificante: <N, X> + d = 0, donde d = - <N, P>."""
        d = -float(np.dot(self.N, self.point))
        return self.N, d

    def __repr__(self) -> str:
        return (
            f"FrenetFrame(t={self.t:.3f}, kappa={self.curvature:.4f}, "
            f"tau={self.torsion:.4f}, rho={self.radius_of_curvature:.4f})"
        )


def compute_frenet_apparatus(curve: ParametricCurve, t: float) -> FrenetFrame:
    """
    Calcula el aparato completo de Frenet-Serret para cualquier curva regular
    con parametrización general t (no necesariamente natural).

    Fórmulas invariantes por reparametrización:
      v = gamma'(t)
      a = gamma''(t)
      j = gamma'''(t)

      T = v / ||v||
      B = (v x a) / ||v x a||
      N = B x T
      kappa = ||v x a|| / ||v||^3
      tau = (v x a . j) / ||v x a||^2
    """
    p = curve(t)
    v = curve.velocity(t)
    a = curve.acceleration(t)
    j = curve.jerk(t)

    speed = np.linalg.norm(v)
    if speed < 1e-7:
        raise ValueError(f"La curva no es regular en t={t} (||v|| = 0).")

    T = v / speed

    v_cross_a = np.cross(v, a)
    cross_norm = np.linalg.norm(v_cross_a)

    if cross_norm < 1e-7:
        # Caso de punto de inflexión o recta: aceleración paralela a velocidad
        kappa = 0.0
        tau = 0.0
        # Escogemos una normal arbitraria ortogonal a T
        arb = np.array([0.0, 0.0, 1.0]) if abs(T[2]) < 0.9 else np.array([0.0, 1.0, 0.0])
        N = np.cross(arb, T)
        N = N / np.linalg.norm(N)
        B = np.cross(T, N)
    else:
        kappa = float(cross_norm / (speed**3))
        B = v_cross_a / cross_norm
        N = np.cross(B, T)
        # Normalizar por estabilidad numérica
        N = N / np.linalg.norm(N)
        tau = float(np.dot(v_cross_a, j) / (cross_norm**2))

    return FrenetFrame(
        point=p,
        tangent=T,
        normal=N,
        binormal=B,
        curvature=kappa,
        torsion=tau,
        t_param=t
    )


FrenetApparatus = compute_frenet_apparatus

