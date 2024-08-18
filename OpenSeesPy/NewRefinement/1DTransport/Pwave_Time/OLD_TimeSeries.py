# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 09:52:58 2023

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
pi = np.pi
# lamb_cs = 0.1 #total length cs
Soil_10row= 10 # dt= 5e-4       #cpdt = 2.67e-4
Soil_20row= 20 # dt= 2.5e-4     #cpdt = 1.33e-4
Soil_40row= 40 # dt= 1.25e-4    #cpdt = 6.68e-05
Soil_80row= 80 # dt= 6.25e-05   #cpdt = 3.34e-05
Soil_100row= 100 # dt= 6.25e-05   #cpdt = 3.34e-05

Nele = Soil_10row # Soil_80row
End_Ele = Nele-1
cs = 200 # m/s
L = 10 # m(Soil_Depth)
nu = (1/3)  #  0.3 -> (epsilon_z /=0)
rho = 2000 # kg/m3 
G = (cs*cs)*rho  # N/m^2 = Kg/(m*s^2)
E =  G*2*(1+nu)  # N/m^2 = Kg/(m*s^2)
cp = (E*(1-nu)/((1+nu)*(1-2*nu)*rho))**(0.5)

A = 0.1# 0.1
# ======== Different frequency to Control Ws and Wp (v = f * lambda)======================
ws_40HZ =  (2*pi)/5 # 0 to 5m = 0 to 2*pi => x = 2*pi/5
ws_20HZ =  pi/5  # 0 to 10m = 0 to 2*pi => x = pi/5
ws_10HZ =  pi/10 # 0 to 20m = 0 to 2*pi => x = pi/10

wp_20HZ =  pi/10 # 0 to 20m = 0 to 2*pi => x = pi/10
wp_10HZ =  pi/20 # 0 to 40m = 0 to 2*pi => x = pi/20
wp_40HZ =  pi/5 # 0 to 10m = 0 to 2*pi => x = pi/5

# ============================== Consider PWave ======================================
# calculate eace step time
tns_cp = L/cp # wave transport time
dcell_cp = tns_cp/Nele #each cell time
dt_cp = dcell_cp*0.1 #eace cell have 10 steps
print(f"Pwave travel = {tns_cp} ;dcell = {dcell_cp} ;dt = {dt_cp}")

time_cp = np.arange(0.0, 0.02503,dt_cp)
timecp_Node = np.arange(0.0, 0.02503,dt_cp)
Nt_cp = len(time_cp)

#----------- Soil Coordinate --------------
x = cp*time_cp #m
def Incoming_wave(w, x, cp, t):  #事實上為（xi,yi,t），空間跟時間資訊全寫進去，目前只用到yi的空間
    return np.sin(w*(x-cp*t)) # Normal：np.sin(w*(x-cs*t))

def Outgoing_wave(w, x, cp, t):
    return np.sin(w*(x+cp*t)) # Norrmal： np.sin(w*(x+cs*t))

Nnode = Nele + 1
End_Node = Nele
dy = L/Nele # 1, 0.1
dx= dy/10 # 0.1, 0.01 each element have 10 step dx

total_Transport_cp = np.arange(0.0,20.1, dx)

# ---------- Incoming wave (Beam distributed load)------------------
XIn = np.zeros((len(total_Transport_cp), Nele))
# X = 0~10 m 
for j in range(Nele): #100 
    tin = time_cp[10*j+5]
    x0 = x[10*j+5]  # 0.05,0.15,0.25....,9.95
    # print(x0,cp*tin)
    for i in range(len(time_cp)):      
        xii = x0 + dx*i 
        XIn[5+10*j+i,j] = Incoming_wave(wp_40HZ, xii, cp, tin)  #from 0.05m to 9.95m

# ---------- Outcoming wave (Beam distributed load)-------------------
XOut = np.zeros((len(total_Transport_cp), Nele))
Output_disp = 5 # 9.95
End_disp = 10*Nele-5
# X = 10m ~ 20m
for j in range(Nele):# 100 Nele
    tout = time_cp[Output_disp+10*j] 
    x0 = (L-(dy/2))-dy*j   #9.5/9.75/9.875/9.9375/9.95-dy*j 
    # print(x0,cp*tout)
    for i in range(len(time_cp)):      
        xoo = x0 + dx*i 
        XOut[End_disp-10*j+i,End_Ele-j] = Outgoing_wave(wp_40HZ, xoo, cp, tout)  #from 9.95m to 0.05m      
        
