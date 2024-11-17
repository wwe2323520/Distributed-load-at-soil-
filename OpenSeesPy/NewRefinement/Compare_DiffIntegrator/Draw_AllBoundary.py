# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:50:48 2024

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
from matplotlib.ticker import ScalarFormatter
from matplotlib import pyplot as plt, ticker as mticker
import scipy.signal
from scipy.signal import find_peaks
from matplotlib.lines import Line2D
from matplotlib.ticker import LogLocator, NullFormatter, LogFormatter

plt.rc('font', family= 'Times New Roman')
pi = np.pi
        
#------------- Read file ---------------------
def rdnumpy(textname):
    f = open(textname)
    line = f.readlines()
    lines = len(line)
    for l in line:
        le = l.strip('\n').split(' ')
        columns = len(le)
    
    A = np.zeros((lines, columns), dtype = float)
    A_row = 0
    
    for lin in line:
        list = lin.strip('\n').split(' ')
        A[A_row:] = list[0:columns]
        A_row += 1
    return A

# ===================== Theory Pwave =============================================
Soil_80row= 80 # dt= 6.25e-05   #cpdt = 3.34e-05

Nele = Soil_80row # Soil_80row
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
# ws_40HZ =  (2*pi)/5 # 0 to 5m = 0 to 2*pi => x = 2*pi/5
# ws_20HZ =  pi/5  # 0 to 10m = 0 to 2*pi => x = pi/5
# ws_10HZ =  pi/10 # 0 to 20m = 0 to 2*pi => x = pi/10

wp_20HZ =  pi/10 # 0 to 20m = 0 to 2*pi => x = pi/10
wp_10HZ =  pi/20 # 0 to 40m = 0 to 2*pi => x = pi/20
wp_40HZ =  pi/5 # 0 to 10m = 0 to 2*pi => x = pi/5

Pwave_HZ = wp_40HZ

HZ = 40
# ============================== Consider PWave ======================================
# calculate eace step time
tns_cp = L/cp # wave transport time
dcell_cp = tns_cp/Nele #each cell time
dt_cp = dcell_cp*0.1 #eace cell have 10 steps
print(f"Pwave travel = {tns_cp} ;dcell = {dcell_cp} ;dt = {dt_cp}")

time_cp = np.arange(0.0, 0.02503,dt_cp)
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
        XIn[5+10*j+i,j] = Incoming_wave(Pwave_HZ, xii, cp, tin)  #from 0.05m to 9.95m

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
        XOut[End_disp-10*j+i,End_Ele-j] = Outgoing_wave(Pwave_HZ, xoo, cp, tout)  #from 9.95m to 0.05m      
    
total_time = np.arange(0.0,0.40003,dt_cp)
Pwave = np.zeros((len(total_time),Nele))

# ===== New BC Sideforce on Left and Right ==============
PSideforce_y = np.zeros((len(total_time),Nele))  # 10
PSideforce_x = np.zeros((len(total_time),Nele))  # 10

# ----- 事實上是算 taux、tauy ------------------
Cp_vel_Coefficient =  2*1e4/(A*rho*cp)

# Pwave Hz=10 => Xin + Xin (入射波跟回彈波都一樣 xin)
# ===== Input Incoming Wave and Outcoming Wave to wave1 =======================
for g in range(Nele): #Nele
    to = 5 + 10*g
    for t in range(len(total_time)):
        if total_time[t] < 0.025:
            Pwave[to+t,g] = (Pwave[to+t,g] + Cp_vel_Coefficient*XIn[to+t,g])  # original wave transport
            
        if total_time[t] >= 0.025 and total_time[t] <= 0.050:
            Pwave[to+t,End_Ele-g] = Pwave[to+t,End_Ele-g] + Cp_vel_Coefficient*XIn[t-to,End_Ele-g]   # XOut[t-to,End_Ele-g]

Analysis_column = 79
def Find_ColMaxValue(column_index,ele80_Mid):
    column = ele80_Mid[:, column_index]
    max_value = np.max(column)
    max_index = np.argmax(column)
    
    min_value = np.min(column)
    min_index = np.argmin(column)

    print(f'max_value= {max_value}; max_index= {max_index}; min_value= {min_value}; min_index= {min_index}')
    return(max_value,min_value)

maxAnaly, minAnaly = Find_ColMaxValue(Analysis_column,Pwave)

# -------------- Read File --------------------------
row80 = f'node161'
row40 = f'node81'
row20 = f'node41'
row10 = f'node21'
# =================== HHT_Alpha =================================
Integrator1 = f'Test_Integrator/HHT_Alpha' # Central_Differential / HHT_Alpha / Newmark_Linear / Newmark_Constant

Condition1 =  f"{Integrator1}/Dt_0.2"# 
file1 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/row80/Velocity/{row80}.out"
file2 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/row40/Velocity/{row40}.out"
file3 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/row20/Velocity/{row20}.out"
file4 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition1}/row10/Velocity/{row10}.out"

HHT_Dt02_80 = rdnumpy(file1)
HHT_Dt02_40 = rdnumpy(file2)
HHT_Dt02_20 = rdnumpy(file3)
HHT_Dt02_10 = rdnumpy(file4)

Condition2 =  f"{Integrator1}/Dt_0.4"# 
file5 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/row80/Velocity/{row80}.out"
file6 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/row40/Velocity/{row40}.out"
file7 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/row20/Velocity/{row20}.out"
file8 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition2}/row10/Velocity/{row10}.out"

HHT_Dt04_80 = rdnumpy(file5)
HHT_Dt04_40 = rdnumpy(file6)
HHT_Dt04_20 = rdnumpy(file7)
HHT_Dt04_10 = rdnumpy(file8)

Condition3 =  f"{Integrator1}/Dt_0.6"# 
file9 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/row80/Velocity/{row80}.out"
file10 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/row40/Velocity/{row40}.out"
file11 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/row20/Velocity/{row20}.out"
file12 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition3}/row10/Velocity/{row10}.out"

HHT_Dt06_80 = rdnumpy(file9)
HHT_Dt06_40 = rdnumpy(file10)
HHT_Dt06_20 = rdnumpy(file11)
HHT_Dt06_10 = rdnumpy(file12)

Condition4 =  f"{Integrator1}/Dt_0.8"# 
file13 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/row80/Velocity/{row80}.out"
file14 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/row40/Velocity/{row40}.out"
file15 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/row20/Velocity/{row20}.out"
file16 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition4}/row10/Velocity/{row10}.out"

HHT_Dt08_80 = rdnumpy(file13)
HHT_Dt08_40 = rdnumpy(file14)
HHT_Dt08_20 = rdnumpy(file15)
HHT_Dt08_10 = rdnumpy(file16)

Condition5 =  f"{Integrator1}/Dt_1.0"# 
file17 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/row80/Velocity/{row80}.out"
file18 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/row40/Velocity/{row40}.out"
file19 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/row20/Velocity/{row20}.out"
file20 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition5}/row10/Velocity/{row10}.out"

HHT_Dt10_80 = rdnumpy(file17)
HHT_Dt10_40 = rdnumpy(file18)
HHT_Dt10_20 = rdnumpy(file19)
HHT_Dt10_10 = rdnumpy(file20)

Condition6 =  f"{Integrator1}/Dt_1.2"# 
file21 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/row80/Velocity/{row80}.out"
file22 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/row40/Velocity/{row40}.out"
file23 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/row20/Velocity/{row20}.out"
file24 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition6}/row10/Velocity/{row10}.out"

HHT_Dt12_80 = rdnumpy(file21)
HHT_Dt12_40 = rdnumpy(file22)
HHT_Dt12_20 = rdnumpy(file23)
HHT_Dt12_10 = rdnumpy(file24)

Condition7 =  f"{Integrator1}/Dt_1.4"# 
file25 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/row80/Velocity/{row80}.out"
file26 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/row40/Velocity/{row40}.out"
file27 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/row20/Velocity/{row20}.out"
file28 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition7}/row10/Velocity/{row10}.out"

HHT_Dt14_80 = rdnumpy(file25)
HHT_Dt14_40 = rdnumpy(file26)
HHT_Dt14_20 = rdnumpy(file27)
HHT_Dt14_10 = rdnumpy(file28)

Condition8 =  f"{Integrator1}/Dt_1.6"# 
file29 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/row80/Velocity/{row80}.out"
file30 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/row40/Velocity/{row40}.out"
file31 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/row20/Velocity/{row20}.out"
file32 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition8}/row10/Velocity/{row10}.out"

HHT_Dt16_80 = rdnumpy(file29)
HHT_Dt16_40 = rdnumpy(file30)
HHT_Dt16_20 = rdnumpy(file31)
HHT_Dt16_10 = rdnumpy(file32)

Condition9 =  f"{Integrator1}/Dt_1.8"# 
file33 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/row80/Velocity/{row80}.out"
file34 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/row40/Velocity/{row40}.out"
file35 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/row20/Velocity/{row20}.out"
file36 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition9}/row10/Velocity/{row10}.out"

