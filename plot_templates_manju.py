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
    
    
def dataframe_scatter_polyfit_plot(df,xcol,ycols,xlim=None,ylim=None,
                                   xlbl='X-axis',ylbl='Y-axis',
                                   polfit_deg=1,scatter_alpha=1,
                                       fig_name = 'samples_polyfit.png'):
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    clr_list = mcolors.TABLEAU_COLORS
    # # Access limits
    if xlim==None:
        xlim = [df[xcol[0]].min()*0.95,df[xcol[0]].max()*1.1]
    if ylim==None:
        if len(ycols)>=2:
            ylim = [df[ycols].min().min()*0.95,df[ycols].max().max()*1.1]
        else:
            ylim = [df[ycols].min()*0.95,df[ycols].max()*1.1]
    # print(xlim)
    # print(ylim)
    # convert clr_list of keys, values into a list
    clr_list = list(dict(clr_list).values())
    # Find the columns where each value is null
    empty_cols = [col for col in df[ycols].columns if df[col].isnull().all()]
    # Drop these columns from the dataframe
    # print(ycols)
    ycols = [x for x in ycols if x not in empty_cols]
    # print(ycols)
    # Perform polyfit, predict and plot the samples and prediction        
    for i in range(len(ycols)):
        pfit  = np.polyfit(df[xcol[0]],df[ycols[i]],polfit_deg)
        pred = np.poly1d(pfit)
        plt.scatter(df[xcol[0]],df[ycols[i]],marker='.',color=clr_list[i],alpha=0.2,label='%s'%(ycols[i]))
        plt.plot(df[xcol[0]].tolist()+[xlim[1]],pred(df[xcol[0]].tolist()+[xlim[1]]),'-',color=clr_list[i],label='%s_fit'%(ycols[i]))
        plt.axis([xlim[0],xlim[1],ylim[0],ylim[1]])
    ## Plot settings
    plt.legend(loc='best',fontsize=12)
    plt.xlabel('%s'%(xlbl))
    plt.ylabel('%s'%(ylbl))
    plt.subplots_adjust(left=0.12, right=0.97, top=0.95, bottom=0.15)
    plt.savefig(fig_name,bbox_inches='tight',pad_inches=0.1, dpi=250)
    plt.show()
    
def dataframe_html_3dscatterplot(df,xcol,ycol,zcol,
                                   clr_col,clr_labels=[],
                                   # clr_type=
                                   size_col=None):
    import plotly.express as px
    from plotly.offline import plot
    import plotly
    # for camera view position to save as png
    # Refer: https://nbviewer.org/github/etpinard/plotly-misc-nbs/blob/master/3d-camera-controls.ipynb
    if size_col !=None:
        df[size_col] = df[size_col].astype(float)
    fig = px.scatter_3d(df, x=xcol, y=ycol, z=zcol,
                  color=clr_col,opacity=1,
                  color_continuous_scale  = plotly.colors.sequential.Viridis,
                   size=size_col)
    print(clr_labels)
    if len(clr_labels) > 2:
        cat_labels = clr_labels
        fig.update_coloraxes(colorbar=dict(ticktext=cat_labels, 
                                        tickvals=list(range(1, len(cat_labels)+1)),
                                        thickness=20,
                                        ticklabelposition='outside',
                                        orientation='v',
                                        x=0.7),
                             colorbar_tickfont=dict(size=24))
    if size_col==None:
        fig.update_traces(marker_size = 4)
    fig.update_layout(
        # title="Plot Title",
        # xaxis_title="X Axis Title",
        # yaxis_title="Y Axis Title",
        # legend_title="Legend Title",
        font=dict(
        #     # family="Aerial",
            size=14,
        #     # color="RebeccaPurple"
        ),
        margin=dict(t=30, r=30, l=30, b=30
    )
    )
    # xaxis.backgroundcolor is used to set background color
    fig.update_layout(scene = dict(
                        xaxis = dict(
                             backgroundcolor="rgb(200, 200, 230)",
                             gridcolor="white",
                             showbackground=True,
                             zerolinecolor="white",),
                        yaxis = dict(
                            backgroundcolor="rgb(230, 200,230)",
                            gridcolor="white",
                            showbackground=True,
                            zerolinecolor="white",
                            range=[0,2.5]),
                        zaxis = dict(
                            backgroundcolor="rgb(230, 230,200)",
                            gridcolor="white",
                            showbackground=True,
                            zerolinecolor="white",),))
    # fig.update_layout(font=dict(size=20))
    fig.update_xaxes(tickfont_size=20)
    fig.update_scenes(xaxis_title_font=dict(size=24),
                      yaxis_title_font=dict(size=24),
                      zaxis_title_font=dict(size=24))
    # fig.update_yaxes(title_standoff = 25)
    # fig.update_layout(
    # #     # title='Mt Bruno Elevation',
    #     # width=400, height=400,
    #     margin=dict(t=0, r=0, l=0, b=0
    # ))
    
    name = 'eye = (x:0., y:2.5, z:0.)'
    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=1.94, y=0.1, z=0.1)
    )
    fig.update_layout(scene_camera=camera, 
                        # title=name
                      )
    ## Render the html 3d plot
    fig.show(renderer='browser')