# ---------- Incoming wave (Nodal Load)------------------
XNodeIn = np.zeros((len(total_Transport_cp),Nnode))
# X = 0~10 m 
for j in range(Nnode): #Nele 101
    tNin = timecp_Node[10*j+0]
    x0 = x[10*j+0] # 1,2,3
    # print(x0,cp*tNin)
    for i in range(len(timecp_Node)):      
        xii = x0 + dx*i 
        XNodeIn[0+10*j+i,j] = Incoming_wave(wp_40HZ, xii, cp, tNin)  #from 0.05m to 9.95m
        # print(xii)
        
# ---------- Outcoming wave (Nodal load)-------------------
XNodeOut = np.zeros((len(total_Transport_cp),Nnode))
Endx0 = Nele*10
# X = 10m ~ 20m
for j in range(Nnode):# Nnode 101
    tNout = timecp_Node[10*j]
    x0 =  x[Endx0-10*j]
    # print(x0,cp*tNout)
    for i in range(len(timecp_Node)):      
        xoo = x0 + dx*i 
        XNodeOut[Endx0-10*j+i,End_Node-j] = Outgoing_wave(wp_40HZ, xoo, cp, tNout)  #from 10.0m to 0.0m   

total_time = np.arange(0.0,0.40003,dt_cp)
Pwave = np.zeros((len(total_time),Nele))

# ===== New BC Sideforce on Left and Right ==============
PNodeforce_x = np.zeros((len(total_time),Nnode)) # 11  ## 名字也不能叫force，需乘以面積才能叫force
PNodeforce_y = np.zeros((len(total_time),Nnode)) # 11

PSideforce_y = np.zeros((len(total_time),Nele))  # 10
PSideforce_x = np.zeros((len(total_time),Nele))  # 10

# ----- 事實上是算 taux、tauy ------------------

ForceX_Cofficient = nu/(1-nu)
ForceY_Cofficient = (cs/cp)

# Pwave Hz=10 => Xin + Xin (入射波跟回彈波都一樣 xin)
# ===== Input Incoming Wave and Outcoming Wave to wave1 =======================
for g in range(Nele): #Nele
    to = 5 + 10*g
    for t in range(len(total_time)):
        if total_time[t] < 0.025:
            Pwave[to+t,g] = (Pwave[to+t,g] + XIn[to+t,g])  # original wave transport
# ----- Swave sigma_yy --------------------------   
            PSideforce_x[to+t,g] = PSideforce_x[to+t,g] + (ForceX_Cofficient*XIn[to+t,g])
# ----- Swave eta_p*(Vx) --------------------------             
            PSideforce_y[to+t,g] = PSideforce_y[to+t,g] + (ForceY_Cofficient *XIn[to+t,g])
            
        if total_time[t] >= 0.025 and total_time[t] < 0.050:
            Pwave[to+t,End_Ele-g] = Pwave[to+t,End_Ele-g] + XOut[t-to,End_Ele-g]   # original wave transport
# ----- Swave sigma_yy --------------------------
            PSideforce_x[to+t,End_Ele-g] = PSideforce_x[to+t,End_Ele-g] - (ForceX_Cofficient*XOut[t-to,End_Ele-g]) # + (-XOut[t-to,End_Ele-g])
# ----- Swave eta_p*(Vx) taux --------------------------             
            PSideforce_y[to+t,End_Ele-g] = PSideforce_y[to+t,End_Ele-g] + (ForceY_Cofficient*XOut[t-to,End_Ele-g]) # + (ForceX_Cofficient *XOut[t-to,End_Ele-g])

for m in range(Nnode): #Nnode 101/ 81
    t1 = 10*m
    # print(t1)
    for n in range(len(total_time)):
        if total_time[n] < 0.025:
# ----- Swave eta_p*(Vx) -------------------------- 
            PNodeforce_x[t1+n,m] = PNodeforce_x[t1+n,m] + (ForceX_Cofficient *XNodeIn[t1+n,m])
# ----- Swave sigma_xy ---------------------------------------
            PNodeforce_y[t1+n,m] = PNodeforce_y[t1+n,m] + (ForceY_Cofficient *XNodeIn[t1+n,m])
            
        if total_time[n] >= 0.025 and total_time[n] < 0.050: 
# ----- Swave eta_p*(Vx) taux -------------------------- 
            PNodeforce_x[t1+n,End_Node-m] = PNodeforce_x[t1+n,End_Node-m] - (ForceX_Cofficient *XNodeOut[n-t1,End_Node-m]) # XNodeOut[n-t1,End_Node-m]