HHT_Dt18_80 = rdnumpy(file33)
HHT_Dt18_40 = rdnumpy(file34)
HHT_Dt18_20 = rdnumpy(file35)
HHT_Dt18_10 = rdnumpy(file36)
# =================== Central_Differential =================================
Integrator2 = f'Test_Integrator/Central Differential' # Central_Differential / HHT_Alpha / Newmark_Linear / Newmark_Constant

Condition10 =  f"{Integrator2}/Dt_0.2"# 
file37 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition10}/row80/Velocity/{row80}.out"
file38 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition10}/row40/Velocity/{row40}.out"
file39 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition10}/row20/Velocity/{row20}.out"
file40 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition10}/row10/Velocity/{row10}.out"

Cen_Dt02_80 = rdnumpy(file37)
Cen_Dt02_40 = rdnumpy(file38)
Cen_Dt02_20 = rdnumpy(file39)
Cen_Dt02_10 = rdnumpy(file40)

Condition11 =  f"{Integrator2}/Dt_0.4"# 
file41 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition11}/row80/Velocity/{row80}.out"
file42 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition11}/row40/Velocity/{row40}.out"
file43 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition11}/row20/Velocity/{row20}.out"
file44 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition11}/row10/Velocity/{row10}.out"

Cen_Dt04_80 = rdnumpy(file41)
Cen_Dt04_40 = rdnumpy(file42)
Cen_Dt04_20 = rdnumpy(file43)
Cen_Dt04_10 = rdnumpy(file44)

Condition12 =  f"{Integrator2}/Dt_0.6"# 
file45 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition12}/row80/Velocity/{row80}.out"
file46 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition12}/row40/Velocity/{row40}.out"
file47 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition12}/row20/Velocity/{row20}.out"
file48 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition12}/row10/Velocity/{row10}.out"

Cen_Dt06_80 = rdnumpy(file45)
Cen_Dt06_40 = rdnumpy(file46)
Cen_Dt06_20 = rdnumpy(file47)
Cen_Dt06_10 = rdnumpy(file48)

Condition13 =  f"{Integrator2}/Dt_0.8"# 
file49 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition13}/row80/Velocity/{row80}.out"
file50 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition13}/row40/Velocity/{row40}.out"
file51 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition13}/row20/Velocity/{row20}.out"
file52 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition13}/row10/Velocity/{row10}.out"

Cen_Dt08_80 = rdnumpy(file49)
Cen_Dt08_40 = rdnumpy(file50)
Cen_Dt08_20 = rdnumpy(file51)
Cen_Dt08_10 = rdnumpy(file52)

Condition14 =  f"{Integrator2}/Dt_1.0"# 
file53 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition14}/row80/Velocity/{row80}.out"
file54 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition14}/row40/Velocity/{row40}.out"
file55 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition14}/row20/Velocity/{row20}.out"
file56 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition14}/row10/Velocity/{row10}.out"

Cen_Dt10_80 = rdnumpy(file53)
Cen_Dt10_40 = rdnumpy(file54)
Cen_Dt10_20 = rdnumpy(file55)
Cen_Dt10_10 = rdnumpy(file56)

Condition15 =  f"{Integrator2}/Dt_1.2"# 
file57 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition15}/row80/Velocity/{row80}.out"
file58 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition15}/row40/Velocity/{row40}.out"
file59 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition15}/row20/Velocity/{row20}.out"
file60 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition15}/row10/Velocity/{row10}.out"

Cen_Dt12_80 = rdnumpy(file57)
Cen_Dt12_40 = rdnumpy(file58)
Cen_Dt12_20 = rdnumpy(file59)
Cen_Dt12_10 = rdnumpy(file60)

Condition16 =  f"{Integrator2}/Dt_1.4"# 
file61 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition16}/row80/Velocity/{row80}.out"
file62 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition16}/row40/Velocity/{row40}.out"
file63 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition16}/row20/Velocity/{row20}.out"
file64 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition16}/row10/Velocity/{row10}.out"

Cen_Dt14_80 = rdnumpy(file61)
Cen_Dt14_40 = rdnumpy(file62)
Cen_Dt14_20 = rdnumpy(file63)
Cen_Dt14_10 = rdnumpy(file64)

Condition17 =  f"{Integrator2}/Dt_1.6"# 
file65 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition17}/row80/Velocity/{row80}.out"
file66 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition17}/row40/Velocity/{row40}.out"
file67 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition17}/row20/Velocity/{row20}.out"
file68 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition17}/row10/Velocity/{row10}.out"

Cen_Dt16_80 = rdnumpy(file65)
Cen_Dt16_40 = rdnumpy(file66)
Cen_Dt16_20 = rdnumpy(file67)
Cen_Dt16_10 = rdnumpy(file68)

Condition18 =  f"{Integrator2}/Dt_1.8"# 
file69 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition18}/row80/Velocity/{row80}.out"
file70 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition18}/row40/Velocity/{row40}.out"
file71 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition18}/row20/Velocity/{row20}.out"
file72 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition18}/row10/Velocity/{row10}.out"

Cen_Dt18_80 = rdnumpy(file69)
Cen_Dt18_40 = rdnumpy(file70)
Cen_Dt18_20 = rdnumpy(file71)
Cen_Dt18_10 = rdnumpy(file72)
# =================== Newmark_Linear =================================
Integrator3 = f'Test_Integrator/Newmark Linear'

Condition19 =  f"{Integrator3}/Dt_0.2"# 
file73 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition19}/row80/Velocity/{row80}.out"
file74 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition19}/row40/Velocity/{row40}.out"
file75 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition19}/row20/Velocity/{row20}.out"
file76 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition19}/row10/Velocity/{row10}.out"

Lin_Dt02_80 = rdnumpy(file73)
Lin_Dt02_40 = rdnumpy(file74)
Lin_Dt02_20 = rdnumpy(file75)
Lin_Dt02_10 = rdnumpy(file76)

Condition20 =  f"{Integrator3}/Dt_0.4"# 
file77 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition20}/row80/Velocity/{row80}.out"
file78 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition20}/row40/Velocity/{row40}.out"
file79 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition20}/row20/Velocity/{row20}.out"
file80 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition20}/row10/Velocity/{row10}.out"

Lin_Dt04_80 = rdnumpy(file77)
Lin_Dt04_40 = rdnumpy(file78)
Lin_Dt04_20 = rdnumpy(file79)
Lin_Dt04_10 = rdnumpy(file80)

Condition21 =  f"{Integrator3}/Dt_0.6"# 
file81 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition21}/row80/Velocity/{row80}.out"
file82 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition21}/row40/Velocity/{row40}.out"
file83 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition21}/row20/Velocity/{row20}.out"
file84 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition21}/row10/Velocity/{row10}.out"

Lin_Dt06_80 = rdnumpy(file81)
Lin_Dt06_40 = rdnumpy(file82)
Lin_Dt06_20 = rdnumpy(file83)
Lin_Dt06_10 = rdnumpy(file84)

Condition22 =  f"{Integrator3}/Dt_0.8"# 
file85 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition22}/row80/Velocity/{row80}.out"
file86 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition22}/row40/Velocity/{row40}.out"
file87 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition22}/row20/Velocity/{row20}.out"
file88 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition22}/row10/Velocity/{row10}.out"

Lin_Dt08_80 = rdnumpy(file85)
Lin_Dt08_40 = rdnumpy(file86)
Lin_Dt08_20 = rdnumpy(file87)
Lin_Dt08_10 = rdnumpy(file88)

Condition23 =  f"{Integrator3}/Dt_1.0"# 
file89 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition23}/row80/Velocity/{row80}.out"
file90 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition23}/row40/Velocity/{row40}.out"
file91 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition23}/row20/Velocity/{row20}.out"
file92 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition23}/row10/Velocity/{row10}.out"

Lin_Dt10_80 = rdnumpy(file89)
Lin_Dt10_40 = rdnumpy(file90)
Lin_Dt10_20 = rdnumpy(file91)
Lin_Dt10_10 = rdnumpy(file92)

Condition24 =  f"{Integrator3}/Dt_1.2"# 
file93 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition24}/row80/Velocity/{row80}.out"
file94 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition24}/row40/Velocity/{row40}.out"
file95 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition24}/row20/Velocity/{row20}.out"
file96 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition24}/row10/Velocity/{row10}.out"

Lin_Dt12_80 = rdnumpy(file93)
Lin_Dt12_40 = rdnumpy(file94)
Lin_Dt12_20 = rdnumpy(file95)
Lin_Dt12_10 = rdnumpy(file96)

