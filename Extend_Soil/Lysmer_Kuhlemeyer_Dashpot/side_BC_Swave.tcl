wipe
# ================== Build quad element with block2D ================================
model BasicBuilder -ndm 2 -ndf 2
set nx 5    ;# X-dri elements 
set ny 100  ;# Y-dir elements
set e1 1    ;# from which element start
set n1 1    ;# from which node start  
# ------------------ quad element (node 1~707)-----------------------------------------
#                           $matTag   $E           $v    $rho
nDMaterial ElasticIsotropic  2000    15005714.286  0.3   2020  ;# E:unit -> Pa
block2D $nx $ny $e1 $n1 quad "1 PlaneStrain 2000" {
    1 0   0
    2 0.5 0
    3 0.5 10
    4 0   10 
} 
# print -node 603
# print -ele 500
# ------------------ B.C(left/right equal)--tie side / use dashpot in side ------------------------
set n 100
# for {set i 0} {$i < [expr $n+1]} {incr i} { 
#     #---- Only Left and Right node have same disp x,y----------
#     equalDOF [expr 6*$i+1] [expr 6*$i+6] 1 2
#     #---- much rigorous way to each node have same disp -------
#     # equalDOF [expr 6*$i+1] [expr 6*$i+2] 1 2
#     # equalDOF [expr 6*$i+2] [expr 6*$i+3] 1 2
#     # equalDOF [expr 6*$i+3] [expr 6*$i+4] 1 2
#     # equalDOF [expr 6*$i+4] [expr 6*$i+5] 1 2
#     # equalDOF [expr 6*$i+5] [expr 6*$i+6] 1 2
# }
model BasicBuilder -ndm 2 -ndf 3
for {set r 0} {$r < $n+1} {incr r} {   
# ------------- left side dashpot node (626,627~826,827)/B.C -----------------
    node [expr 626+2*$r] 0.0 [expr 0.1*$r]
    node [expr 627+2*$r] 0.0 [expr 0.1*$r]

    # fix [expr 626+2*$r] 1 0 1  ;# y dir dashpot　
    fix [expr 626+2*$r] 0 1 1  ;# x dir dashpot　
    fix [expr 627+2*$r] 1 1 1
# ------------- right side dashpot node (828,829~1028,1029)/B.C-----------------
    node [expr 828+2*$r] 0.5 [expr 0.1*$r]
    node [expr 829+2*$r] 0.5 [expr 0.1*$r]

    # fix [expr 828+2*$r] 1 0 1  ;# P wave - y dir dashpot　
    fix [expr 828+2*$r] 0 1 1  ;# S wave - x-dir dashpot 
    fix [expr 829+2*$r] 1 1 1
}
# ------ connect dashpot with SOIL Layer :Vs with x dir / Vp with y-dir --------------
for {set r 0} {$r < $n+1} {incr r} {  
# ---------- left side equal (x-dir) ----------------------
    equalDOF [expr 6*$r+1] [expr 626+2*$r] 1
# ---------- right side equal (x-dir)----------------------
    equalDOF [expr 6*$r+6] [expr 828+2*$r] 1
}

# ------ Build lef/right side dashpot element/ Viscous Material -------------------------------
set rho 2020   ;# kg/m3 
set Vp 100     ;# m/s 
set Vs 53.45224838248488     ;# m/s 
set sizeX 0.1  ;# m
set mp  [expr $rho*$Vp*$sizeX]  ;# N (newton)
set ms  [expr $rho*$Vs*$sizeX]  ;# N (newton)

uniaxialMaterial Viscous 4000 $ms 1   ;# S wave
# uniaxialMaterial Viscous 4000 $mp 1 ;# P wave
#----------- side dashpot elements: Vs with x dir / Vp with y-dir------------------
for {set q 0} {$q < $n+1} {incr q} {  
# -------------- right dashpot (ele 5000~5100) -----------------
    element zeroLength [expr 5000+$q] [expr 627+2*$q] [expr 626+2*$q] -mat 4000 -dir 1
# -------------- left dashpot (ele 5101~5201) -----------------
    element zeroLength [expr 5101+$q] [expr 829+2*$q] [expr 828+2*$q] -mat 4000 -dir 1
}

