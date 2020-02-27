from matplotlib import pyplot as plt


def bar_graph(stats, days=7):
    x = stats.index[-days:]
    y1 = stats['flightsCount'][-days:]
    y2 = stats['vsWeek'][-days:]
    y3 = stats['vsMonth'][-days:]

    color_main = '#6c9bff'
    color_inc = '#98ff88'
    color_exc = '#ff6752'
    colors2 = [color_exc if i < 0 else color_inc for i in y2]
    colors3 = [color_exc if i < 0 else color_inc for i in y3]

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(days, 10))
    ax2.axhline(0, color='black', linewidth=0.5)
    ax3.axhline(0, color='black', linewidth=0.5)

    rects1 = ax1.bar(x, y1, color=color_main)
    rects2 = ax2.bar(x, y2, color=colors2)
    rects3 = ax3.bar(x, y3, color=colors3)

    def autolabel(axis, rects, diff=()):
        sign = lambda a: -1 if a < 0 else 1
        for i, rect in enumerate(rects):
            height = rect.get_height()
            if len(diff) and diff[i] != 0:
                axis.annotate('{} ({})'.format(height, diff[i]),
                              xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, sign(height) * 10),
                              textcoords="offset points", ha='center', va='center')
            else:
                axis.annotate('{}'.format(height), xy=(rect.get_x() + rect.get_width() / 2, height),
                              xytext=(0, sign(height) * 10), textcoords="offset points",
                              ha='center', va='center')
    autolabel(ax1, rects1, y2)
    autolabel(ax2, rects2)
    autolabel(ax3, rects3)
    ax1.margins(y=0.15)
    ax2.margins(y=0.15)
    ax3.margins(y=0.15)
    plt.subplots_adjust(hspace=0.5)
    ax1.set_title('amount of flights')
    ax2.set_title('compared to last week')
    ax3.set_title('compared to mean for last month')