Condition25 =  f"{Integrator3}/Dt_1.4"# 
file97 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition25}/row80/Velocity/{row80}.out"
file98 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition25}/row40/Velocity/{row40}.out"
file99 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition25}/row20/Velocity/{row20}.out"
file100 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition25}/row10/Velocity/{row10}.out"

Lin_Dt14_80 = rdnumpy(file97)
Lin_Dt14_40 = rdnumpy(file98)
Lin_Dt14_20 = rdnumpy(file99)
Lin_Dt14_10 = rdnumpy(file100)

Condition26 =  f"{Integrator3}/Dt_1.6"# 
file101 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition26}/row80/Velocity/{row80}.out"
file102 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition26}/row40/Velocity/{row40}.out"
file103 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition26}/row20/Velocity/{row20}.out"
file104 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition26}/row10/Velocity/{row10}.out"

Lin_Dt16_80 = rdnumpy(file101)
Lin_Dt16_40 = rdnumpy(file102)
Lin_Dt16_20 = rdnumpy(file103)
Lin_Dt16_10 = rdnumpy(file104)

Condition27 =  f"{Integrator3}/Dt_1.8"# 
file105 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition27}/row80/Velocity/{row80}.out"
file106 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition27}/row40/Velocity/{row40}.out"
file107 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition27}/row20/Velocity/{row20}.out"
file108 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition27}/row10/Velocity/{row10}.out"

Lin_Dt18_80 = rdnumpy(file105)
Lin_Dt18_40 = rdnumpy(file106)
Lin_Dt18_20 = rdnumpy(file107)
Lin_Dt18_10 = rdnumpy(file108)
# =================== Newmark_Constant =================================
Integrator4 = f'Test_Integrator/Newmark Constant'

Condition28 =  f"{Integrator4}/Dt_0.2"# 
file109 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition28}/row80/Velocity/{row80}.out"
file110 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition28}/row40/Velocity/{row40}.out"
file111 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition28}/row20/Velocity/{row20}.out"
file112 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition28}/row10/Velocity/{row10}.out"

Const_Dt02_80 = rdnumpy(file109)
Const_Dt02_40 = rdnumpy(file110)
Const_Dt02_20 = rdnumpy(file111)
Const_Dt02_10 = rdnumpy(file112)

Condition29 =  f"{Integrator4}/Dt_0.4"# 
file113 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition29}/row80/Velocity/{row80}.out"
file114 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition29}/row40/Velocity/{row40}.out"
file115 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition29}/row20/Velocity/{row20}.out"
file116 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition29}/row10/Velocity/{row10}.out"

Const_Dt04_80 = rdnumpy(file113)
Const_Dt04_40 = rdnumpy(file114)
Const_Dt04_20 = rdnumpy(file115)
Const_Dt04_10 = rdnumpy(file116)

Condition30 =  f"{Integrator4}/Dt_0.6"# 
file117 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition30}/row80/Velocity/{row80}.out"
file118 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition30}/row40/Velocity/{row40}.out"
file119 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition30}/row20/Velocity/{row20}.out"
file120 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition30}/row10/Velocity/{row10}.out"

Const_Dt06_80 = rdnumpy(file117)
Const_Dt06_40 = rdnumpy(file118)
Const_Dt06_20 = rdnumpy(file119)
Const_Dt06_10 = rdnumpy(file120)

Condition31 =  f"{Integrator4}/Dt_0.8"# 
file121 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition31}/row80/Velocity/{row80}.out"
file122 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition31}/row40/Velocity/{row40}.out"
file123 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition31}/row20/Velocity/{row20}.out"
file124 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition31}/row10/Velocity/{row10}.out"

Const_Dt08_80 = rdnumpy(file121)
Const_Dt08_40 = rdnumpy(file122)
Const_Dt08_20 = rdnumpy(file123)
Const_Dt08_10 = rdnumpy(file124)

Condition32 =  f"{Integrator4}/Dt_1.0"# 
file125 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition32}/row80/Velocity/{row80}.out"
file126 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition32}/row40/Velocity/{row40}.out"
file127 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition32}/row20/Velocity/{row20}.out"
file128 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition32}/row10/Velocity/{row10}.out"

Const_Dt10_80 = rdnumpy(file125)
Const_Dt10_40 = rdnumpy(file126)
Const_Dt10_20 = rdnumpy(file127)
Const_Dt10_10 = rdnumpy(file128)

Condition33 =  f"{Integrator4}/Dt_1.2"# 
file129 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition33}/row80/Velocity/{row80}.out"
file130 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition33}/row40/Velocity/{row40}.out"
file131 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition33}/row20/Velocity/{row20}.out"
file132 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition33}/row10/Velocity/{row10}.out"

Const_Dt12_80 = rdnumpy(file129)
Const_Dt12_40 = rdnumpy(file130)
Const_Dt12_20 = rdnumpy(file131)
Const_Dt12_10 = rdnumpy(file132)

Condition34 =  f"{Integrator4}/Dt_1.4"# 
file133 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition34}/row80/Velocity/{row80}.out"
file134 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition34}/row40/Velocity/{row40}.out"
file135 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition34}/row20/Velocity/{row20}.out"
file136 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition34}/row10/Velocity/{row10}.out"

Const_Dt14_80 = rdnumpy(file133)
Const_Dt14_40 = rdnumpy(file134)
Const_Dt14_20 = rdnumpy(file135)
Const_Dt14_10 = rdnumpy(file136)

Condition35 =  f"{Integrator4}/Dt_1.6"# 
file137 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition35}/row80/Velocity/{row80}.out"
file138 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition35}/row40/Velocity/{row40}.out"
file139 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition35}/row20/Velocity/{row20}.out"
file140 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition35}/row10/Velocity/{row10}.out"

Const_Dt16_80 = rdnumpy(file137)
Const_Dt16_40 = rdnumpy(file138)
Const_Dt16_20 = rdnumpy(file139)
Const_Dt16_10 = rdnumpy(file140)

Condition36 =  f"{Integrator4}/Dt_1.8"# 
file141 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition36}/row80/Velocity/{row80}.out"
file142 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition36}/row40/Velocity/{row40}.out"
file143 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition36}/row20/Velocity/{row20}.out"
file144 = f"D:/shiang/opensees/20220330/OpenSeesPy/{Condition36}/row10/Velocity/{row10}.out"

Const_Dt18_80 = rdnumpy(file141)
Const_Dt18_40 = rdnumpy(file142)
Const_Dt18_20 = rdnumpy(file143)
Const_Dt18_10 = rdnumpy(file144)

start_time = 0.0
end_time = 0.20 # 0.035
def process_column(matrix, column_index):
    # 选择在指定时间范围内的数据
    time_column = matrix[:, 0]
    column = matrix[:, column_index]
    
    # 限定在时间范围内
    within_time_range = (time_column >= start_time) & (time_column <= end_time)
    filtered_column = column[within_time_range]
    
    # 计算绝对值并找出最大值
    abs_filtered_column = np.abs(filtered_column)
    max_peak = np.max(abs_filtered_column)
    max_index = np.argmax(abs_filtered_column)
    
    print(f'max_value= {max_peak}; max_index= {max_index}')
    return max_peak

# =========== Find Grounf Surface Max/ Min Peak Value ==========================
column_index = 2 # Pwave = 2 (yaxis)
# ============================ HHT_Alpha =========================================
# ------------ Dt = 0.2-----------------------
max02_80HHT = process_column(HHT_Dt02_80, column_index)
max02_40HHT = process_column(HHT_Dt02_40, column_index)
max02_20HHT = process_column(HHT_Dt02_20, column_index)
max02_10HHT = process_column(HHT_Dt02_10, column_index)
# ------------ Dt = 0.4-----------------------
max04_80HHT = process_column(HHT_Dt04_80, column_index)
max04_40HHT = process_column(HHT_Dt04_40, column_index)
max04_20HHT = process_column(HHT_Dt04_20, column_index)
max04_10HHT = process_column(HHT_Dt04_10, column_index)
# ------------ Dt = 0.6-----------------------
max06_80HHT = process_column(HHT_Dt06_80, column_index)
max06_40HHT = process_column(HHT_Dt06_40, column_index)
max06_20HHT = process_column(HHT_Dt06_20, column_index)
max06_10HHT = process_column(HHT_Dt06_10, column_index)
# ------------ Dt = 0.8-----------------------
max08_80HHT = process_column(HHT_Dt08_80, column_index)
max08_40HHT = process_column(HHT_Dt08_40, column_index)
max08_20HHT = process_column(HHT_Dt08_20, column_index)
max08_10HHT = process_column(HHT_Dt08_10, column_index)
# ------------ Dt = 1.0-----------------------
max10_80HHT = process_column(HHT_Dt10_80, column_index)
max10_40HHT = process_column(HHT_Dt10_40, column_index)
max10_20HHT = process_column(HHT_Dt10_20, column_index)
max10_10HHT = process_column(HHT_Dt10_10, column_index)
# ------------ Dt = 1.2-----------------------
max12_80HHT = process_column(HHT_Dt12_80, column_index)
max12_40HHT = process_column(HHT_Dt12_40, column_index)
max12_20HHT = process_column(HHT_Dt12_20, column_index)
max12_10HHT = process_column(HHT_Dt12_10, column_index)

