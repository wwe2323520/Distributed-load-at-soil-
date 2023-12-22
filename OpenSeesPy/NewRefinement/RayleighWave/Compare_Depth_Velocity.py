# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 22:03:39 2023

@author: User
"""
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
from matplotlib.ticker import ScalarFormatter
from matplotlib import pyplot as plt, ticker as mticker
import scipy.signal
from scipy.signal import find_peaks

start = time.time()

pi = np.pi
plt.rc('font', family= 'Times New Roman')


soilWidth = 10.0
SoilDepth = 10.0 
DW = 0.125
nx = int(soilWidth/DW)
ny = 80

yMesh = SoilDepth/ny
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

# --------- Tie Boundary Condition ----------------
fileNumber = 0
# for a in range(len(a_cofficient)):
#     akz = a_cofficient[a]
#     for b in range(len(b_cofficient)):
#         fileNumber = fileNumber + 1
#         bkz = b_cofficient[b]
        # file[fileNumber] = 
        
# Depth = np.array([0.25,0.5,1.25,2.5]) 
# a_cofficient = np.array([0.5, 2.0])
# b_cofficient = np.array([0.5, 1.0, 2.0])

# for Apply_Depth in Depth:
#     Applt_D = round(Apply_Depth, 2)
#     Apply_node = Applt_D/0.125
#     print(f'Applt Rayleigh Depth = {Applt_D}', f"; Node = {Apply_node}")

    # for akz in a_cofficient:

    #     for bkz in b_cofficient:
    #         a = round(akz, 2)
    #         b = round(bkz, 2)
    #         print(f'a_Cofficient = {a} ; b_Cofficient = {b} ')


def Input_File(Apply_D, akz, bkz):
    file_paths = []
    file = []

    file_paths2 = []
    file2 = []
    
    for o in range(ny+1):
    # ---------------- Left Side ------------
        Depth = yMesh*o 
        LeftNode = int(1 + (nx+1)*o)
        file_paths.append(f"E:/unAnalysisFile/RayleighDashpot/Tie_cpdt/DepthTest/H{Apply_D}/Ca{akz}_Cb{bkz}/Velocity/D{Depth}_Lnode{LeftNode}.out")
    
        name =  f'D{Depth}_Lnode{LeftNode}'
        file.append(name)
    # ---------------- Center Side ------------
    for o in range(ny+1):
        Depth = yMesh*o 
        CenterNode = int((1 + (nx/2)) + (nx+1)*o)
        file_paths.append(f"E:/unAnalysisFile/RayleighDashpot/Tie_cpdt/DepthTest/H{Apply_D}/Ca{akz}_Cb{bkz}/Velocity/D{Depth}_Cnode{CenterNode}.out")
        name =  f'D{Depth}_Cnode{CenterNode}'
        file.append(name)
    
    # ---------------- Right Side ------------
    for o in range(ny+1):
        Depth = yMesh*o 
        RightNode = int((1+nx)+ (nx+1)*o)
        file_paths.append(f"E:/unAnalysisFile/RayleighDashpot/Tie_cpdt/DepthTest/H{Apply_D}/Ca{akz}_Cb{bkz}/Velocity/D{Depth}_Rnode{RightNode}.out")
        name =  f'D{Depth}_Rnode{RightNode}'
        file.append(name)
    
    # ---------------- Surface Side ------------
    topLeftNode = 1 + (nx+1)* (ny)
    
    for width in range(nx+1):
        topNode = topLeftNode + width
        MeshWidth = DW*width # 0.125*
    
        file_paths2.append(f"E:/unAnalysisFile/RayleighDashpot/Tie_cpdt/DepthTest/H{Apply_D}/Ca{akz}_Cb{bkz}/SurfaceVelocity/W{MeshWidth}node{topNode}.out")
        name =  f'W{MeshWidth}node{topNode}'
        file2.append(name)
        
    for size in range(len(file)): #
        file[size] = rdnumpy(file_paths[size]) # Convert File into array
    
    for size2 in range(len(file2)): #
        file2[size2] = rdnumpy(file_paths2[size2]) # Convert File into array

    #===================== Make x - Vx Matrix (each depth) =====================
    # ----------------- Depth amd Time Matrix -------------------------
    surfaceID = ny
    Depth_Array = np.arange(0.0, SoilDepth+yMesh, yMesh)
    Width_Array = np.arange(0.0, soilWidth+DW, DW)
    
    Total_Time = []
    Dstep = 10 # Contol TimeStep*******
    TotalStep = int(len(file[0][:,0])/Dstep)
    
    for i in range(TotalStep+1):
        t = i
        if i > 0:    
            t = 10*i-1    
        Total_Time.append(file[0][t,0])

    # ----------------- Grab each Depth and Velocity Data -------------------------
    LDep_Vel = np.zeros((ny+1,len(Total_Time)+1))
    CDep_Vel = np.zeros((ny+1,len(Total_Time)+1))
    RDep_Vel = np.zeros((ny+1,len(Total_Time)+1))
    
    LDep_Vel[:,0] = Depth_Array[:]
    CDep_Vel[:,0] = Depth_Array[:]
    RDep_Vel[:,0] = Depth_Array[:]
    
    CDepId = ny+1 
    RDepId = 2*(ny+1) 

    # ------------- Left / Center / Column Differ Depth vs Velocity y Store
    Vdir = 2 ## Velocity Direction
    for i in range(TotalStep+1):     #TotalStep+1
        if i == 0:    
            t = i
            for Dep in range(len(Depth_Array)):
                LDep_Vel[Dep, 1] = file[Dep][t][Vdir] 
                CDep_Vel[Dep, 1] = file[CDepId+Dep][t][Vdir] 
                RDep_Vel[Dep, 1] = file[RDepId+Dep][t][Vdir]
    
        if i > 0:
            t = (10*i) - 1
            for Dep in range(len(Depth_Array)):
                LDep_Vel[Dep, i+1] = file[Dep][t][Vdir] 
                CDep_Vel[Dep, i+1] = file[CDepId+Dep][t][Vdir] 
                RDep_Vel[Dep, i+1] = file[RDepId+Dep][t][Vdir]
    
    # ------------ Surface Width : Width- Velocity Data -----------------------
    Surface_Vel = np.zeros((nx+1, len(Total_Time)+1))
    Surface_Vel[:,0] = Width_Array[:]
            
    for g in range(TotalStep+1):
        if g == 0:    
            t = g
            for Wid in range(len(Width_Array)):
                Surface_Vel[Wid, 1] = file2[Wid][t][Vdir] 
        if g > 0:
            t = (10*g) - 1
            for Wid in range(len(Width_Array)):
                Surface_Vel[Wid, g+1] = file2[Wid][t][Vdir]    
    
    return(LDep_Vel, CDep_Vel, RDep_Vel, Surface_Vel, Total_Time, TotalStep)

LDep_Vela0_b0, CDep_Vela0_b0, RDep_Vela0_b0, Surface_Vela0_b0, Total_Time, TotalStep = Input_File(0.0, 0.0, 0.0)
LDep_Vela20_b5, CDep_Vela20_b5, RDep_Vela20_b5, Surface_Vela20_b5, Total_Time, TotalStep = Input_File(1.25, 2.0, 0.5)
LDep_Vela20_b10, CDep_Vela20_b10, RDep_Vela20_b10, Surface_Vela20_b10, Total_Time, TotalStep = Input_File(1.25, 2.0, 1.0)
LDep_Vela20_b20, CDep_Vela20_b20, RDep_Vela20_b20, Surface_Vela20_b20, Total_Time, TotalStep = Input_File(1.25, 2.0, 2.0)
# # ----------------- Build File to Store Image ---------------------------
output_folder1 = f'E:/unAnalysisFile/RayleighDashpot/Image_Video/Tie_cpdt_Output/DepthTest/Compare_Cb/Vel_Dep/LeftColumn'
os.makedirs(output_folder1, exist_ok=True)

output_folder2 = f'E:/unAnalysisFile/RayleighDashpot/Image_Video/Tie_cpdt_Output/DepthTest/Compare_Cb/Vel_Dep/CenterColumn'
os.makedirs(output_folder2, exist_ok=True)

output_folder3 = f'E:/unAnalysisFile/RayleighDashpot/Image_Video/Tie_cpdt_Output/DepthTest/Compare_Cb/Vel_Dep/RightColumn'
os.makedirs(output_folder3, exist_ok=True)

output_folder4 = f'E:/unAnalysisFile/RayleighDashpot/Image_Video/Tie_cpdt_Output/DepthTest/Compare_Cb/SurfaceVel'
os.makedirs(output_folder4, exist_ok=True) 

x_axis = 1
def draw_Depthh_Velocity(ColumnName,LDep_Vela0_b0, LDep_Vela5_b5, LDep_Vela20_b5, LDep_Vela20_b20, label1, label2, label3, output_folder1):
    for pt in range(TotalStep+1):     #TotalStep+1
        plt.figure(figsize= (8,6))
        font_props = {'family': 'Arial', 'size': 16}
        
        plt.title(f"{ColumnName} Velocity: t = {Total_Time[pt]}s", fontsize = 20)
        
        plt.ylabel('Depth (m)', fontsize = 20)
        plt.xlabel(r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", fontsize = 20)

        plt.plot(LDep_Vela0_b0[:, 1+pt], LDep_Vela0_b0[:,0], label = "Ca=0.0; Cb=0.0", color= 'blue', ls = '-',linewidth=6.0)
        plt.plot(LDep_Vela5_b5[:, 1+pt], LDep_Vela5_b5[:,0], label = label1, color= 'darkorange', ls = '--',linewidth=5.0)
        plt.plot(LDep_Vela20_b5[:, 1+pt], LDep_Vela20_b5[:,0], label = label2, color= 'limegreen', ls = '-.',linewidth=4.0)    
        plt.plot(LDep_Vela20_b20[:, 1+pt], LDep_Vela20_b20[:,0], label = label3, color= 'red', ls = ':',linewidth=3.0)
        
        plt.ylim(0.0, SoilDepth)
        plt.xlim(-5e-6, 6e-6)
        
        plt.legend(loc='upper left',prop=font_props) #ncol=2,fontsize=16
        
        plt.xticks(fontsize = 16)
        plt.yticks(fontsize = 16)
        plt.grid(True)
        
        ax1 = plt.gca()
        ax1.yaxis.set_major_locator(ticker.MultipleLocator(x_axis))
        ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='x')
        ax1.xaxis.get_offset_text().set(size=18)
        
        image_path = os.path.join(output_folder1, f'{pt+1}.png')
        plt.savefig(image_path, bbox_inches='tight')
        plt.close()
    print("Images saved to", output_folder1) 

draw_Depthh_Velocity('Left Column', LDep_Vela0_b0, LDep_Vela20_b5, LDep_Vela20_b10, LDep_Vela20_b20,
                      'Ca=2.0; Cb=0.5', 'Ca=2.0; Cb=1.0', 'Ca=2.0; Cb=2.0', output_folder1)
draw_Depthh_Velocity('Center Column', CDep_Vela0_b0, CDep_Vela20_b5, CDep_Vela20_b10, CDep_Vela20_b20,
                      'Ca=2.0; Cb=0.5', 'Ca=2.0; Cb=1.0', 'Ca=2.0; Cb=2.0', output_folder2)
draw_Depthh_Velocity('Right Column', RDep_Vela0_b0, RDep_Vela20_b5, RDep_Vela20_b10, RDep_Vela20_b20,
                      'Ca=2.0; Cb=0.5', 'Ca=2.0; Cb=1.0', 'Ca=2.0; Cb=2.0', output_folder3)  

x_axix2 = 0.50
def draw_Width_Velocity(ColumnName, Surface_Vela0_b0, Surface_Vela5_b5, Surface_Vela20_b5, Surface_Vela20_b20, label1, label2, label3,output_folder1):
    for pt in range(TotalStep+1):     #TotalStep+1
        plt.figure(figsize= (8,6))
        font_props = {'family': 'Arial', 'size': 16}
        
        plt.title(f"{ColumnName} Velocity: t = {Total_Time[pt]}s", fontsize = 20)
        
        plt.xlabel('Width (m)', fontsize = 20)
        plt.ylabel(r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", fontsize = 20)

        plt.plot(Surface_Vela0_b0[:,0], Surface_Vela0_b0[:, 1+pt], label = "Ca=0.0; Cb=0.0", color= 'blue', ls = '-',linewidth=6.0)    
        plt.plot(Surface_Vela5_b5[:,0], Surface_Vela5_b5[:, 1+pt], label = label1, color= 'darkorange', ls = '--',linewidth=5.0)
        plt.plot(Surface_Vela20_b5[:,0], Surface_Vela20_b5[:, 1+pt], label = label2, color= 'limegreen', ls = '-.',linewidth=4.0)
        plt.plot(Surface_Vela20_b20[:,0], Surface_Vela20_b20[:, 1+pt], label = label3, color= 'red', ls = ':',linewidth=3.0)   
        
        plt.xlim(0.0, soilWidth)
        plt.ylim(-5e-6, 6e-6)
        
        plt.legend(loc='upper left',prop=font_props) #ncol=2,fontsize=16
        
        plt.xticks(fontsize = 14)
        plt.yticks(fontsize = 16)
        plt.grid(True)
        
        ax2 = plt.gca()
        ax2.xaxis.set_major_locator(ticker.MultipleLocator(x_axix2))
        ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
        ax2.yaxis.get_offset_text().set(size=18)
        
        image_path = os.path.join(output_folder1, f'{pt+1}.png')
        plt.savefig(image_path, bbox_inches='tight')
        plt.close()
    print("Images saved to", output_folder1)     

draw_Width_Velocity('Surface', Surface_Vela0_b0, Surface_Vela20_b5, Surface_Vela20_b10, Surface_Vela20_b20,
                    'Ca=2.0; Cb=0.5', 'Ca=2.0; Cb=1.0', 'Ca=2.0; Cb=2.0',output_folder4)    


end = time.time()
print('Total Time =', end - start)
print('Finish All Cofficient Image Output')
                                
                                
                                
                                
