wipe
# ================== Build quad element with block2D ================================
model BasicBuilder -ndm 2 -ndf 2
set nx 100    ;# X-dri elements 
set ny 100  ;# Y-dir elements
set e1 1    ;# from which element start
set n1 1    ;# from which node start  

# ------------------ quad element (node 1~10201)-----------------------------------------
#                           $matTag   $E           $v    $rho
nDMaterial ElasticIsotropic  2000    15005714.286  0.3   2020  ;# E:unit -> Pa
block2D $nx $ny $e1 $n1 quad "1 PlaneStrain 2000" {
    1 0.0   0.0
    2 10.0  0.0
    3 10.0  10.0
    4 0.0   10.0 
}
set n 100
for {set i 0} {$i < [expr $n+1]} {incr i} { 
    #---- tie B.C : Only Left and Right node have same disp x,y----------
    equalDOF [expr ($nx+1)*$i+1] [expr ($nx+1)*$i+101] 1 2
    #---- much rigorous way to each node have same disp -------
    # equalDOF [expr 6*$i+1] [expr 6*$i+2] 1 2
    # equalDOF [expr 6*$i+2] [expr 6*$i+3] 1 2
    # equalDOF [expr 6*$i+3] [expr 6*$i+4] 1 2
    # equalDOF [expr 6*$i+4] [expr 6*$i+5] 1 2
    # equalDOF [expr 6*$i+5] [expr 6*$i+6] 1 2
}
# print -node 808 
# ==================== Build Beam element (node 10202~10302)-----------------------------------------
model BasicBuilder -ndm 2 -ndf 3
for {set j 0} {$j < $nx+1} {incr j} {
    node [expr 10202+$j] [expr 0.1*$j] 0.0
    mass [expr 10202+$j] 1 1 1
    fix [expr 10202+$j] 0 0 1
}
# # --------  simple beam setting -----------------
# for {set j 0} {$j < 4} {incr j} {
#     fix [expr 2*$j+810] 1 1 1     ;# even: pin support
#     fix [expr 2*$j+811] 0 1 1     ;# odd : roller support
# }

# # for {set j 0} {$j < 7} {incr j} {
# #     equalDOF 810 [expr 811+$j] 1 2
# #     # puts "810 ,[expr 811+$j]"
# # }
# ------------------- Beam equalDOF: same x,y disp --------------------
equalDOF 10202 10302 1 2

# ------------------ elastic BeamColumn element (100 ele:10001~10100)------------------------
set A [expr 0.1*1]
set E1 1e+05;                      # bigger much harder(1e+05) / smaller much softer (1e-06)
set Iz [expr (0.1*0.1*0.1)/12]
geomTransf Linear 1

for {set k 0} {$k < $nx} {incr k} {
    element elasticBeamColumn [expr 10001+$k] [expr 10202+$k] [expr 10203+$k]  $A  $E1 $Iz 1 ;# 
}

#---------- Bottom Beam and Soil connect ------------------------
for {set l 0} {$l < $nx+1} {incr l} {
    equalDOF [expr 10202+$l] [expr 1+$l] 1 2
}
# ============================ Dashpot Parameter ================================
set rho 2020   ;# kg/m3 
set Vp 100     ;# m/s 
set Vs 53.45224838248488     ;# m/s 
set sizeX 0.1  ;# m

# ========================== Side dashpot =========================================
for {set q 0} {$q < $nx+1} {incr q} {
# ------------- Left Side -----------------
# ------------- traction dashpot: "y" dir (node 10707,10708 ~ 10907,10908)---------------------------------
    node [expr 10707+2*$q] 0.0 [expr 0.1*$q]
    node [expr 10708+2*$q] 0.0 [expr 0.1*$q]
    fix [expr 10707+2*$q] 1 0 1
    fix [expr 10708+2*$q] 1 1 1
# ------------- Normal dashpot: "x" dir (node 10909,10910 ~ 11109,11110)---------------------------------
    node [expr 10909+2*$q] 0.0 [expr 0.1*$q]
    node [expr 10910+2*$q] 0.0 [expr 0.1*$q]
    fix [expr 10909+2*$q] 0 1 1
    fix [expr 10910+2*$q] 1 1 1
# ------------  Right Side -----------------
# ------------- traction dashpot: "y" dir (node 11111,11112 ~ 11311,11312)---------------------------------
    node [expr 11111+2*$q] 10.0 [expr 0.1*$q]
    node [expr 11112+2*$q] 10.0 [expr 0.1*$q]
    fix [expr 11111+2*$q] 1 0 1
    fix [expr 11112+2*$q] 1 1 1
# ------------- Normal dashpot: "x" dir (node 11313,11314 ~ 11513,11514)---------------------------------
    node [expr 11313+2*$q] 10.0 [expr 0.1*$q]
    node [expr 11314+2*$q] 10.0 [expr 0.1*$q]
    fix [expr 11313+2*$q] 0 1 1
    fix [expr 11314+2*$q] 1 1 1
}

