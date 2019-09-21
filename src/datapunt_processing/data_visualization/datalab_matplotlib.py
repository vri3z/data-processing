import brewer2mpl
import matplotlib as mpl
import matplotlib.image as image
import matplotlib.pyplot as plt
from matplotlib.rcsetup import cycler

# look at the map @http://colorbrewer2.org, pick a set and map to a variable
gmap = brewer2mpl.get_map('YlOrRd', 'Sequential', 7, reverse=True).hex_colors

mpl.rcParams['figure.figsize'] = (10, 6)
mpl.rcParams['figure.dpi'] = 150
mpl.rcParams['axes.prop_cycle'] = cycler('color', gmap)
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['axes.facecolor'] = 'white'
mpl.rcParams['font.size'] = 14
mpl.rcParams['patch.edgecolor'] = 'white'
mpl.rcParams['patch.facecolor'] = gmap[0]
mpl.rcParams['font.family'] = 'StixGeneral'
mpl.rcParams['axes.titlepad'] = 10
mpl.rcParams['figure.constrained_layout.use'] = True


def datalab_default(
        axes=None,
        show_axes=(True, False, True, False),
        grid=None,
        xlim=None,
        ylim=None,
        title=None,
        xlabel=None,
        ylabel=None,
        labelpad=15,
        add_datalab_logo=None
):
    """
    Produces a clean default Matplotlib plot with minimize chartjunk.
    Args:
        axes: axes to be used for the plot
        show_axes: (left, right, bottom, top) show or not
        grid : grid to be shown in plot. Default is False
        xlim: tuple containing x axis limits (start, end)
        ylim: tuple containting y axis limits (start, end)
        title: title to be shon on top of the plot. Default is False
        xlabel: Empty if none, else show xlabel
        ylabel: Empty if none, else show ylabel
        labelpad: Space between graph and labels
        add_datalab_logo: if True places Gemeente logo in the plot (top right)

    returns
        an empty axes object on which data can be plotted
    """
    left, right, bottom, top = show_axes

    ax = axes or plt.gca()
    ax.spines['top'].set_visible(top)
    ax.spines['right'].set_visible(right)
    ax.spines['left'].set_visible(left)
    ax.spines['bottom'].set_visible(bottom)

    # turn off all ticks
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')

    # re-enable visibles for tweaking
    if top:
        ax.xaxis.tick_top()
    if bottom:
        ax.xaxis.tick_bottom()
    if left:
        ax.yaxis.tick_left()
    if right:
        ax.yaxis.tick_right()

    if isinstance(xlim, tuple):
        ax.set_xlim(xlim)
    if isinstance(ylim, tuple):
        ax.set_ylim(ylim)

    if grid is not None or grid != 'off':
        assert grid in ('x', 'y', 'both')
        ax.grid(axis=grid, color='gray', linestyle='--', linewidth=0.3, alpha=.3)

    if title:
        ax.set_title(title, pad=labelpad)
    if xlabel:
        ax.set_xlabel(xlabel, labelpad=labelpad)
    if ylabel:
        ax.set_ylabel(ylabel, labelpad=labelpad)

    if add_datalab_logo:
        # adding Gemeente Watermark Image on the top right of the plot
        logo = image.imread('AMS.jpg')
        ax.figure.figimage(
            logo,
            xo=int((ax.figure.get_figwidth() * ax.figure.dpi)) - logo.shape[1],
            yo=int((ax.figure.get_figheight() * ax.figure.dpi)) - logo.shape[0],
            alpha=.3,
            zorder=1
        )

    return ax
