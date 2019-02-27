import numpy as np
import holoviews as hv
from bokeh.resources import CDN
from bokeh.embed import file_html
hv.extension('bokeh')

def get_dipole():
    
    x = np.linspace(0, 4*np.pi, 100)
    y = np.sin(x)

    scatter1 = hv.Scatter((x, y), label='sin(x)')
    scatter2 = hv.Scatter((x, y*2), label='2*sin(x)').opts(color='orange')
    scatter3 = hv.Scatter((x, y*3), label='3*sin(x)').opts(color='green')
    scatter4 = hv.Scatter(scatter3).opts(line_color='green', marker='square', fill_alpha=0, size=5)

    curve1 = hv.Curve(scatter1)
    curve2 = hv.Curve(scatter2).opts(line_dash=(4, 4), color='orange')
    curve3 = hv.Curve(scatter3).opts(color='orange')

    example = scatter1 *  curve1 * curve2 * scatter4 * curve3

    example.relabel("Dipole Dummy Example")

    bokeh_plot =  hv.renderer('bokeh').get_plot(example).state
    html = file_html(bokeh_plot, CDN, "my plot")

    return html