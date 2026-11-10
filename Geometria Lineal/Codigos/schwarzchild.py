from einsteinpy.hypersurface import SchwarzschildEmbedding
from einsteinpy.plotting import HypersurfacePlotter
from astropy import units as u
# Declarar el peso de un agujero de gusano hipermasivo
surface_obj = SchwarzschildEmbedding(5.927e25 * u.kg)
# Plotear el resultado
surface = HypersurfacePlotter(embedding=surface_obj, plot_type='surface')
surface.plot()
surface.show()