# ------------ Dt = 1.4-----------------------
max14_80HHT = process_column(HHT_Dt14_80, column_index)
max14_40HHT = process_column(HHT_Dt14_40, column_index)
max14_20HHT = process_column(HHT_Dt14_20, column_index)
max14_10HHT = process_column(HHT_Dt14_10, column_index)
# ------------ Dt = 1.6-----------------------
max16_80HHT = process_column(HHT_Dt16_80, column_index)
max16_40HHT = process_column(HHT_Dt16_40, column_index)
max16_20HHT = process_column(HHT_Dt16_20, column_index)
max16_10HHT = process_column(HHT_Dt16_10, column_index)
# ------------ Dt = 1.8-----------------------
max18_80HHT = process_column(HHT_Dt18_80, column_index)
max18_40HHT = process_column(HHT_Dt18_40, column_index)
max18_20HHT = process_column(HHT_Dt18_20, column_index)
max18_10HHT = process_column(HHT_Dt18_10, column_index)
# ============================ Central_Differential =========================================
# ------------ Dt = 0.2-----------------------
max02_80Cen = process_column(Cen_Dt02_80, column_index)
max02_40Cen = process_column(Cen_Dt02_40, column_index)
max02_20Cen = process_column(Cen_Dt02_20, column_index)
max02_10Cen = process_column(Cen_Dt02_10, column_index)
# ------------ Dt = 0.4-----------------------
max04_80Cen = process_column(Cen_Dt04_80, column_index)
max04_40Cen = process_column(Cen_Dt04_40, column_index)
max04_20Cen = process_column(Cen_Dt04_20, column_index)
max04_10Cen = process_column(Cen_Dt04_10, column_index)
# ------------ Dt = 0.6-----------------------
max06_80Cen = process_column(Cen_Dt06_80, column_index)
max06_40Cen = process_column(Cen_Dt06_40, column_index)
max06_20Cen = process_column(Cen_Dt06_20, column_index)
max06_10Cen = process_column(Cen_Dt06_10, column_index)
# ------------ Dt = 0.8-----------------------
max08_80Cen = process_column(Cen_Dt08_80, column_index)
max08_40Cen = process_column(Cen_Dt08_40, column_index)
max08_20Cen = process_column(Cen_Dt08_20, column_index)
max08_10Cen = process_column(Cen_Dt08_10, column_index)
# ------------ Dt = 1.0-----------------------
max10_80Cen = process_column(Cen_Dt10_80, column_index)
max10_40Cen = process_column(Cen_Dt10_40, column_index)
max10_20Cen = process_column(Cen_Dt10_20, column_index)
max10_10Cen = process_column(Cen_Dt10_10, column_index)
# ------------ Dt = 1.2-----------------------
max12_80Cen = process_column(Cen_Dt12_80, column_index)
max12_40Cen = process_column(Cen_Dt12_40, column_index)
max12_20Cen = process_column(Cen_Dt12_20, column_index)
max12_10Cen = process_column(Cen_Dt12_10, column_index)

# ------------ Dt = 1.4-----------------------
max14_80Cen = process_column(Cen_Dt14_80, column_index)
max14_40Cen = process_column(Cen_Dt14_40, column_index)
max14_20Cen = process_column(Cen_Dt14_20, column_index)
max14_10Cen = process_column(Cen_Dt14_10, column_index)
# ------------ Dt = 1.6-----------------------
max16_80Cen = process_column(Cen_Dt16_80, column_index)
max16_40Cen = process_column(Cen_Dt16_40, column_index)
max16_20Cen = process_column(Cen_Dt16_20, column_index)
max16_10Cen = process_column(Cen_Dt16_10, column_index)
# ------------ Dt = 1.8-----------------------
max18_80Cen = process_column(Cen_Dt18_80, column_index)
max18_40Cen = process_column(Cen_Dt18_40, column_index)
max18_20Cen = process_column(Cen_Dt18_20, column_index)
max18_10Cen = process_column(Cen_Dt18_10, column_index)
# ============================ Newmark_Linear =========================================
# ------------ Dt = 0.2-----------------------
max02_80Lin = process_column(Lin_Dt02_80, column_index)
max02_40Lin = process_column(Lin_Dt02_40, column_index)
max02_20Lin = process_column(Lin_Dt02_20, column_index)
max02_10Lin = process_column(Lin_Dt02_10, column_index)
# ------------ Dt = 0.4-----------------------
max04_80Lin = process_column(Lin_Dt04_80, column_index)
max04_40Lin = process_column(Lin_Dt04_40, column_index)
max04_20Lin = process_column(Lin_Dt04_20, column_index)
max04_10Lin = process_column(Lin_Dt04_10, column_index)
# ------------ Dt = 0.6-----------------------
max06_80Lin = process_column(Lin_Dt06_80, column_index)
max06_40Lin = process_column(Lin_Dt06_40, column_index)
max06_20Lin = process_column(Lin_Dt06_20, column_index)
max06_10Lin = process_column(Lin_Dt06_10, column_index)
# ------------ Dt = 0.8-----------------------
max08_80Lin = process_column(Lin_Dt08_80, column_index)
max08_40Lin = process_column(Lin_Dt08_40, column_index)
max08_20Lin = process_column(Lin_Dt08_20, column_index)
max08_10Lin = process_column(Lin_Dt08_10, column_index)
# ------------ Dt = 1.0-----------------------
max10_80Lin = process_column(Lin_Dt10_80, column_index)
max10_40Lin = process_column(Lin_Dt10_40, column_index)
max10_20Lin = process_column(Lin_Dt10_20, column_index)
max10_10Lin = process_column(Lin_Dt10_10, column_index)
# ------------ Dt = 1.2-----------------------
max12_80Lin = process_column(Lin_Dt12_80, column_index)
max12_40Lin = process_column(Lin_Dt12_40, column_index)
max12_20Lin = process_column(Lin_Dt12_20, column_index)
max12_10Lin = process_column(Lin_Dt12_10, column_index)

# ------------ Dt = 1.4-----------------------
max14_80Lin = process_column(Lin_Dt14_80, column_index)
max14_40Lin = process_column(Lin_Dt14_40, column_index)
max14_20Lin = process_column(Lin_Dt14_20, column_index)
max14_10Lin = process_column(Lin_Dt14_10, column_index)
# ------------ Dt = 1.6-----------------------
max16_80Lin = process_column(Lin_Dt16_80, column_index)
max16_40Lin = process_column(Lin_Dt16_40, column_index)
max16_20Lin = process_column(Lin_Dt16_20, column_index)
max16_10Lin = process_column(Lin_Dt16_10, column_index)
# ------------ Dt = 1.8-----------------------
max18_80Lin = process_column(Lin_Dt18_80, column_index)
max18_40Lin = process_column(Lin_Dt18_40, column_index)
max18_20Lin = process_column(Lin_Dt18_20, column_index)
max18_10Lin = process_column(Lin_Dt18_10, column_index)
# ============================ Newmark_Constant =========================================
# ------------ Dt = 0.2-----------------------
max02_80Const = process_column(Const_Dt02_80, column_index)
max02_40Const = process_column(Const_Dt02_40, column_index)
max02_20Const = process_column(Const_Dt02_20, column_index)
max02_10Const = process_column(Const_Dt02_10, column_index)
# ------------ Dt = 0.4-----------------------
max04_80Const = process_column(Const_Dt04_80, column_index)
max04_40Const = process_column(Const_Dt04_40, column_index)
max04_20Const = process_column(Const_Dt04_20, column_index)
max04_10Const = process_column(Const_Dt04_10, column_index)
# ------------ Dt = 0.6-----------------------
max06_80Const = process_column(Const_Dt06_80, column_index)
max06_40Const = process_column(Const_Dt06_40, column_index)
max06_20Const = process_column(Const_Dt06_20, column_index)
max06_10Const = process_column(Const_Dt06_10, column_index)
# ------------ Dt = 0.8-----------------------
max08_80Const = process_column(Const_Dt08_80, column_index)
max08_40Const = process_column(Const_Dt08_40, column_index)
max08_20Const = process_column(Const_Dt08_20, column_index)
max08_10Const = process_column(Const_Dt08_10, column_index)
# ------------ Dt = 1.0-----------------------
max10_80Const = process_column(Const_Dt10_80, column_index)
max10_40Const = process_column(Const_Dt10_40, column_index)
max10_20Const = process_column(Const_Dt10_20, column_index)
max10_10Const = process_column(Const_Dt10_10, column_index)
# ------------ Dt = 1.2-----------------------
max12_80Const = process_column(Const_Dt12_80, column_index)
max12_40Const = process_column(Const_Dt12_40, column_index)
max12_20Const = process_column(Const_Dt12_20, column_index)
max12_10Const = process_column(Const_Dt12_10, column_index)