# ------------- Connect side node with soil node -------------------------
for {set q 0} {$q < $nx+1} {incr q} {
# ------------- Left Side -----------------
# ------- traction dashpot: "y" dir (ms) --------------
    equalDOF [expr 1+101*$q] [expr 10707+2*$q] 2
# ------- Normal dashpot: "x" dir (mp)--------------
    equalDOF [expr 1+101*$q] [expr 10909+2*$q] 1

# ------------- Right Side -----------------
# ------- traction dashpot: "y" dir (ms) --------------
    equalDOF [expr 101+101*$q] [expr 11111+2*$q] 2
# ------- Normal dashpot: "x" dir (mp)--------------
    equalDOF [expr 101+101*$q] [expr 11313+2*$q] 1
}
# ------------- Side dashpot material -----------------------
set S_Smp  [expr 0.5*$rho*$Vs*$sizeX]  ;# Side dashpot : y dir --  N (newton)
set S_Sms  [expr 0.5*$rho*$Vp*$sizeX]  ;# Side dashpot : x dir --  N (newton)
set S_Cmp  [expr $rho*$Vs*$sizeX]  ;# Center node dashpot : y dir --  N (newton)
set S_Cms  [expr $rho*$Vp*$sizeX]  ;# Center node dashpot : x dir --  N (newton)

uniaxialMaterial Viscous 5000 $S_Smp 1   ;# P wave: Side node
uniaxialMaterial Viscous 5001 $S_Sms 1   ;# S wave: Side node
uniaxialMaterial Viscous 5002 $S_Cmp 1   ;# P wave: Center node
uniaxialMaterial Viscous 5003 $S_Cms 1   ;# S wave: Center node

for {set f 0} {$f < $nx+1} {incr f} {
# -------------- Left side ------------------------
# -------------- traction dashpot element(ele 20202~20302) -----------------------
    element zeroLength [expr 20202+$f] [expr 10708+2*$f] [expr 10707+2*$f] -mat 5002 -dir 2  ;# 0.5*rho*Vs : P wave
    # puts "[expr 20202+$f], [expr 10708+2*$f], [expr 10707+2*$f]"
# -------------- Normal dashpot element(ele 20303~20403) -----------------------
    element zeroLength [expr 20303+$f] [expr 10910+2*$f] [expr 10909+2*$f] -mat 5003 -dir 1  ;# 0.5*rho*Vp: S wave

# -------------- Right side ------------------------
# -------------- traction dashpot element(ele 20404~ 20504) -----------------------
    element zeroLength [expr 20404+$f] [expr 11112+2*$f] [expr 11111+2*$f] -mat 5002 -dir 2  ;# 0.5*rho*Vs : P wave
# -------------- Normal dashpot element(ele 20505~ 20605) -----------------------
    element zeroLength [expr 20505+$f] [expr 11314+2*$f] [expr 11313+2*$f] -mat 5003 -dir 1  ;# 0.5*rho*Vp: S wave

}
puts "Finished creating Side dashpot material and element..."

