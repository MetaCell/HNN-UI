import holoviews as hv
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.layouts import layout

hv.extension('bokeh')


def get_experimental_plot(exp_data=None, fig_size=(40, 8)):
    if exp_data is None or not exp_data['x'] or not exp_data['y']:
        return ""
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"
    fig = figure(title="Dipole Plot", tools=TOOLS, plot_width=fig_size[0], plot_height=fig_size[1])
    fig.line(exp_data['x'], exp_data['y'], color='black', legend=exp_data['label'])
    plot_layout = layout(fig, sizing_mode='stretch_both')
    html = file_html(plot_layout, CDN, title="Dipole Plot")
    return html
