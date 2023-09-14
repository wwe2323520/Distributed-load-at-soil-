# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 23:17:24 2022

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
plt.rc('font', family= 'Times New Roman')
#----- SurfeceLoad wave propogate -----------
#Give p-wave vel 
pi = np.pi
cp = 100  # m/s 
Lp  = 10  # 10 m  2

fp = cp/Lp
Tp = 1/fp
wp = (2*pi)/Tp
print(f"lamb_cp= {Lp} ;fcp= {fp} ;Tp= {Tp} ;wp= {wp}")

step = 1000#1000
Tstep = 2*step

time = np.arange(0,0.8001,1e-4)
fp = np.zeros(len(time))
u2 = np.zeros(len(time))
top_force = np.zeros(len(time)) # top Structure force
top10_force = np.zeros(len(time))

for i in range(len(time)):
    # if i < st！ep:#step
        # fp[i] = +1*np.sin(wp*time[i])
        # fp[i] = +2*np.sin(wp*time[i])
    if (i > step and i < 2*step):
        top_force[i] = +2*np.sin(wp*time[i])
        # top10_force[i] = 1*np.sin(wp*time[i])
        
    # if (i > 2*step and i < 3*step):
    #     fp[i] = -np.sin(wp*time[int(i-Tstep)])
        # u2[i] = -np.sin(wp*time[int(i-Tstep)])
    # if (i > step and i < Tstep):
    #     top_force[i] = 1*np.sin(wp*time[int(i-step)])
    
# ==============================================================================# 

title_name = "Load timeSeries" #Load timeSeries / Distributed Load timeSeries/Structure impose force

# plt.plot(time, fp,label="force(P wave).txt",color='tab:blue') #ele 101
plt.plot(time, top_force,label="Structure force.txt",color='tab:red') #top Structure force

# plt.plot(time, u2,label="ele 201", color='m')
#plt.plot(time, vel, label="velocity",color='tab:orange')
#plt.plot(time[:size-1],accel[:size-1],label="acceleration",color='m')



plt.title(title_name, fontsize = 25)
plt.xlabel("tns",fontsize=18)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.xlim(0,0.5) #0.5
plt.legend(loc='upper right',fontsize=20)
plt.grid(True) 

ax1 = plt.gca()
ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
ax1.xaxis.set_major_locator(ticker.MultipleLocator(0.05)) # 0.02
ax1.yaxis.get_offset_text().set(size=18)







