# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 15:45:04 2023

@author: User
"""
##use for vs wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
plt.rc('font', family= 'Times New Roman')

Soil_Width =  5 # m
#Give S-wave vel to calculate P-wave 
pi = np.pi
m = 10 #each cell mass

# lamb_cs = 0.1 #total length cs
Soil_10row= 10 # dt= 5e-4       #cpdt = 2.67e-4
Soil_20row= 20 # dt= 2.5e-4     #cpdt = 1.33e-4
Soil_40row= 40 # dt= 1.25e-4    #cpdt = 6.68e-05
Soil_80row= 80 # dt= 6.25e-05   #cpdt = 3.34e-05
Soil_100row= 100 # dt= 6.25e-05   #cpdt = 3.34e-05

#
nu = 1/3 #  0.3 -> (epsilon_z /=0) ; 1/3 -> (cp = 400 m/s)
rho = 2000 #1600 kg/m3  ; =1.6 ton/m3  
cs = 200 # m/s
print("Cs= ", cs)

G = (cs*cs)*rho  # N/m^2 = Kg/(m*s^2)
E =  G*2*(1+nu)  # N/m^2 = Kg/(m*s^2)
cp = (E*(1-nu)/((1+nu)*(1-2*nu)*rho))**(0.5)

def Cal_fp(fcp):
    Tp = 1/ fcp
    wp = 2*pi/ Tp
    
    SoilLength = 10 #m
    lamb_cp = cp/fcp #total length cp
    
    print(f"lamb_cp= {lamb_cp} ;fcp= {fcp} ;Tp= {Tp} ;wp= {wp}")
    
    tnscp = SoilLength/cp # wave transport time
    dcellcp = tnscp/Soil_40row #each cell time
    cpdt = dcellcp*0.1 #eace cell have 10 steps
    print(f"Pwave travel = {tnscp} ;dcell = {dcellcp} ;dt = {cpdt}")
    # ===============================Timeseries:Disp, Vel, Accel (Vs)====================================
    A = 0.125 # 0.1*10 or 0.1*1
    P = 2 #10
    
    Input_Time = lamb_cp/cp
    
    timeCp = np.arange(0, 0.2+cpdt, cpdt)
    fp = np.zeros(len(timeCp))
    
    # -------- Pwave From Bottom / TopForce Apply with P wave transport -------------------
    TopForce_fp = np.zeros(len(timeCp))
    P_Surface_Step = int(0.025/cpdt) # **********
    # P_Surface_Step = int(tnscp/cpdt) # **********
    
    Top_Time = SoilLength/cp
    print(f'Pwave Travel Time = {Input_Time}')
    
    for i in range(len(timeCp)):
        if timeCp[i] < Input_Time:
            fp[i] = 2*np.sin(wp*timeCp[i])
            
        if timeCp[i] >= Top_Time and timeCp[i] < (Top_Time + Input_Time):
            TopForce_fp[i] = 2*np.sin(wp*timeCp[i-P_Surface_Step])

    return fp, timeCp, TopForce_fp

# =========== Compare Integrator Frequency ==================================
fcp_40HZ = 40
fcp_80HZ = 80
fcp_160HZ = 160
fcp_320HZ = 320

fp_HZ40, timeCp_HZ40, TopHZ40_fp =  Cal_fp(fcp_40HZ)
fp_HZ80, timeCp_HZ80, TopHZ80_fp =  Cal_fp(fcp_80HZ)
fp_HZ160, timeCp_HZ160, TopHZ160_fp = Cal_fp(fcp_160HZ)
fp_HZ320, timeCp_HZ320, TopHZ320_fp = Cal_fp(fcp_320HZ)


def draw_plot(title_name, time,fp, time1,fp1, time2,fp2, time3,fp3):
    plt.figure(figsize=(10,8))
    plt.rcParams["figure.figsize"] = (14, 8)
    
    plt.plot(time, fp, label= r'$\mathrm {Original}$ $,t_d = 1/40$', color = 'black',linewidth = 3.0) 
    plt.plot(time1, fp1, label= r'$t_d = 1/80$', linewidth = 3.0) 
    plt.plot(time2, fp2, label= r'$t_d = 1/160$', linewidth = 3.0)
    plt.plot(time3, fp3, label= r'$t_d = 1/320$', linewidth = 3.0)
    
    plt.title(title_name, fontsize = 25)
    plt.xlabel("time t (s)", fontsize=18) # "time t (s)" / r'$t/t_d$'
    # plt.ylabel(r"$\mathrm {Velocity}$  $v_x$  $\mathrm {(m/s)}$",fontsize=18)
    plt.xticks(fontsize = 18)
    plt.yticks(fontsize = 18)
    plt.xlim(0, 0.025) # 0.025
    # plt.ylim(0,6e-6)
    plt.legend(loc='upper right',fontsize=18)
    plt.grid(True)
    
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
    ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    ax.yaxis.get_offset_text().set(size=18)

x_axis= 0.0125/2 #0.025 / 0.0267
# ------------ Force TimeSeries -----------------------------
# draw_plot("P wave Impulse TimeSeries", timeCp_HZ40,fp_HZ40, timeCp_HZ80,fp_HZ80, timeCp_HZ160,fp_HZ160, timeCp_HZ320,fp_HZ320) # "time t (s)"

# =========== Compare 1D Transport Frequency：Pwave ==================================
fcp_10HZ = 10
fcp_20HZ = 20
# fcp_40HZ = 40

fp_HZ10, timeCp_HZ10, TopHZ10_fp =  Cal_fp(fcp_10HZ)
fp_HZ20, timeCp_HZ20, TopHZ20_fp =  Cal_fp(fcp_20HZ)
# fp_HZ40, timeCp_HZ40 =  Cal_fp(fcp_40HZ)

def draw_plot2(title_name, time,fp, time1,fp1, time2,fp2):
    plt.figure(figsize=(10,8))
    plt.rcParams["figure.figsize"] = (14, 8)
    
    plt.plot(time, fp, label= r'$\mathrm {Original}$ $,t_d = 1/40$', color = 'black',linewidth = 3.0) 
    plt.plot(time1, fp1, label= r'$t_d = 1/10$', linewidth = 3.0) 
    plt.plot(time2, fp2, label= r'$t_d = 1/20$', linewidth = 3.0)

    plt.title(title_name, fontsize = 25)
    plt.xlabel("time t (s)", fontsize=18) # "time t (s)" / r'$t/t_d$'
    # plt.ylabel(r"$\mathrm {Velocity}$  $v_x$  $\mathrm {(m/s)}$",fontsize=18)
    plt.xticks(fontsize = 18)
    plt.yticks(fontsize = 18)
    plt.xlim(0, 0.2) # 0.025
    # plt.ylim(-2,2)
    plt.legend(loc='upper right',fontsize=18)
    plt.grid(True)
    
    ax = plt.gca()
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
    ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    ax.yaxis.get_offset_text().set(size=18)
    
# draw_plot2("P wave Impulse TimeSeries", timeCp_HZ40,fp_HZ40, timeCp_HZ10,fp_HZ10, timeCp_HZ20,fp_HZ20) # "time t (s)"
# draw_plot2("P wave Surface Impulse TimeSeries", timeCp_HZ40,TopHZ40_fp, timeCp_HZ10,TopHZ10_fp, timeCp_HZ20,TopHZ20_fp)

def Cal_fs(fcs):
    Ts = 1/ fcs
    ws = 2*pi/ Ts
    
    SoilLength = 10 #m
    lamb_cs = cs/fcs #total length cp
    
    print(f"lamb_cs= {lamb_cs} ;fcs= {fcs} ;Ts= {Ts} ;ws= {ws}")
    
    tnscs = SoilLength/cs # wave transport time
    dcellcs = tnscs/Soil_40row #each cell time
    csdt = dcellcs*0.1 #eace cell have 10 steps
    print(f"Swave travel = {tnscs} ;dcell = {dcellcs} ;dt = {csdt}")
    # ===============================Timeseries:Disp, Vel, Accel (Vs)====================================
    A = 0.125 # 0.1*10 or 0.1*1
    P = 2 #10
    
    Input_Time = lamb_cs/cs
    
    timeCs = np.arange(0, 0.2+csdt, csdt)
    fs = np.zeros(len(timeCs))
    
    # -------- Pwave From Bottom / TopForce Apply with P wave transport -------------------
    TopForce_fs = np.zeros(len(timeCs))
    S_Surface_Step = int(0.050/csdt) # **********
    
    Top_Time = SoilLength/cs
    print(f'Swave Travel Time = {Input_Time}')
    
    for i in range(len(timeCs)):
        if timeCs[i] < Input_Time:
            fs[i] = 2*np.sin(ws*timeCs[i])
            
        if timeCs[i] >= Top_Time and timeCs[i] < (Top_Time + Input_Time):
            TopForce_fs[i] = 2*np.sin(ws*timeCs[i-S_Surface_Step])

    return fs, timeCs, TopForce_fs
# =========== Compare 1D Transport Frequency： Swave ==================================
fcs_10HZ = 10
fcs_20HZ = 20
fcs_40HZ = 40

fs_HZ10, timeCs_HZ10,  Topfs_HZ10 = Cal_fs(fcs_10HZ)
fs_HZ20, timeCs_HZ20,  Topfs_HZ20 = Cal_fs(fcs_20HZ)
fs_HZ40, timeCs_HZ40,  Topfs_HZ40 = Cal_fs(fcs_40HZ)


def draw_plot3(title_name, time,fs, time1,fs1, time2,fs2):
    plt.figure(figsize=(10,8))
    plt.rcParams["figure.figsize"] = (14, 8)
    
    plt.plot(time, fs, label= r'$\mathrm {Original}$ $,t_d = 1/20$', color = 'black',linewidth = 3.0) 
    plt.plot(time1, fs1, label= r'$t_d = 1/10$', linewidth = 3.0) 
    plt.plot(time2, fs2, label= r'$t_d = 1/40$', linewidth = 3.0)

    plt.title(title_name, fontsize = 25)
    plt.xlabel("time t (s)", fontsize=18) # "time t (s)" / r'$t/t_d$'
    # plt.ylabel(r"$\mathrm {Velocity}$  $v_x$  $\mathrm {(m/s)}$",fontsize=18)
    plt.xticks(fontsize = 18)
    plt.yticks(fontsize = 18)
    plt.xlim(0, 0.2) # 0.025
    # plt.ylim(-2,2)
    plt.legend(loc='upper right',fontsize=18)
    plt.grid(True)
    
    ax = plt.gca()
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
    ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    ax.yaxis.get_offset_text().set(size=18)
    
# draw_plot3("S wave Impulse TimeSeries", timeCs_HZ20,fs_HZ20, timeCs_HZ10,fs_HZ10, timeCs_HZ40,fs_HZ40)

draw_plot3("S wave Surface Impulse TimeSeries", timeCs_HZ20,Topfs_HZ20, timeCs_HZ10,Topfs_HZ10, timeCs_HZ40,Topfs_HZ40)
