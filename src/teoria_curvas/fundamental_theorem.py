"""
Módulo del Teorema Fundamental de Curvas y Representación Canónica.

Teorema Fundamental de la Teoría Local de Curvas:
  Dadas dos funciones suaves kappa(s) > 0 y tau(s) definidas en [0, L],
  existe una única curva parametrizada por longitud de arco gamma(s)
  cuyas curvatura y torsión coinciden con kappa y tau, única salvo
  movimiento rígido directo en SE(3) = R^3 ⋊ SO(3).

Implementa:
- Integrador numérico de las Fórmulas de Frenet-Serret acopladas.
- Reconstrucción de curvas 3D a partir de sus ecuaciones intrínsecas.
- Expansión canónica local de Taylor en el triedro {T_0, N_0, B_0}.
"""

from __future__ import annotations
from typing import Callable, Tuple, Optional, Dict, Any
import numpy as np
from scipy.integrate import solve_ivp


def reconstruct_curve_from_intrinsic(
    kappa_func: Callable[[float], float],
    tau_func: Callable[[float], float],
    s_span: Tuple[float, float] = (0.0, 10.0),
    initial_point: Optional[np.ndarray] = None,
    initial_T: Optional[np.ndarray] = None,
    initial_N: Optional[np.ndarray] = None,
    num_points: int = 300
) -> Dict[str, np.ndarray]:
    """
    Integra numéricamente el sistema diferencial de Frenet-Serret:
      d(gamma)/ds = T
      d(T)/ds     =  kappa(s) * N
      d(N)/ds     = -kappa(s) * T + tau(s) * B
      d(B)/ds     = -tau(s)   * N
    """
    p0 = np.array([0.0, 0.0, 0.0]) if initial_point is None else np.array(initial_point, dtype=np.float64)
    T0 = np.array([1.0, 0.0, 0.0]) if initial_T is None else np.array(initial_T, dtype=np.float64)
    N0 = np.array([0.0, 1.0, 0.0]) if initial_N is None else np.array(initial_N, dtype=np.float64)
    T0 = T0 / np.linalg.norm(T0)
    N0 = N0 - np.dot(N0, T0) * T0
    N0 = N0 / np.linalg.norm(N0)
    B0 = np.cross(T0, N0)

    # Estado: [x, y, z, Tx, Ty, Tz, Nx, Ny, Nz, Bx, By, Bz] (12 variables)
    y0 = np.concatenate([p0, T0, N0, B0])

    def frenet_ode(s, state):
        # Desempaquetar
        r = state[0:3]
        T = state[3:6]
        N = state[6:9]
        B = state[9:12]

        k = float(kappa_func(s))
        t = float(tau_func(s))

        dr_ds = T
        dT_ds = k * N
        dN_ds = -k * T + t * B
        dB_ds = -t * N

        return np.concatenate([dr_ds, dT_ds, dN_ds, dB_ds])

    s_eval = np.linspace(s_span[0], s_span[1], num_points)
    sol = solve_ivp(
        frenet_ode,
        s_span,
        y0,
        t_eval=s_eval,
        method="RK45",
        rtol=1e-8,
        atol=1e-10
    )

    trajectory = sol.y[0:3, :].T
    T_traj = sol.y[3:6, :].T
    N_traj = sol.y[6:9, :].T
    B_traj = sol.y[9:12, :].T

    # Re-ortonormalización por proyección QR en cada paso para evitar deriva numérica
    for i in range(len(s_eval)):
        M = np.column_stack([T_traj[i], N_traj[i], B_traj[i]])
        Q, R = np.linalg.qr(M)
        # Asegurar orientación positiva det(Q) == +1
        if np.linalg.det(Q) < 0:
            Q[:, 2] *= -1
        T_traj[i], N_traj[i], B_traj[i] = Q[:, 0], Q[:, 1], Q[:, 2]

    return {
        "s": s_eval,
        "points": trajectory,
        "T": T_traj,
        "N": N_traj,
        "B": B_traj
    }


def local_canonical_expansion(
    kappa0: float,
    tau0: float,
    d_kappa0: float = 0.0,
    s_range: Tuple[float, float] = (-0.5, 0.5),
    num_points: int = 100
) -> Dict[str, np.ndarray]:
    """
    Calcula la representación canónica local de la curva en el triedro de Frenet
    alrededor de s = 0 mediante la serie de Taylor truncada de orden 3:
      x(s) = s - (kappa0^2 / 6) * s^3 + O(s^4)
      y(s) = (kappa0 / 2) * s^2 + (d_kappa0 / 6) * s^3 + O(s^4)
      z(s) = (kappa0 * tau0 / 6) * s^3 + O(s^4)

    Permite estudiar las tres proyecciones ortogonales locales fundamentales:
      1. Plano Osculador (xy): Parábola y ≈ (kappa0 / 2) x^2
      2. Plano Rectificante (xz): Cúbica de inflexión z ≈ (kappa0 * tau0 / 6) x^3
      3. Plano Normal (yz): Cúspide semicúbica neiliana z^2 ≈ (2 tau0^2 / 9 kappa0) y^3
    """
    ss = np.linspace(s_range[0], s_range[1], num_points)
    xs = ss - (kappa0**2 / 6.0) * (ss**3)
    ys = (kappa0 / 2.0) * (ss**2) + (d_kappa0 / 6.0) * (ss**3)
    zs = (kappa0 * tau0 / 6.0) * (ss**3)

    return {
        "s": ss,
        "x": xs, # Eje T
        "y": ys, # Eje N
        "z": zs, # Eje B
        "points_canonical": np.column_stack([xs, ys, zs])
    }

