"""
Módulo de Definición de Curvas Paramétricas y Regulares.

Cubre:
- Representaciones regulares de curvas de clase C^m: gamma'(t) != 0.
- Cálculo de derivadas de orden superior (velocidad, aceleración, sobreaceleración / jerk).
- Longitud de arco s(t) = integral_a^t ||gamma'(u)|| du.
- Reparametrización natural por longitud de arco (||gamma'(s)|| = 1).
- Familias canónicas de curvas en R^3 (Hélice circular, Curva de Viviani).
"""

from __future__ import annotations
from typing import Callable, Tuple, Sequence, Optional, Union
import numpy as np
from scipy.integrate import quad
from scipy.optimize import root_scalar


class ParametricCurve:
    """
    Representa una curva regular gamma: [a, b] -> R^3 (o R^2 embebido).
    Permite diferenciación numérica de alta precisión y reparametrización por longitud de arco.
    """

    def __init__(
        self,
        func: Callable[[float], Union[Sequence[float], np.ndarray]],
        t_range: Tuple[float, float],
        name: str = "Curva Paramétrica",
        h: float = 1e-4
    ):
        self.func = func
        self.t_min, self.t_max = t_range
        self.name = name
        self.h = h

    def __call__(self, t: float) -> np.ndarray:
        """Evalúa la curva en el parámetro t."""
        pt = np.array(self.func(t), dtype=np.float64).flatten()
        if len(pt) == 2:
            return np.append(pt, 0.0) # Embebido en R^3
        return pt

    def derivative(self, t: float, order: int = 1) -> np.ndarray:
        """
        Calcula la derivada numérica de orden 1, 2 o 3 mediante diferencias finitas centrales.
        """
        h = self.h
        if order == 1:
            # Orden O(h^4)
            return (-self(t + 2*h) + 8*self(t + h) - 8*self(t - h) + self(t - 2*h)) / (12 * h)
        elif order == 2:
            return (-self(t + 2*h) + 16*self(t + h) - 30*self(t) + 16*self(t - h) - self(t - 2*h)) / (12 * h**2)
        elif order == 3:
            return (self(t + 2*h) - 2*self(t + h) + 2*self(t - h) - self(t - 2*h)) / (2 * h**3)
        else:
            raise NotImplementedError("Derivadas de orden superior a 3 no están implementadas.")

    def velocity(self, t: float) -> np.ndarray:
        """Vector velocidad gamma'(t)."""
        return self.derivative(t, order=1)

    def acceleration(self, t: float) -> np.ndarray:
        """Vector aceleración gamma''(t)."""
        return self.derivative(t, order=2)

    def jerk(self, t: float) -> np.ndarray:
        """Vector sobreaceleración gamma'''(t)."""
        return self.derivative(t, order=3)

    def speed(self, t: float) -> float:
        """Rapidez escalar ||gamma'(t)||."""
        return float(np.linalg.norm(self.velocity(t)))

    def is_regular(self, num_samples: int = 100, tol: float = 1e-6) -> Tuple[bool, Optional[float]]:
        """
        Verifica si la curva es regular (||gamma'(t)|| > 0 para todo t en [a, b]).
        Devuelve (es_regular, t_singular_si_existe).
        """
        ts = np.linspace(self.t_min, self.t_max, num_samples)
        for t in ts:
            if self.speed(t) < tol:
                return False, float(t)
        return True, None

    def arc_length(self, t_start: Optional[float] = None, t_end: Optional[float] = None) -> float:
        """
        Calcula la longitud de arco: s = integral ||gamma'(u)|| du mediante cuadratura numérica.
        """
        t0 = self.t_min if t_start is None else t_start
        t1 = self.t_max if t_end is None else t_end
        val, _ = quad(lambda u: self.speed(u), t0, t1, limit=100)
        return float(val)

    def t_from_arc_length(self, s: float, t0: Optional[float] = None) -> float:
        """
        Inversión de la función longitud de arco: halla t tal que s(t) = s.
        Dado que s'(t) = ||gamma'(t)|| > 0, s(t) es estrictamente monótona creciente.
        """
        start = self.t_min if t0 is None else t0
        total_len = self.arc_length(start, self.t_max)
        if s < 0 or s > total_len + 1e-7:
            raise ValueError(f"Longitud s={s:.4f} fuera de rango [0, {total_len:.4f}].")

        # Función objetivo: f(t) = arc_length(start, t) - s = 0
        def f(t_val):
            return self.arc_length(start, t_val) - s

        sol = root_scalar(f, bracket=[self.t_min, self.t_max], method="brentq")
        return float(sol.root)

    def evaluate_points(self, num_points: int = 150) -> np.ndarray:
        """Genera una trayectoria discreta de puntos en R^3 (num_points x 3)."""
        ts = np.linspace(self.t_min, self.t_max, num_points)
        return np.array([self(t) for t in ts])


class HelixCurve(ParametricCurve):
    """
    Hélice circular cilíndrica:
      gamma(t) = (a * cos(t), a * sin(t), b * t)
    Curvatura constante: kappa = a / (a^2 + b^2)
    Torsión constante:   tau   = b / (a^2 + b^2)
    """

    def __init__(self, a: float = 2.0, b: float = 0.5, t_range: Tuple[float, float] = (0.0, 4 * np.pi)):
        self.a = float(a)
        self.b = float(b)

        def f(t):
            return np.array([self.a * np.cos(t), self.a * np.sin(t), self.b * t])

        super().__init__(f, t_range, name=f"Hélice Circular (a={a}, b={b})")

    @property
    def exact_curvature(self) -> float:
        return self.a / (self.a**2 + self.b**2)

    @property
    def exact_torsion(self) -> float:
        return self.b / (self.a**2 + self.b**2)


class VivianiCurve(ParametricCurve):
    """
    Curva de Viviani: intersección de la esfera x^2 + y^2 + z^2 = 4*a^2
    con el cilindro (x - a)^2 + y^2 = a^2.
      gamma(t) = (a * (1 + cos(t)), a * sin(t), 2 * a * sin(t / 2))
    """

    def __init__(self, a: float = 2.0, t_range: Tuple[float, float] = (-2 * np.pi, 2 * np.pi)):
        self.a = float(a)

        def f(t):
            return np.array([
                self.a * (1.0 + np.cos(t)),
                self.a * np.sin(t),
                2.0 * self.a * np.sin(t / 2.0)
            ])

        super().__init__(f, t_range, name=f"Curva de Viviani (a={a})")


class Circle2D(ParametricCurve):
    """Círculo en el plano xy."""

    def __init__(self, radius: float = 2.0, center: Tuple[float, float] = (0.0, 0.0)):
        self.radius = radius
        self.cx, self.cy = center

        def f(t):
            return np.array([self.cx + radius * np.cos(t), self.cy + radius * np.sin(t), 0.0])

        super().__init__(f, (0.0, 2 * np.pi), name=f"Círculo R={radius}")

