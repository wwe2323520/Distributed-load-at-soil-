# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 15:21:58 2023

@author: User
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
pi = np.pi

# Soil_10row= 10 # dt= 5e-4       #cpdt = 2.67e-4
# Soil_20row= 20 # dt= 2.5e-4     #cpdt = 1.33e-4
# Soil_40row= 40 # dt= 1.25e-4    #cpdt = 6.68e-05
# Soil_80row= 80 # dt= 6.25e-05   #cpdt = 3.34e-05
# Soil_100row= 100 # dt= 6.25e-05   #cpdt = 3.34e-05

wave_Choose = 'Swave'
Nele = 80 # Soil_80row
End_Ele = Nele-1
Nnode = Nele + 1

# --------------------------- Give S wave Velocity to Calculate P wave Velocity ----------------------------
cs = 200 # m/s
Soil_Depth = 10 # m(Soil_Depth)
nu = 0.3  #  0.3 -> (epsilon_z /=0)
rho = 2000 # kg/m3 
G = (cs*cs)*rho  # N/m^2 = Kg/(m*s^2)
E =  G*2*(1+nu)  # N/m^2 = Kg/(m*s^2)
cp = (E*(1-nu)/((1+nu)*(1-2*nu)*rho))**(0.5)

# -------- calaulate wave parameter: P wave and S wave ---------------------------
fcs = cs / Soil_Depth
Ts = 1/ fcs
ws = 2*pi/ Ts

fcp = cp / Soil_Depth
Tp = 1/ fcp
wp = 2*pi/ Tp

# --------------------------- Soil Parameter ---------------------------
A = 0.1 # 0.1
w =  pi/5 # 0 to 10 = 0 to 2*pi => x = pi/5

DW = 0.125 # x Column Mesh Size (m)
DC = 0.125 # y Roe Mesh Size (m)

# =========== For 2-D, decide by the wave transmit direction to use x or y ======================
# ====================== wave transmit with time (t) and space (x or y) ======================
def Incoming_Wave(x,y,t):
    return np.sin(w*(x+y-cs*t))

def OutGoing_Wave(x,y,t):
    return np.sin(w*(x+y+cs*t))

# ============= Calculate wave Transmit TimeStep ===============================
if wave_Choose in ['Swave']:
    wave_Vel = cs
    tns = Soil_Depth/(wave_Vel) # wave transport time
    dcell = tns/Nele #each cell time
    dt = dcell/10 #eace cell have 10 steps
    print(f"wave travel = {tns} ;dcell = {dcell} ;dt = {dt}")
    
elif wave_Choose in ['Pwave']:
    wave_Vel = cp
    tns = Soil_Depth/(wave_Vel) # wave transport time
    dcell = tns/Nele #each cell time
    dt = dcell/10 #eace cell have 10 steps
    print(f"wave travel = {tns} ;dcell = {dcell} ;dt = {dt}")
    
dy = Soil_Depth/Nele # 1, 0.1
dx= dy/10 # 0.1, 0.01 each element have 10 step dx
    
time = np.arange(0.0, 4*tns+dt, dt)  # 4*soilDepth TimeStep (each element have 10 step)
y = cs*time  # 4*soilDepth dy
x = 0.0

# -------------------------- calculate eace step time ---------------------------
def Give_me_Data(wave, x,y,time):
    # --------------- LK Dashpot Cofficient -----------------------
    eta_x = rho*cs 
    eta_y = rho*cp
    if wave in ['Swave']:
        wave_Vel = cs
        Condition = 'Swave'
    elif wave in ['Pwave']:
        wave_Vel = cp
        Condition = 'Pwave'
        
    # ----------- Stress / Velocity----------------------
    Impulse_Time = np.arange(0.0, Soil_Depth/wave_Vel, dt)
    Distributed_Force = 20 #(N)
    
    wave_Transport = np.zeros((len(time), Nnode))
    Stress = np.zeros((len(time), Nnode))
    
    Out_Ele = Nele*10
    
    for i in range(Nnode): #Nnode
        y_Incoming = y[10*i]
        y_OutGoing = y[Out_Ele-10*i]
        
        x_Incoming = 0.0
        x_OutGoing = 0.0
        tNode = time[10*i]
        
        for t in range(len(time)):
# ------------------ Incoming Wave Transport ------------------------------------
            if time[t] < tns:
                yin = y_Incoming + dx*t
                wave_Transport[t+10*i,i] = wave_Transport[t+10*i,i] + np.sin(w*(x_Incoming + yin-cs*tNode))#Incoming_Wave(x_Incoming, yin, tNode)
                Stress[t+10*i, i] = Stress[t+10*i, i] + np.sin(w*(x_Incoming + yin-cs*tNode)) # Incoming_Wave(x_Incoming, yin, tNode)

