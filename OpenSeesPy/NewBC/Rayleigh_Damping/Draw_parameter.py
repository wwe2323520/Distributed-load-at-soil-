# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 15:45:46 2024

@author: User
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import MultipleLocator

plt.rc('font', family= 'Times New Roman')

pi = np.pi
# # ============ Theory Impulse Force ======================
# --------- Real Quad Element -----------------
t = 1.0
nu = 0.3

Dx = 0.125
Dy = 0.125
cs = 200

rho = 2000
G = rho*cs*cs
E =  G*2*(1+nu)  # N/m^2 = Kg/(m*s^2)

cp = (E*(1-nu)/((1+nu)*(1-2*nu)*rho))**(0.5)
M = rho*cp*cp 

dt_Real = (Dy/cp)*(1/10) 
print(f"Real Element Dt = {dt_Real}")

Scale = np.array([0.5, 1.0, 2.0])
# --------- Ghost Quad Element (v = 0)-----------------
nu2 = 0.0
rho2 = 1e-0*rho

E_G = Scale*E # 1e-0*2*G
M_G = E_G
G_  = E_G/2

cp_Ghost = (E_G/rho2)**0.5
# Dy_Ghost = cp_Ghost* (Dy/cp)
print("--------- Ghost Element change parameter: ------------------")
print(f"rho2 = {rho2}; M_G = E_G = {E_G}; G_ = {G_}; Cp' = {cp_Ghost} m/s") #; Dy_Ghost = {Dy_Ghost} m

print("------------ Calculate Side + Bot Rayleigh Damping Force")
Py = 40*Dx*0.5
A = 0.125
vy = (1/(rho*cp))*(Py/A)
Rayleigh_Damping = t*Dx*rho*(cp+cs)*vy

LK_Damping = 0.5*t*Dx*rho*(cp+cs)*vy

print(f"vy = {vy}; Rayleigh_Damping Force = {Rayleigh_Damping}; LK_Damping Force = {LK_Damping}")
# ===========Test 1: Parameter compare (Ghost and LK Dashpot Element)==========================
Dy_cofficient = np.array([0.5, 1.0, 2.0]) # Dy_Ghost/Dy
M_cofficient = np.linspace(1e-4, 100, 2000) # M_G/ M 
G_cofficient = np.linspace(1e-4, 100, 2000) # G_/ G
rho_cofficient = np.linspace(1e-4, 100, 2000) # rho2/ rho

# -----Test 1: Compare for Stiffness parameter ----------------
kx_Kx = np.zeros((len(G_cofficient) ,len(Dy_cofficient)+1))
ky_Ky = np.zeros((len(M_cofficient) ,len(Dy_cofficient)+1))

mx_Mx = np.zeros((len(rho_cofficient) ,len(Dy_cofficient)+1))

for i in range(len(Dy_cofficient)): 
    for j in range(len(G_cofficient)):
        kx_Kx[j, 0] = G_cofficient[j]
        kx_Kx[j, 1+i] = (1 + G_cofficient[j]*(1/Dy_cofficient[i]))
        
        ky_Ky[j, 0] = M_cofficient[j]
        ky_Ky[j, 1+i] = (1 + M_cofficient[j]*(1/Dy_cofficient[i])) 
        
        mx_Mx[j, 0] = rho_cofficient[j]
        mx_Mx[j, 1+i] = (1 + rho_cofficient[j]*Dy_cofficient[i])

def plot_Test1(titleName, G_cofficient, kx_Kx, xlabel, ylabel):
    plt.figure(figsize=(10,8))
    # plt.title(titleName, fontsize = 20)
    plt.plot(G_cofficient[:], kx_Kx[:, 1], label = r"$\Delta_{y}'/\Delta_{y} = 0.5$", color= 'darkorange', linewidth = 6.0) # , ls = '--'
    plt.plot(G_cofficient[:], kx_Kx[:, 2], label = r"$\Delta_{y}'/\Delta_{y} = 1.0$", color= 'blue',  linewidth = 4.0) # , ls = '-.'
    plt.plot(G_cofficient[:], kx_Kx[:, 3], label = r"$\Delta_{y}'/\Delta_{y} = 2.0$", color= 'red',  linewidth = 2.0) # , ls = ':'

    plt.xscale("log") # ,base = 10
    plt.yscale("log",base = 10) # ,base = 10
    plt.grid(True)
    # ========== set up figure thick ============================
    bwidth = 2
    TK = plt.gca()
    TK.spines['bottom'].set_linewidth(bwidth)
    TK.spines['left'].set_linewidth(bwidth)
    TK.spines['top'].set_linewidth(bwidth)
    TK.spines['right'].set_linewidth(bwidth)
    
    legend1 = plt.legend(loc='upper left',fontsize=18)
    legend1.get_frame().set_edgecolor('grey')
    legend1.get_frame().set_linewidth(2)  # 設置外框寬度
    
    plt.xlim(1e-4, 100)
    plt.xlabel(xlabel, fontsize = 20) # r"$G^{'}/G$"
    plt.ylabel(ylabel, fontsize = 20)  # r"$m_{x'}/m_{x}$"
    # plt.gca().invert_xaxis() # invert the xais to make bigger value to the left
    plt.xticks(fontsize = 18, fontweight='bold', color='black')
    plt.yticks(fontsize = 18, fontweight='bold', color='black')
    
    ax = plt.gca()
    ax.tick_params(axis='x', which='major', labelsize= 20, length=8, width=2)
    ax.tick_params(axis='x', which='minor', length=4, width=2, color='gray')
    
    ax.tick_params(axis='y', which='major', labelsize= 20, length=8, width=2)
    ax.tick_params(axis='y', which='minor', length=4, width=2, color='gray')
    
# plot_Test1("Compare Ghost element Stiffness matrix ratio with LK Dashpot", G_cofficient, kx_Kx, r"$E_{i}'/E_{i}$", r"$k_{i}'/k_{i}$")
# # plot_Test1("Compare Ghost element Stiffness matrix ratio with LK Dashpot", M_cofficient, ky_Ky, r"$E_{i}/E_{i}$", r"$k_{i}'/k_{i}$")
# plot_Test1("Compare Ghost element Mass matrix ratio with LK Dashpot", rho_cofficient, mx_Mx, r"$\rho^{'}/\rho$", r"$m_{i}'/m_{i}$")

# ===========Test 2-1: Parameter compare (Ghost and LK Dashpot Element) (Xlabel = rho_cofficient2)==========================
Dy_cofficient2 = np.array([0.5, 1.0, 2.0]) # Dy_Ghost/Dy *
M_cofficient2 = np.array([1e-0, 1e-1, 1e-2, 1e-4]) # M_G/ M 
G_cofficient2 = np.array([1e-0, 1e-1, 1e-2, 1e-4]) # G_/ G
rho_cofficient2 = np.linspace(1e-4, 100, 2000) # rho2/ rho

# -----Test 2-1: Compare for Damping ratio and Natural Frequence parameter ----------------
Dy5_xix_Xix = np.zeros((len(rho_cofficient2) ,len(G_cofficient2)+1))
Dy10_xix_Xix = np.zeros((len(rho_cofficient2) ,len(G_cofficient2)+1))
Dy20_xix_Xix = np.zeros((len(rho_cofficient2) ,len(G_cofficient2)+1))

Dy5_wx_Wx = np.zeros((len(rho_cofficient2) ,len(G_cofficient2)+1))
Dy10_wx_Wx = np.zeros((len(rho_cofficient2) ,len(G_cofficient2)+1))
Dy20_wx_Wx = np.zeros((len(rho_cofficient2) ,len(G_cofficient2)+1))
for i in range(len(G_cofficient2)):
    for j in range(len(rho_cofficient2)):
# -----------------(Xlabel = rho_cofficient2) Xi_x cofficient in Dy/Dy_Ghost = 0.5, 1.0, 2.0 (compare with LK Dashpot)----------------------------------
        Dy5_xix_Xix[j, 0] =  rho_cofficient2[j]
        Dy5_xix_Xix[j, 1+i] = abs( 1/((1+ rho_cofficient2[j]*Dy_cofficient2[0])*(1+ G_cofficient2[i]*(1/Dy_cofficient2[0])))**0.5 )
        
        Dy10_xix_Xix[j, 0] =  rho_cofficient2[j]
        Dy10_xix_Xix[j, 1+i] = abs( 1/((1+ rho_cofficient2[j]*Dy_cofficient2[1])*(1+ G_cofficient2[i]*(1/Dy_cofficient2[1])))**0.5 )
        
        Dy20_xix_Xix[j, 0] =  rho_cofficient2[j]
        Dy20_xix_Xix[j, 1+i] = abs( 1/((1+ rho_cofficient2[j]*Dy_cofficient2[2])*(1+ G_cofficient2[i]*(1/Dy_cofficient2[2])))**0.5 )

