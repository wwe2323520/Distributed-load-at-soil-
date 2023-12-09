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

Nele = Soil_80row # Soil_80row
End_Ele = Nele-1
cs = 200 # m/s
L = 10 # m(Soil_Depth)
nu = 0.3  #  0.3 -> (epsilon_z /=0)
rho = 2000 # kg/m3 
G = (cs*cs)*rho  # N/m^2 = Kg/(m*s^2)
E =  G*2*(1+nu)  # N/m^2 = Kg/(m*s^2)
cp = (E*(1-nu)/((1+nu)*(1-2*nu)*rho))**(0.5)

A = 0.1# 0.1
w =  pi/5 # 0 to 10 = 0 to 2*pi => x = pi/5

# calculate eace step time
tns = L/cs # wave transport time
dcell = tns/Nele #each cell time
dt = dcell/10 #eace cell have 10 steps
print(f"wave travel = {tns} ;dcell = {dcell} ;dt = {dt}")

time = np.arange(0.0,0.050005,dt)
time_Node = np.arange(0.0,0.050005,dt)
Nt = len(time)
#----------- Soil Coordinate --------------
x = cs*time #m
def Incoming_wave(x,t):  #事實上為（xi,yi,t），空間跟時間資訊全寫進去，目前只用到yi的空間
    return np.sin(w*(x-cs*t))

def Outgoing_wave(x,t):
    return np.sin(w*(x+cs*t))

Nnode = Nele + 1
End_Node = Nele
dy = L/Nele # 1, 0.1
dx= dy/10 # 0.1, 0.01 each element have 10 step dx

total_Transport = np.arange(0.0,20.1, dx)

# ---------- Incoming wave (Beam distributed load)------------------
XIn = np.zeros((len(total_Transport),Nele))
# X = 0~10 m 
for j in range(Nele): #100
    tin = time[10*j+5]
    x0 = x[10*j+5]  # 0.05,0.15,0.25....,9.95
    # print(x0,cs*tin)
    for i in range(len(time)):      
        xii = x0 + dx*i 
        XIn[5+10*j+i,j] = Incoming_wave(xii,tin)  #from 0.05m to 9.95m

# ---------- Outcoming wave (Beam distributed load)-------------------
XOut = np.zeros((len(total_Transport),Nele))
Output_disp = 5 # 9.95
End_disp = 10*Nele-5
# X = 10m ~ 20m
for j in range(Nele):# 100
    tout = time[Output_disp+10*j] 
    x0 = (L-(dy/2))-dy*j   #9.5/9.75/9.875/9.9375/9.95-dy*j 
    # print(x0,cs*tout)
    for i in range(len(time)):      
        xoo = x0 + dx*i 
        XOut[End_disp-10*j+i,End_Ele-j] = Outgoing_wave(xoo,tout)  #from 9.95m to 0.05m      
        
# ---------- Incoming wave (Nodal Load)------------------
XNodeIn = np.zeros((len(total_Transport),Nnode))
# X = 0~10 m 
for j in range(Nnode): #Nele 101
    tNin = time[10*j+0]
    x0 = x[10*j+0] # 1,2,3
    # print(x0,cs*tNin)
    for i in range(len(time)):      
        xii = x0 + dx*i 
        XNodeIn[0+10*j+i,j] = Incoming_wave(xii,tNin)  #from 0.05m to 9.95m
        # print(xii)
# ---------- Outcoming wave (Nodal load)-------------------
XNodeOut = np.zeros((len(total_Transport),Nnode))
Endx0 = Nele*10
# X = 10m ~ 20m
for j in range(Nnode):# Nnode 101
    tNout = time[10*j]
    x0 =  x[Endx0-10*j]
    # print(x0,cs*tNout)
    for i in range(len(time)):      
        xoo = x0 + dx*i 
        XNodeOut[Endx0-10*j+i,End_Node-j] = Outgoing_wave(xoo,tNout)  #from 10.0m to 0.0m   

total_time = np.arange(0.0,0.4001,dt)
Swave = np.zeros((len(total_time),Nele))

# ===== New BC Sideforce on Left and Right ==============

SNodeforce_x = np.zeros((len(total_time),Nnode)) # 11  ## 名字也不能叫force，需乘以面積才能叫force
SNodeforce_y = np.zeros((len(total_time),Nnode)) # 11

SSideforce_y = np.zeros((len(total_time),Nele))  # 10