# ----- Swave sigma_xy tauy---------------------------------------
            PNodeforce_y[t1+n, End_Node-m] = PNodeforce_y[t1+n, End_Node-m] + (ForceY_Cofficient* XNodeOut[n-t1, End_Node-m]) # XNodeOut[n-t1, End_Node-m]
# --只需要vx vy sx sy sxy etax etay(7個)----
            

# # # ---- Output matrix eace column to txt file --------------
FilePath = f"D:/shiang/opensees/20220330/OpenSeesPy/TimeSeries/Pwave_Time"
# num_rows, num_cols = PSideforce_x.shape# SNodeforce_y.shape
# # # # # 建立資料夾
# # ---------- Swave ---------------
# S_folder_name_x = f"{FilePath}/SideBeam_Time/HZ40_P_Sideforce_{Nele}rowx" # "S_Nodeforce_80rowx"

# os.makedirs(S_folder_name_x, exist_ok=True)
# for col in range(num_cols):
#     column_values = PSideforce_x[:, col] # SNodeforce_x
#     output_file = f"ele{col + 1}.txt" # node{col + 1}.txt
#     with open(os.path.join(S_folder_name_x, output_file), 'w') as f:
#         for value in column_values:
#             f.write(f"{value}\n")
            
# # ---- Output matrix eace column to txt file --------------
# num_rows, num_cols = PSideforce_y.shape# 8001,100

# S_folder_name_y = f"{FilePath}/SideBeam_Time/HZ40_P_Sideforce_{Nele}rowy" # S_Sideforce_y
# os.makedirs(S_folder_name_y, exist_ok=True)
# # 逐一建立txt檔案並放入資料夾
# for col in range(num_cols):
#     column_values = PSideforce_y[:, col] #SSideforce_y
#     output_file = f"ele{col + 1}.txt"
#     with open(os.path.join(S_folder_name_y, output_file), 'w') as f:
#         for value in column_values:
#             f.write(f"{value}\n")

# # ---------- S wave NodalForce Wx---------------
# num_rows, num_cols = PNodeforce_x.shape# 8001,100

# S_folder_name_y = f"{FilePath}/SideBeam_Time/HZ40_P_Nodeforce_{Nele}rowx" # NodalForce
# os.makedirs(S_folder_name_y, exist_ok=True)
# for col in range(num_cols):
#     column_values = PNodeforce_x[:, col]
#     output_file = f"node{col + 1}.txt"
#     with open(os.path.join(S_folder_name_y, output_file), 'w') as f:
#         for value in column_values:
#             f.write(f"{value}\n")
            
# # ---------- S wave NodalForce Wy---------------
# num_rows, num_cols = PNodeforce_y.shape# 8001,100

# S_folder_name_y = f"{FilePath}/SideBeam_Time/HZ40_P_Nodeforce_{Nele}rowy" # NodalForce
# os.makedirs(S_folder_name_y, exist_ok=True)
# for col in range(num_cols):
#     column_values = PNodeforce_y[:, col]
#     output_file = f"node{col + 1}.txt"
#     with open(os.path.join(S_folder_name_y, output_file), 'w') as f:
#         for value in column_values:
#             f.write(f"{value}\n")

# # ------- wave put into the timeSeries ---------------   
plt.figure(figsize=(8,6))
# plt.title('Wave Transport',fontsize = 18)   
 
plt.title(r'SideForce $\nu/(1-\nu)$ $\sigma_{yy}$',fontsize = 18)    
# plt.title(r'SideForce $\eta_{s}v_y$',fontsize = 18)   

# plt.title(r'NodeForce $\sigma_{yy}$',fontsize = 18)      
# plt.title(r'NodeForce $\eta_{s}v_y$',fontsize = 18)   

plt.xlabel("time t(s)",fontsize=18)

# ----- Swave sigma_yy -------------
plt.plot(total_time,PSideforce_x[:,0],label ='Bot Element', marker='o', markevery=100)
plt.plot(total_time,PSideforce_x[:, int(Nele/2)-1],label ='Center Element', marker='x', markevery=100)
plt.plot(total_time,PSideforce_x[:, int(Nele-1)],label ='Top Element', marker='d', markevery=100)