# ------------ Dt = 1.4-----------------------
max14_80Const = process_column(Const_Dt14_80, column_index)
max14_40Const = process_column(Const_Dt14_40, column_index)
max14_20Const = process_column(Const_Dt14_20, column_index)
max14_10Const = process_column(Const_Dt14_10, column_index)
# ------------ Dt = 1.6-----------------------
max16_80Const = process_column(Const_Dt16_80, column_index)
max16_40Const = process_column(Const_Dt16_40, column_index)
max16_20Const = process_column(Const_Dt16_20, column_index)
max16_10Const = process_column(Const_Dt16_10, column_index)
# ------------ Dt = 1.8-----------------------
max18_80Const = process_column(Const_Dt18_80, column_index)
max18_40Const = process_column(Const_Dt18_40, column_index)
max18_20Const = process_column(Const_Dt18_20, column_index)
max18_10Const = process_column(Const_Dt18_10, column_index)

Mesh_Size = np.zeros(4)
ele = 80 
for m in range(len(Mesh_Size)):
    if m == 0 :    
        Mesh_Size[m] = L/ (ele)
    if m > 0:    
        Mesh_Size[m] = Mesh_Size[m-1]*2
        
# ================================== Prepare L2-Norm Error ============================
TheoryTime = total_time[:]

def Calculate_RelativeL2norm(TheoryTime,Pwave, Tie_W20_Mid80row, time_range=(0, 0.20)):
    Element_Time = Tie_W20_Mid80row[:, 0]
# ------------------------- L-2 Norm Error ------------------------
    common80 = set(TheoryTime) & set(Element_Time)
    filtered_common80 = [value for value in common80 if time_range[0] <= value <= time_range[1]]
    
    differences = []
    Mom = []

    for common_value in common80:
        index1 = np.where(Element_Time == common_value)[0][0]
        index2 = np.where(TheoryTime == common_value)[0][0]

        diff = (Tie_W20_Mid80row[index1, column_index] - Pwave[index2, Analysis_column])
        differences.append(diff)
        
        Mother =  Pwave[index2, Analysis_column]
        Mom.append(Mother)
        
# ------------- numerator and denominator seperate calculate -------------------- 
    compare = np.array(differences)
    Momm = np.array(Mom)
# ------------- numerator and denominator seperate Square --------------------    
    squared_values = np.square(compare)
    squared_value2 = np.square(Momm)
    
    sum_of_squares = np.sum(squared_values)
    sum_of_square2 = np.sum(squared_value2)
    result = np.sqrt((sum_of_squares)/sum_of_square2)
    
    return result, len(compare)

def Add_Err(MidTieErr20, Tie_W20_Mid80row, Tie_W20_Mid40row, Tie_W20_Mid20row, Tie_W20_Mid10row):
    MidTieErr20[:,0] = Mesh_Size[:] 
# ===================================== Calculate_L2NormError Normalization ============================================================
    MidTieErr20[0,1], MidTieErr20[0,2] = Calculate_RelativeL2norm(TheoryTime,Pwave, Tie_W20_Mid80row)
    MidTieErr20[1,1], MidTieErr20[1,2] = Calculate_RelativeL2norm(TheoryTime,Pwave, Tie_W20_Mid40row)
    MidTieErr20[2,1], MidTieErr20[2,2] = Calculate_RelativeL2norm(TheoryTime,Pwave, Tie_W20_Mid20row)
    MidTieErr20[3,1], MidTieErr20[3,2] = Calculate_RelativeL2norm(TheoryTime,Pwave, Tie_W20_Mid10row)
    
HHT_02Err_L2 = np.zeros((4,3))
HHT_04Err_L2 = np.zeros((4,3))
HHT_06Err_L2 = np.zeros((4,3))
HHT_08Err_L2 = np.zeros((4,3))
HHT_10Err_L2 = np.zeros((4,3))
HHT_12Err_L2 = np.zeros((4,3))
HHT_14Err_L2 = np.zeros((4,3))
HHT_16Err_L2 = np.zeros((4,3))
HHT_18Err_L2 = np.zeros((4,3))

Add_Err(HHT_02Err_L2, HHT_Dt02_80, HHT_Dt02_40, HHT_Dt02_20, HHT_Dt02_10)
Add_Err(HHT_04Err_L2, HHT_Dt04_80, HHT_Dt04_40, HHT_Dt04_20, HHT_Dt04_10)
Add_Err(HHT_06Err_L2, HHT_Dt06_80, HHT_Dt06_40, HHT_Dt06_20, HHT_Dt06_10)
Add_Err(HHT_08Err_L2, HHT_Dt08_80, HHT_Dt08_40, HHT_Dt08_20, HHT_Dt08_10)
Add_Err(HHT_10Err_L2, HHT_Dt10_80, HHT_Dt10_40, HHT_Dt10_20, HHT_Dt10_10)

Add_Err(HHT_12Err_L2, HHT_Dt12_80, HHT_Dt12_40, HHT_Dt12_20, HHT_Dt12_10)
Add_Err(HHT_14Err_L2, HHT_Dt14_80, HHT_Dt14_40, HHT_Dt14_20, HHT_Dt14_10)
Add_Err(HHT_16Err_L2, HHT_Dt16_80, HHT_Dt16_40, HHT_Dt16_20, HHT_Dt16_10)
Add_Err(HHT_18Err_L2, HHT_Dt18_80, HHT_Dt18_40, HHT_Dt18_20, HHT_Dt18_10)

Cen_02Err_L2 = np.zeros((4,3))
Cen_04Err_L2 = np.zeros((4,3))
Cen_06Err_L2 = np.zeros((4,3))
Cen_08Err_L2 = np.zeros((4,3))
Cen_10Err_L2 = np.zeros((4,3))
Cen_12Err_L2 = np.zeros((4,3))
Cen_14Err_L2 = np.zeros((4,3))
Cen_16Err_L2 = np.zeros((4,3))
Cen_18Err_L2 = np.zeros((4,3))

Add_Err(Cen_02Err_L2, Cen_Dt02_80, Cen_Dt02_40, Cen_Dt02_20, Cen_Dt02_10)
Add_Err(Cen_04Err_L2, Cen_Dt04_80, Cen_Dt04_40, Cen_Dt04_20, Cen_Dt04_10)
Add_Err(Cen_06Err_L2, Cen_Dt06_80, Cen_Dt06_40, Cen_Dt06_20, Cen_Dt06_10)
Add_Err(Cen_08Err_L2, Cen_Dt08_80, Cen_Dt08_40, Cen_Dt08_20, Cen_Dt08_10)
Add_Err(Cen_10Err_L2, Cen_Dt10_80, Cen_Dt10_40, Cen_Dt10_20, Cen_Dt10_10)

Add_Err(Cen_12Err_L2, Cen_Dt12_80, Cen_Dt12_40, Cen_Dt12_20, Cen_Dt12_10)
Add_Err(Cen_14Err_L2, Cen_Dt14_80, Cen_Dt14_40, Cen_Dt14_20, Cen_Dt14_10)
Add_Err(Cen_16Err_L2, Cen_Dt16_80, Cen_Dt16_40, Cen_Dt16_20, Cen_Dt16_10)
Add_Err(Cen_18Err_L2, Cen_Dt18_80, Cen_Dt18_40, Cen_Dt18_20, Cen_Dt18_10)

Lin_02Err_L2 = np.zeros((4,3))
Lin_04Err_L2 = np.zeros((4,3))
Lin_06Err_L2 = np.zeros((4,3))
Lin_08Err_L2 = np.zeros((4,3))
Lin_10Err_L2 = np.zeros((4,3))
Lin_12Err_L2 = np.zeros((4,3))
Lin_14Err_L2 = np.zeros((4,3))
Lin_16Err_L2 = np.zeros((4,3))
Lin_18Err_L2 = np.zeros((4,3))

Add_Err(Lin_02Err_L2, Lin_Dt02_80, Lin_Dt02_40, Lin_Dt02_20, Lin_Dt02_10)
Add_Err(Lin_04Err_L2, Lin_Dt04_80, Lin_Dt04_40, Lin_Dt04_20, Lin_Dt04_10)
Add_Err(Lin_06Err_L2, Lin_Dt06_80, Lin_Dt06_40, Lin_Dt06_20, Lin_Dt06_10)
Add_Err(Lin_08Err_L2, Lin_Dt08_80, Lin_Dt08_40, Lin_Dt08_20, Lin_Dt08_10)
Add_Err(Lin_10Err_L2, Lin_Dt10_80, Lin_Dt10_40, Lin_Dt10_20, Lin_Dt10_10)