# ----- 事實上是算 taux、tauy ------------------
# ===== Input Incoming Wave and Outcoming Wave to wave1 =======================
for g in range(Nele): #Nele
    to = 5 + 10*g
    for t in range(len(total_time)):
        if total_time[t] < 0.05:
            Swave[to+t,g] = (Swave[to+t,g] + XIn[to+t,g])  # original wave transport
# ----- Swave sigma_yy --------------------------   
            SSideforce_y[to+t,g] = SSideforce_y[to+t,g] + (XIn[to+t,g])
            
        if total_time[t] >= 0.05 and total_time[t] < 0.1:
            Swave[to+t,End_Ele-g] = Swave[to+t,End_Ele-g] + XOut[t-to,End_Ele-g]   # original wave transport
# ----- Swave sigma_yy --------------------------
            SSideforce_y[to+t,End_Ele-g] = SSideforce_y[to+t,End_Ele-g] + (-XOut[t-to,End_Ele-g])

ForceX_Cofficient = (cp/cs)
for m in range(Nnode): #Nnode 101/ 81
    t1 = 10*m
    # print(t1)
    for n in range(len(total_time)):
        if total_time[n] < 0.05:
# ----- Swave eta_p*(Vx) -------------------------- 
            SNodeforce_x[t1+n,m] = SNodeforce_x[t1+n,m] + (ForceX_Cofficient *XNodeIn[t1+n,m])
# ----- Swave sigma_xy ---------------------------------------
            SNodeforce_y[t1+n,m] = SNodeforce_y[t1+n,m] + (XNodeIn[t1+n,m])
            
        if total_time[n] >= 0.05 and total_time[n] < 0.1: 
# ----- Swave eta_p*(Vx) taux -------------------------- 
            SNodeforce_x[t1+n,End_Node-m] = SNodeforce_x[t1+n,End_Node-m] + (ForceX_Cofficient *XNodeOut[n-t1,End_Node-m])
# ----- Swave sigma_xy tauy---------------------------------------
            SNodeforce_y[t1+n, End_Node-m] = SNodeforce_y[t1+n, End_Node-m] + (-XNodeOut[n-t1, End_Node-m])
# --只需要vx vy sx sy sxy etax etay(7個)----
            
            
# ---- Output matrix eace column to txt file --------------
num_rows, num_cols = SNodeforce_y.shape# 8001,100
# # 建立資料夾
# # ---------- Swave ---------------
# S_folder_name_x = "S_Nodeforce_80rowx"

# os.makedirs(S_folder_name_x, exist_ok=True)
# for col in range(num_cols):
#     column_values = SNodeforce_x[:, col]
#     output_file = f"node{col + 1}.txt"
#     with open(os.path.join(S_folder_name_x, output_file), 'w') as f:
#         for value in column_values:
#             f.write(f"{value}\n")

# ---------- S wave NodalForce Wy---------------
S_folder_name_y = "S_Nodeforce_80rowy" # NodalForce
os.makedirs(S_folder_name_y, exist_ok=True)
for col in range(num_cols):
    column_values = SNodeforce_x[:, col]
    output_file = f"node{col + 1}.txt"
    with open(os.path.join(S_folder_name_y, output_file), 'w') as f:
        for value in column_values:
            f.write(f"{value}\n")
            
# ---- Output matrix eace column to txt file --------------
# num_rows, num_cols = SSideforce_y.shape# 8001,100

# S_folder_name_y = "S_Sideforce_y"
# os.makedirs(S_folder_name_y, exist_ok=True)
# # 逐一建立txt檔案並放入資料夾
# for col in range(num_cols):
#     column_values = SSideforce_y[:, col]
#     output_file = f"ele{col + 1}.txt"
#     with open(os.path.join(S_folder_name_y, output_file), 'w') as f:
#         for value in column_values:
#             f.write(f"{value}\n")
            
# # ------- wave put into the timeSeries ---------------   
plt.figure(figsize=(8,6))
# plt.title('Wave Transport',fontsize = 18)   
 
# plt.title(r'SideForce $\sigma_{xy}$',fontsize = 18)    
plt.title(r'NodeForce $\sigma_{xy}$',fontsize = 18)      
# plt.title(r'NodeForce $\eta_{p}v_x$',fontsize = 18)   

