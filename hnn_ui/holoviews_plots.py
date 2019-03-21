import numpy as np
import holoviews as hv
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.layouts import layout
hv.extension('bokeh')


def _plot(color1, color2):
    
    x = np.linspace(0, 4*np.pi, 100)
    y = np.sin(x)

    scatter1 = hv.Scatter((x, y), label='sin(x)')
    scatter2 = hv.Scatter((x, y*2), label='2*sin(x)').opts(color=color1)
    scatter3 = hv.Scatter((x, y*3), label='3*sin(x)').opts(color=color2)
    scatter4 = hv.Scatter(scatter3).opts(line_color=color2, marker='square', fill_alpha=0, size=5)

    curve1 = hv.Curve(scatter1)
    curve2 = hv.Curve(scatter2).opts(line_dash=(4, 4), color=color1)
    curve3 = hv.Curve(scatter3).opts(color=color1)

    example = scatter1 * curve1 * curve2 * scatter4 * curve3

    example.relabel("Dipole Dummy Example")

    bokeh_plot = hv.renderer('bokeh').get_plot(example)
    plot_layout = layout(bokeh_plot.state, sizing_mode='scale_both')
    html = file_html(plot_layout, CDN, "dipole")

    return html


def get_dipole():
    return _plot('green', 'orange')


def get_traces():
    return _plot('blue', 'yellow')


def get_psd():
    return _plot('red', 'black')


def get_raster():
    return _plot('gray', 'green')


def get_spectrogram():
    return _plot('brown', 'blue')
