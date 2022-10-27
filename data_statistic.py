import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib import gridspec
import numpy as np

df = pd.read_json('drivers_messages.json')

def hist(param, plot_size, bins, title='', xlabel_name='', ylabel_name=''):
    fig, ax = plt.subplots(1, figsize=plot_size)
    plt.title(f'{title}', loc='center', fontsize=14)
    plt.xlabel(f'\n{xlabel_name}', fontsize=12)
    plt.ylabel(f'{ylabel_name}', fontsize=12)

    n, bins, patches = plt.hist(df[param], edgecolor='w', bins=bins)
    binspie = bins

    minor_locator = AutoMinorLocator(2)
    plt.gca().xaxis.set_minor_locator(minor_locator)
    plt.grid(which='minor', color='white', lw=0.5)

    plt.grid(axis='y', color='#3475D0', lw=0.5, alpha=0.5)

    xticks = [(bins[idx + 1] + value) / 2 for idx, value in enumerate(bins[:-1])]
    xticks_labels = ["[{:.2f},\n{:.2f}]".format(value, bins[idx + 1]) for idx, value in enumerate(bins[:-1])]
    plt.xticks(xticks, labels=xticks_labels, fontsize=8)
    for idx, value in enumerate(n):
        if value > 0:
            plt.text(xticks[idx], value + 5, int(value), ha='center')

    plt.savefig(f'./plot images/hist_{param}.png')
    plt.clf()
    return bins

def plot(param):
    fig, ax = plt.subplots(1, figsize=(12, 7))

    plt.title(f'{param}', loc='center', fontsize=14)
    plt.xlabel('\nВремя', fontsize=12)
    plt.ylabel(f'{param}', fontsize=12)

    plt.grid(axis='y', color='#3475D0', lw=0.5, alpha=0.5)
    plt.plot(df['time'], df[f'{param}'], marker='o', markersize=1.5, label=f'{param}')
    plt.tick_params(
        axis='x',
        which='both',
        bottom=False,
        top=False,
        labelbottom=False)

    plt.legend(loc='lower center')
    plt.savefig(f'./plot images/plot_{param}.png')
    plt.clf()

def piechart(param, binspie):
    plt.title(f'Частота записей параметра {param}', loc='center', fontsize=14)
    xticks = [(binspie[idx + 1] + value) / 2 for idx, value in enumerate(binspie[:-1])]
    xticks_labels = ["[{:.2f},\n{:.2f}]".format(value, binspie[idx + 1]) for idx, value in enumerate(binspie[:-1])]

    plt.pie(xticks, labels=xticks_labels, autopct='%1.1f%%')
    plt.savefig(f'./plot images/pie_{param}.png')

def main():
    print(df)

    params = ['sound', 'illuminance', 'voltage']

    for param in params:
        bins = hist(param, plot_size=(12, 7), bins=10, title=f'{param}',
                    xlabel_name=f'Интервалы уровня {param}', ylabel_name='Частота записей')
        plot(param)
        piechart(param, bins)

if __name__ == '__main__':
    main()