Add_Err(Lin_12Err_L2, Lin_Dt12_80, Lin_Dt12_40, Lin_Dt12_20, Lin_Dt12_10)
Add_Err(Lin_14Err_L2, Lin_Dt14_80, Lin_Dt14_40, Lin_Dt14_20, Lin_Dt14_10)
Add_Err(Lin_16Err_L2, Lin_Dt16_80, Lin_Dt16_40, Lin_Dt16_20, Lin_Dt16_10)
Add_Err(Lin_18Err_L2, Lin_Dt18_80, Lin_Dt18_40, Lin_Dt18_20, Lin_Dt18_10)

Const_02Err_L2 = np.zeros((4,3))
Const_04Err_L2 = np.zeros((4,3))
Const_06Err_L2 = np.zeros((4,3))
Const_08Err_L2 = np.zeros((4,3))
Const_10Err_L2 = np.zeros((4,3))
Const_12Err_L2 = np.zeros((4,3))
Const_14Err_L2 = np.zeros((4,3))
Const_16Err_L2 = np.zeros((4,3))
Const_18Err_L2 = np.zeros((4,3))

Add_Err(Const_02Err_L2, Const_Dt02_80, Const_Dt02_40, Const_Dt02_20, Const_Dt02_10)
Add_Err(Const_04Err_L2, Const_Dt04_80, Const_Dt04_40, Const_Dt04_20, Const_Dt04_10)
Add_Err(Const_06Err_L2, Const_Dt06_80, Const_Dt06_40, Const_Dt06_20, Const_Dt06_10)
Add_Err(Const_08Err_L2, Const_Dt08_80, Const_Dt08_40, Const_Dt08_20, Const_Dt08_10)
Add_Err(Const_10Err_L2, Const_Dt10_80, Const_Dt10_40, Const_Dt10_20, Const_Dt10_10)

Add_Err(Const_12Err_L2, Const_Dt12_80, Const_Dt12_40, Const_Dt12_20, Const_Dt12_10)
Add_Err(Const_14Err_L2, Const_Dt14_80, Const_Dt14_40, Const_Dt14_20, Const_Dt14_10)
Add_Err(Const_16Err_L2, Const_Dt16_80, Const_Dt16_40, Const_Dt16_20, Const_Dt16_10)
Add_Err(Const_18Err_L2, Const_Dt18_80, Const_Dt18_40, Const_Dt18_20, Const_Dt18_10)

# ==================Draw L2 Norm error : C data =============================
HHT_CData = np.arange(0.2, 2.0, 0.2)
HHT_Dy80row_errL2 = np.zeros((len(HHT_CData),2))
HHT_Dy40row_errL2 = np.zeros((len(HHT_CData),2))
HHT_Dy20row_errL2 = np.zeros((len(HHT_CData),2))
HHT_Dy10row_errL2 = np.zeros((len(HHT_CData),2))

Const_CData = np.arange(0.2, 2.0, 0.2)
Const_Dy80row_errL2 = np.zeros((len(Const_CData),2))
Const_Dy40row_errL2 = np.zeros((len(Const_CData),2))
Const_Dy20row_errL2 = np.zeros((len(Const_CData),2))
Const_Dy10row_errL2 = np.zeros((len(Const_CData),2))

Cen_CData = np.arange(0.2, 1.0, 0.2)
Cen_Dy80row_errL2 = np.zeros((len(Cen_CData),2))
Cen_Dy40row_errL2 = np.zeros((len(Cen_CData),2))
Cen_Dy20row_errL2 = np.zeros((len(Cen_CData),2))
Cen_Dy10row_errL2 = np.zeros((len(Cen_CData),2))

Lin_CData = np.arange(0.2, 1.8, 0.2)
Lin_Dy80row_errL2 = np.zeros((len(Lin_CData),2))
Lin_Dy40row_errL2 = np.zeros((len(Lin_CData),2))
Lin_Dy20row_errL2 = np.zeros((len(Lin_CData),2))
Lin_Dy10row_errL2 = np.zeros((len(Lin_CData),2))

# ------------- For Relative Error -------------------
def Infinite_Relative(C_Data, Dy80row_err, Mesh_Num, Dt02_err, Dt04_err, Dt06_err, Dt08_err, Dt10_err, Dt12_err, Dt14_err, Dt16_err, Dt18_err):
    Dy80row_err[:,0] = C_Data[:]
    Dy80row_err[0,1] = Dt02_err[Mesh_Num, 1]
    Dy80row_err[1,1] = Dt04_err[Mesh_Num, 1]
    Dy80row_err[2,1] = Dt06_err[Mesh_Num, 1]
    Dy80row_err[3,1] = Dt08_err[Mesh_Num, 1]
    Dy80row_err[4,1] = Dt10_err[Mesh_Num, 1]
    Dy80row_err[5,1] = Dt12_err[Mesh_Num, 1]
    Dy80row_err[6,1] = Dt14_err[Mesh_Num, 1]
    Dy80row_err[7,1] = Dt16_err[Mesh_Num, 1]
    Dy80row_err[8,1] = Dt18_err[Mesh_Num, 1]#  ; 2.62104e+10
    return Dy80row_err

# ---------- Mesh Size = 80, 40, 20, 10 row -------------
Infinite_Relative(HHT_CData, HHT_Dy80row_errL2, 0, HHT_02Err_L2, HHT_04Err_L2, HHT_06Err_L2, HHT_08Err_L2, HHT_10Err_L2, HHT_12Err_L2, HHT_14Err_L2, HHT_16Err_L2, HHT_18Err_L2)
Infinite_Relative(HHT_CData, HHT_Dy40row_errL2, 1, HHT_02Err_L2, HHT_04Err_L2, HHT_06Err_L2, HHT_08Err_L2, HHT_10Err_L2, HHT_12Err_L2, HHT_14Err_L2, HHT_16Err_L2, HHT_18Err_L2)
Infinite_Relative(HHT_CData, HHT_Dy20row_errL2, 2, HHT_02Err_L2, HHT_04Err_L2, HHT_06Err_L2, HHT_08Err_L2, HHT_10Err_L2, HHT_12Err_L2, HHT_14Err_L2, HHT_16Err_L2, HHT_18Err_L2)
Infinite_Relative(HHT_CData, HHT_Dy10row_errL2, 3, HHT_02Err_L2, HHT_04Err_L2, HHT_06Err_L2, HHT_08Err_L2, HHT_10Err_L2, HHT_12Err_L2, HHT_14Err_L2, HHT_16Err_L2, HHT_18Err_L2)

Infinite_Relative(Const_CData, Const_Dy80row_errL2, 0, Const_02Err_L2, Const_04Err_L2, Const_06Err_L2, Const_08Err_L2, Const_10Err_L2, Const_12Err_L2, Const_14Err_L2, Const_16Err_L2, Const_18Err_L2)
Infinite_Relative(Const_CData, Const_Dy40row_errL2, 1, Const_02Err_L2, Const_04Err_L2, Const_06Err_L2, Const_08Err_L2, Const_10Err_L2, Const_12Err_L2, Const_14Err_L2, Const_16Err_L2, Const_18Err_L2)
Infinite_Relative(Const_CData, Const_Dy20row_errL2, 2, Const_02Err_L2, Const_04Err_L2, Const_06Err_L2, Const_08Err_L2, Const_10Err_L2, Const_12Err_L2, Const_14Err_L2, Const_16Err_L2, Const_18Err_L2)
Infinite_Relative(Const_CData, Const_Dy10row_errL2, 3, Const_02Err_L2, Const_04Err_L2, Const_06Err_L2, Const_08Err_L2, Const_10Err_L2, Const_12Err_L2, Const_14Err_L2, Const_16Err_L2, Const_18Err_L2)

def Cen_Relative(C_Data, Dy80row_err, Mesh_Num, Dt02_err, Dt04_err, Dt06_err, Dt08_err, Dt10_err):
    Dy80row_err[:,0] = C_Data[:]
    Dy80row_err[0,1] = Dt02_err[Mesh_Num, 1]
    Dy80row_err[1,1] = Dt04_err[Mesh_Num, 1]
    Dy80row_err[2,1] = Dt06_err[Mesh_Num, 1]
    Dy80row_err[3,1] = Dt08_err[Mesh_Num, 1]
    # Dy80row_err[4,1] = Dt10_err[Mesh_Num, 1]
    # Dy80row_err[5,1] = Dt12_err[Mesh_Num, 1]
    # Dy80row_err[6,1] = Dt14_err[Mesh_Num, 1]
    # Dy80row_err[7,1] = Dt16_err[Mesh_Num, 1]
    # Dy80row_err[8,1] = Dt18_err[Mesh_Num, 1]#  ; 2.62104e+10
    return Dy80row_err