# plt.plot(total_time,PNodeforce_x[:,0],label ='Bot node', marker='o', markevery=100)
# plt.plot(total_time,PNodeforce_x[:,int(Nele/2)],label ='Center node', marker='x', markevery=100)
# plt.plot(total_time,PNodeforce_x[:,int(Nele)],label ='Top node', marker='d', markevery=100)

# # ----- Swave eta_s*(Vy) -------------
# plt.plot(total_time,PSideforce_y[:,0],label ='Bot Element', marker='o', markevery=100)
# plt.plot(total_time,PSideforce_y[:, int(Nele/2)-1],label ='Center Element', marker='x', markevery=100)
# plt.plot(total_time,PSideforce_y[:, int(Nele-1)],label ='Top Element', marker='d', markevery=100)

# plt.plot(total_time,PNodeforce_y[:,0],label ='Bot node', marker='o', markevery=100)
# plt.plot(total_time,PNodeforce_y[:,int(Nele/2)],label ='Center node', marker='x', markevery=100)
# plt.plot(total_time,PNodeforce_y[:,int(Nele)],label ='Top node', marker='d', markevery=100)

plt.legend(loc='upper right',fontsize=18)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlim(0.0, 0.20) # 0.40
plt.grid(True)

# # ============ Beam "node" element transport =====================================================

# # ========== Incoming Wave ==========================================
# plt.figure()
# plt.title('Node Incoming Wave',fontsize = 18)
# plt.xlabel("x(m)",fontsize=18)
# plt.ylabel(r"$y=sin\omega(x-c_{s}t)$",fontsize=18)
# plt.plot(total_Transport,XNodeIn[:,0],label ='Node 1',marker='o', markevery=100)
# plt.plot(total_Transport,XNodeIn[:, int(Nele/2)],label ='Node 40',marker='d', markevery=100) # XNodeIn[:,40]
# plt.plot(total_Transport,XNodeIn[:, int(Nele)],label ='Node 81',marker='x', markevery=100) # XNodeIn[:,80]
# plt.legend(loc='upper right',fontsize=18)
# plt.xlim(0,30.0)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.grid(True)

# # ========== Outcoming Wave ========================================== Nnode
# plt.figure()
# plt.title('Node Outcoming Wave',fontsize = 18)
# plt.xlabel("x(m)",fontsize=18)
# plt.ylabel(r"$y=sin\omega(x+c_{s}t)$",fontsize=18)
# plt.plot(total_Transport,XNodeOut[:,0],label ='Node 1',marker='o', markevery=100)
# plt.plot(total_Transport,XNodeOut[:, int(Nele/2)],label ='Node 40',marker='d', markevery=100)
# plt.plot(total_Transport,XNodeOut[:, int(Nele)],label ='Node 80',marker='x', markevery=100)
# plt.xlim(0,30.0)

# plt.legend(loc='upper right',fontsize=18)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.grid(True)

# # # ============ Beam element transport =====================================================
# # ========== Incoming Wave ==========================================
# plt.figure()
# plt.title('Incoming Wave' + r"f = 40Hz",fontsize = 18)
# plt.xlabel("x(m)",fontsize=18)
# plt.ylabel(r"$y=sin\omega(x-c_{s}t)$",fontsize=18)
# plt.plot(total_Transport_cp, XIn[:,0],label ='ele 1',marker='o', markevery=100) # XIn[:,0]
# plt.plot(total_Transport_cp, XIn[:, int(Nele/2)-1],label ='ele 39',marker='d', markevery=100) # XIn[:,39]
# plt.plot(total_Transport_cp, XIn[:, int(Nele-1)],label ='ele 79',marker='x', markevery=100) # XIn[:,79]
# plt.legend(loc='upper right',fontsize=18)
# plt.xlim(0,30.0)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.grid(True)

# # ========== Outcoming Wave ==========================================
# plt.figure()
# plt.title('Outcoming Wave'+ r"f = 40Hz",fontsize = 18)
# plt.xlabel("x(m)",fontsize=18)
# plt.ylabel(r"$y=sin\omega(x+c_{s}t)$",fontsize=18)
# plt.plot(total_Transport_cp, XOut[:,0],label ='ele 1',marker='o', markevery=100)
# plt.plot(total_Transport_cp, XOut[:,int(Nele/2)-1],label ='ele 39',marker='d', markevery=100)
# plt.plot(total_Transport_cp, XOut[:,int(Nele-1)],label ='ele 79',marker='x', markevery=100)
# plt.xlim(0,30.0)

# plt.legend(loc='upper right',fontsize=18)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.grid(True)


        