# ================== Build Beam element(node 607~612) ================================
# model BasicBuilder -ndm 2 -ndf 3
for {set j 0} {$j < 6} {incr j} {
    node [expr 607+$j] [expr 0.1*$j] 0.0
    fix [expr 607+$j] 0 0 1
}

# ------------------ elastic BeamColumn element ------------------------
set A [expr 0.1*1]
set E1 1e+05;                      # bigger much harder(1e+05) / smaller much softer (1e-06)
set Iz [expr (0.1*0.1*0.1)/12]
geomTransf Linear 1 

element elasticBeamColumn 505 607 608  $A  $E1 $Iz 1 ;# 
element elasticBeamColumn 506 608 609  $A  $E1 $Iz 1 ;# 
element elasticBeamColumn 507 609 610  $A  $E1 $Iz 1 ;# 
element elasticBeamColumn 508 610 611  $A  $E1 $Iz 1 ;# 
element elasticBeamColumn 509 611 612  $A  $E1 $Iz 1 ;# -release 3

#------------ Make Beam elements only Right and Left node have same disp --------------- 
equalDOF 607 612  1 2
#---------- Bottom Beam and Soil connect ------------------------
for {set l 0} {$l < 6} {incr l} {
    equalDOF [expr 607+$l] [expr 1+$l] 1 2
}

# # =================== Build Structure(Portal Frame) ====================================
# model BasicBuilder -ndm 2 -ndf 3
# set g    9.81 ;# m/s2
# set LCol 0.2   ;# Column Length
# set LBeam 0.2  ;# Beam Length
# set Weight 196 ;# MPa
# #-------- Beam / Column Section --------------------
# set HCol 0.01   
# set BCol 0.01
# set HBeam 0.01
# set BBeam 0.01
# #---------------------- calculated parameters ------------------------------------------
# set PCol [expr $Weight/2]; 		# nodal dead-load weight per column
# set Mass [expr $PCol/$g];		# nodal mass = 20 kg
# # set MCol [expr 1./12.*($Weight/$LBeam)*pow($LBeam,2)];	# beam-end moment due to distributed load.
# #--------- calculated geometry parameters ---------------------
# set ACol [expr $BCol*$HCol];					# cross-sectional area
# set ABeam [expr $BBeam*$HBeam];
# set IzCol [expr (1./12.)*$BCol*pow($HCol,3)]; 			# Column moment of inertia
# set IzBeam [expr (1./12.)*$BBeam*pow($HBeam,3)]; 		# Beam moment of inertia
# #---------- Node Coordinates----------------
# node 715 0.2 10.0 ;# 0.2 9.9 (bottom surface)
# node 716 0.4 10.0 ;# 0.4 9.9
# node 717 0.2 10.2 ;# 0.2 10.1
# node 718 0.4 10.2 ;# 0.4 10.1

# #----------- B.C --------------
# fix 715 1 1 1
# fix 716 1 0 1
# fix 717 0 0 0
# fix 718 0 0 0

# mass 715 0 $Mass  0.0
# mass 716 0 $Mass  0.0
# mass 717 0 $Mass  0.0
# mass 718 0 $Mass  0.0

# # define geometric transformation: performs a linear geometric transformation of beam stiffness and resisting force from the basic system to the global-coordinate system
# set ColTransfTag 1; 			# associate a tag to column transformation
# set BeamTransfTag 2 ; #2			# associate a tag to beam transformation (good practice to keep col and beam separate)
# set ColTransfType Linear ;			# options, Linear PDelta Corotational 
# geomTransf $ColTransfType $ColTransfTag ; 	# only columns can have PDelta effects (gravity effects)
# geomTransf Linear $BeamTransfTag; # $BeamTransfTag
# # Define ELEMENTS -------------------------------------------------------------
# # Material parameters (1 ksi = 6.89 MPa)
# set fc 25; 		# CONCRETE Compressive Strength (+Tension, -Compression)
# set Ec [expr 4700*sqrt($fc)]; 	# Concrete Elastic Modulus

