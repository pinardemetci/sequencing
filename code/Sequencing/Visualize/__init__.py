import igv_colors
import scipy.stats
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def optional_ax(original_function):
    def possibly_new_ax(*args, **kwargs):
        ax_given = kwargs.get('ax')
        if not ax_given:
            fig, ax = plt.subplots(figsize=(12, 8))
            kwargs['ax'] = ax
        
        result = original_function(*args, **kwargs)
        
        figure_file_name = kwargs.get('save_as')
        if figure_file_name:
            assert not ax_given, 'Can\'t give ax and figure_file_name'
            fig.savefig(figure_file_name, bbox_inches='tight')
            plt.close(fig)
        
        return result
    
    return possibly_new_ax

def add_commas_to_yticks(ax):
    def commas_formatter(x, pos):
        return '{0:,}'.format(int(x))
    tick_formatter = matplotlib.ticker.FuncFormatter(commas_formatter)
    ax.yaxis.set_major_formatter(tick_formatter)

def enhanced_scatter(x_list,
                     y_list,
                     x_label,
                     y_label,
                     title,
                     ax_scatter,
                     lims=None,
                     color_by_density=True,
                     do_fit=True,
                    ):
    same_lists = np.allclose(x_list, y_list)

    if color_by_density and not same_lists:
        sampled_points = np.vstack([x_list[:10000], y_list[:10000]])
        points = np.vstack([x_list, y_list])
        kernel = scipy.stats.gaussian_kde(sampled_points)
        colors = kernel(points)
    else:
        colors = np.ones_like(x_list)

    if same_lists:
        do_fit = False

    kwargs = {'cmap': matplotlib.cm.jet,
              's': 4,
              'linewidths' : (0.1,),
             }

    ax_scatter.scatter(x_list, y_list, c=colors, **kwargs)

    ax_scatter.set_xlabel(x_label)
    ax_scatter.set_ylabel(y_label)

    ax_scatter.set_title(title)

    if do_fit:
        fit = np.polyfit(x_list, y_list, 1)
        beta, _ = fit
        fit_function = np.poly1d(fit)
        xs = ax_scatter.get_xlim()
        ax_scatter.plot(xs, fit_function(xs), color='black', alpha=0.5)
        ax_scatter.set_xlim(min(x_list), max(x_list))
        
        r, p = scipy.stats.pearsonr(x_list, y_list)
        ax_scatter.annotate('r = {:0.2f}, p={:0.2e}'.format(r, p),
                            xy=(1, 0),
                            xycoords='axes fraction',
                            xytext=(-10, 15),
                            textcoords='offset points',
                            horizontalalignment='right',
                           )
        ax_scatter.annotate(r'$\beta$ = {:0.2f}'.format(beta),
                            xy=(1, 0),
                            xycoords='axes fraction',
                            xytext=(-10, 30),
                            textcoords='offset points',
                            horizontalalignment='right',
                           )
    
    ax_scatter.set_aspect(1.)
    if lims:
        ax_scatter.set_xlim(*lims)
        ax_scatter.set_ylim(*lims)
