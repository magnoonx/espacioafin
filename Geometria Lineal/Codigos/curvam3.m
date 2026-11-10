t = linspace(0, 2*pi, 70);  % Parámetro

% Definir la curva paramétrica en el espacio R^3
x = cos(t);
y = sin(t);
z = t;

% Calcular las derivadas de primer, segundo y tercer orden
dx_dt = -sin(t);
dy_dt = cos(t);
dz_dt = ones(size(t));

d2x_dt2 = -cos(t);
d2y_dt2 = -sin(t);
d2z_dt2 = zeros(size(t));

d3x_dt3 = sin(t);
d3y_dt3 = -cos(t);
d3z_dt3 = zeros(size(t));

% Graficar la curva y los vectores tangente, normal y binormal
figure;
plot3(x, y, z, 'b', 'LineWidth', 2);
hold on;
quiver3(x, y, z, dx_dt, dy_dt, dz_dt, 'r', 'LineWidth', 1.5, 'MaxHeadSize', 0.5, 'AutoScale', 'off');
quiver3(x, y, z, d2x_dt2, d2y_dt2, d2z_dt2, 'g', 'LineWidth', 1.5, 'MaxHeadSize', 0.5, 'AutoScale', 'off');
quiver3(x, y, z, d3x_dt3, d3y_dt3, d3z_dt3, 'm', 'LineWidth', 1.5, 'MaxHeadSize', 0.5, 'AutoScale', 'off');
xlabel('x');
ylabel('y');
zlabel('z');
legend('Curva paramétrica', 'Vector tangente', 'Vector normal', 'Vector Ortonormal');
hold off;