# -----------------(Xlabel = rho_cofficient2) Wx cofficient in Dy/Dy_Ghost = 0.5, 1.0, 2.0 (compare with LK Dashpot)----------------------------------
        Dy5_wx_Wx[j, 0] = rho_cofficient2[j]
        Dy5_wx_Wx[j, 1+i] = abs( ((1+ G_cofficient2[i]*(1/Dy_cofficient2[0]))*(1/(1+ rho_cofficient2[j]*Dy_cofficient2[0])))**0.5 )

        Dy10_wx_Wx[j, 0] = rho_cofficient2[j]
        Dy10_wx_Wx[j, 1+i] = abs( ((1+ G_cofficient2[i]*(1/Dy_cofficient2[1]))*(1/(1+ rho_cofficient2[j]*Dy_cofficient2[1])))**0.5 )
        
        Dy20_wx_Wx[j, 0] = rho_cofficient2[j]
        Dy20_wx_Wx[j, 1+i] = abs( ((1+ G_cofficient2[i]*(1/Dy_cofficient2[2]))*(1/(1+ rho_cofficient2[j]*Dy_cofficient2[2])))**0.5 )

# ===========Test 2-2: Parameter compare (Ghost and LK Dashpot Element) (Xlabel = M, G cofficient)==========================
M_cofficient3 = np.linspace(1e-4, 100, 2000) # M_G/ M 
G_cofficient3 = np.linspace(1e-4, 100, 2000) # G_/ G
rho_cofficient3 = np.array([1e-0, 1e-1, 1e-2, 1e-4]) # rho2/ rho
# -----Test 2-2: Compare for Damping ratio and Natural Frequence parameter ----------------
Dy5_xix_Xix2 = np.zeros((len(G_cofficient3) ,len(rho_cofficient3)+1))
Dy10_xix_Xix2 = np.zeros((len(G_cofficient3) ,len(rho_cofficient3)+1))
Dy20_xix_Xix2 = np.zeros((len(G_cofficient3) ,len(rho_cofficient3)+1))

Dy5_wx_Wx2 = np.zeros((len(G_cofficient3) ,len(rho_cofficient3)+1))
Dy10_wx_Wx2 = np.zeros((len(G_cofficient3) ,len(rho_cofficient3)+1))
Dy20_wx_Wx2 = np.zeros((len(G_cofficient3) ,len(rho_cofficient3)+1))
for h in range(len(rho_cofficient3)):
    for j in range(len(G_cofficient3)):
# -----------------(Xlabel = M,G_cofficient) Xi_x cofficient in Dy/Dy_Ghost = 0.5, 1.0, 2.0 (compare with LK Dashpot)----------------------------------
        Dy5_xix_Xix2[j, 0] = G_cofficient3[j]
        Dy5_xix_Xix2[j, 1+h] = abs( 1/((1+ rho_cofficient3[h]*Dy_cofficient2[0])*(1+ G_cofficient3[j]*(1/Dy_cofficient2[0])))**0.5 )
        
        Dy10_xix_Xix2[j, 0] = G_cofficient3[j]
        Dy10_xix_Xix2[j, 1+h] = abs( 1/((1+ rho_cofficient3[h]*Dy_cofficient2[1])*(1+ G_cofficient3[j]*(1/Dy_cofficient2[1])))**0.5 )
        
        Dy20_xix_Xix2[j, 0] = G_cofficient3[j]
        Dy20_xix_Xix2[j, 1+h] = abs( 1/((1+ rho_cofficient3[h]*Dy_cofficient2[2])*(1+ G_cofficient3[j]*(1/Dy_cofficient2[2])))**0.5 )
# -----------------(Xlabel = M,G_cofficient) Wx cofficient in Dy/Dy_Ghost = 0.5, 1.0, 2.0 (compare with LK Dashpot)----------------------------------
        Dy5_wx_Wx2[j, 0] = G_cofficient3[j]
        Dy5_wx_Wx2[j, 1+h] = abs( ((1+ G_cofficient3[j]*(1/Dy_cofficient2[0]))* (1/(1+ rho_cofficient3[h]*Dy_cofficient2[0])))**0.5 )
        
        Dy10_wx_Wx2[j, 0] = G_cofficient3[j]
        Dy10_wx_Wx2[j, 1+h] = abs( ((1+ G_cofficient3[j]*(1/Dy_cofficient2[1]))* (1/(1+ rho_cofficient3[h]*Dy_cofficient2[1])))**0.5 )
        
        Dy20_wx_Wx2[j, 0] = G_cofficient3[j]
        Dy20_wx_Wx2[j, 1+h] = abs( ((1+ G_cofficient3[j]*(1/Dy_cofficient2[2]))* (1/(1+ rho_cofficient3[h]*Dy_cofficient2[2])))**0.5 )


def plot_Test2(rho_cofficient2, Dy5_xix_Xix):
# # -------------Test 2-1 (Xlabel = rho_cofficient2 -----------------------------
#     plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 1], label = r"$E_{i}'/E_{i} = 1.0$",  color= 'darkgrey', linewidth = 6.0)
#     plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 2], label = r"$E_{i}'/E_{i} = 1/10$" , color= 'blue',  linewidth = 5.0)
#     plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 3], label = r"$E_{i}'/E_{i} = 1/100$",  color= 'darkorange',  linewidth = 4.0)
#     plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 4], label = r"$E_{i}'/E_{i} = 1/10000$", ls = '--',  color= 'red',  linewidth = 2.0)
    # -----------------Test 2-2 (Xlabel = M,G_cofficient) -------------------------   
    plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 1], label = r"$\rho'/\rho = 1.0$", color= 'darkgrey', linewidth = 6.0) # , ls = '--' 
    plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 2], label = r"$\rho'/\rho= 1/10$", color= 'blue',  linewidth = 5.0) # , ls = '-.'
    plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 3], label = r"$\rho'/\rho = 1/100$", color= 'darkorange',  linewidth = 4.0) # , ls = ':'
    plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 4], label = r"$\rho'/\rho = 1/10000$", ls = '--', color= 'red',  linewidth = 2.0) # , ls = '-'
   
    # # # -----------------Test 2-3 (Xlabel = M,G_cofficient) -------------------------   
    # plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 1], label = r"$\Delta_{y}'/\Delta_{y} = 0.5$", color= 'orange', linewidth = 6.0) # , ls = '--' 
    # plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 2], label = r"$\Delta_{y}'/\Delta_{y} = 1.0$", color= 'aqua',  linewidth = 5.0) # , ls = '-.'
    # plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 3], label = r"$\Delta_{y}'/\Delta_{y} = 2.0$", color= 'red',  linewidth = 4.0) # , ls = ':'

    plt.grid(True)  
    # ========== set up figure thick ============================
    bwidth = 2
    TK = plt.gca()
    TK.spines['bottom'].set_linewidth(bwidth)
    TK.spines['left'].set_linewidth(bwidth)
    TK.spines['top'].set_linewidth(bwidth)
    TK.spines['right'].set_linewidth(bwidth)
    
    plt.xlim(1e-4, 100)
    # plt.gca().invert_xaxis() # invert the xais to make bigger value to the left
    plt.xticks(fontsize = 18, fontweight='bold', color='black')
    plt.yticks(fontsize = 18, fontweight='bold', color='black')
    
    ax = plt.gca()
    ax.tick_params(axis='x', which='major', labelsize= 18, length=8, width=2)
    ax.tick_params(axis='x', which='minor', length=4, width=2, color='gray')
    
    ax.tick_params(axis='y', which='major', labelsize= 20, length=8, width=2)
    ax.tick_params(axis='y', which='minor', length=4, width=2, color='gray')

# # ------------- (Xlabel = rho_cofficient2 -----------------------------
# row_heights = [3,3,3]
# fig1, (ax1,ax2,ax3) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # fig1.suptitle(f'Compare Ghost element Damping Ratio with LK Dashpot ',x=0.50,y =0.95,fontsize = 20)
# fig1.text(0.14,0.71, r"$E_{i}'$ $\mathrm {Control}$", color = "black", fontsize=20) 
# fig1.text(0.025, 0.5, r"$\xi_{i}'/\xi_{i}$", va= 'center', rotation= 'vertical', fontsize=22)
# fig1.text(0.46,0.04, r"$\rho'/\rho$", va= 'center', fontsize=20)

# ax1 = plt.subplot(311)
# plot_Test2(rho_cofficient2, Dy5_xix_Xix)
# ax1.set_title(r"$\Delta_{y}'/\Delta_{y} = 0.5$",fontsize =23, x=0.16, y=0.02)
# ax1.set_xscale('log') # , base=10
# ax1.set_yscale('log') # , base=10
 
# ax2 = plt.subplot(312)
# plot_Test2(rho_cofficient2, Dy10_xix_Xix)
# ax2.set_title(r"$\Delta_{y}'/\Delta_{y} = 1.0$",fontsize =23, x=0.16, y=0.02)
# ax2.set_xscale('log') # , base=10
# ax2.set_yscale('log') # , base=10