# element elasticBeamColumn 611 715 717 $ACol $Ec $IzCol  $ColTransfTag      ;# Column 1
# element elasticBeamColumn 612 716 718 $ACol $Ec $IzCol  $ColTransfTag      ;# Column 2
# element elasticBeamColumn 613 717 718 $ABeam $Ec $IzBeam  $BeamTransfTag   ;# Beam 3

# # ======== EqualDOF Structure connect Soil ===================================
# equalDOF 696 715 1 2
# equalDOF 698 716 1 2

#=============== Apply Dashpot at the bot to absorb the wave form the top ================
# --- node 613.614 to 623.624 have the same coordinate -----
for {set q 0} {$q < 6} {incr q} {   
    node [expr 613+2*$q] [expr 0.1*$q] 0.0
    node [expr 614+2*$q] [expr 0.1*$q] 0.0
}
for {set q 0} {$q < 6} {incr q} {   
    fix [expr 613+2*$q] 0 1 1     ;# use to connect soil (S wave:x free)
    # fix [expr 613+2*$q] 1 0 1       ;# use to connect soil (P wave: y free)
    fix [expr 614+2*$q] 1 1 1       ;# use to build Viscous element   
}
# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
equalDOF 607 613 1
equalDOF 608 615 1
equalDOF 609 617 1
equalDOF 610 619 1
equalDOF 611 621 1
equalDOF 612 623 1

# equalDOF 607 613 2
# equalDOF 608 615 2
# equalDOF 609 617 2
# equalDOF 610 619 2
# equalDOF 611 621 2
# equalDOF 612 623 2

puts "Finished creating all dashpot boundary conditions and equalDOF..."
# ------ Build dashpot element/ Viscous Material -------------------------------
# set rho 2020   ;# kg/m3 
# set Vp 100     ;# m/s 
# set Vs 53.45224838248488     ;# m/s 
# set sizeX 0.1  ;# m
# set mp  [expr $rho*$Vp*$sizeX]  ;# N (newton)
# set ms  [expr $rho*$Vs*$sizeX]  ;# N (newton)

# uniaxialMaterial Viscous 4000 $mp 1 ;# P wave
# uniaxialMaterial Viscous 4000 $ms 1   ;# S wave
#----------- dashpot elements: Vs with x dir / Vp with y-dir------------------
element zeroLength 5202 614 613 -mat 4000 -dir 1
element zeroLength 5203 616 615 -mat 4000 -dir 1
element zeroLength 5204 618 617 -mat 4000 -dir 1
element zeroLength 5205 620 619 -mat 4000 -dir 1
element zeroLength 5206 622 621 -mat 4000 -dir 1
element zeroLength 5207 624 623 -mat 4000 -dir 1

# element zeroLength 5202 614 613 -mat 4000 -dir 2
# element zeroLength 5203 616 615 -mat 4000 -dir 2
# element zeroLength 5204 618 617 -mat 4000 -dir 2
# element zeroLength 5205 620 619 -mat 4000 -dir 2
# element zeroLength 5206 622 621 -mat 4000 -dir 2
# element zeroLength 5207 624 623 -mat 4000 -dir 2

puts "Finished creating dashpot material and element..."

# ----------given input force (node 1,2) and "Bottom Stress B.C"---------------------#
set filePath fs.txt   ;# fp.txt/ fs.txt
timeSeries Path 702 -dt 0.0001 -filePath $filePath;                                     #10(m)/100=0.1(s); 0.1/100 cell=0.001(s); 0.001/10 steps=0.0001(s)
set p [expr (2.0/6.0)]
set Stress 20.0

