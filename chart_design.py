import numpy as np
from matplotlib.colors import hex2color, rgb2hex

tableau_palette = ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2',
                   '#59a14f', '#edc948', '#b07aa1', '#ff9da7', '#9c755f',
                   '#bab0ac']

BG_COLOR = '#EFECEA'
LEGEND_BG_COLOR = '#E5E2E0'
LEGEND_BORDER_COLOR = '#C0C0BB'
DARK_TEXT_COLOR = '#635f5d'
LIGHT_TEXT_COLOR = '#8E8883'
#
FONT_FAMILY = 'IBM Plex Sans Condensed'
#


def light_palette(color_palette=tableau_palette,
                  mixing_color=BG_COLOR,
                  mixing_factor=0.75):
    '''This function provides a lighter shade of a color palette.

    Args:
        color_palette (list(str), default: tableau_palette):
            list of colors in hex format
        mixing_color (str, default: #efecea): color to mix the palette with

    Returns:
        light_palette (list(str))
    '''
    tp_rgb = map(lambda s: np.array(hex2color(s)), color_palette)
    mixing_color_rgb = np.array(hex2color(mixing_color))
    light_palette = map(
        lambda c: rgb2hex(mixing_factor * c + (1. - mixing_factor) * mixing_color_rgb),
        tp_rgb)
    return list(light_palette)

# The following functions are inspired from
# http://sunlightfoundation.com/blog/2014/03/12/datavizguide/


def layout_with_titles(
        height=450, width=450 * (1. + np.sqrt(5)) / 2,
        font_family=FONT_FAMILY, font_size=16, r=(1. + np.sqrt(5)) / 2,
        bgcolor=BG_COLOR, dark_text_color=DARK_TEXT_COLOR, light_text_color=LIGHT_TEXT_COLOR,
        title='title', subtitle='', ylabel='ylabel', xlabel='xlabel',
        margin=None,
        **kwargs):
    '''This function returns a dictionary to be used in
    plotly.graph_objs.Figure(data=data, layout=dict_general_new()). The axes
    labels and title are handled by annotation instead of the axes themselves
    in order to use horizontal labelling for the vertical axis. The input
    margin helps in fixing the position of the title and axis labels whatever
    the size of the figure: the title and Y-label are 20px off the left side
    and 10px from the top while the X-label is 10px from the bottom.

    Args:
        height, width (float, defaults: 450, 450 * (1. + np.sqrt(5.)) / 2)
        font_family (str, default: 'PT Sans Narrow'): font family
        font_size (int, default: 20): font size of labels
        r (float, default: (1. + np.sqrt(5)) / 2): ratio between the labels and the title font size (r * font_size)
        title, ylabel, xlabel (str, defaults: 'title', 'ylabel', 'xlabel'): title and axes labels
        margin (dict, default: dict(l=80, r=80, t=100, b=80))

    Returns:
        dict: dictionary containing the parameters of the layout
    '''
    if margin is None:
        margin = dict(l=80, r=80, t=100, b=80)
    if subtitle:
        margin['t'] = 150
        y_label_tilt = 50
        d_subtitle = dict(
            x=-(margin['l'] - 20) / (width - margin['l'] - margin['r']),
            y=1 + (margin['t'] - 10 - (font_size + 8) - 10) / (height - margin['b'] - margin['t']),
            font=dict(size=font_size - 2, color=dark_text_color),
            xref='paper',
            xanchor='left',
            yref='paper',
            yanchor='top',
            text=subtitle,
            align='left',
            showarrow=False)
    else:
        y_label_tilt = 0
        d_subtitle = dict()

    labels = [
        dict(
            x=-(margin['l'] - 20) / (width - margin['l'] - margin['r']),
            y=1 + (margin['t'] - 10) / (height - margin['b'] - margin['t']),
            font=dict(size=font_size + 8, color=dark_text_color),
            xref='paper',
            xanchor='left',
            yref='paper',
            yanchor='top',
            text=title,
            showarrow=False
        ),
        dict(
            x=-(margin['l'] - 20) / (width - margin['l'] - margin['r']),
            y=1 + (margin['t'] - 10 - (font_size + 8) - 20 - y_label_tilt) /
            (height - margin['b'] - margin['t']),
            font=dict(size=font_size, color=dark_text_color),
            xref='paper',
            xanchor='left',
            yref='paper',
            yanchor='top',
            text=ylabel,
            showarrow=False
        ),
        dict(
            x=0.5,
            y=-(margin['b'] - 10) / (height - margin['b'] - margin['t']),
            font=dict(size=font_size, color=light_text_color),
            xref='paper',
            xanchor='center',
            yref='paper',
            yanchor='bottom',
            text=xlabel,
            showarrow=False
        )]
    if d_subtitle:
        labels.append(d_subtitle)
    layout = dict(
        width=width,
        height=height,
        font=dict(family=font_family),
        hoverlabel=dict(font=dict(family=font_family)),
        plot_bgcolor=bgcolor,
        paper_bgcolor=bgcolor,
        margin=margin,
        annotations=labels)
    layout.update(kwargs)

    return layout


def axis_no_title(
        font_size=14,
        ticklen=5,
        showgrid=True, gridcolor='#ffffff', gridwidth=2,
        zeroline=False, linewidth=6, linecolor=BG_COLOR,
        **kwargs):
    '''
    This function returns the parameters for an axis.

    Args:
        font_size (int, default: 18): font size
        ticklen (int, default: 5)
        showgrid (bool, default: True)
        gridcolor (str, default: '#ffffff')
        gridwidth (int, default: 2): manages the tick width too
        zeroline (bool, default: False): show line for the axis
        linewidth (int, default: 6),
        linecolor (str, default: BG_COLOR)

    Returns:
        dict: dictionary containing the parameters of the axis
    '''
    d = dict(
        tickfont=dict(size=font_size),
        ticklen=ticklen,
        tickwidth=gridwidth,
        showgrid=showgrid,
        gridcolor=gridcolor,
        gridwidth=gridwidth,
        zeroline=zeroline,
        linewidth=linewidth,
        linecolor=linecolor
    )
    d.update(kwargs)
    return d


def legend_dark(
        bgcolor=LEGEND_BG_COLOR,
        bordercolor=LEGEND_BORDER_COLOR, borderwidth=1,
        font_size=16, font_color=DARK_TEXT_COLOR,
        traceorder='normal',
        xanchor='left', x=1.05, yanchor='bottom', y=0.,
        **kwargs):
    '''
    This function returns the parameters for the legend. The position is
    determined in regards of the plotting area (paperref).

    Args:
        bgcolor (str, default: LEGEND_BG_COLOR)
        bordercolor (str, default: LEGEND_BORDER_COLOR)
        borderwidth (int, default: 1)
        font_size (int, default: 20)
        font_color (str, default: DARK_TEXT_COLOR)
        traceorder (str, default:'normal')
        xanchor (str, default: 'left')
        x (float, default: 1.05): legend X position
        yanchor (str, default: 'bottom')
        y (float, default: 0.): legend Y position
    '''
    legend = dict(
        traceorder=traceorder,
        bgcolor=bgcolor,
        bordercolor=bordercolor,
        borderwidth=borderwidth,
        font=dict(size=font_size, color=font_color),
        xanchor=xanchor,
        x=x,
        yanchor=yanchor,
        y=y
    )
    legend.update(kwargs)
    return legend


def main():
    pass


if __name__ == '__main__':
    main()