# ax3 = plt.subplot(313)
# plot_Test2(rho_cofficient2, Dy20_xix_Xix)
# ax3.set_title(r"$\Delta_{y}'/\Delta_{y} = 2.0$",fontsize =23, x=0.16, y=0.02)
# ax3.set_xscale('log') # , base=10
# ax3.set_yscale('log') # , base=10

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting
# lines, labels = fig1.axes[-1].get_legend_handles_labels()
# legend1 = fig1.legend(lines, labels, ncol=2, loc = (0.25, 0.88),prop=font_props) # 'center right'
# legend1.get_frame().set_edgecolor('grey')
# legend1.get_frame().set_linewidth(2)  # 設置外框寬度

# row_heights = [3,3,3]
# fig2, (ax4,ax5,ax6) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # fig2.suptitle(f'Compare Ghost element natrue frequency with LK Dashpot ',x=0.50,y =0.95,fontsize = 20)
# fig2.text(0.14,0.71, r"$E_{i}'$ $\mathrm {Control}$", color = "black", fontsize=20) 
# fig2.text(0.025, 0.5, r"$\omega_{i}'/\omega_{i}$", va= 'center', rotation= 'vertical', fontsize=22)
# fig2.text(0.46,0.04, r"$\rho'/\rho$", va= 'center', fontsize=20)

# ax4 = plt.subplot(311)
# plot_Test2(rho_cofficient2, Dy5_wx_Wx)
# ax4.set_title(r"$\Delta_{y}'/\Delta_{y} = 0.5$",fontsize =23, x=0.16, y=0.02)
# ax4.set_xscale('log') # , base=10
# ax4.set_yscale('log') # , base=10

# ax5 = plt.subplot(312)
# plot_Test2(rho_cofficient2, Dy10_wx_Wx)
# ax5.set_title(r"$\Delta_{y}'/\Delta_{y} = 1.0$",fontsize =23, x=0.16, y=0.02)
# ax5.set_xscale('log') # , base=10
# ax5.set_yscale('log') # , base=10

# ax6 = plt.subplot(313)
# plot_Test2(rho_cofficient2, Dy20_wx_Wx)
# ax6.set_title(r"$\Delta_{y}'/\Delta_{y} = 2.0$",fontsize =23, x=0.16, y=0.02)
# ax6.set_xscale('log') # , base=10
# ax6.set_yscale('log') # , base=10

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting
# lines, labels = fig2.axes[-1].get_legend_handles_labels()
# legend2 = fig2.legend(lines, labels, ncol=2, loc = (0.25, 0.88),prop=font_props) # 'center right'
# legend2.get_frame().set_edgecolor('grey')
# legend2.get_frame().set_linewidth(2)  # 設置外框寬度

# #  -----------------(Xlabel = M,G_cofficient) -------------------------   
# row_heights = [3,3,3]
# fig3, (ax7,ax8,ax9) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # fig3.suptitle(f'Compare Ghost element Damping Ratio with LK Dashpot ',x=0.50,y =0.95,fontsize = 20)
# fig3.text(0.14,0.71, r"$\rho'$ $\mathrm {Control}$", color = "black", fontsize=20) 
# fig3.text(0.015,0.5, r"$\xi_{i'}/\xi_{i}$", va= 'center', rotation= 'vertical', fontsize=20)
# fig3.text(0.47,0.04, r"$E_{i}'/E_{i}$", va= 'center', fontsize=20)

# ax7 = plt.subplot(311)
# plot_Test2(G_cofficient3, Dy5_xix_Xix2)
# ax7.set_title(r"$\Delta_{y}'/\Delta_{y} = 0.5$",fontsize =23, x=0.16, y=0.02)
# ax7.set_xscale('log') # , base=10
# ax7.set_yscale('log') # , base=10

# ax8 = plt.subplot(312)
# plot_Test2(G_cofficient3, Dy10_xix_Xix2)
# ax8.set_title(r"$\Delta_{y}'/\Delta_{y} = 1.0$",fontsize =23, x=0.16, y=0.02)
# ax8.set_xscale('log') # , base=10
# ax8.set_yscale('log') # , base=10

# ax9 = plt.subplot(313)
# plot_Test2(G_cofficient3, Dy20_xix_Xix2)
# ax9.set_title(r"$\Delta_{y}'/\Delta_{y} = 2.0$",fontsize =23, x=0.16, y=0.02)
# ax9.set_xscale('log') # , base=10
# ax9.set_yscale('log') # , base=10

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# lines, labels = fig3.axes[-1].get_legend_handles_labels()
# legend1 = fig3.legend(lines, labels, ncol=2, loc = (0.25, 0.88),prop=font_props) # 'center right'
# legend1.get_frame().set_edgecolor('grey')
# legend1.get_frame().set_linewidth(2)  # 設置外框寬度

# row_heights = [3,3,3]
# fig4, (ax10,ax11,ax12) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # fig4.suptitle(f'Compare Ghost element natrue frequency with LK Dashpot ',x=0.50,y =0.95,fontsize = 20)
# fig4.text(0.14,0.78, r"$\rho'$ $\mathrm {Control}$", color = "black", fontsize=20) 
# fig4.text(0.015,0.5, r"$\omega_{i}'/\omega_{i}$", va= 'center', rotation= 'vertical', fontsize=20)
# fig4.text(0.47,0.04, r"$E_{i}'/E_{i}$", va= 'center', fontsize=20)

# ax10 = plt.subplot(311)
# plot_Test2(G_cofficient3, Dy5_wx_Wx2)
# ax10.set_title(r"$\Delta_{y}'/\Delta_{y} = 0.5$",fontsize =23, x=0.16, y=0.79)
# ax10.set_xscale('log') # , base=10
# ax10.set_yscale('log') # , base=10

# ax11 = plt.subplot(312)
# plot_Test2(G_cofficient3, Dy10_wx_Wx2)
# ax11.set_title(r"$\Delta_{y}'/\Delta_{y} = 1.0$",fontsize =23, x=0.16, y=0.79)
# ax11.set_xscale('log') # , base=10
# ax11.set_yscale('log') # , base=10

# ax12 = plt.subplot(313)
# plot_Test2(G_cofficient3, Dy20_wx_Wx2)
# ax12.set_title(r"$\Delta_{y}'/\Delta_{y} = 2.0$",fontsize =23, x=0.16, y=0.79)
# ax12.set_xscale('log') # , base=10
# ax12.set_yscale('log') # , base=10

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# lines, labels = fig4.axes[-1].get_legend_handles_labels()
# legend2 = fig4.legend(lines, labels, ncol=2, loc = (0.25, 0.88),prop=font_props) # 'center right'
# legend2.get_frame().set_edgecolor('grey')
# legend2.get_frame().set_linewidth(2)  # 設置外框寬度

# ===========Test 2-3: Parameter compare (Dy_Ghost/Dy Compare) (Xlabel = Ei'/Ei and rho2/rho)==========================
# Dy_cofficient2 = np.array([0.5, 1.0, 2.0]) # Dy_Ghost/Dy *
G_rho_cofficient9 = np.linspace(1e-4, 100, 2000) # G_/G and rho2/rho
# -----Test  2-3: Compare for Damping ratio and Natural Frequence parameter ----------------
Dy_xix_Xix3 = np.zeros((len(G_rho_cofficient9) ,len(Dy_cofficient2)+1))

Dy_wx_Wx3 = np.zeros((len(G_rho_cofficient9) ,len(Dy_cofficient2)+1))

for h in range(len(Dy_cofficient2)):
    for j in range(len(G_rho_cofficient9)):
        Dy_xix_Xix3[j, 0] = G_rho_cofficient9[j]
        Dy_xix_Xix3[j, 1+h] = 1/((1+ G_rho_cofficient9[j]*Dy_cofficient2[h])*(1+ G_rho_cofficient9[j]*(1/Dy_cofficient2[h])))**0.5 
        
        Dy_wx_Wx3[j, 0] = G_rho_cofficient9[j]
        Dy_wx_Wx3[j, 1+h] = ((1+ G_rho_cofficient9[j]*(1/Dy_cofficient2[h]))* (1/(1+ G_rho_cofficient9[j]*Dy_cofficient2[h])))**0.5

