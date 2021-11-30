import matplotlib.pyplot as plt


def plot_(data, step, smooth=True, show_plot=False, save_chart=False):
    fig, axs = plt.subplots(4, 2)

    fig.set_figheight(10)
    fig.set_figwidth(10)

    if smooth:
        data = [d.rolling(max(1, int(len(d)/10)), center=True).mean() for d in data]

    ds1, ds2 = data

    # Entropy Col
    columns = ds1.columns
    axs[0, 0].title.set_text("Entropy")

    l1, l2 = axs[0, 0].plot(ds1[columns[0:2]])
    axs[0, 0].legend((l1, l2), (columns[0], columns[1]), loc='best')

    l3, l4 = axs[1, 0].plot(ds1[columns[2:4]])
    axs[1, 0].legend((l3, l4), (columns[2], columns[3]), loc='best')

    axs[2, 0].plot(ds1[columns[4]], label=columns[4])
    axs[2, 0].legend(loc='best')

    axs[3, 0].plot(ds1[columns[5]], label=columns[5])
    axs[3, 0].legend(loc='best')

    # Emergence Col
    columns = ds2.columns
    axs[0, 1].title.set_text("Emergence")

    l1, l2 = axs[0, 1].plot(ds2[columns[0:2]])
    axs[0, 1].legend((l1, l2), (columns[0], columns[1]), loc='best')

    l3, l4 = axs[1, 1].plot(ds2[columns[2:4]])
    axs[1, 1].legend((l3, l4), (columns[2], columns[3]), loc='best')

    axs[2, 1].plot(ds2[columns[4]], label=columns[4])
    axs[2, 1].legend(loc='best')

    axs[3, 1].plot(ds2[columns[5]], label=columns[5])
    axs[3, 1].legend(loc='best')

    plt.tight_layout()
    plt.subplots_adjust(hspace=0)

    if save_chart:
        plt.savefig(fname=f"charts/t{step}.jpg")
    if show_plot:
        plt.show()

    plt.close(fig)
