"""
Motor de Renderizado Vectorial SVG Liviano para el Laboratorio Interactivo.
Independiente de backends gráficos externos; soporta 2D y proyección isométrica 3D.
"""

from typing import Sequence, Tuple, Optional, List, Union
import numpy as np


class SVGPlotter:
    """Generador de gráficos vectoriales interactivos en SVG."""

    def __init__(self, width: int = 650, height: int = 550, xlim: Tuple[float, float] = (-5.0, 5.0), ylim: Tuple[float, float] = (-5.0, 5.0)):
        self.w = width
        self.h = height
        self.xmin, self.xmax = xlim
        self.ymin, self.ymax = ylim
        self.elements: List[str] = []

    def to_screen(self, x: float, y: float) -> Tuple[float, float]:
        """Mapea coordenadas cartesianas 2D a coordenadas de pantalla SVG."""
        sx = (x - self.xmin) / (self.xmax - self.xmin) * self.w
        sy = self.h - (y - self.ymin) / (self.ymax - self.ymin) * self.h
        return sx, sy

    def project_3d(self, x: float, y: float, z: float, yaw: float = 0.65, pitch: float = 0.45, scale: float = 0.9) -> Tuple[float, float]:
        """Proyección isométrica/dimétrica de coordenadas 3D a pantalla 2D."""
        # Rotación alrededor del eje Z (yaw) y luego inclinación respecto a X (pitch)
        u = (-x * np.cos(yaw) + y * np.sin(yaw)) * scale
        v = (-x * np.sin(yaw) * np.sin(pitch) - y * np.cos(yaw) * np.sin(pitch) + z * np.cos(pitch)) * scale
        return self.to_screen(u, v)

    def draw_grid_and_axes(self, step: float = 1.0):
        """Dibuja la rejilla cartesiana 2D y los ejes principales con marcas numéricas."""
        self.elements.append(f'<rect width="{self.w}" height="{self.h}" fill="#181e29" rx="10"/>')

        xs = np.arange(np.ceil(self.xmin), np.floor(self.xmax) + 0.1, step)
        ys = np.arange(np.ceil(self.ymin), np.floor(self.ymax) + 0.1, step)

        for x in xs:
            s_x, s_y0 = self.to_screen(x, self.ymin)
            _, s_y1 = self.to_screen(x, self.ymax)
            self.elements.append(
                f'<line x1="{s_x:.1f}" y1="{s_y0:.1f}" x2="{s_x:.1f}" y2="{s_y1:.1f}" stroke="#2a3447" stroke-width="1" stroke-dasharray="3,3"/>'
            )

        for y in ys:
            s_x0, s_y = self.to_screen(self.xmin, y)
            s_x1, _ = self.to_screen(self.xmax, y)
            self.elements.append(
                f'<line x1="{s_x0:.1f}" y1="{s_y:.1f}" x2="{s_x1:.1f}" y2="{s_y:.1f}" stroke="#2a3447" stroke-width="1" stroke-dasharray="3,3"/>'
            )

        ax_x0, ax_y0 = self.to_screen(self.xmin, 0.0)
        ax_x1, ax_y1 = self.to_screen(self.xmax, 0.0)
        self.elements.append(
            f'<line x1="{ax_x0:.1f}" y1="{ax_y0:.1f}" x2="{ax_x1:.1f}" y2="{ax_y1:.1f}" stroke="#64748b" stroke-width="1.8"/>'
        )

        ay_x0, ay_y0 = self.to_screen(0.0, self.ymin)
        ay_x1, ay_y1 = self.to_screen(0.0, self.ymax)
        self.elements.append(
            f'<line x1="{ay_x0:.1f}" y1="{ay_y0:.1f}" x2="{ay_x1:.1f}" y2="{ay_y1:.1f}" stroke="#64748b" stroke-width="1.8"/>'
        )

    def draw_axes_3d(self, length: float = 3.5, scale: float = 0.9):
        """Dibuja un triedro coordenado 3D (X: rojo, Y: verde, Z: azul)."""
        self.elements.append(f'<rect width="{self.w}" height="{self.h}" fill="#181e29" rx="10"/>')
        ox, oy = self.project_3d(0, 0, 0, scale=scale)

        # Eje X
        xx, xy = self.project_3d(length, 0, 0, scale=scale)
        self.draw_arrow_screen(ox, oy, xx, xy, color="#ef4444", width=2.0, label="X")

        # Eje Y
        yx, yy = self.project_3d(0, length, 0, scale=scale)
        self.draw_arrow_screen(ox, oy, yx, yy, color="#22c55e", width=2.0, label="Y")

        # Eje Z
        zx, zy = self.project_3d(0, 0, length, scale=scale)
        self.draw_arrow_screen(ox, oy, zx, zy, color="#38bdf8", width=2.0, label="Z")

    def draw_curve_3d(self, points: np.ndarray, stroke: str = "#2dd4bf", width: float = 2.5, scale: float = 0.9):
        """Proyecta y dibuja una curva en R^3 a partir de una matriz (N, 3)."""
        screen_pts = [self.project_3d(p[0], p[1], p[2], scale=scale) for p in points]
        pts_str = " ".join(f"{sx:.1f},{sy:.1f}" for sx, sy in screen_pts)
        self.elements.append(
            f'<polyline points="{pts_str}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round"/>'
        )

    def draw_vector_3d(self, start: np.ndarray, vec: np.ndarray, color: str = "#f97316", width: float = 2.5, label: str = "", scale: float = 0.9):
        """Dibuja un vector 3D proyectado a partir de su punto de anclaje."""
        sx0, sy0 = self.project_3d(start[0], start[1], start[2], scale=scale)
        target = start + vec
        sx1, sy1 = self.project_3d(target[0], target[1], target[2], scale=scale)
        self.draw_arrow_screen(sx0, sy0, sx1, sy1, color=color, width=width, label=label)

    def draw_point_3d(self, pt: np.ndarray, color: str = "#fbbf24", radius: float = 5.0, label: str = "", scale: float = 0.9):
        sx, sy = self.project_3d(pt[0], pt[1], pt[2], scale=scale)
        self.elements.append(
            f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{radius}" fill="{color}" stroke="#ffffff" stroke-width="1.5"/>'
        )
        if label:
            self.elements.append(
                f'<text x="{sx + 8:.1f}" y="{sy - 8:.1f}" fill="{color}" font-family="sans-serif" font-size="12" font-weight="bold">{label}</text>'
            )

    def draw_point(self, x: float, y: float, color: str = "#38bdf8", radius: float = 6.0, label: str = ""):
        sx, sy = self.to_screen(x, y)
        self.elements.append(
            f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{radius}" fill="{color}" stroke="#ffffff" stroke-width="1.5"/>'
        )
        if label:
            self.elements.append(
                f'<text x="{sx + 10:.1f}" y="{sy - 8:.1f}" fill="{color}" font-family="sans-serif" font-size="13" font-weight="bold">{label}</text>'
            )

    def draw_line(self, x0: float, y0: float, x1: float, y1: float, color: str = "#94a3b8", width: float = 1.5, dashed: bool = False):
        sx0, sy0 = self.to_screen(x0, y0)
        sx1, sy1 = self.to_screen(x1, y1)
        dash_attr = 'stroke-dasharray="5,5"' if dashed else ''
        self.elements.append(
            f'<line x1="{sx0:.1f}" y1="{sy0:.1f}" x2="{sx1:.1f}" y2="{sy1:.1f}" stroke="{color}" stroke-width="{width}" {dash_attr}/>'
        )

    def draw_arrow_screen(self, sx0: float, sy0: float, sx1: float, sy1: float, color: str = "#38bdf8", width: float = 2.5, label: str = ""):
        dx = sx1 - sx0
        dy = sy1 - sy0
        length = np.hypot(dx, dy)
        if length < 1e-4:
            return

        ux, uy = dx / length, dy / length
        arrow_size = 8.5
        px = sx1 - arrow_size * ux
        py = sy1 - arrow_size * uy
        perp_x = -uy * (arrow_size * 0.55)
        perp_y = ux * (arrow_size * 0.55)

        self.elements.append(
            f'<line x1="{sx0:.1f}" y1="{sy0:.1f}" x2="{px:.1f}" y2="{py:.1f}" stroke="{color}" stroke-width="{width}"/>'
        )
        self.elements.append(
            f'<polygon points="{sx1:.1f},{sy1:.1f} {px + perp_x:.1f},{py + perp_y:.1f} {px - perp_x:.1f},{py - perp_y:.1f}" fill="{color}"/>'
        )
        if label:
            mid_x = (sx0 + sx1) / 2.0 + perp_x * 2.0
            mid_y = (sy0 + sy1) / 2.0 + perp_y * 2.0
            self.elements.append(
                f'<text x="{mid_x:.1f}" y="{mid_y:.1f}" fill="{color}" font-family="sans-serif" font-size="12" font-weight="bold">{label}</text>'
            )

    def draw_arrow(self, x0: float, y0: float, x1: float, y1: float, color: str = "#38bdf8", width: float = 2.5, label: str = ""):
        sx0, sy0 = self.to_screen(x0, y0)
        sx1, sy1 = self.to_screen(x1, y1)
        self.draw_arrow_screen(sx0, sy0, sx1, sy1, color=color, width=width, label=label)

    def draw_polygon(self, pts: Sequence[Sequence[float]], fill: str = "rgba(56, 189, 248, 0.2)", stroke: str = "#38bdf8", width: float = 2.0, label: str = ""):
        screen_pts = [self.to_screen(p[0], p[1]) for p in pts]
        pts_str = " ".join(f"{sx:.1f},{sy:.1f}" for sx, sy in screen_pts)
        self.elements.append(
            f'<polygon points="{pts_str}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'
        )
        if label and len(screen_pts) > 0:
            cx = sum(p[0] for p in screen_pts) / len(screen_pts)
            cy = sum(p[1] for p in screen_pts) / len(screen_pts)
            self.elements.append(
                f'<text x="{cx:.1f}" y="{cy:.1f}" fill="{stroke}" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold">{label}</text>'
            )

    def draw_polyline(self, pts: Sequence[Sequence[float]], stroke: str = "#e2e8f0", width: float = 2.0, dashed: bool = False):
        screen_pts = [self.to_screen(p[0], p[1]) for p in pts]
        pts_str = " ".join(f"{sx:.1f},{sy:.1f}" for sx, sy in screen_pts)
        dash_attr = 'stroke-dasharray="5,5"' if dashed else ''
        self.elements.append(
            f'<polyline points="{pts_str}" fill="none" stroke="{stroke}" stroke-width="{width}" {dash_attr}/>'
        )

    def render(self) -> str:
        """Devuelve el código SVG completo envuelto en contenedor responsivo."""
        body = "\n".join(self.elements)
        svg_code = f'''
        <div style="display:flex; justify-content:center; margin: 10px 0;">
            <svg width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg" style="border-radius:12px; box-shadow: 0 8px 24px rgba(0,0,0,0.35);">
                {body}
            </svg>
        </div>
        '''
        return svg_code