def plot_Test2_3(titleName, rho_cofficient2, Dy5_xix_Xix, xlabel, ylabel):
    plt.figure(figsize=(10,8))
    # plt.title(titleName, fontsize = 20)
   # # -----------------Test 2-3 (Xlabel = M,G_cofficient) -------------------------   
    plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 1], label = r"$\Delta_{y}'/\Delta_{y} = 0.5$", color= 'darkorange', linewidth = 6.0) # , ls = '--' 
    plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 2], label = r"$\Delta_{y}'/\Delta_{y} = 1.0$", color= 'blue',  linewidth = 4.0) # , ls = '-.'
    plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 3], label = r"$\Delta_{y}'/\Delta_{y} = 2.0$", color= 'red', ls = '--', linewidth = 2.0) # , ls = ':'

    plt.xscale("log") # ,base = 10
    plt.yscale("log",base = 10) # ,base = 10
    plt.grid(True)
    # ========== set up figure thick ============================
    bwidth = 2
    TK = plt.gca()
    TK.spines['bottom'].set_linewidth(bwidth)
    TK.spines['left'].set_linewidth(bwidth)
    TK.spines['top'].set_linewidth(bwidth)
    TK.spines['right'].set_linewidth(bwidth)
    
    legend1 = plt.legend(loc='lower left',fontsize=18)
    legend1.get_frame().set_edgecolor('grey')
    legend1.get_frame().set_linewidth(2)  # 設置外框寬度
    
    plt.xlim(1e-4, 100)
    
    plt.xlabel(xlabel, fontsize = 20) # r"$G^{'}/G$"
    plt.ylabel(ylabel, fontsize = 20)  # r"$m_{x'}/m_{x}$"
    plt.xticks(fontsize = 18, fontweight='bold', color='black')
    plt.yticks(fontsize = 18, fontweight='bold', color='black')
    
    ax = plt.gca()
    ax.tick_params(axis='x', which='major', labelsize= 18, length=8, width=2)
    ax.tick_params(axis='x', which='minor', length=4, width=2, color='gray')
    
    ax.tick_params(axis='y', which='major', labelsize= 20, length=8, width=2)
    ax.tick_params(axis='y', which='minor', length=4, width=2, color='gray')


# plot_Test2_3(f'Compare Ghost element Damping Ratio with LK Dashpot', G_rho_cofficient9, Dy_xix_Xix3, r"$E_{i}'/E_{i}$ $,$ $\rho'/\rho$", r"$\xi_{i}'/\xi_{i}$")

# plot_Test2_3(f'Compare Ghost element Nature Frequency with LK Dashpot', G_rho_cofficient9, Dy_wx_Wx3, r"$E_{i}'/E_{i}$ $,$ $\rho'/\rho$", r"$\omega_{i}'/\omega_{i}$")
# ax1 = plt.gca()
# ax1.yaxis.set_major_formatter(ticker.ScalarFormatter())
# ax1.yaxis.set_minor_formatter(ticker.ScalarFormatter())
# ax1.tick_params(axis='y', which='major', labelsize=18)  # 主刻度字体大小
# ax1.tick_params(axis='y', which='minor', labelsize=18)  # 次刻度字体大小

# ===========Test 3: Error compare (Ghost and LK Dashpot Element) (Xlabel = M, G cofficient, rho cofficient)========================== 
# Dy_cofficient = np.array([0.5, 1.0, 2.0]) # Dy_Ghost/Dy
M_cofficient4 = np.linspace(1e-4, 100, 2000) # M_G/ M 
G_cofficient4 = np.linspace(1e-4, 100, 2000) # G_/ G
rho_cofficient4 = np.linspace(1e-4, 100, 2000) # rho2/ rho

# -----Test 3: Error Compare for Stiffness parameter ----------------
kx_Kx_Err = np.zeros((len(G_cofficient4) ,len(Dy_cofficient)+1))
ky_Ky_Err = np.zeros((len(M_cofficient4) ,len(Dy_cofficient)+1))
# 
mx_Mx_Err = np.zeros((len(rho_cofficient4) ,len(Dy_cofficient)+1))

for i in range(len(Dy_cofficient)): 
    for j in range(len(G_cofficient4)):
        kx_Kx_Err[j, 0] = G_cofficient4[j]
        kx_Kx_Err[j, 1+i] = (G_cofficient4[j]*(1/Dy_cofficient[i])) 
        
#         ky_Ky_Err[j, 0] = M_cofficient4[j]
#         ky_Ky_Err[j, 1+i] = (M_cofficient4[j]*(1/Dy_cofficient[i]))
        
        mx_Mx_Err[j, 0] = rho_cofficient4[j]
        mx_Mx_Err[j, 1+i] = (rho_cofficient4[j]*Dy_cofficient[i])
        
def plot_Test3(titleName, G_cofficient, kx_Kx, xlabel, ylabel):
    plt.figure(figsize=(10,8))
    # plt.title(titleName, fontsize = 20)
    plt.plot(G_cofficient[:], kx_Kx[:, 1], label = r"$\Delta_{y}'/\Delta_{y} = 0.5$", color= 'darkorange', linewidth = 5.0) # , ls = '--'
    plt.plot(G_cofficient[:], kx_Kx[:, 2], label = r"$\Delta_{y}'/\Delta_{y} = 1.0$", color= 'blue',  linewidth = 3.0) # , ls = '-.'
    plt.plot(G_cofficient[:], kx_Kx[:, 3], label = r"$\Delta_{y}'/\Delta_{y} = 2.0$", color= 'red',  linewidth = 2.0) # , ls = ':'

    plt.xscale("log") # ,base = 10
    plt.yscale("log") # ,base = 10
    plt.grid(True)
    # ========== set up figure thick ============================
    bwidth = 2
    TK = plt.gca()
    TK.spines['bottom'].set_linewidth(bwidth)
    TK.spines['left'].set_linewidth(bwidth)
    TK.spines['top'].set_linewidth(bwidth)
    TK.spines['right'].set_linewidth(bwidth)
    
    legend1 = plt.legend(loc='upper left',fontsize=18)
    legend1.get_frame().set_edgecolor('grey')
    legend1.get_frame().set_linewidth(2)  # 設置外框寬度
    
    plt.xlim(1e-4, 10)
    plt.xlabel(xlabel, fontsize = 20) # r"$G^{'}/G$"
    plt.ylabel(ylabel, fontsize = 20)  # r"$m_{x'}/m_{x}$"
    # plt.gca().invert_xaxis() # invert the xais to make bigger value to the left
    plt.xticks(fontsize = 18, fontweight='bold', color='black')
    plt.yticks(fontsize = 18, fontweight='bold', color='black')
    
    ax = plt.gca()
    ax.tick_params(axis='x', which='major', labelsize= 18, length=8, width=2)
    ax.tick_params(axis='x', which='minor', length=4, width=2, color='gray')
    
    ax.tick_params(axis='y', which='major', labelsize= 20, length=8, width=2)
    ax.tick_params(axis='y', which='minor', length=4, width=2, color='gray')
    
# plot_Test3("Error Compare with LK Dashpot: Stiffness ratio", G_cofficient4, kx_Kx_Err, r"$E_{i}'/E_{i}$", r"$(k_{i}'-k_{i})/k_{i}$")
# # plot_Test3("Error Compare with LK Dashpot: Stiffness ratio", M_cofficient4, ky_Ky_Err, r"$M'/M$", r"$(k_{y'}-k_{y})/k_{y}$" + r" (%)" )
# plot_Test3("Error Compare with LK Dashpot: Mass ratio", rho_cofficient4, mx_Mx_Err, r"$\rho'/\rho$", r"$(m_{i}'-m_{i})/m_{i}$")

# # ===========Test 4-1: Parameter compare (Ghost and LK Dashpot Element) (Xlabel = rho_cofficient2)==========================
# # Dy_cofficient2 = np.array([0.5, 1.0, 2.0]) # Dy_Ghost/Dy
# M_cofficient5 = np.array([1e-0, 1e-1, 1e-2, 1e-4]) # M_G/ M 
# G_cofficient5 = np.array([1e-0, 1e-1, 1e-2, 1e-4]) # G_/ G
# rho_cofficient5 = np.arange(1e-8, 1, 1e-6) # np.linspace(1e-8, 1, 8000) # rho2/ rho : 1e-4, 100, 2000

# # -----(Xlabel = rho Cofficient)Test 4-1: Compare for Damping ratio and Natural Frequence parameter ----------------
# Dy5_xix_Xix_Err = np.zeros((len(rho_cofficient5) ,len(G_cofficient5)+1))
# Dy10_xix_Xix_Err= np.zeros((len(rho_cofficient5) ,len(G_cofficient5)+1))
# Dy20_xix_Xix_Err = np.zeros((len(rho_cofficient5) ,len(G_cofficient5)+1))

# Dy5_wx_Wx_Err = np.zeros((len(rho_cofficient5) ,len(G_cofficient5)+1))
# Dy10_wx_Wx_Err = np.zeros((len(rho_cofficient5) ,len(G_cofficient5)+1))
# Dy20_wx_Wx_Err = np.zeros((len(rho_cofficient5) ,len(G_cofficient5)+1))

# for i in range(len(G_cofficient5)):
#     for j in range(len(rho_cofficient5)):
# # -----------------Test 4-1 (Xlabel = rho_cofficient2) Xi_x cofficient in Dy/Dy_Ghost = 0.5, 1.0, 2.0 (compare with LK Dashpot)----------------------------------
#         Dy5_xix_Xix_Err[j, 0] =  rho_cofficient5[j]
#         Dy5_xix_Xix_Err[j, 1+i] = abs( (1/((1+ rho_cofficient5[j]*Dy_cofficient2[0])*(1+ G_cofficient5[i]*(1/Dy_cofficient2[0])))**0.5) -1 )
        