Cen_Relative(Cen_CData, Cen_Dy80row_errL2, 0, Cen_02Err_L2, Cen_04Err_L2, Cen_06Err_L2,Cen_08Err_L2, Cen_10Err_L2)
Cen_Relative(Cen_CData, Cen_Dy40row_errL2, 1, Cen_02Err_L2, Cen_04Err_L2, Cen_06Err_L2,Cen_08Err_L2, Cen_10Err_L2)
Cen_Relative(Cen_CData, Cen_Dy20row_errL2, 2, Cen_02Err_L2, Cen_04Err_L2, Cen_06Err_L2,Cen_08Err_L2, Cen_10Err_L2)
Cen_Relative(Cen_CData, Cen_Dy10row_errL2, 3, Cen_02Err_L2, Cen_04Err_L2, Cen_06Err_L2,Cen_08Err_L2, Cen_10Err_L2)

def Lin_Relative(C_Data, Dy80row_err, Mesh_Num, Dt02_err, Dt04_err, Dt06_err, Dt08_err, Dt10_err, Dt12_err, Dt14_err, Dt16_err, ):
    Dy80row_err[:,0] = C_Data[:]
    Dy80row_err[0,1] = Dt02_err[Mesh_Num, 1]
    Dy80row_err[1,1] = Dt04_err[Mesh_Num, 1]
    Dy80row_err[2,1] = Dt06_err[Mesh_Num, 1]
    Dy80row_err[3,1] = Dt08_err[Mesh_Num, 1]
    Dy80row_err[4,1] = Dt10_err[Mesh_Num, 1]
    Dy80row_err[5,1] = Dt12_err[Mesh_Num, 1]
    Dy80row_err[6,1] = Dt14_err[Mesh_Num, 1]
    Dy80row_err[7,1] = Dt16_err[Mesh_Num, 1]
    # Dy80row_err[8,1] = Dt18_err[Mesh_Num, 1]#  ; 2.62104e+10
    return Dy80row_err

Lin_Relative(Lin_CData, Lin_Dy80row_errL2, 0, Lin_02Err_L2, Lin_04Err_L2, Lin_06Err_L2, Lin_08Err_L2, Lin_10Err_L2, Lin_12Err_L2, Lin_14Err_L2, Lin_16Err_L2)
Lin_Relative(Lin_CData, Lin_Dy40row_errL2, 1, Lin_02Err_L2, Lin_04Err_L2, Lin_06Err_L2, Lin_08Err_L2, Lin_10Err_L2, Lin_12Err_L2, Lin_14Err_L2, Lin_16Err_L2)
Lin_Relative(Lin_CData, Lin_Dy20row_errL2, 2, Lin_02Err_L2, Lin_04Err_L2, Lin_06Err_L2, Lin_08Err_L2, Lin_10Err_L2, Lin_12Err_L2, Lin_14Err_L2, Lin_16Err_L2)
Lin_Relative(Lin_CData, Lin_Dy10row_errL2, 3, Lin_02Err_L2, Lin_04Err_L2, Lin_06Err_L2, Lin_08Err_L2, Lin_10Err_L2, Lin_12Err_L2, Lin_14Err_L2, Lin_16Err_L2)

def DifferBoundary_L2NormError2(HHT_Dy80row_errL2, HHT_Dy40row_errL2, HHT_Dy20row_errL2, HHT_Dy10row_errL2, Const_Dy80row_errL2, Const_Dy40row_errL2, Const_Dy20row_errL2, Const_Dy10row_errL2,
                                Lin_Dy80row_errL2, Lin_Dy40row_errL2, Lin_Dy20row_errL2, Lin_Dy10row_errL2, Cen_Dy80row_errL2, Cen_Dy40row_errL2, Cen_Dy20row_errL2, Cen_Dy10row_errL2): 
    plt.figure(figsize=(12,10))
    # plt.title(f'Different Integrator L2-Norm Error', fontsize = 25) # Compare / Integrator
    # plt.text(0.02, 0.06, r'$C_{cricital}=$ $\mathrm{infinite}$', fontsize=25, transform=plt.gca().transAxes)
    
    font_props = {'family': 'Arial', 'size': 18}
# ================= HHT-Alpha ==============================
    plt.plot(HHT_Dy80row_errL2[:,0], HHT_Dy80row_errL2[:,1],marker = '^',markersize=12,markerfacecolor = 'none',label = r'$\Delta_y =  $ $\mathrm {0.125m}$', color = 'limegreen', linewidth = 3.0)
    plt.plot(HHT_Dy40row_errL2[:,0], HHT_Dy40row_errL2[:,1],marker = 'o',markersize=12,markerfacecolor = 'none',label =  r'$\Delta_y =  $ $\mathrm {0.250m}$', color= 'limegreen', linewidth = 3.0)
    plt.plot(HHT_Dy20row_errL2[:,0], HHT_Dy20row_errL2[:,1],marker = '<',markersize=12,markerfacecolor = 'none',label = r'$\Delta_y =  $ $\mathrm {0.500m}$', color= 'limegreen', linewidth = 3.0)
    plt.plot(HHT_Dy10row_errL2[:,0], HHT_Dy10row_errL2[:,1],marker = 's',markersize=12,markerfacecolor = 'none',label = r'$\Delta_y =  $ $\mathrm {1.000m}$', color= 'limegreen', linewidth = 3.0)
# ================= Newmark Constant ==============================
    plt.plot(Const_Dy80row_errL2[:,0], Const_Dy80row_errL2[:,1],marker = '^',markersize=12,markerfacecolor = 'none', color = 'darkorange', ls = '-.', linewidth = 3.0)
    plt.plot(Const_Dy40row_errL2[:,0], Const_Dy40row_errL2[:,1],marker = 'o',markersize=12,markerfacecolor = 'none', color= 'darkorange', ls = '-.', linewidth = 3.0)
    plt.plot(Const_Dy20row_errL2[:,0], Const_Dy20row_errL2[:,1],marker = '<',markersize=12,markerfacecolor = 'none', color= 'darkorange', ls = '-.', linewidth = 3.0)
    plt.plot(Const_Dy10row_errL2[:,0], Const_Dy10row_errL2[:,1],marker = 's',markersize=12,markerfacecolor = 'none', color= 'darkorange', ls = '-.', linewidth = 3.0)
# ================= Newmark Linear ==============================
    plt.plot(Lin_Dy80row_errL2[:,0], Lin_Dy80row_errL2[:,1],marker = '^',markersize=12,markerfacecolor = 'none', color = 'mediumblue', ls = ':', linewidth = 3.0)
    plt.plot(Lin_Dy40row_errL2[:,0], Lin_Dy40row_errL2[:,1],marker = 'o',markersize=12,markerfacecolor = 'none', color= 'mediumblue', ls = ':', linewidth = 3.0)
    plt.plot(Lin_Dy20row_errL2[:,0], Lin_Dy20row_errL2[:,1],marker = '<',markersize=12,markerfacecolor = 'none', color= 'mediumblue', ls = ':', linewidth = 3.0)
    plt.plot(Lin_Dy10row_errL2[:,0], Lin_Dy10row_errL2[:,1],marker = 's',markersize=12,markerfacecolor = 'none', color= 'mediumblue', ls = ':', linewidth = 3.0)