pattern Plain 703 702 {
#-------------  S wave -------------------------
    # load 607 $p 0 0
    # load 608 $p 0 0
    # load 609 $p 0 0
    # load 610 $p 0 0
    # load 611 $p 0 0
    # load 612 $p 0 0
    eleLoad -ele 505 -type -beamUniform 0 [expr ($Stress/5.0)] 0
    eleLoad -ele 506 -type -beamUniform 0 [expr ($Stress/5.0)] 0
    eleLoad -ele 507 -type -beamUniform 0 [expr ($Stress/5.0)] 0
    eleLoad -ele 508 -type -beamUniform 0 [expr ($Stress/5.0)] 0
    eleLoad -ele 509 -type -beamUniform 0 [expr ($Stress/5.0)] 0

#-------------  P wave ------------------------- 
    # load 607 0 $p 0
    # load 608 0 $p 0
    # load 609 0 $p 0
    # load 610 0 $p 0
    # load 611 0 $p 0
    # load 612 0 $p 0
    # eleLoad -ele 505 -type -beamUniform [expr ($Stress/5.0)] 0
    # eleLoad -ele 506 -type -beamUniform [expr ($Stress/5.0)] 0
    # eleLoad -ele 507 -type -beamUniform [expr ($Stress/5.0)] 0
    # eleLoad -ele 508 -type -beamUniform [expr ($Stress/5.0)] 0
    # eleLoad -ele 509 -type -beamUniform [expr ($Stress/5.0)] 0
}
puts "finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)" 

# file mkdir extend_soil;
# file mkdir extend_soil/velocity
# file mkdir extend_soil/stress

#---------- Left B.C -----------------------
recorder Element -file "extend_soil/stress/ele1_stress.out" -time -ele 1 material 1 stress
recorder Element -file "extend_soil/stress/ele251_stress.out" -time -ele 251 material 1 stress
recorder Element -file "extend_soil/stress/ele496_stress.out" -time -ele 496 material 1 stress

recorder Node -file "extend_soil/velocity/node1_vel.out" -time -node 1 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node301_vel.out" -time -node 301 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node601_vel.out" -time -node 601 -dof 1 2 3 vel;

#---------- Right B.C -----------------------
recorder Element -file "extend_soil/stress/ele5_stress.out" -time -ele 5 material 1 stress
recorder Element -file "extend_soil/stress/ele255_stress.out" -time -ele 255 material 1 stress
recorder Element -file "extend_soil/stress/ele500_stress.out" -time -ele 500 material 1 stress

recorder Node -file "extend_soil/velocity/node6_vel.out" -time -node 3 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node306_vel.out" -time -node 306 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node606_vel.out" -time -node 606 -dof 1 2 3 vel;

#---------- Center Element/Node -----------------------
recorder Element -file "extend_soil/stress/ele3_stress.out" -time -ele 3 material 1 stress
recorder Element -file "extend_soil/stress/ele253_stress.out" -time -ele 253 material 1 stress
recorder Element -file "extend_soil/stress/ele498_stress.out" -time -ele 498 material 1 stress

recorder Node -file "extend_soil/velocity/node3_vel.out" -time -node 3 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node303_vel.out" -time -node 303 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node603_vel.out" -time -node 603 -dof 1 2 3 vel;

# # ---------- Structure stress/velocity -----------------------
# # recorder Element -file "extend_soil/stress/Column1_stress.out" -time -ele 611 globalForce
# # recorder Element -file "extend_soil/stress/Column2_stress.out" -time -ele 612 globalForce
# # recorder Element -file "extend_soil/stress/Beam_stress.out" -time -ele 613 globalForce

# # recorder Node -file "extend_soil/velocity/node715_vel.out" -time -node 715 -dof 1 2 3 vel;
# # recorder Node -file "extend_soil/velocity/node716_vel.out" -time -node 716 -dof 1 2 3 vel;
# # recorder Node -file "extend_soil/velocity/node717_vel.out" -time -node 717 -dof 1 2 3 vel;
# # recorder Node -file "extend_soil/velocity/node718_vel.out" -time -node 718 -dof 1 2 3 vel;

# ============= recorder MPCO HDF5 ====================
# recorder mpco "extend_soil/MPCO/allele" -E material.stress force localforce -N velocity ;#
# recorder mpco "extend_soil/MPCO/Pwave_block2D" -E material.stress force localforce -N velocity displacement ;#

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