# ------------------ Reflecting Wave Transport ------------------------------------    
            if time[t] >= tns and time[t] < 2*tns:
                yout = y_OutGoing + dx*(t-Out_Ele)
                wave_Transport[t+10*i, Nele-i] =  wave_Transport[t+10*i, Nele-i] +  np.sin(w*(x_OutGoing + yout +cs*tNode)) #OutGoing_Wave(x_OutGoing, yout, tNode)
                Stress[t+10*i, Nele-i] =  Stress[t+10*i, Nele-i] - np.sin(w*(x_OutGoing + yout + cs*tNode)) # OutGoing_Wave(x_OutGoing, yout, tNode)
    
    P0 = -Distributed_Force*DW #np.sin(ws*(Impulse_Time)) # Distributed Force * DW            
    # ================ S Wave Input (Input File: sin(ws*t)=======================================
    if Condition in ['Swave']:
        Sxx = P0 / DW
        Vx = -(1/eta_x)*Sxx
        
        Velocity_x = Vx*wave_Transport
        Velocity_y = 0.0
        # ------------ Side Boundary Stress -----------------    
        Stress_xx = 0.0
        Stress_yy = 0.0
        Stress_xy = Sxx * Stress
        #------------- Output TimeSeries ------------------------
        SNodeforce_x = cp*Velocity_x#(cp/cs)*Stress
        SNodeforce_y = Stress
        
    # # ================ P Wave Input (Input File: sin(wp*t)=======================================     
    elif Condition in ['Pwave']:
        Syy = P0/DW  
        Vy = -(1/eta_y)*Syy
    
        Velocity_x = 0.0
        Velocity_y = Vy*wave_Transport
    # ------------ Side Boundary Stress -----------------
        Stress_xx = Syy*Stress
        Stress_yy = 0.0
        Stress_xy = 0.0
        #------------- Output TimeSeries ------------------------
        SNodeforce_x = Stress
        SNodeforce_y = (cs/cp)*Stress
    
    return(Velocity_x, Velocity_y, Stress_xx, Stress_yy, Stress_xy, eta_x, eta_y, SNodeforce_x, SNodeforce_y)

Vx, Vy, Sxx, Syy, Sxy, Eta_x, Eta_y, SNodeforce_x, SNodeforce_y = Give_me_Data('Swave',x,y,time)

# Vx, Vy, Sxx, Syy, Sxy, Ex, Ey, PNodeforce_x, PNodeforce_y = Give_me_Data('Swave',x,y,time)


# # ---- Output matrix eace column to txt file --------------
# num_rows, num_cols = SNodeforce_x.shape# 8001,100
# # 建立資料夾
# # ---------- Swave ---------------
# S_folder_name_x = "S_Nodeforce_80rowX"

# os.makedirs(S_folder_name_x, exist_ok=True)
# for col in range(num_cols):
#     column_values = SNodeforce_x[:, col]
#     output_file = f"node{col + 1}.txt"
#     with open(os.path.join(S_folder_name_x, output_file), 'w') as f:
#         for value in column_values:
#             f.write(f"{value}\n")

# # ---------- S wave NodalForce Wy---------------
# S_folder_name_y = "S_Nodeforce_80rowy" # NodalForce
# os.makedirs(S_folder_name_y, exist_ok=True)
# for col in range(num_cols):
#     column_values = SNodeforce_y[:, col]
#     output_file = f"node{col + 1}.txt"
#     with open(os.path.join(S_folder_name_y, output_file), 'w') as f:
#         for value in column_values:
#             f.write(f"{value}\n")



# draw('Wave Transport in space', wave_Transport, y)
# plt.plot(Impulse_Time[:], P0[:])
# plt.plot(Impulse_Time[:], Sxx[:]) # -20 ~ 20
x_axis = 0.025
def draw(titlename,ylabel, wave_Transport,y):
    plt.figure(figsize= (8,6))
    plt.title(titlename, fontsize = 20)
    
    plt.xlabel('time t (s)', fontsize = 20)
    # plt.ylabel(r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", fontsize = 20)
    plt.ylabel(ylabel, fontsize = 20)
        
    plt.plot(y[:], wave_Transport[:,0])
    plt.plot(y[:], wave_Transport[:,40])
    plt.plot(y[:], wave_Transport[:,80])
    # plt.ylim(0.0, SoilDepth)
    # plt.xlim(0,3*Soil_Depth) # For Space
    plt.xlim(0,0.16) # For time
    
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.grid(True)
    
    ax1 = plt.gca()
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
    ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    ax1.yaxis.get_offset_text().set(size=18)
                
# ---------- S wave plot ------------------
draw('Velocity TimeSeries', r"$v_{xx}$ $\mathrm {(m/s)}$",Vx, time)
draw(r"$\sigma_{xx}$ $\mathrm {TimeSeries}$", r"$\sigma_{xy}$ $\mathrm {(N/m)}$", Sxy, time)
# ------------ Output x、y direction TimeSeries plot ---------------------
draw('Node TimeSeries: X direction', 'SNode_x TimeSeries',SNodeforce_x, time)
draw('Node TimeSeries: Y direction', 'SNode_y TimeSeries',SNodeforce_y, time)

# # ---------- P wave plot ------------------
# draw('Velocity TimeSeries', r"$v_{yy}$ $\mathrm {(m/s)}$",Vy, time)
# draw(r"$\sigma_{xx}$ $\mathrm {TimeSeries}$", r"$\sigma_{xx}$ $\mathrm {(N/m)}$", Sxx, time)
# # ------------ Output x、y direction TimeSeries plot ---------------------
# draw('Node TimeSeries: X direction', 'PNode_x TimeSeries',PNodeforce_x, time)
# draw('Node TimeSeries: Y direction', 'PNode_y TimeSeries',PNodeforce_y, time)