#         Dy10_xix_Xix_Err[j, 0] =  rho_cofficient5[j]
#         Dy10_xix_Xix_Err[j, 1+i] = abs( (1/((1+ rho_cofficient5[j]*Dy_cofficient2[1])*(1+ G_cofficient5[i]*(1/Dy_cofficient2[1])))**0.5) -1 )
        
#         Dy20_xix_Xix_Err[j, 0] =  rho_cofficient5[j]
#         Dy20_xix_Xix_Err[j, 1+i] = abs( (1/((1+ rho_cofficient5[j]*Dy_cofficient2[2])*(1+ G_cofficient5[i]*(1/Dy_cofficient2[2])))**0.5) -1 )

# # -----------------Test 4-1 (Xlabel = rho_cofficient2) Wx cofficient in Dy/Dy_Ghost = 0.5, 1.0, 2.0 (compare with LK Dashpot)----------------------------------
#         Dy5_wx_Wx_Err[j, 0] = rho_cofficient5[j]
#         Dy5_wx_Wx_Err[j, 1+i] = abs( (((1+ G_cofficient5[i]*(1/Dy_cofficient2[0]))*(1/(1+ rho_cofficient5[j]* Dy_cofficient2[0])))**0.5) -1 )

#         Dy10_wx_Wx_Err[j, 0] = rho_cofficient5[j]
#         Dy10_wx_Wx_Err[j, 1+i] = abs( (((1+ G_cofficient5[i]*(1/Dy_cofficient2[1]))*(1/(1+ rho_cofficient5[j]* Dy_cofficient2[1])))**0.5) -1 )
        
#         Dy20_wx_Wx_Err[j, 0] = rho_cofficient5[j]
#         Dy20_wx_Wx_Err[j, 1+i] = abs( (((1+ G_cofficient5[i]*(1/Dy_cofficient2[2]))*(1/(1+ rho_cofficient5[j]* Dy_cofficient2[2])))**0.5) -1 )

# # -----(Xlabel = G,M Cofficient)Test 4-2: Compare for Damping ratio and Natural Frequence parameter ----------------
# # Dy_cofficient2 = np.array([0.5, 1.0, 2.0]) # Dy_Ghost/Dy
# M_cofficient6 = np.linspace(1e-8, 1.0, 8000) # M_G/ M 
# G_cofficient6 = np.arange(1e-8, 1, 1e-6) # np.linspace(1e-8, 1.0, 8000) # G_/ G :1e-4, 100, 2000
# rho_cofficient6 = np.array([1e-0, 1e-1, 1e-2, 1e-4]) # rho2/ rho

# Dy5_xix_Xix_Err2 = np.zeros((len(G_cofficient6) ,len(rho_cofficient6)+1))
# Dy10_xix_Xix_Err2 = np.zeros((len(G_cofficient6) ,len(rho_cofficient6)+1))
# Dy20_xix_Xix_Err2 = np.zeros((len(G_cofficient6) ,len(rho_cofficient6)+1))

# Dy5_wx_Wx_Err2 = np.zeros((len(G_cofficient6) ,len(rho_cofficient6)+1))
# Dy10_wx_Wx_Err2 = np.zeros((len(G_cofficient6) ,len(rho_cofficient6)+1))
# Dy20_wx_Wx_Err2 = np.zeros((len(G_cofficient6) ,len(rho_cofficient6)+1))

# for i in range(len(rho_cofficient6)):
#     for j in range(len(G_cofficient6)):
# # -----------------Test 4-2 (Xlabel = rho_cofficient2) Xi_x cofficient in Dy/Dy_Ghost = 0.5, 1.0, 2.0 (compare with LK Dashpot)----------------------------------
#         Dy5_xix_Xix_Err2[j, 0] =  G_cofficient6[j]
#         Dy5_xix_Xix_Err2[j, 1+i] = abs( (1/((1+ rho_cofficient6[i]*Dy_cofficient2[0])*(1+ G_cofficient6[j]*(1/Dy_cofficient2[0])))**0.5) -1 )
        
#         Dy10_xix_Xix_Err2[j, 0] =  G_cofficient6[j]
#         Dy10_xix_Xix_Err2[j, 1+i] = abs( (1/((1+ rho_cofficient6[i]*Dy_cofficient2[1])*(1+ G_cofficient6[j]*(1/Dy_cofficient2[1])))**0.5) -1 )
        
#         Dy20_xix_Xix_Err2[j, 0] =  G_cofficient6[j]
#         Dy20_xix_Xix_Err2[j, 1+i] = abs( (1/((1+ rho_cofficient6[i]*Dy_cofficient2[2])*(1+ G_cofficient6[j]*(1/Dy_cofficient2[2])))**0.5) -1 )

# # -----------------Test 4-2 (Xlabel = rho_cofficient2) Wx cofficient in Dy/Dy_Ghost = 0.5, 1.0, 2.0 (compare with LK Dashpot)----------------------------------
#         Dy5_wx_Wx_Err2[j, 0] = G_cofficient6[j]
#         Dy5_wx_Wx_Err2[j, 1+i] = abs( (((1+ G_cofficient6[j]*(1/Dy_cofficient2[0]))*(1/(1+ rho_cofficient6[i]* Dy_cofficient2[0])))**0.5) -1 )

#         Dy10_wx_Wx_Err2[j, 0] = G_cofficient6[j]
#         Dy10_wx_Wx_Err2[j, 1+i] = abs( (((1+ G_cofficient6[j]*(1/Dy_cofficient2[1]))*(1/(1+ rho_cofficient6[i]* Dy_cofficient2[1])))**0.5) -1 )
        
#         Dy20_wx_Wx_Err2[j, 0] = G_cofficient6[j]
#         Dy20_wx_Wx_Err2[j, 1+i] = abs( (((1+ G_cofficient6[j]*(1/Dy_cofficient2[2]))*(1/(1+ rho_cofficient6[i]* Dy_cofficient2[2])))**0.5) -1 )

# def Find_zero(Name,matrix):
#     # 查找每个列中最接近0的元素的索引
#     closest_to_zero_indices = np.argmin(np.abs(matrix), axis=0)
#     # 输出结果
#     print(f"---------------{Name}---------------------")
#     for col in range(matrix.shape[1]):
#         index = closest_to_zero_indices[col]
#         value = matrix[index, col]
#         print(f"Column {col}: Closest to 0 is {value} at index {index}")
#     return closest_to_zero_indices

# Dy5_wx_Wx_Err_zero = Find_zero("Dy5_wx_Wx_Err", Dy5_wx_Wx_Err)
# Dy10_wx_Wx_Err_zero = Find_zero("Dy10_wx_Wx_Err", Dy10_wx_Wx_Err)
# Dy20_wx_Wx_Err_zero = Find_zero("Dy20_wx_Wx_Err", Dy20_wx_Wx_Err)

# Dy5_wx_Wx_Err2_zero = Find_zero("Dy5_wx_Wx_Err2", Dy5_wx_Wx_Err2)
# Dy10_wx_Wx_Err2_zero = Find_zero("Dy10_wx_Wx_Err2", Dy10_wx_Wx_Err2)
# Dy20_wx_Wx_Err2_zero = Find_zero("Dy20_wx_Wx_Err2", Dy20_wx_Wx_Err2)

# print(rho_cofficient5[Dy5_wx_Wx_Err_zero[4]], Dy5_wx_Wx_Err[Dy5_wx_Wx_Err_zero[4], 4])

# def plot_Test4(rho_cofficient2, Dy5_xix_Xix, Dy5_wx_Wx_Err_zero): # , Dy5_wx_Wx_Err_zero (when frequency Compare)
# # # ------------- (Xlabel = rho_cofficient2 -----------------------------
# #     plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 1], label = r"$E_{i}'/E_{i} = 1.0$", color= 'darkgrey', linewidth = 6.0) # , ls = '--'
# #     plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 2], label = r"$E_{i}'/E_{i} = 1/10$", color= 'blue',  linewidth = 5.0) # , ls = '-.'
# #     plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 3], label = r"$E_{i}'/E_{i} = 1/100$", color= 'darkorange',  linewidth = 4.0) # , ls = ':'
# #     plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 4], label = r"$E_{i}'/E_{i} = 1/10000$", ls = '--', color= 'red',  linewidth = 2.0) # , ls = '-'

#     # -----------------(Xlabel = M,G_cofficient) -------------------------   
#     plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 1], label = r"$\rho'/\rho = 1.0$", color= 'darkgrey', linewidth = 6.0)
#     plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 2], label = r"$\rho'/\rho= 1/10$", color= 'blue',  linewidth = 5.0)
#     plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 3], label = r"$\rho'/\rho = 1/100$", color= 'darkorange',  linewidth = 4.0)
#     plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 4], label = r"$\rho'/\rho = 1/10000$", ls = '--', color= 'red',  linewidth = 2.0)

