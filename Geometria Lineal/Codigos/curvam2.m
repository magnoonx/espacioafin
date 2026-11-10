t = linspace(0, 2*pi, 15);  % Parámetro

% Definir la curva paramétrica: x(t) = t, y(t) = t^2
x = t;
y = t.^2;

% Calcular las derivadas de primer, segundo y tercer orden
dx_dt = ones(size(t));
dy_dt = 2*t;
d2x_dt2 = zeros(size(t));
d2y_dt2 = 2*ones(size(t));
d3x_dt3 = zeros(size(t));
d3y_dt3 = zeros(size(t));

% Graficar la curva
figure;
plot(x, y, 'b', 'LineWidth', 2);
hold on;
quiver(x, y, dx_dt, dy_dt, 'r', 'LineWidth', 1.5);
quiver(x, y, d2x_dt2, d2y_dt2, 'g', 'LineWidth', 1.5);
quiver(x, y, d3x_dt3, d3y_dt3, 'm', 'LineWidth', 1.5);
legend('Curva paramétrica', 'Vector tangente', 'Vector de curvatura', 'Vector de torsión');
axis equal;
hold off;