# ============================ Beam element dashpot =============================== #
for {set k 0} {$k < $nx+1} {incr k} {
# ------------- traction dashpot (node 10303,10304, 10503,10504)------------
    node [expr 10303+2*$k] [expr 0.1*$k] 0.0
    node [expr 10304+2*$k] [expr 0.1*$k] 0.0
# ---------- dashpot dir: cp -> y dir; cs -> x dir ---------------------     
    fix [expr 10303+2*$k] 0 1 1  ;# x dir dashpot　
    fix [expr 10304+2*$k] 1 1 1  
# ------------- Normal dashpot (node 10505,10506~ 10705,10706) ------------
    node [expr 10505+2*$k] [expr 0.1*$k] 0.0
    node [expr 10506+2*$k] [expr 0.1*$k] 0.0
    fix [expr 10505+2*$k] 1 0 1  ;# y dir dashpot　
    fix [expr 10506+2*$k] 1 1 1 
}
# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
# --------------traction dashpot------------------
for {set k 0} {$k < $nx+1} {incr k} {
# ------- traction dashpot --------------
    equalDOF [expr 10202+$k] [expr 10303+2*$k] 1
# ------- Normal dashpot --------------
    equalDOF [expr 10202+$k] [expr 10505+2*$k] 2
}
puts "Finished creating all Bottom dashpot boundary conditions and equalDOF..."
# ------------------- ZeroLength to Build dashpot:Bottom Material ---------------------------------
set B_Smp  [expr 0.5*$rho*$Vp*$sizeX]  ;# Side node dashpot :N (newton)
set B_Sms  [expr 0.5*$rho*$Vs*$sizeX]  ;# Side node dashpot :N (newton)
set B_Cmp  [expr $rho*$Vp*$sizeX]  ;# Center node dashpot :N (newton)
set B_Cms  [expr $rho*$Vs*$sizeX]  ;# Center node dashpot :N (newton)

uniaxialMaterial Viscous 4000 $B_Smp 1   ;# P wave: Side node
uniaxialMaterial Viscous 4001 $B_Sms 1   ;# S wave: Side node

uniaxialMaterial Viscous 4002 $B_Cmp 1   ;# P wave: Center node
uniaxialMaterial Viscous 4003 $B_Cms 1   ;# S wave: Center node
#----------- dashpot elements: Vs with x dir / Vp with y-dir------------------
set xdir 1
set ydir 2
# # ---- traction dashpot element ---(left and right)
# element zeroLength 20000 10304 10303 -mat 4001 -dir $xdir
# element zeroLength 20100 10504 10503 -mat 4001 -dir $xdir
# # ---- Normal dashpot element ---(left and right)
# element zeroLength 20101 10506 10505 -mat 4000 -dir $ydir
# element zeroLength 20201 10706 10705 -mat 4000 -dir $ydir

for {set m 0} {$m < $nx+1} {incr m} {
# -------------- traction dashpot element(ele 20001~20099) -----------------------
    element zeroLength [expr 20000+$m] [expr 10304+2*$m] [expr 10303+2*$m] -mat 4003 -dir $xdir
    # puts "[expr 20000+$m] ,[expr 10304+2*$m] ,[expr 10303+2*$m]"
# -------------- Normal dashpot element (ele 20102~20200)-----------------------
    element zeroLength [expr 20101+$m] [expr 10506+2*$m] [expr 10505+2*$m] -mat 4002 -dir $ydir
    # puts "[expr 20101+$m] ,[expr 10506+2*$m] ,[expr 10505+2*$m]"
}
puts "Finished creating Bottom dashpot material and element..."
# ================= Apply Distributed Load at Beam element ==========================
# ----------given input force (node 1,2) and "Bottom Stress B.C"---------------------#
set filePath fp.txt   ;# fp.txt/ fs.txt
timeSeries Path 702 -dt 0.0001 -filePath $filePath;        #10(m)/100=0.1(s); 0.1/100 cell=0.001(s); 0.001/10 steps=0.0001(s)

set p [expr (2.0/($nx+1))]
set Stress 20.0  ;#20.0

pattern Plain 703 702 {
    #-------------  S wave -------------------------
    # load 810 $p 0 0
    # load 811 $p 0 0
    # load 812 $p 0 0
    # load 813 $p 0 0
    # load 814 $p 0 0
    # load 815 $p 0 0
    # load 816 $p 0 0
    # load 817 $p 0 0
    # for {set u 0} {$u < $nx} {incr u} {
    #     eleLoad -ele [expr 10001+$u] -type -beamUniform 0 20 0
    # }
#-------------  P wave ------------------------- 
    # load 810 0 $p 0
    # load 811 0 $p 0
    # load 812 0 $p 0
    # load 813 0 $p 0
    # load 814 0 $p 0
    # load 815 0 $p 0
    # load 816 0 $p 0
    # load 817 0 $p 0
    for {set u 0} {$u < $nx} {incr u} {
        eleLoad -ele [expr 10001+$u] -type -beamUniform 20 0
    }

}
puts "finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)" 