# # ------ Marker each line approach zero point (Just For Frequency Compare)----------use (rho_cofficient2, Dy5_xix_Xix, Dy5_wx_Wx_Err_zero)
#     plt.plot(rho_cofficient2[Dy5_wx_Wx_Err_zero[1]], Dy5_xix_Xix[Dy5_wx_Wx_Err_zero[1], 1],'o', color= 'black')
#     plt.plot(rho_cofficient2[Dy5_wx_Wx_Err_zero[2]], Dy5_xix_Xix[Dy5_wx_Wx_Err_zero[2], 2],'o', color= 'black')
#     plt.plot(rho_cofficient2[Dy5_wx_Wx_Err_zero[3]], Dy5_xix_Xix[Dy5_wx_Wx_Err_zero[3], 3],'o', color= 'black')
#     plt.plot(rho_cofficient2[Dy5_wx_Wx_Err_zero[4]], Dy5_xix_Xix[Dy5_wx_Wx_Err_zero[4], 4],'o', color= 'black')
    
#     plt.grid(True)  
#     # ========== set up figure thick ============================
#     bwidth = 2
#     TK = plt.gca()
#     TK.spines['bottom'].set_linewidth(bwidth)
#     TK.spines['left'].set_linewidth(bwidth)
#     TK.spines['top'].set_linewidth(bwidth)
#     TK.spines['right'].set_linewidth(bwidth)
    
#     plt.xlim(1E-8, 1) # 1E-4, 100
#     # plt.ylim() # 0,2 *******************
#     # plt.gca().invert_xaxis() # invert the xais to make bigger value to the left
#     plt.xticks(fontsize = 18, fontweight='bold', color='black')
#     plt.yticks(fontsize = 18, fontweight='bold', color='black')
    
#     ax = plt.gca()
#     ax.tick_params(axis='x', which='major', labelsize= 18, length=8, width=2)
#     ax.tick_params(axis='x', which='minor', length=4, width=2, color='gray')

#     # ax.yaxis.set_major_locator(MultipleLocator(10**(-1)))
#     # ax.tick_params(axis='y', which='major', labelsize=16, length=8, width=2)
#     # ax.tick_params(axis='y', which='minor', length=4, width=2, color='gray')
    
# # # -----(Xlabel = rho Cofficient) Test 4-1 ------------------------------\mid
# # row_heights = [3,3,3]
# # fig5, (ax13,ax14,ax15) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # # fig5.suptitle(f'Error Compare Ghost element Damping Ratio with LK Dashpot ',x=0.50,y =0.95,fontsize = 20)
# # fig5.text(0.73,0.71, r"$E_{i}'$ $\mathrm {Control}$", color = "black", fontsize=20) 
# # fig5.text(0.015,0.5, r"$\mid(\xi_{i}'-\xi{i})/\xi{i}\mid$", va= 'center', rotation= 'vertical', fontsize=20)
# # fig5.text(0.47,0.04, r"$\rho'/\rho$", va= 'center', fontsize=20)

# # ax13 = plt.subplot(311)
# # plot_Test4(rho_cofficient5, Dy5_xix_Xix_Err)
# # ax13.set_title(r"$\Delta_{y}'/\Delta_{y} = 0.5$",fontsize =20, x=0.86, y=0.04)
# # ax13.set_xscale('log', base=10) # , base=10
# # ax13.set_yscale('log', base=10) # , base=10

# # ax14 = plt.subplot(312)
# # plot_Test4(rho_cofficient5, Dy10_xix_Xix_Err)
# # ax14.set_title(r"$\Delta_{y}'/\Delta_{y} = 1.0$",fontsize =20, x=0.86, y=0.04)
# # ax14.set_xscale('log') # , base=10
# # ax14.set_yscale('log') # , base=10

# # ax15 = plt.subplot(313)
# # plot_Test4(rho_cofficient5, Dy20_xix_Xix_Err)
# # ax15.set_title(r"$\Delta_{y}'/\Delta_{y} = 2.0$",fontsize =20, x=0.86, y=0.04)
# # ax15.set_xscale('log') # , base=10
# # ax15.set_yscale('log') # , base=10

# # font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# # lines, labels = fig5.axes[-1].get_legend_handles_labels()
# # legend1 = fig5.legend(lines, labels, ncol=2, loc = (0.25, 0.88),prop=font_props) # 'center right'
# # legend1.get_frame().set_edgecolor('grey')
# # legend1.get_frame().set_linewidth(2)  # 設置外框寬度
    
# # row_heights = [3,3,3]
# # fig6, (ax16,ax17,ax18) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # # fig6.suptitle(f'Error Compare Ghost element Nature Frequency with LK Dashpot ',x=0.50,y =0.95,fontsize = 20)
# # fig6.text(0.14,0.71, r"$E_{i}'$ $\mathrm {Control}$", color = "black", fontsize=20) 
# # fig6.text(0.010,0.5, r"$\mid(\omega_{i}'-\omega_{i})/\omega_{i}\mid$", va= 'center', rotation= 'vertical', fontsize=20)
# # fig6.text(0.47,0.04, r"$\rho'/\rho$", va= 'center', fontsize=20)

# # ax16 = plt.subplot(311)
# # plot_Test4(rho_cofficient5, Dy5_wx_Wx_Err, Dy5_wx_Wx_Err_zero)
# # ax16.set_title(r"$\Delta_{y}'/\Delta_{y} = 0.5$",fontsize =20, x=0.14, y=0.04)
# # ax16.set_xscale('log') # , base=10
# # ax16.set_yscale('log') # , base=10

# # ax17 = plt.subplot(312)
# # plot_Test4(rho_cofficient5, Dy10_wx_Wx_Err, Dy10_wx_Wx_Err_zero)
# # ax17.set_title(r"$\Delta_{y}'/\Delta_{y} = 1.0$",fontsize =20, x=0.14, y=0.04)
# # ax17.set_xscale('log') # , base=10
# # ax17.set_yscale('log', base=10) # 

# # ax18 = plt.subplot(313)
# # plot_Test4(rho_cofficient5, Dy20_wx_Wx_Err, Dy20_wx_Wx_Err_zero)
# # ax18.set_title(r"$\Delta_{y}'/\Delta_{y} = 2.0$",fontsize =20, x=0.14, y=0.04)
# # ax18.set_xscale('log') # , base=10
# # ax18.set_yscale('log') # , base=10

# # font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# # lines, labels = fig6.axes[-1].get_legend_handles_labels()
# # legend1 = fig6.legend(lines, labels, ncol=2, loc = (0.25, 0.88), prop=font_props) # 'center right'
# # legend1.get_frame().set_edgecolor('grey')
# # legend1.get_frame().set_linewidth(2)  # 設置外框寬度

# # # -----(Xlabel = G,M Cofficient)Test 4-2 -------------------------------------------
# # row_heights = [3,3,3]
# # fig7, (ax19,ax20,ax21) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # # fig7.suptitle(f'Error Compare Ghost element Damping Ratio with LK Dashpot ',x=0.50,y =0.95,fontsize = 20)
# # fig7.text(0.73,0.71, r"$\rho'$ $\mathrm {Control}$", color = "black", fontsize=20) 
# # fig7.text(0.015,0.5, r"$\mid(\xi_{i}'-\xi{i})/\xi{i}\mid$", va= 'center', rotation= 'vertical', fontsize=20)
# # fig7.text(0.47,0.04, r"$E_{i}'/E_{i}$", va= 'center', fontsize=20)

# # ax19 = plt.subplot(311)
# # plot_Test4(G_cofficient6, Dy5_xix_Xix_Err2)
# # ax19.set_title(r"$\Delta_{y}'/\Delta_{y} = 0.5$",fontsize =20, x=0.86, y=0.04)
# # ax19.set_xscale('log') # , base=10
# # ax19.set_yscale('log') # , base=10

# # ax20 = plt.subplot(312)
# # plot_Test4(G_cofficient6, Dy10_xix_Xix_Err2)
# # ax20.set_title(r"$\Delta_{y}'/\Delta_{y} = 1.0$",fontsize =20, x=0.86, y=0.04)
# # ax20.set_xscale('log') # , base=10
# # ax20.set_yscale('log') # , base=10

# # ax21 = plt.subplot(313)
# # plot_Test4(G_cofficient6, Dy20_xix_Xix_Err2)
# # ax21.set_title(r"$\Delta_{y}'/\Delta_{y} = 2.0$",fontsize =20, x=0.86, y=0.04)
# # ax21.set_xscale('log') # , base=10
# # ax21.set_yscale('log') # , base=10

# # font_props = {'family': 'Arial', 'size': 15}  #Legend Setting
# # lines, labels = fig7.axes[-1].get_legend_handles_labels()
# # legend1 = fig7.legend(lines, labels, ncol=2, loc = (0.25, 0.88),prop=font_props) # 'center right'
# # legend1.get_frame().set_edgecolor('grey')
# # legend1.get_frame().set_linewidth(2)  # 設置外框寬度

