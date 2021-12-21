# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 20:39:23 2021

@author: MMatam
"""
import matplotlib.pyplot as plt
#https://matplotlib.org/stable/gallery/color/named_colors.html
import matplotlib.colors as mcolors



def oscilloscope_plot(df,x='x',y=['y1','y2'],xlbl = ['xlabel','xuni'],
                      ylbl = [['ylabel1','yuni1'],['ylabel2','yuni2']],
                      saveformat='Oscilloscope_plot.jpg'):
    color_list = list(mcolors.TABLEAU_COLORS)
    n = len(y)
    fig, axes = plt.subplots(nrows=n,ncols=1,sharex=True)
    for i in range(n):
        # print('%s'%(y[i][0]))
        axes[i] = plt.subplot((n*100)+10+(i+1))
        plt.plot(df[x], df[y[i]],'-',color=color_list[i])
        axes[i].grid(axis="y")
        axes[i].legend(['%s'%(ylbl[i][0])])
        axes[i].spines['left'].set_color(color_list[i])
        axes[i].tick_params(axis='y', color=color_list[i],
                            labelcolor=color_list[i])
        plt.ylabel('(in %s)'%(ylbl[i][1]), color=color_list[i])
        if i==0:
            axes[i].spines['bottom'].set_visible(False)
        elif i!=(n-1):
            plt.setp(axes[i].get_xaxis(), visible=False)
            axes[i].spines['top'].set_visible(False)
            axes[i].spines['bottom'].set_visible(False)
        else:
            plt.setp(axes[i].get_xaxis(), visible=True)
            axes[i].spines['top'].set_visible(False)
            axes[i].spines['bottom'].set_visible(True)
            axes[i].set_xlabel('%s (in %s)'%(xlbl[0],xlbl[1]))
    plt.subplots_adjust(hspace=0.01)
    plt.subplots_adjust(left=0.12, right=0.97, top=0.95, bottom=0.15)
    temp_name = 'sun_inverterDCparams.png'
    plt.savefig(temp_name,bbox_inches='tight',pad_inches=0.1, dpi=250)
    plt.show()