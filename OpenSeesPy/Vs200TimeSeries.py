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

#Give S-wave vel to calculate P-wave 
pi = np.pi
m = 10 #each cell mass
lamb_cp = 10 #total length cp
# lamb_cs = 0.1 #total length cs
Soil_10row= 10 # dt= 5e-4       #cpdt = 2.67e-4
Soil_20row= 20 # dt= 2.5e-4     #cpdt = 1.33e-4
Soil_40row= 40 # dt= 1.25e-4    #cpdt = 6.68e-05
Soil_80row= 80 # dt= 6.25e-05   #cpdt = 3.34e-05
#
nu = 0.3  #  0.3 -> (epsilon_z /=0)
rho = 2000 #1600 kg/m3  ; =1.6 ton/m3  
cs = 200 # m/s
print("Cs= ", cs)

G = (cs*cs)*rho  # N/m^2 = Kg/(m*s^2)
E =  G*2*(1+nu)  # N/m^2 = Kg/(m*s^2)
cp = (E*(1-nu)/((1+nu)*(1-2*nu)*rho))**(0.5)

E1 = E/(1-nu**2)
E2 = nu*E1
print("E= ",E,"G= ",G)


#calaulate wave length
fcs = cs / lamb_cp
Ts = 1/ fcs
ws = 2*pi/ Ts

fcp = cp / lamb_cp
Tp = 1/ fcp
wp = 2*pi/ Tp

# calculate eace step time
tns = lamb_cp/cs # wave transport time
dcell = tns/Soil_10row #each cell time
dt = dcell/10 #eace cell have 10 steps

print(f"lamb_cp= {lamb_cp} ;fcp= {fcp} ;Tp= {Tp} ;wp= {wp}")
print(f"lamb_cs= {lamb_cp} ;fcs= {fcs} ;Ts= {Ts} ;ws= {ws}")
print(f"wave travel = {tns} ;dcell = {dcell} ;dt = {dt}")
print(f"E1= {E1}; E2={E2}")

tnscp = lamb_cp/cp # wave transport time
dcellcp = tnscp/Soil_20row #each cell time
cpdt = dcellcp/10 #eace cell have 10 steps
print(f"Pwave travel = {tnscp} ;dcell = {dcellcp} ;dt = {cpdt}")
# ===============================Timeseries:Disp, Vel, Accel (Vs)====================================
A = 0.125 # 0.1*10 or 0.1*1
P = 2 #10

#time = np.linspace(0, 0.3, timeLEN) # np.arange(0,0.3001,1e-4)
time = np.arange(0,0.30005,dt)
timeCp = np.arange(0,0.30014,cpdt)
timeLEN =len(time)  #10001   3001

Stress = np.zeros(timeLEN)
vel = np.zeros(timeLEN)
Accel = np.zeros(timeLEN)
# Disp = np.zeros(timeLEN)
fs = np.zeros(timeLEN)

step = 100 #1870
#step = int(timeLEN-1)/3 #1/3 timeLEN
#Tstep = (timeLEN-1)*2/3 #2/3 timeLEN
#print("Step= ", step, "Tstep= ", Tstep)
Tstep = 2*step

TopForce =np.zeros(len(timeCp))
# sigma(x,t)= -P*sin(ws*t)/A
for i in range(timeLEN):
    # if i <= (step): # 0~0.05s
    if time[i] <= 0.05: # 0~0.05s
        Stress[i] = -P*np.sin(ws*time[i])/A
        vel[i] = -P*np.sin(ws*time[i])/(-rho*cs*A)
        # fs[i] = 1*np.sin(ws*time[i])
        fs[i] = 2*np.sin(ws*time[i])
    # elif  (time[i] > 0.1 and  time[i] < 0.15):
    #     fs[i] = -np.sin(ws*time[int(i-Tstep)])
    #     vel[i] = -P*np.sin(ws*time[int(i-Tstep)])/(-rho*cs*A)
    #     Stress[i] = +P*np.sin(ws*time[int(i-Tstep)])/A
    
##    if i >= (timeLEN/150) and i <= (timeLEN/100): #0.002~0.003s
##        vel[i] = time[i]
##        u1[i] = np.sin(w_s*time[i-200])
##        print("time= ", time[i])
    
for i in range(len(timeCp)):
    if timeCp[i] > 0.0267 and timeCp[i] < 0.0534:
        TopForce[i] = 2*np.sin(wp*timeCp[i])
        
size = len(time) #1e-5
# =========================integrate:Trapezodial rule===========================
def integrate(tns,vel):
    Trape = np.zeros(size)
    for i in range(size-1):
        dt = time[i+1] - time[i]
        Trape[i+1] = Trape[i] + (vel[i+1]+vel[i])*dt/2
    return(Trape)
#
#========================integrate:simpson 1/3 rule============================
def simpson(time,vel):
    simpson = np.zeros(size)
    summ = vel[0] + vel[30000]
    h = time[1]-time[0]
    for j in range(1,size-1):
#        k = time[0] + j*h 
        if (j%2) == 0: #even
            simpson[j] = summ+simpson[j-1] + 2* vel[j]
        else:          #odd
            simpson[j] = summ+simpson[j-1] + 4* vel[j]
    simpson = simpson*(h/3)
   
    return simpson
# ========================Differential:Finite differential Method=====================
#--------calculate by theory--------------
#def df(x):
#    if (0 <= x and x <= 0.1):
#        return -np.cos(2.0*np.pi*x/0.1)
#    elif (0.1 <= x and x <= 0.2):
#        return 0.0
#    else:
#        return -np.cos(2.0*np.pi*x/0.1)

def differential(tns,vel):
    FDM = np.zeros(size)
    for i in range(size-1):
        dt = time[i+1]-time[i]
        FDM[i] = (vel[i+1]-vel[i])/dt
    return FDM

eta = -1/(3)**(0.5)
xi1 = +1/(3)**(0.5)
xi2 = -1/(3)**(0.5)
## ==============================================================================#
disp = integrate(time,vel)  
accel = differential(time,vel)  

txy_1 = G*+5*(1+xi1)*disp
txy_2 = G*+5*(1-xi2)*disp
txy_total = +10*disp*G
txy_total2 = txy_1+txy_2

#
plt.figure(figsize=(10,8))
plt.rcParams["figure.figsize"] = (14, 8)

title_name = "TimeSeries" # Displacement\Node 3.4 shear stress

# plt.plot(time, disp,label="displacement",color='tab:red')
# plt.plot(time, vel, label="velocity",color='tab:blue')
# plt.plot(time, accel, label = "acceleration")
# plt.plot(time, Stress, label="Stress",color='tab:orange')
#plt.plot(time[:size-1],accel[:size-1],label="acceleration",color='m')
# plt.plot(time, fs, label= "force(Shear wave).txt")

plt.plot(timeCp, TopForce, label= "TopForce.txt")
# plt.plot(time, txy_1,label=r"integration point 1",color='tab:red')
# plt.plot(time, txy_2,label=r"integration point 2",color='tab:blue')
# plt.plot(time, txy_total,label=r"$\tau_{xy}$",color='tab:blue')
# plt.plot(time, txy_total2,label=r"$\tau_{xy2}$",color='tab:red')
# $\sigma_{x}$

#
plt.title(title_name, fontsize = 25)
plt.xlabel("tns",fontsize=18)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlim(0,0.2)
# plt.ylim(0,6e-6)

plt.legend(loc='upper right',fontsize=20)
plt.grid(True)
#
# x_axis=0.06

ax1 = plt.gca()
# ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax1.yaxis.get_offset_text().set(size=18)








