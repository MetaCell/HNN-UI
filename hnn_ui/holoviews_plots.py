import numpy as np
import holoviews as hv
from holoviews import opts, dim
import pandas as pd
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.layouts import layout
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

    bokeh_plot = hv.renderer('bokeh').get_plot(example)
    plot_layout = layout(bokeh_plot.state, sizing_mode='scale_both')
    html = file_html(plot_layout, CDN, "dipole")

    return html


def get_traces():

    return get_dipole()


def get_psd():
    return get_dipole()


def get_raster():
    return get_dipole()


def get_spectrogram():
    return get_dipole()
