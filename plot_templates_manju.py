# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 20:39:23 2021

@author: MMatam
"""
import matplotlib.pyplot as plt





def oscilloscope_plot(df,x='x',y=['y1','y2'],xlbl = ['xlabel','xuni'],
                      ylbl = [['ylabel1','yuni1'],['ylabel2','yuni2'],['ylabel3','yuni3']],
                      saveformat='Oscilloscope_plot.jpg'):
    ax1 = plt.subplot(311, sharex=None)
    plt.plot(df[x], df[y[0]],'-r')
    plt.ylabel('%s'%(ylbl[0][0]))
    ax2 = plt.subplot(312, sharex=ax1)
    plt.plot(df[x], df[y[1]],'-r')
    plt.ylabel('%s'%(ylbl[1][0]))
    ax3 = plt.subplot(313, sharex=ax1)
    plt.plot(df[x], df[y[2]],'-r')
    plt.ylabel('%s'%(ylbl[2][0]))
    # ax1.get_shared_x_axes().join(ax1, ax2, ax3)
    # make x axis on upper invisible
    plt.setp(ax1.get_xaxis(), visible=False)
    plt.setp(ax2.get_xaxis(), visible=False)
    ax1.spines['bottom'].set_visible(False)
    # ax1.set_ylim([20,40])
    ax2.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    # ax2.set_ylim([0,1])
    ax3.spines['top'].set_visible(False)
    ax3.spines['bottom'].set_visible(True)
    ax1.legend('(in %s)'%(ylbl[0][1]))
    ax2.legend('(in %s)'%(ylbl[1][1]))
    ax3.legend('(in %s)'%(ylbl[2][1]))
    # ax3.set_ylim([0,25])
    ax1.grid(axis="y")
    ax2.grid(axis="y")
    ax3.grid(axis="y")
    ax3.set_xlabel('%s'%(ylbl[1][0]))
    plt.subplots_adjust(hspace=0.01)
    plt.subplots_adjust(left=0.12, right=0.97, top=0.95, bottom=0.15)
    plt.savefig(saveformat,bbox_inches='tight',pad_inches=0.1, dpi=250)
    plt.show()