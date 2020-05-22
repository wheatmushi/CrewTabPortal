from matplotlib import pyplot as plt
from matplotlib import gridspec
import numpy as np
from datetime import datetime


def autolabel(axis, rects, diff=np.empty(0), shift=0):
    sign = lambda a: -1 if a < 0 else 1
    for i, rect in enumerate(rects):
        height = rect.get_height()
        height_print = height if height != 0 else ''
        if diff.any():
            diff_print = ' ({})'.format(diff[i]) if diff[i] != 0 else ''
            fontsize = 8
        else:
            diff_print = ''
            fontsize = 9
        axis.annotate('{}{}'.format(height_print, diff_print),
                      xy=(rect.get_x() + rect.get_width() / 2, height),
                      xytext=(shift*3, sign(height) * 10),
                      textcoords="offset points",
                      ha='center',
                      va='center',
                      fontsize=fontsize)


def draw_bars(ax, df, columns, depth, title, graph_type='regular', add_lables=np.empty(0)):
    color_main = '#6c9bff'
    color_excess = '#98ff88'
    color_missing = '#ff6752'

    width = 0.8
    scale = 1+int((depth-1)/10)

    columns_amount = len(columns)
    y = []
    colors = []

    x = df['date'][-depth:]
    for i in range(columns_amount):
        y.append(df[columns[i]][-depth:])

        if graph_type == 'difference':
            colors.append([color_missing if t < 0 else color_excess for t in y[i]])
            ax.axhline(0, color='black', linewidth=0.5)
        else:
            colors.append(color_main)

        rects = ax.bar(x, y[i], width=width, color=colors[i])
        additional_lables = add_lables[-depth:]
        if depth < 18:
            autolabel(ax, rects, additional_lables)

    ax.set_xticks(x[::scale])
    ax.set_xticklabels(x[::scale])
    ax.set_title(title)


def plot_bars(df, columns, depth, title, graph_type='regular', add_lables=np.empty(0), figsize=(8.45,3), save=True, filename=None):
    plt.figure(figsize=figsize)
    color_main = '#6c9bff'
    color_excess = '#98ff88'
    color_missing = '#ff6752'

    width = 0.8
    scale = 1+int((depth-1)/10)

    columns_amount = len(columns)
    y = []
    colors = []

    x = df['date'][-depth:]
    for i in range(columns_amount):
        y.append(df[columns[i]][-depth:])

        if graph_type == 'difference':
            colors.append([color_missing if t < 0 else color_excess for t in y[i]])
            plt.axhline(0, color='black', linewidth=0.5)
        else:
            colors.append(color_main)

        rects = plt.bar(x, y[i], width=width, color=colors[i])
        additional_lables = add_lables[-depth:]
        if depth < 18:
            autolabel(plt, rects, additional_lables)

    plt.xticks(x[::scale], x[::scale])
    plt.title(title)
    plt.margins(y=0.15)
    plt.tight_layout()
    if save:
        plt.savefig('../_DB/stat_imgs/{}_{}_days.svg'.format(filename, '0' * (2-len(str(depth))) + str(depth)))
        plt.close()


def draw_bars_double(ax, x, y, depth, title, shift=0, add_lables=()):
    color_0 = '#80a8ff'
    color_1 = '#b3cbff'

    x_labels = x[-depth:]
    x = np.arange(len(x_labels))
    y[0] = y[0][-depth:]
    y[1] = np.append(y[1][-depth+shift:], np.zeros(shift, dtype='int'))

    width = 0.4
    scale = 1 + int((depth-1)/25)

    rects0 = ax.bar(x-width/2, y[0], width, color=color_0)
    rects1 = ax.bar(x+width/2, y[1], width, color=color_1)

    ax.set_xticks(x[::scale])
    ax.set_xticklabels(x_labels[::scale])

    additional_lables0 = add_lables[0][-depth:]
    additional_lables1 = np.append(add_lables[1][-depth+shift:], np.zeros(shift, dtype='int'))
    if depth < 15:
        autolabel(ax, rects0, additional_lables0, shift=-shift)
        autolabel(ax, rects1, additional_lables1, shift=shift)

    ax.legend(('flights', 'reports'))
    ax.set_title(title)