plt.xlabel("time t(s)",fontsize=18)
# # ----- Swave -------------
# plt.plot(total_time,Swave[:,0],label ='Node 1', marker='o', markevery=100)
# plt.plot(total_time,Swave[:,20],label ='Node 5', marker='x', markevery=100)
# plt.plot(total_time,Swave[:,39],label ='Node 10', marker='d', markevery=100)

# ----- Swave eta_p*(Vx) -------------
# plt.plot(total_time,SNodeforce_x[:,0],label ='Bot node', marker='o', markevery=100)
# plt.plot(total_time,SNodeforce_x[:,40],label ='Center node', marker='x', markevery=100)
# plt.plot(total_time,SNodeforce_x[:,80],label ='Top node', marker='d', markevery=100)

# ----- Swave sigma_xy -------------
# plt.plot(total_time,SSideforce_y[:,0],label ='Element 1', marker='o', markevery=100)
# plt.plot(total_time,SSideforce_y[:,40],label ='Element 5', marker='x', markevery=100)
# plt.plot(total_time,SSideforce_y[:,79],label ='Element 10', marker='d', markevery=100)

plt.plot(total_time,SNodeforce_y[:,0],label ='Bot node', marker='o', markevery=100)
plt.plot(total_time,SNodeforce_y[:,40],label ='Center node', marker='x', markevery=100)
plt.plot(total_time,SNodeforce_y[:,80],label ='Top node', marker='d', markevery=100)

plt.legend(loc='lower right',fontsize=18)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlim(0.0, 0.20) # 0.40
plt.grid(True)

# # ========== Incoming Wave ==========================================
# plt.figure()
# plt.title('Node Incoming Wave',fontsize = 18)
# plt.xlabel("x(m)",fontsize=18)
# plt.ylabel(r"$y=sin\omega(x-c_{s}t)$",fontsize=18)
# plt.plot(total_Transport,XNodeIn[:,0],label ='Node 1',marker='o', markevery=100)
# plt.plot(total_Transport,XNodeIn[:,40],label ='Node 40',marker='d', markevery=100)
# plt.plot(total_Transport,XNodeIn[:,80],label ='Node 81',marker='x', markevery=100)
# plt.legend(loc='upper right',fontsize=18)
# plt.xlim(0,30.0)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.grid(True)

# # ========== Outcoming Wave ==========================================
# plt.figure()
# plt.title('Node Outcoming Wave',fontsize = 18)
# plt.xlabel("x(m)",fontsize=18)
# plt.ylabel(r"$y=sin\omega(x+c_{s}t)$",fontsize=18)
# plt.plot(total_Transport,XNodeOut[:,0],label ='Node 1',marker='o', markevery=100)
# plt.plot(total_Transport,XNodeOut[:,40],label ='Node 40',marker='d', markevery=100)
# plt.plot(total_Transport,XNodeOut[:,80],label ='Node 80',marker='x', markevery=100)
# plt.xlim(0,30.0)

# plt.legend(loc='upper right',fontsize=18)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.grid(True)

# # ========== Incoming Wave ==========================================
# plt.figure()
# plt.title('Incoming Wave',fontsize = 18)
# plt.xlabel("x(m)",fontsize=18)
# plt.ylabel(r"$y=sin\omega(x-c_{s}t)$",fontsize=18)
# plt.plot(total_Transport,XIn[:,0],label ='ele 1',marker='o', markevery=100)
# plt.plot(total_Transport,XIn[:,39],label ='ele 39',marker='d', markevery=100)
# plt.plot(total_Transport,XIn[:,79],label ='ele 79',marker='x', markevery=100)
# plt.legend(loc='upper right',fontsize=18)
# plt.xlim(0,30.0)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.grid(True)

# # ========== Outcoming Wave ==========================================
# plt.figure()
# plt.title('Outcoming Wave',fontsize = 18)
# plt.xlabel("x(m)",fontsize=18)
# plt.ylabel(r"$y=sin\omega(x+c_{s}t)$",fontsize=18)
# plt.plot(total_Transport,XOut[:,0],label ='ele 1',marker='o', markevery=100)
# plt.plot(total_Transport,XOut[:,39],label ='ele 39',marker='d', markevery=100)
# plt.plot(total_Transport,XOut[:,79],label ='ele 79',marker='x', markevery=100)
# plt.xlim(0,30.0)

# plt.legend(loc='upper right',fontsize=18)
# plt.xticks(fontsize = 15)
# plt.yticks(fontsize = 15)
# plt.grid(True)


        