# ================= Central Differential ==============================
    plt.plot(Cen_Dy80row_errL2[:,0], Cen_Dy80row_errL2[:,1],marker = '^',markersize=12,markerfacecolor = 'none', color = 'crimson', ls = '--', linewidth = 3.0)
    plt.plot(Cen_Dy40row_errL2[:,0], Cen_Dy40row_errL2[:,1],marker = 'o',markersize=12,markerfacecolor = 'none', color= 'crimson', ls = '--', linewidth = 3.0)
    plt.plot(Cen_Dy20row_errL2[:,0], Cen_Dy20row_errL2[:,1],marker = '<',markersize=12,markerfacecolor = 'none', color= 'crimson', ls = '--', linewidth = 3.0)
    plt.plot(Cen_Dy10row_errL2[:,0], Cen_Dy10row_errL2[:,1],marker = 's',markersize=12,markerfacecolor = 'none', color= 'crimson', ls = '--', linewidth = 3.0)
    
    legend_elements = [Line2D([0], [0], color='limegreen', lw=3, label= f'HHT-'+r'$\alpha$'),
                    Line2D([0], [0], color='darkorange', lw=3, ls = '-.', label='Newmark Constant'),
                    Line2D([0], [0], color='mediumblue', lw=3, ls = ':', label='Newmark Linear'),
                    Line2D([0], [0], color='crimson', lw=3, ls = '--', label='Central Differential')]
    
    legend_elements2 = [Line2D([0], [0], color='black',marker = '^',markersize=12,markerfacecolor = 'none', label= r'$\Delta_{c}=0.125$ $\mathrm{m}$'),
                   Line2D([0], [0], color='black',marker = 'o',markersize=12,markerfacecolor = 'none', label=r'$\Delta_{c}=0.250$ $\mathrm{m}$'),
                   Line2D([0], [0], color='black',marker = '<',markersize=12,markerfacecolor = 'none', label=r'$\Delta_{c}=0.500$ $\mathrm{m}$'),
                   Line2D([0], [0], color='black',marker = 's',markersize=12,markerfacecolor = 'none', label=r'$\Delta_{c}=1.000$ $\mathrm{m}$')]
    
    legend1 = plt.legend(ncol=1, handles=legend_elements, prop=font_props, loc=(0.01, 0.95)) #ncol=2,fontsize=16 frameon=False , loc='upper left'
    legend1.get_frame().set_edgecolor('grey')
    legend1.get_frame().set_linewidth(2)  # 設置外框寬度
    plt.gca().add_artist(legend1)
    
    legend2 = plt.legend(ncol=1, handles=legend_elements2, prop=font_props, loc=(0.35, 0.95)) #ncol=2,fontsize=16 frameon=False , loc='upper left'
    legend2.get_frame().set_edgecolor('grey')
    legend2.get_frame().set_linewidth(2)  # 設置外框寬度
    
    plt.xticks(fontsize = 20, fontweight='bold', color='black')
    plt.yticks(fontsize = 20, fontweight='bold', color='black')
    
    plt.xlabel(f'Time Increment Ratio ' +r'$C$', fontsize = 28)
    plt.ylabel('Normalized L2 Norm Error '+ r"$\ E_{L2}$"  , fontsize = 28) # 'L2 Norm Error: '+ r"$\ E_{L2}$" / 'L2 normalization'+ r"$\ E_{L2N}$"

    plt.xlim(0.2, 1.8)
    plt.ylim(0, 0.6)
    plt.grid(True)
    # ========== set up figure thick ============================
    bwidth = 2
    TK = plt.gca()
    TK.spines['bottom'].set_linewidth(bwidth)
    TK.spines['left'].set_linewidth(bwidth)
    TK.spines['top'].set_linewidth(bwidth)
    TK.spines['right'].set_linewidth(bwidth)
    
    ax = plt.gca()
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(0.2))
    # -------------- Consider X-axis  -----------------------
    ax.set_xscale('log', base=10)
    ax.set_xticks([], minor=False)
    ax.set_xticks([], minor=True)
    x_ticks_Num = np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8])  # 设置线性刻度间距为0.125
    ax.set_xticks(x_ticks_Num)
    
    ax.set_xticklabels([f'{tick:.1f}' for tick in x_ticks_Num], rotation=0, fontsize=12)
    # 设置x轴的刻度大小
    ax.tick_params(axis='x', which='major', labelsize= 25, length=8, width=2)
    
    # -------------- Consider Y-axis  -----------------------
    ax.set_yscale('log', base=10)
    ax.set_yticks([], minor=False)
    ax.set_yticks([], minor=True)
    y_ticks_Num = np.array([0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.4, 0.6])  # 设置线性刻度间距为0.1  np.arange(0.1, 10.1, 0.1)
    ax.set_yticks(y_ticks_Num)
    ax.set_yticklabels([f'{tick:.2f}' for tick in y_ticks_Num], rotation=0, fontsize=12)
    ax.tick_params(axis='y', which='major', labelsize= 25, length=8, width=2)
    # ------- Miner ticks -----------------
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis='y', which='minor', length=4, width=2, color='gray')
    
    # # 使用科学计数法显示y轴刻度标签
    # ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    # ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))  # 使用科学计数法格式化   
    ax.set_ylim(0.0, 0.6)  # 例如从0.1到10
    
DifferBoundary_L2NormError2(HHT_Dy80row_errL2, HHT_Dy40row_errL2, HHT_Dy20row_errL2, HHT_Dy10row_errL2, Const_Dy80row_errL2, Const_Dy40row_errL2, Const_Dy20row_errL2, Const_Dy10row_errL2,
                                Lin_Dy80row_errL2, Lin_Dy40row_errL2, Lin_Dy20row_errL2, Lin_Dy10row_errL2, Cen_Dy80row_errL2, Cen_Dy40row_errL2, Cen_Dy20row_errL2, Cen_Dy10row_errL2)

def DifferMesh_L2NormError2(titleName, HHT_Dy80row_errL2, Const_Dy80row_errL2, Lin_Dy80row_errL2, Cen_Dy80row_errL2): 
    plt.figure(figsize=(10, 8))
    plt.title(titleName, fontsize = 25) # Compare / Integrator
    # plt.text(0.02, 0.06, r'$C_{cricital}=$ $\mathrm{infinite}$', fontsize=25, transform=plt.gca().transAxes)
    
    font_props = {'family': 'Arial', 'size': 18}
# ================= HHT-Alpha ==============================
    plt.plot(HHT_Dy80row_errL2[:,0], HHT_Dy80row_errL2[:,1],marker = '^',markersize=12,markerfacecolor = 'white', color = 'limegreen', label= f'HHT-'+r'$\alpha$',linewidth = 3.0)
# ================= Newmark Constant ==============================
    plt.plot(Const_Dy80row_errL2[:,0], Const_Dy80row_errL2[:,1],marker = 'o',markersize=11,markerfacecolor = 'white', color = 'orange', label= f'Newmark Constant', ls = '-.', linewidth = 3.0)
# ================= Newmark Linear ==============================
    plt.plot(Lin_Dy80row_errL2[:,0], Lin_Dy80row_errL2[:,1],marker = '<',markersize=10,markerfacecolor = 'white', color = 'purple', label= f'Newmark Linear', ls = ':', linewidth = 3.0)
# ================= Central Differential ==============================
    plt.plot(Cen_Dy80row_errL2[:,0], Cen_Dy80row_errL2[:,1],marker = 's',markersize=9,markerfacecolor = 'white', color = 'red', label= f'Central Differential', ls = '--', linewidth = 3.0)
    
    plt.legend(ncol=1, prop=font_props, loc= 'upper left')
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
    
    plt.xlabel(f'Time Increment Ratio ' +r'$C$', fontsize = 25)
    plt.ylabel('L2 Norm Error: '+ r"$\ E_{L2}$" , fontsize = 25) # 'L2 Norm Error: '+ r"$\ E_{L2}$" / 'L2 normalization'+ r"$\ E_{L2N}$"

    plt.xlim(0.2, 1.8)
    plt.ylim(0, 0.6)
    plt.grid(True)
    
    ax = plt.gca()
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(0.2))
    # -------------- Consider X-axis  -----------------------
    ax.set_xscale('log', base=10)
    ax.set_xticks([], minor=False)
    ax.set_xticks([], minor=True)
    x_ticks_Num = np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8])  # 设置线性刻度间距为0.125
    ax.set_xticks(x_ticks_Num)
    
    ax.set_xticklabels([f'{tick:.1f}' for tick in x_ticks_Num], rotation=0, fontsize=12)
    # 设置x轴的刻度大小
    ax.tick_params(axis='x', which='both', labelsize=22)
    
    # -------------- Consider Y-axis  -----------------------
    ax.set_yscale('log', base=10)
    ax.set_yticks([], minor=False)
    ax.set_yticks([], minor=True)
    y_ticks_Num = np.array([0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.4, 0.6])  # 设置线性刻度间距为0.1  np.arange(0.1, 10.1, 0.1)
    ax.set_yticks(y_ticks_Num)
    ax.get_yaxis().set_major_formatter(LogFormatter(labelOnlyBase=False))
    # ------- Miner ticks -----------------
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis='y', which='minor', length=4, color='gray')
    
    ax.set_yticklabels([f'{tick:.2f}' for tick in y_ticks_Num], rotation=0, fontsize=12)
    ax.tick_params(axis='y', which='both', labelsize=20)
    
    # # 使用科学计数法显示y轴刻度标签
    # ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    # ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))  # 使用科学计数法格式化   
    ax.set_ylim(0.0, 0.6)  # 例如从0.1到10
    
# DifferMesh_L2NormError2(f'Boundary Compare: '+r'$\Delta_c =  $ $\mathrm {0.125m}$', HHT_Dy80row_errL2, Const_Dy80row_errL2, Lin_Dy80row_errL2, Cen_Dy80row_errL2)
# DifferMesh_L2NormError2(f'Boundary Compare: '+r'$\Delta_c =  $ $\mathrm {0.250m}$', HHT_Dy40row_errL2, Const_Dy40row_errL2, Lin_Dy40row_errL2, Cen_Dy40row_errL2)
# DifferMesh_L2NormError2(f'Boundary Compare: '+r'$\Delta_c =  $ $\mathrm {0.500m}$', HHT_Dy20row_errL2, Const_Dy20row_errL2, Lin_Dy20row_errL2, Cen_Dy20row_errL2)
# DifferMesh_L2NormError2(f'Boundary Compare: '+r'$\Delta_c =  $ $\mathrm {1.000m}$', HHT_Dy10row_errL2, Const_Dy10row_errL2, Lin_Dy10row_errL2, Cen_Dy10row_errL2)