# # row_heights = [3,3,3]
# # fig8, (ax22,ax23,ax24) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # # fig8.suptitle(f'Error Compare Ghost element Nature Frequency with LK Dashpot ',x=0.50,y =0.95,fontsize = 20)
# # fig8.text(0.14,0.71, r"$\rho'$ $\mathrm {Control}$", color = "black", fontsize=20) 
# # fig8.text(0.015,0.5, r"$\mid(\omega_{i}'-\omega_{i})/\omega_{i}\mid$", va= 'center', rotation= 'vertical', fontsize=20)
# # fig8.text(0.47,0.04, r"$E_{i}'/E_{i}$", va= 'center', fontsize=20)

# # ax22 = plt.subplot(311)
# # plot_Test4(G_cofficient6, Dy5_wx_Wx_Err2, Dy5_wx_Wx_Err2_zero)
# # ax22.set_title(r"$\Delta_{y}'/\Delta_{y} = 0.5$",fontsize =20, x=0.14, y=0.04)
# # ax22.set_xscale('log') # , base=10
# # ax22.set_yscale('log') # , base=10

# # ax23 = plt.subplot(312)
# # plot_Test4(G_cofficient6, Dy10_wx_Wx_Err2, Dy10_wx_Wx_Err2_zero)
# # ax23.set_title(r"$\Delta_{y}'/\Delta_{y} = 1.0$",fontsize =20, x=0.14, y=0.04)
# # ax23.set_xscale('log') # , base=10
# # ax23.set_yscale('log') # , base=10

# # ax24 = plt.subplot(313)
# # plot_Test4(G_cofficient6, Dy20_wx_Wx_Err2, Dy20_wx_Wx_Err2_zero)
# # ax24.set_title(r"$\Delta_{y}'/\Delta_{y} = 2.0$",fontsize =20, x=0.14, y=0.04)
# # ax24.set_xscale('log') # , base=10
# # ax24.set_yscale('log') # , base=10

# # font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# # lines, labels = fig8.axes[-1].get_legend_handles_labels()
# # legend1 = fig8.legend(lines, labels, ncol=2, loc = (0.25, 0.88), prop=font_props) # 'center right'
# # legend1.get_frame().set_edgecolor('grey')
# # legend1.get_frame().set_linewidth(2)  # 設置外框寬度

# ===========Test 4-3: Parameter compare (Dy_Ghost/Dy Compare) (Xlabel = Ei'/Ei and rho2/rho)==========================
# Dy_cofficient2 = np.array([0.5, 1.0, 2.0]) # Dy_Ghost/Dy *
G_rho_cofficient10 = np.linspace(1e-8, 1, 8000) # G_/G and rho2/rho
# -----Test  4-3: Compare for Damping ratio and Natural Frequence parameter ----------------
Dy_xix_Xix3_Err = np.zeros((len(G_rho_cofficient10) ,len(Dy_cofficient2)+1))

Dy_wx_Wx3_Err = np.zeros((len(G_rho_cofficient10) ,len(Dy_cofficient2)+1))
for h in range(len(Dy_cofficient2)):
    for j in range(len(G_rho_cofficient10)):
        Dy_xix_Xix3_Err[j ,0] = G_rho_cofficient10[j]
        Dy_xix_Xix3_Err[j , 1+h] = abs( (1/((1+ G_rho_cofficient10[j]*Dy_cofficient2[h])* (1+ G_rho_cofficient10[j]*(1/Dy_cofficient2[h])))**0.5) -1 )
        
        Dy_wx_Wx3_Err[j ,0] = G_rho_cofficient10[j]
        Dy_wx_Wx3_Err[j , 1+h] = abs( (((1+ G_rho_cofficient10[j]* (1/Dy_cofficient2[h]))* (1/(1+ G_rho_cofficient10[j]*Dy_cofficient2[h])))**0.5)-1 )

def plot_Test4_3(titleName, rho_cofficient2, Dy5_xix_Xix, xlabel, ylabel):
    plt.figure(figsize=(10,8))
    # plt.title(titleName, fontsize = 20)
    # # -----------------Test 2-3 (Xlabel = M,G_cofficient) -------------------------   
    plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 1], label = r"$\Delta_{y}'/\Delta_{y} = 0.5$", color= 'darkorange', linewidth = 6.0) # , ls = '--' 
    plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 2], label = r"$\Delta_{y}'/\Delta_{y} = 1.0$", color= 'blue',  linewidth = 4.0) # , ls = '-.'
    plt.plot(rho_cofficient2[:], Dy5_xix_Xix[:, 3], label = r"$\Delta_{y}'/\Delta_{y} = 2.0$", color= 'red', ls = '--', linewidth = 2.0) # , ls = ':'

    plt.xscale("log") # ,base = 10
    plt.yscale("log") # ,base = 10
    plt.grid(True)
    # ========== set up figure thick ============================
    bwidth = 2
    TK = plt.gca()
    TK.spines['bottom'].set_linewidth(bwidth)
    TK.spines['left'].set_linewidth(bwidth)
    TK.spines['top'].set_linewidth(bwidth)
    TK.spines['right'].set_linewidth(bwidth)
    
    legend1 = plt.legend(loc='lower right',fontsize=18)
    legend1.get_frame().set_edgecolor('grey')
    legend1.get_frame().set_linewidth(2)  # 設置外框寬度
    
    plt.xlim(1.25e-8, 1.0)
    plt.ylim(1e-8, 0.0)
    plt.xlabel(xlabel, fontsize = 20) # r"$G^{'}/G$"
    plt.ylabel(ylabel, fontsize = 20)  # r"$m_{x'}/m_{x}$"
    plt.xticks(fontsize = 18, fontweight='bold', color='black')
    plt.yticks(fontsize = 18, fontweight='bold', color='black')
    
    ax = plt.gca()
    ax.tick_params(axis='x', which='major', labelsize= 18, length=8, width=2)
    ax.tick_params(axis='x', which='minor', length=4, width=2, color='gray')
    
    ax.tick_params(axis='y', which='major', labelsize= 20, length=8, width=2)
    ax.tick_params(axis='y', which='minor', length=4, width=2, color='gray')
    
# plot_Test4_3(f'Error Compare Ghost element Damping Ratio with LK Dashpot ', G_rho_cofficient10, Dy_xix_Xix3_Err, r"$E_{i}'/E_{i}$ $,$ $\rho'/\rho$", r"$\mid(\xi_{i}'-\xi_{i})/\xi_{i}\mid$")
# plot_Test4_3(f'Error Compare Ghost element Nature Frequency with LK Dashpot ', G_rho_cofficient10, Dy_wx_Wx3_Err, r"$E_{i}'/E_{i}$ $,$ $\rho'/\rho$", r"$\mid(\omega_{i}'-\omega_{i})/\omega_{i}\mid$")

# ============== Test5-1: Critial TimeStep parameter Compare ----------------------
# Dy_cofficient2 = np.array([0.5, 1.0, 2.0]) # Dy_Ghost/Dy
M_cofficient7 = np.linspace(1e-4, 100, 2000) # M_G/ M 
G_cofficient7 = np.linspace(1e-4, 100, 2000) # G_/ G
rho_cofficient7 = np.array([1e+1, 1e-0, 1e-1, 1e-2, 1e-4]) # rho2/ rho

Dy5_dt_Dt = np.zeros((len(G_cofficient7) ,len(rho_cofficient7)+1))
Dy10_dt_Dt = np.zeros((len(G_cofficient7) ,len(rho_cofficient7)+1))
Dy20_dt_Dt = np.zeros((len(G_cofficient7) ,len(rho_cofficient7)+1))

for i in range(len(rho_cofficient7)):
    for j in range(len(G_cofficient7)):
    # ------------- Dt'/Dt = (Dy'/Dy)*sqrt(rho2/rho)*sqrt(Ei/Ei') -------------------------
        Dy5_dt_Dt[j, 0] = G_cofficient7[j]
        Dy5_dt_Dt[j, 1+i] = Dy_cofficient2[0]*((rho_cofficient7[i])**0.5)*(1/G_cofficient7[j])**0.5
      
        Dy10_dt_Dt[j, 0] = G_cofficient7[j]
        Dy10_dt_Dt[j, 1+i] = Dy_cofficient2[1]*((rho_cofficient7[i])**0.5)*(1/G_cofficient7[j])**0.5
        
        Dy20_dt_Dt[j, 0] = G_cofficient7[j]
        Dy20_dt_Dt[j, 1+i] = Dy_cofficient2[2]*((rho_cofficient7[i])**0.5)*(1/G_cofficient7[j])**0.5
    # ------------- Dt'/Dt = (Dy'/Dy)*(rho2/rho)*(Ei/Ei') -------------------------
    
# ============== Test5-2: Critial TimeStep parameter Compare ----------------------
Dy_cofficient3 = np.array([0.25, 0.5, 1.0, 2.0, 4.0]) # Dy_Ghost/Dy
rho_G_cofficient8 = np.linspace(1e-4, 100, 2000) # ((G/G_)*(rho2/ rho)) 
 
