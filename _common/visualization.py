from matplotlib import pyplot as plt


def bar_graph(stats, days=7):
    x = stats.index[-days:]
    y_count = stats['flightsCount'][-days:]
    y_week_excess = stats['vsWeek +'][-days:]
    y_week_missing = stats['vsWeek -'][-days:]
    y_month = stats['vsMonth'][-days:]

    color_main = '#6c9bff'
    color_excess = '#98ff88'
    color_missing = '#ff6752'
    colors_month = [color_missing if i < 0 else color_excess for i in y_month]

    fig, (ax_count, ax_week, ax_month) = plt.subplots(3, 1, figsize=(days, 10))
    ax_week.axhline(0, color='black', linewidth=0.5)
    ax_month.axhline(0, color='black', linewidth=0.5)

    rects_count = ax_count.bar(x, y_count, color=color_main)
    rects_week_excess = ax_week.bar(x, y_week_excess, color=color_excess)
    rects_week_missing = ax_week.bar(x, -y_week_missing, color=color_missing)
    rects_month = ax_month.bar(x, y_month, color=colors_month)

    def autolabel(axis, rects, diff=()):
        sign = lambda a: -1 if a < 0 else 1
        for i, rect in enumerate(rects):
            height = rect.get_height()
            if len(diff) and diff[i] != 0:  # additional text for amount difference
                axis.annotate('{} ({})'.format(height, diff[i]),
                              xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, sign(height) * 10),
                              textcoords="offset points", ha='center', va='center')
            else:
                axis.annotate('{}'.format(height), xy=(rect.get_x() + rect.get_width() / 2, height),
                              xytext=(0, sign(height) * 10), textcoords="offset points",
                              ha='center', va='center')
    autolabel(ax_count, rects_count, y_week_excess-y_week_missing)
    autolabel(ax_week, rects_week_excess)
    autolabel(ax_week, rects_week_missing)
    autolabel(ax_month, rects_month)
    ax_count.margins(y=0.15)
    ax_week.margins(y=0.15)
    ax_month.margins(y=0.15)
    plt.subplots_adjust(hspace=0.2)
    ax_count.set_title('amount of flights')
    ax_week.set_title('compared to last week')
    ax_month.set_title('compared to mean for last month')
