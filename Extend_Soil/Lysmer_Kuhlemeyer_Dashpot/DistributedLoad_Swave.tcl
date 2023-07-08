wipe
# ================== Build quad element with block2D ================================
model BasicBuilder -ndm 2 -ndf 2
set nx 6    ;# X-dri elements 
set ny 100  ;# Y-dir elements
set e1 1    ;# from which element start
set n1 1    ;# from which node start  
# ------------------ quad element (node 1~707)-----------------------------------------
#                           $matTag   $E           $v    $rho
nDMaterial ElasticIsotropic  2000    15005714.286  0.3   2020  ;# E:unit -> Pa
block2D $nx $ny $e1 $n1 quad "1 PlaneStrain 2000" {
    1 0   0
    2 0.6 0
    3 0.6 10
    4 0   10 
} 
# print -node 358
# ------------------ B.C(left/right equal); (free inside) ------------------------
set n 100
for {set i 0} {$i < [expr $n+1]} {incr i} { 
    #---- Only Left and Right node have same disp x,y----------
    equalDOF [expr 7*$i+1] [expr 7*$i+7] 1 2

    #---- much rigorous way to each node have same disp -------
    # equalDOF [expr 7*$i+1] [expr 7*$i+2] 1 2
    # equalDOF [expr 7*$i+2] [expr 7*$i+3] 1 2
    # equalDOF [expr 7*$i+3] [expr 7*$i+4] 1 2
    # equalDOF [expr 7*$i+4] [expr 7*$i+5] 1 2
    # equalDOF [expr 7*$i+5] [expr 7*$i+6] 1 2
    # equalDOF [expr 7*$i+6] [expr 7*$i+7] 1 2
}

# ================== Build Beam element(node 708~714) ================================
model BasicBuilder -ndm 2 -ndf 3
for {set j 0} {$j < 7} {incr j} {
    node [expr 708+$j] [expr 0.1*$j] 0.0
}
# ------------------ elastic BeamColumn element ------------------------
set A [expr 0.1*1]
set E1 1e+05;                      # bigger much harder(1e+05) / smaller much softer (1e-06)
set Iz [expr (0.1*0.1*0.1)/12]
geomTransf Linear 1

element elasticBeamColumn 605 708 709  $A  $E1 $Iz 1 ;# -release 3
element elasticBeamColumn 606 709 710  $A  $E1 $Iz 1 ;# 
element elasticBeamColumn 607 710 711  $A  $E1 $Iz 1 ;# 
element elasticBeamColumn 608 711 712  $A  $E1 $Iz 1 ;# 
element elasticBeamColumn 609 712 713  $A  $E1 $Iz 1 ;# 
element elasticBeamColumn 610 713 714  $A  $E1 $Iz 1 ;# -release 3