rho_G_dt_Dt2 = np.zeros((len(rho_G_cofficient8) ,len(Dy_cofficient3)+1)) 
rho_G_dt_Dt3 = np.zeros((len(rho_G_cofficient8) ,len(Dy_cofficient3)+1)) 

for i in range(len(Dy_cofficient3)):
    for j in range(len(rho_G_cofficient8)):
        rho_G_dt_Dt2[j, 0] = (rho_G_cofficient8[j])**0.5
        rho_G_dt_Dt2[j, 1+i] = Dy_cofficient3[i]* (rho_G_cofficient8[j])**0.5
        
        rho_G_dt_Dt3[j, 0] = rho_G_cofficient8[j]
        rho_G_dt_Dt3[j, 1+i] = (Dy_cofficient3[i])* rho_G_cofficient8[j] # ((Dy_cofficient3[i])**2)* rho_G_cofficient8[j]

def plot_Test5(G_cofficient6, Dy5_dt_Dt):
# # ------------- (Test5-1: Xlabel = rho_cofficient2)-----------------------------
#     plt.plot(G_cofficient6[:], Dy5_dt_Dt[:, 1], label = r"$\rho'/\rho = 10.0$", color= 'darkgrey', linewidth = 7.0) # ,ls = '--'
#     plt.plot(G_cofficient6[:], Dy5_dt_Dt[:, 2], label = r"$\rho'/\rho = 1.0$", color= 'darkgreen',  linewidth = 6.0) # , ls = '-.'
#     plt.plot(G_cofficient6[:], Dy5_dt_Dt[:, 3], label = r"$\rho'/\rho = 1/10$", color= 'darkorange',  linewidth = 5.0) # , ls = ':'
#     plt.plot(G_cofficient6[:], Dy5_dt_Dt[:, 4], label = r"$\rho'/\rho = 1/100$", color= 'red',  linewidth = 4.0) # , ls = '-'
#     plt.plot(G_cofficient6[:], Dy5_dt_Dt[:, 5], label = r"$\rho'/\rho = 1/10000$", color= 'blue',  linewidth = 3.0) # , ls = '-'

# ------------- (Test5-2: Xlabel = G_rho_cofficient8)-----------------------------
    plt.plot(G_cofficient6[:], Dy5_dt_Dt[:, 1], label = r"$\Delta_{y}'/\Delta_{y} = 0.25$", color= 'darkgrey', linewidth = 7.0) # ,ls = '--'
    plt.plot(G_cofficient6[:], Dy5_dt_Dt[:, 2], label = r"$\Delta_{y}'/\Delta_{y} = 0.50$", color= 'darkorange',  linewidth = 6.0) # , ls = '-.'
    plt.plot(G_cofficient6[:], Dy5_dt_Dt[:, 3], label = r"$\Delta_{y}'/\Delta_{y} = 1.0$", color= 'blue',  linewidth = 5.0) # ,
    plt.plot(G_cofficient6[:], Dy5_dt_Dt[:, 4], label = r"$\Delta_{y}'/\Delta_{y} = 2.0$", color= 'red',  linewidth = 4.0) # ,
    plt.plot(G_cofficient6[:], Dy5_dt_Dt[:, 5], label = r"$\Delta_{y}'/\Delta_{y} = 4.0$", color= 'darkgreen',  linewidth = 3.0) # ,
    
    plt.grid(True)  
    # ========== set up figure thick ============================
    bwidth = 2
    TK = plt.gca()
    TK.spines['bottom'].set_linewidth(bwidth)
    TK.spines['left'].set_linewidth(bwidth)
    TK.spines['top'].set_linewidth(bwidth)
    TK.spines['right'].set_linewidth(bwidth)
    
    plt.xlim(1e-2, 1e2) # 1e-2, 10 for sqrt;  1e-4, 100 for squre
    plt.ylim(1e-1,1e1)
    # plt.gca().invert_xaxis() # invert the xais to make bigger value to the left
    plt.xticks(fontsize = 18, fontweight='bold', color='black')
    plt.yticks(fontsize = 18, fontweight='bold', color='black')
    
    ax = plt.gca()
    ax.tick_params(axis='x', which='major', labelsize= 18, length=8, width=2)
    ax.tick_params(axis='x', which='minor', length=4, width=2, color='gray')
    
    ax.tick_params(axis='y', which='major', labelsize= 20, length=8, width=2)
    ax.tick_params(axis='y', which='minor', length=4, width=2, color='gray')
    
# # ------------- (Test5-1: Xlabel = rho_cofficient2)-----------------------------
# row_heights = [3,3,3]
# fig9, (ax25,ax26,ax27) = plt.subplots(nrows= 3, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # fig9.suptitle(f'Compare Ghost element and Real Element Critial TimeStep',x=0.50,y =0.95,fontsize = 20)
# fig9.text(0.73,0.85, r"$\rho'$ $\mathrm {Control}$", color = "black", fontsize=20) 
# fig9.text(0.015,0.5, r"$\Delta_{t}'/\Delta_{t}$", va= 'center', rotation= 'vertical', fontsize=20)
# fig9.text(0.47,0.04, r"$E_{i}'/E_{i}$", va= 'center', fontsize=20)

# ax25 = plt.subplot(311)
# plot_Test5(M_cofficient7, Dy5_dt_Dt)
# ax25.set_title(r"$\Delta_{y}'/\Delta_{y} = 0.5$",fontsize =21, x=0.15, y=0.03)
# ax25.set_xscale('log') # , base=10
# ax25.set_yscale('log') # , base=10

# ax26 = plt.subplot(312)
# plot_Test5(M_cofficient7, Dy10_dt_Dt)
# ax26.set_title(r"$\Delta_{y}'/\Delta_{y} = 1.0$",fontsize =21, x=0.15, y=0.03)
# ax26.set_xscale('log') # , base=10
# ax26.set_yscale('log') # , base=10

# ax27 = plt.subplot(313)
# plot_Test5(M_cofficient7, Dy20_dt_Dt)
# ax27.set_title(r"$\Delta_{y}'/\Delta_{y} = 2.0$",fontsize =21, x=0.15, y=0.03)
# ax27.set_xscale('log') # , base=10
# ax27.set_yscale('log') # , base=10

# font_props = {'family': 'Arial', 'size': 15}  #Legend Setting

# lines, labels = fig9.axes[-1].get_legend_handles_labels()
# legend1 = fig9.legend(lines, labels, ncol=2, loc = (0.25, 0.88), prop=font_props) # 'center right'
# legend1.get_frame().set_edgecolor('grey')
# legend1.get_frame().set_linewidth(2)  # 設置外框寬度

dt = 2e-5 #2e-5
time = np.arange(0.0, 1.0+dt, dt)

# # ------------- (Test5-2: Xlabel = G_rho_cofficient8)-----------------------------
# row_heights = [2,4,2]
# fig10, (ax28) = plt.subplots(nrows= 1, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # fig10.suptitle(f'Compare Ghost element and Real Element Critial TimeStep',x=0.50,y =0.95,fontsize = 20)
# # fig10.text(0.42,0.89, r"$\rho'$ $\mathrm {Control}$", color = "red", fontsize=20) 
# fig10.text(0.015,0.5, r"$\Delta_{t}'/\Delta_{t}$", va= 'center', rotation= 'vertical', fontsize=20)
# fig10.text(0.40,0.04, r"$\sqrt{\rho'/\rho}$/$\sqrt{E_{i}/E_{i}'}$", va= 'center', fontsize=20)

# ax28 = plt.subplot(111)
# plot_Test5(rho_G_cofficient8, rho_G_dt_Dt2)
# # ax28.set_title(r"$\Delta_{y}'/\Delta_{y} = 0.5$",fontsize =23, x=0.80, y=0.80)
# ax28.set_xscale('log') # , base=10
# ax28.set_yscale('log') # , base=10
# ax28.legend(loc='upper left',fontsize=18)

# row_heights = [2,4,2]
# fig11, (ax29) = plt.subplots(nrows= 1, ncols=1, sharex=True, figsize=(8, sum(row_heights)))
# # fig11.suptitle(f'Compare Ghost element and Real Element Critial TimeStep',x=0.50,y =0.95,fontsize = 20)
# # fig10.text(0.42,0.89, r"$\rho'$ $\mathrm {Control}$", color = "red", fontsize=20) 
# fig11.text(0.015,0.5, r"$\Delta_{t}'/\Delta_{t}$", va= 'center', rotation= 'vertical', fontsize=20)
# fig11.text(0.40,0.03, r"$(\rho'/\rho)/$ $(E_{i}/E_{i}')$", va= 'center', fontsize=20)

# ax29 = plt.subplot(111)
# plot_Test5(rho_G_cofficient8, rho_G_dt_Dt3)
# # ax28.set_title(r"$\Delta_{y}'/\Delta_{y} = 0.5$",fontsize =23, x=0.80, y=0.80)
# ax29.set_xscale('log') # , base=10
# ax29.set_yscale('log') # , base=10
# ax29.legend(loc='upper left',fontsize=16)


    