def plot_bars_double(x, y, depth, title, shift=0, add_lables=(), figsize=(20, 3), save=True, filename=None):
    plt.figure(figsize=figsize)
    color_0 = '#80a8ff'
    color_1 = '#b3cbff'

    x_labels = x[-depth:]
    x = np.arange(len(x_labels))
    y[0] = y[0][-depth:]
    y[1] = np.append(y[1][-depth+shift:], np.zeros(shift, dtype='int'))

    width = 0.4
    scale = 1 + int((depth-1)/25)

    rects0 = plt.bar(x-width/2, y[0], width, color=color_0)
    rects1 = plt.bar(x+width/2, y[1], width, color=color_1)

    plt.xticks(x[::scale], x_labels[::scale])

    additional_lables0 = add_lables[0][-depth:]
    additional_lables1 = np.append(add_lables[1][-depth+shift:], np.zeros(shift, dtype='int'))
    if depth < 15:
        autolabel(plt, rects0, additional_lables0, shift=-shift)
        autolabel(plt, rects1, additional_lables1, shift=shift)

    plt.legend(('flights', 'reports'))
    plt.title(title)
    plt.margins(y=0.15)
    plt.tight_layout()
    if save:
        plt.savefig('../_DB/stat_imgs/{}_{}_days.svg'.format(filename, '0' * (2-len(str(depth))) + str(depth)))
        plt.close()


def draw_dashboard(stats_flights, stats_reports, stats_reports_for_hour, depth=9, save=False):
    print('drawing graphs...')
    fig = plt.figure(figsize=(20, 9))
    grid = gridspec.GridSpec(ncols=2, nrows=3, figure=fig)
    ax_top = fig.add_subplot(grid[0, :])
    axis = [fig.add_subplot(grid[i, j:j + 1]) for i in range(1, 3) for j in range(2)]

    draw_bars_double(ax=ax_top,  # pared flights and reports amount
                     x=stats_flights['date'],
                     y=[stats_flights['flightsCount'], stats_reports_for_hour['byDepartureDate']],
                     depth=depth,
                     title='amount of flights (vs previous week) and purser reports (vs yesterday)',
                     shift=2,
                     add_lables=[stats_flights['vsWeek +'] + stats_flights['vsWeek -'],
                                 stats_reports_for_hour['vsYesterday'].values])

    draw_bars(ax=axis[0],  # flights amount compared to last month's mean values for every weekday
              df=stats_flights,
              columns=['vsMonth'],
              depth=depth,
              title='flights amount compared to mean for last month',
              graph_type='difference')

    draw_bars(ax=axis[2],
              # flights amount compared to previous week (added flight numbers in green and missing in red)
              df=stats_flights,
              columns=['vsWeek +', 'vsWeek -'],
              depth=depth,
              title='flights amount compared to previous week (green = new, red = missing)',
              graph_type='difference')

    draw_bars(ax=axis[1],  # reports amount (described above) compared to mean amount for month
              df=stats_reports_for_hour,
              columns=['vsMonth %'],
              depth=depth,
              title='reports amount compared to mean for last month, %',
              graph_type='difference')

    draw_bars(ax=axis[3],  #
              df=stats_reports_for_hour.iloc[:-1, :],
              columns=['vsFlights'],
              depth=depth,
              title='missing reports',
              graph_type='difference')

    ax_top.margins(y=0.15)
    for ax in axis:
        ax.margins(y=0.15)
    plt.subplots_adjust(hspace=0.3)
    fig.tight_layout()
    time = datetime.now().strftime('%D %H:%M')
    fig.text(0.99, 0.99, 'last data check ' + time, horizontalalignment='right', verticalalignment='top')
    if save:
        plt.savefig('../_DB/stat_imgs/dash_{}_days.svg'.format(depth))
        plt.close(fig)


def plot_dashboard_imgs(stats_flights, stats_reports_for_hour, depth):
    print('drawing graphs...')
    plot_bars_double(x=stats_flights['date'],  # pared flights and reports amount
                     y=[stats_flights['flightsCount'], stats_reports_for_hour['byDepartureDate']],
                     depth=depth,
                     title='amount of flights (vs previous week) and purser reports (vs yesterday)',
                     shift=2,
                     add_lables=[stats_flights['vsWeek +'] + stats_flights['vsWeek -'],
                                 stats_reports_for_hour['vsYesterday'].values],
                     filename='amount')

    plot_bars(df=stats_flights,  # flights amount compared to last month's mean values for every weekday
              columns=['vsMonth'],
              depth=depth,
              title='flights amount compared to mean for last month',
              graph_type='difference',
              filename='flights_vs_mean')

    plot_bars(df=stats_flights,
              # flights amount compared to previous week (added flight numbers in green and missing in red)
              columns=['vsWeek +', 'vsWeek -'],
              depth=depth,
              title='flights amount compared to previous week (green = new, red = missing)',
              graph_type='difference',
              filename='flights_vs_week')

    plot_bars(df=stats_reports_for_hour,  # reports amount (described above) compared to mean amount for month
              columns=['vsMonth %'],
              depth=depth,
              title='reports amount compared to mean for last month, %',
              graph_type='difference',
              filename='reports_vs_mean')

    plot_bars(df=stats_reports_for_hour.iloc[:-1, :],
              columns=['vsFlights'],
              depth=depth,
              title='missing reports',
              graph_type='difference',
              filename='reports_vs_flights')