#------------ Make Beam element only Right and Left node have same disp --------------- 
equalDOF 708 714 1 2
#---------- Bottom Beam and Soil connect ------------------------
for {set l 0} {$l < 7} {incr l} {
    equalDOF [expr 708+$l] [expr 1+$l] 1 2
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
# --- node 715.716 to 727.728 have the same coordinate -----
for {set q 0} {$q < 7} {incr q} {   
    node [expr 715+2*$q] [expr 0.1*$q] 0.0
    node [expr 716+2*$q] [expr 0.1*$q] 0.0
}
for {set q 0} {$q < 7} {incr q} {   
    fix [expr 715+2*$q] 0 1 1       ;# use to connect soil
    fix [expr 716+2*$q] 1 1 1       ;# use to build Viscous element     
}
# ------ connect dashpot with soil bot layer : Vs with x-dir --------------
equalDOF 708 715 1
equalDOF 709 717 1
equalDOF 710 719 1
equalDOF 711 721 1
equalDOF 712 723 1
equalDOF 713 725 1
equalDOF 714 727 1
puts "Finished creating all dashpot boundary conditions and equalDOF..."
# ------ Build dashpot element/ Viscous Material -------------------------------
set rho 2020   ;# kg/m3 
set Vp 100     ;# m/s 
set Vs 53.45224838248488 ;# m/s
set sizeX 0.1  ;# m

set mp  [expr $rho*$Vp*$sizeX]  ;# N (newton)
set ms  [expr $rho*$Vs*$sizeX]  ;# N (newton)

uniaxialMaterial Viscous 4000 $ms 1
#----------- dashpot elements ------------------
element zeroLength 5000 716 715 -mat 4000 -dir 1
element zeroLength 5001 718 717 -mat 4000 -dir 1
element zeroLength 5002 720 719 -mat 4000 -dir 1
element zeroLength 5003 722 721 -mat 4000 -dir 1
element zeroLength 5004 724 723 -mat 4000 -dir 1
element zeroLength 5005 726 725 -mat 4000 -dir 1
element zeroLength 5006 728 727 -mat 4000 -dir 1

puts "Finished creating dashpot material and element..."

# ----------given input force (node 1,2) and "Bottom Stress B.C"---------------------#
set filePath fs.txt   ;# fp.txt/ fs.txt
timeSeries Path 702 -dt 0.0001 -filePath $filePath;                                     #10(m)/100=0.1(s); 0.1/100 cell=0.001(s); 0.001/10 steps=0.0001(s)
set p [expr (2.0/7.0)]

pattern Plain 703 702 {
#-------------  S wave -------------------------
    # load 708 $p 0 0
    # load 709 $p 0 0
    # load 710 $p 0 0
    # load 711 $p 0 0
    # load 712 $p 0 0
    # load 713 $p 0 0
    # load 714 $p 0 0 
    eleLoad -ele 605 -type -beamUniform 0 [expr (20.0/6.0)] 0
    eleLoad -ele 606 -type -beamUniform 0 [expr (20.0/6.0)] 0
    eleLoad -ele 607 -type -beamUniform 0 [expr (20.0/6.0)] 0
    eleLoad -ele 608 -type -beamUniform 0 [expr (20.0/6.0)] 0
    eleLoad -ele 609 -type -beamUniform 0 [expr (20.0/6.0)] 0
    eleLoad -ele 610 -type -beamUniform 0 [expr (20.0/6.0)] 0
#-------------  P wave ------------------------- 
    # load 708 0 $p 0
    # load 709 0 $p 0
    # load 710 0 $p 0
    # load 711 0 $p 0
    # load 712 0 $p 0
    # load 713 0 $p 0
    # load 714 0 $p 0 
    # eleLoad -ele 605 -type -beamUniform [expr (20.0/6.0)] 0
    # eleLoad -ele 606 -type -beamUniform [expr (20.0/6.0)] 0
    # eleLoad -ele 607 -type -beamUniform [expr (20.0/6.0)] 0
    # eleLoad -ele 608 -type -beamUniform [expr (20.0/6.0)] 0
    # eleLoad -ele 609 -type -beamUniform [expr (20.0/6.0)] 0
    # eleLoad -ele 610 -type -beamUniform [expr (20.0/6.0)] 0
}
puts "finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)" 

# # file mkdir extend_soil;
# # file mkdir extend_soil/velocity
# # file mkdir extend_soil/stress

#---------- Left B.C -----------------------
recorder Element -file "extend_soil/stress/ele1_stress.out" -time -ele 1 material 1 stress
recorder Element -file "extend_soil/stress/ele301_stress.out" -time -ele 301 material 1 stress
recorder Element -file "extend_soil/stress/ele595_stress.out" -time -ele 595 material 1 stress

recorder Node -file "extend_soil/velocity/node1_vel.out" -time -node 1 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node351_vel.out" -time -node 351 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node701_vel.out" -time -node 701 -dof 1 2 3 vel;

#---------- Right B.C -----------------------
recorder Element -file "extend_soil/stress/ele6_stress.out" -time -ele 6 material 1 stress
recorder Element -file "extend_soil/stress/ele306_stress.out" -time -ele 306 material 1 stress
recorder Element -file "extend_soil/stress/ele600_stress.out" -time -ele 600 material 1 stress

recorder Node -file "extend_soil/velocity/node7_vel.out" -time -node 7 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node357_vel.out" -time -node 357 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node707_vel.out" -time -node 707 -dof 1 2 3 vel;

#---------- Center Element/Node -----------------------
recorder Element -file "extend_soil/stress/ele3_stress.out" -time -ele 3 material 1 stress
recorder Element -file "extend_soil/stress/ele303_stress.out" -time -ele 303 material 1 stress
recorder Element -file "extend_soil/stress/ele597_stress.out" -time -ele 597 material 1 stress

recorder Node -file "extend_soil/velocity/node4_vel.out" -time -node 4 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node354_vel.out" -time -node 354 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node704_vel.out" -time -node 704 -dof 1 2 3 vel;

#---------- Structure stress/velocity -----------------------
# recorder Element -file "extend_soil/stress/Column1_stress.out" -time -ele 611 globalForce
# recorder Element -file "extend_soil/stress/Column2_stress.out" -time -ele 612 globalForce
# recorder Element -file "extend_soil/stress/Beam_stress.out" -time -ele 613 globalForce

# recorder Node -file "extend_soil/velocity/node715_vel.out" -time -node 715 -dof 1 2 3 vel;
# recorder Node -file "extend_soil/velocity/node716_vel.out" -time -node 716 -dof 1 2 3 vel;
# recorder Node -file "extend_soil/velocity/node717_vel.out" -time -node 717 -dof 1 2 3 vel;
# recorder Node -file "extend_soil/velocity/node718_vel.out" -time -node 718 -dof 1 2 3 vel;

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