# print -node 10201
# print -ele 10000
# ---------- Left B.C (ele 1,5001,9901 / node 1,5051 10101) -----------------------
recorder Element -file "extend_soil/stress/10m_soil/ele1_stress_Side_P.out" -time -ele 1 material 1 stress
recorder Element -file "extend_soil/stress/10m_soil/ele5001_stress_Side_P.out" -time -ele 5001 material 1 stress
recorder Element -file "extend_soil/stress/10m_soil/ele9901_stress_Side_P.out" -time -ele 9901 material 1 stress

recorder Node -file "extend_soil/velocity/10m_soil/node1_vel_Side_P.out" -time -node 1 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/10m_soil/node5051_vel_Side_P.out" -time -node 5051 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/10m_soil/node10101_vel_Side_P.out" -time -node 10101 -dof 1 2 3 vel;

#---------- Right B.C (ele 100,5100,10000 / node 101,5151 10201)-----------------------
recorder Element -file "extend_soil/stress/10m_soil/ele100_stress_Side_P.out" -time -ele 100 material 1 stress
recorder Element -file "extend_soil/stress/10m_soil/ele5100_stress_Side_P.out" -time -ele 5100 material 1 stress
recorder Element -file "extend_soil/stress/10m_soil/ele10000_stress_Side_P.out" -time -ele 10000 material 1 stress

recorder Node -file "extend_soil/velocity/10m_soil/node101_vel_Side_P.out" -time -node 101 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/10m_soil/node5151_vel_Side_P.out" -time -node 5151 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/10m_soil/node10201_vel_Side_P.out" -time -node 10201 -dof 1 2 3 vel;

#---------- Center Element/Node (ele 51,5051,9951 / node 51,5101,10151) -----------------------
recorder Element -file "extend_soil/stress/10m_soil/ele51_stress_Side_P.out" -time -ele 51 material 1 stress
recorder Element -file "extend_soil/stress/10m_soil/ele5051_stress_Side_P.out" -time -ele 5051 material 1 stress
recorder Element -file "extend_soil/stress/10m_soil/ele9951_stress_Side_P.out" -time -ele 9951 material 1 stress

recorder Node -file "extend_soil/velocity/10m_soil/node51_vel_Side_P.out" -time -node 51 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/10m_soil/node5101_vel_Side_P.out" -time -node 5101 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/10m_soil/node10151_vel_Side_P.out" -time -node 10151 -dof 1 2 3 vel;

# # # ---------- Structure stress/velocity -----------------------
# # recorder Element -file "extend_soil/stress/Column1_stress.out" -time -ele 611 globalForce
# # recorder Element -file "extend_soil/stress/Column2_stress.out" -time -ele 612 globalForce
# # recorder Element -file "extend_soil/stress/Beam_stress.out" -time -ele 613 globalForce

# # recorder Node -file "extend_soil/velocity/node1030_vel.out" -time -node 1030 -dof 1 2 3 vel;
# # recorder Node -file "extend_soil/velocity/node1031_vel.out" -time -node 1031 -dof 1 2 3 vel;
# # recorder Node -file "extend_soil/velocity/node1032_vel.out" -time -node 1032 -dof 1 2 3 vel;
# # recorder Node -file "extend_soil/velocity/node1033_vel.out" -time -node 1033 -dof 1 2 3 vel;

# # ============= recorder MPCO HDF5 ====================
# # recorder mpco "extend_soil/MPCO/allele" -E material.stress force localforce -N velocity ;#
# # recorder mpco "extend_soil/MPCO/Pwave_dahpot" -E material.stress force localforce -N velocity displacement ;#
# # recorder mpco "extend_soil/MPCO/Swave_sideBC" -E material.stress force localforce -N velocity displacement ;#
recorder mpco "extend_soil/MPCO/Pwave_10msideBC" -E material.stress force localforce -N velocity displacement ;#

#dynamic analysis
constraints Transformation
numberer RCM
system UmfPack
test EnergyIncr 1.0e-8 200; #1.0e-6 200
algorithm Newton
integrator Newmark 0.5 0.25
analysis Transient
analyze 8000 0.0001; #total time: 0.8s
puts "finish analyze:0 ~ 0.8s"

# print -ele 701 702 703 704 705 706 707
