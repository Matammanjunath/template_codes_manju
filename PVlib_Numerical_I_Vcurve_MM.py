# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 10:06:53 2021

@author: MMatam
"""
from pvlib import pvsystem
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Example module parameters for the Canadian Solar CS5P-220M:
parameters = {
    'Name': 'Canadian Solar CS5P-220M',
    'BIPV': 'N',
    'Date': '10/5/2009',
    'T_NOCT': 42.4,
    'A_c': 1.7,
    'N_s': 96,
    'I_sc_ref': 5.1,
    'V_oc_ref': 59.4,
    'I_mp_ref': 4.69,
    'V_mp_ref': 46.9,
    'alpha_sc': 0.004539,
    'beta_oc': -0.22216,
    'a_ref': 2.6373,
    'I_L_ref': 5.114,
    'I_o_ref': 8.196e-10,
    'R_s': 1.065,
    'R_sh_ref': 381.68,
    'Adjust': 8.7,
    'gamma_r': -0.476,
    'Version': 'MM106',
    'PTC': 200.1,
    'Technology': 'Mono-c-Si',
}

####
parameters = {
    'Name': 'Jinko 270W',
    'BIPV': 'N',
    'Date': '10/5/2009',
    'T_NOCT': 45,
    'A_c': 1.7,
    'N_s': 60,
    'I_sc_ref': 9.09,
    'V_oc_ref': 38.8,
    'I_mp_ref': 8.52,
    'V_mp_ref': 31.7,
    'alpha_sc': 0.06,
    'beta_oc': -0.3,
    'a_ref': 1.9,
    'I_L_ref': 9.1,
    'I_o_ref': 10.196e-9,
    'R_s': 0.065,
    'R_sh_ref': 500.68,
    'Adjust': 15,
    'gamma_r': -0.4,
    'Version': 'MM106',
    'PTC': 200.1,
    'Technology': 'Mono-c-Si',
}

cases = [
    (1000, 55),
    (800, 55),
    (600, 55),
    (400, 25),
    (400, 40),
    (400, 55)
]

conditions = pd.DataFrame(cases, columns=['Geff', 'Tcell'])

# adjust the reference parameters according to the operating
# conditions using the De Soto model:
IL, I0, Rs, Rsh, nNsVth = pvsystem.calcparams_desoto(
    conditions['Geff'],
    conditions['Tcell'],
    alpha_sc=parameters['alpha_sc'],
    a_ref=parameters['a_ref'],
    I_L_ref=parameters['I_L_ref'],
    I_o_ref=parameters['I_o_ref'],
    R_sh_ref=parameters['R_sh_ref'],
    R_s=parameters['R_s'],
    EgRef=1.121,
    dEgdT=-0.0002677
)

# plug the parameters into the SDE and solve for IV curves:
curve_info = pvsystem.singlediode(
    photocurrent=IL,
    saturation_current=I0,
    resistance_series=Rs,
    resistance_shunt=Rsh,
    nNsVth=nNsVth,
    ivcurve_pnts=1000,
    method='lambertw'
)

# # plot the calculated curves:
# plt.figure()
# for i, case in conditions.iterrows():
#     label = (
#         "$G_{eff}$ " + f"{case['Geff']} $W/m^2$\n"
#         "$T_{cell}$ " + f"{case['Tcell']} $C$"
#     )
#     plt.plot(curve_info['v'][i]*12, [i*j for i,j in zip(curve_info['i'][i]*100,curve_info['v'][i]*12)], label=label)
#     v_mp = curve_info['v_mp'][i]
#     i_mp = curve_info['i_mp'][i]
#     # mark the MPP
#     # plt.plot([v_mp], [i_mp], ls='', marker='o', c='k')

# plt.legend(loc=(1.0, 0))
# plt.xlabel('Module voltage [V]')
# plt.ylabel('Module current [A]')
# plt.title(parameters['Name'])
# plt.show()
# plt.gcf().set_tight_layout(True)


# # draw trend arrows
# def draw_arrow(ax, label, x0, y0, rotation, size, direction):
#     style = direction + 'arrow'
#     bbox_props = dict(boxstyle=style, fc=(0.8, 0.9, 0.9), ec="b", lw=1)
#     t = ax.text(x0, y0, label, ha="left", va="bottom", rotation=rotation,
#                 size=size, bbox=bbox_props, zorder=-1)

#     bb = t.get_bbox_patch()
#     bb.set_boxstyle(style, pad=0.6)


# ax = plt.gca()
# draw_arrow(ax, 'Irradiance', 20, 2.5, 90, 15, 'r')
# draw_arrow(ax, 'Temperature', 35, 1, 0, 15, 'l')

# print(pd.DataFrame({
#     'i_sc': curve_info['i_sc'],
#     'v_oc': curve_info['v_oc'],
#     'i_mp': curve_info['i_mp'],
#     'v_mp': curve_info['v_mp'],
#     'p_mp': curve_info['p_mp'],
# }))

import seaborn as sns

Nsm = 12#12
Nps = 1#44
df = pd.DataFrame({'PV Array Voltage (V)':curve_info['v'][0]*Nsm,'PV Array Current (A)':curve_info['i'][0]*Nps})
df['Power (kW)'] = df['PV Array Voltage (V)']*df['PV Array Current (A)']#/1000

pstc = df['Power (kW)'].max()
pdx = df['Power (kW)'].idxmax()
vmpp = df['PV Array Voltage (V)'].loc[pdx]

dcac = [1,1.33]+list(np.linspace(2,7,6))
pdcac = [pstc/i for i in dcac]
clpdf = pd.DataFrame({'DC/AC Ratio':dcac})
clpdf['Inverter Rated Power (kW)'] = pstc/clpdf['DC/AC Ratio']
p,v = [],[]
for i in range(len(clpdf)):
    plimit = clpdf['Inverter Rated Power (kW)'].loc[i]
    p.append([plimit]*2)
    xdf = df[df['PV Array Voltage (V)']<vmpp]
    v1 = xdf['PV Array Voltage (V)'].loc[(xdf['Power (kW)']-plimit).abs().idxmin()]
    xdf = df[df['PV Array Voltage (V)']>vmpp]
    v2 = xdf['PV Array Voltage (V)'].loc[(xdf['Power (kW)']-plimit).abs().idxmin()]
    v.append([v1,v2])    
clpdf['Power Limit (kW)'] = p
clpdf['Operating Voltage (V)'] = v
#### Seaborn plot
fig, ax = plt.subplots()
sns.set(font_scale=1.5)
# sns.set_style("whitegrid", {'axes.grid' : True})
sns.set_style("white")
sns.relplot(
            # x='Comm. Date',
            y='Power (kW)',
            # x='DC/AC Ratio',
            x='PV Array Voltage (V)',
            data=df,
            kind='line',
            # hue = 'State',
            # hue='Module Orientation',
            # size='DC/AC Ratio',
            # size='Nameplate Capacity (MW)',
            # palette='crest',
            # col='State',
            # col_wrap=5,
            height=4,aspect=1)
# plt.gcf().autofmt_xdate()
temp_name3 = 'Temp_plot3.png'
plt.subplots_adjust(left=0.05, right=0.79, top=0.99, bottom=0.05)
for i in range(len(clpdf)):
    plt.plot(clpdf['Operating Voltage (V)'].loc[i],clpdf['Power Limit (kW)'].loc[i],
              '--o',label=clpdf['DC/AC Ratio'].loc[i])
    plt.text(clpdf['Operating Voltage (V)'].loc[i][0]-40,clpdf['Power Limit (kW)'].loc[i][0],
             '%d'%(clpdf['Operating Voltage (V)'].loc[i][0]),fontsize=12)
    plt.text(clpdf['Operating Voltage (V)'].loc[i][1]+10,clpdf['Power Limit (kW)'].loc[i][1],
             '%d (%d W)'%(clpdf['Operating Voltage (V)'].loc[i][1],clpdf['Power Limit (kW)'].loc[i][1]),
             fontsize=12)    
plt.legend(loc='best',bbox_to_anchor=(1.27,1),title='DC/AC Ratio')     
# plt.subplots_adjust(left=0.12, right=0.8, top=0.99, bottom=0.15)        
plt.savefig(temp_name3,bbox_inches='tight',pad_inches=0.1, dpi=250)
# plt.close()
plt.show()

####
vol = [260,vmpp,370]
cur = []
for i in vol:
    cur.append(df['PV Array Current (A)'].loc[(df['PV Array Voltage (V)']-i).abs().idxmin()])
pwr = [i*j for i,j in zip(vol,cur)]    
#### I-V curve
fig,ax = plt.subplots(nrows=2, ncols=1,sharey=False,sharex=True, figsize=(6,4))
fig.subplots_adjust(hspace=0.0, wspace=0.00)
ax[0].plot(df['PV Array Voltage (V)'],df['Power (kW)'],linewidth=2)
ax[0].plot(vol,pwr,'o',markersize=12)
ax[0].yaxis.set_tick_params(labelsize=30)
ax[1].plot(df['PV Array Voltage (V)'],df['PV Array Current (A)'],linewidth=2)
ax[1].plot(vol,cur,'o',markersize=12)
ax[1].yaxis.set_tick_params(labelsize=30)
ax[1].xaxis.set_tick_params(labelsize=30)
# plt.yticks(fontsize=20)
temp_name3 = 'Temp_plot4.png'
plt.savefig(temp_name3,bbox_inches='tight',pad_inches=0.1, dpi=250)
plt.show()




