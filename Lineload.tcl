#quad element and Beam element
wipe
set b [expr 10.0/100.0]; #0.1
set n 100
#================================= build quad element ======================
model BasicBuilder -ndm 2 -ndf 2
for { set i 0} {$i <[expr $n+1]} {incr i} { ;
    #       id         x    y 
    node [expr 2*$i+1] 0.0  [expr $i*$b]; # 1.3.5.7-201
    node [expr 2*$i+2] $b [expr $i*$b]; # 2.4.6.8-202
    # fix [expr 2*$i+1] 1 0
    # fix [expr 2*$i+2] 1 0
}
#------------------ Boundary Condition ----------------------
fix 1 1 0
fix 2 1 0


for {set i 1} {$i < [expr $n+1]} {incr i} {
    equalDOF [expr 2*$i+1] [expr 2*$i+2] 1 2
}
#------------------ quad element (element 1-100)----------------------------
#                           $matTag   $E          $v    $rho
nDMaterial ElasticIsotropic  2000   15005714.286  0.3   2020    ;# E ->(n/m2) = Pa
for { set a 0} {$a < $n} {incr a} {
    #                eletag                i              j             k           l                         
    element quad [expr $a+1]     [expr 2*$a+1] [expr 2*$a+2] [expr 2*$a+4] [expr 2*$a+3] 1 "PlaneStress" 2000   
}
#========================= Build elastic BeamColumn element =======================
model BasicBuilder -ndm 2 -ndf 3
set L 1
set c [expr 0.1/$L] 
node 203 0.0 0.0
node 204 0.1 0.0

#------------------ Boundary Condition ----------------------
fix 203 1 0 1
fix 204 1 0 1

# mass 203 0 1 0
# mass 204 0 1 0
#------------------ elastic BeamColumn element ---------------------------
set A [expr 0.1*1]
set E1 1e+05;# bigger much harder / smaller much softer
set Iz [expr (0.1*0.1*0.1)/12]
geomTransf Linear 1
#                        eleTag   i   j
element elasticBeamColumn 105    203 204  $A  $E1 $Iz 1 -release 3
# element elasticBeamColumn 106    204 205  $A  $E1 $Iz 1
# element elasticBeamColumn 107    205 206  $A  $E1 $Iz 1
# element elasticBeamColumn 108    206 207  $A  $E1 $Iz 1
# element elasticBeamColumn 109    207 208  $A  $E1 $Iz 1
# for {set j 0} {$j < $L} {incr j} {
#     element elasticBeamColumn [expr 105+$j] [expr 203+$j] [expr 204+$j] $A  $E1 $Iz 1
# }


# equalDOF 1 203 2
# equalDOF 2 204 2

equalDOF 203 1  2
equalDOF 204 2  2
#=================== Use EqualDOF to connect slave node and quad element ==========================
# node 205  0.0 0.0
# node 206  0.1 0.0

# mass 205 0 1 0
# mass 206 0 1 0

# fix 205 0 0 1
# fix 206 0 0 1
#  impose "slave" dof to be the same as those of "Master" node
#  equalDOF: constraints the slave DOFs to be equal to the respective master DOFs.(slave follow master)
#       m(r) s(c)   
# equalDOF 205 1 1 2   ; #constrained slave
# equalDOF 206 2 1 2
# equalDOF 1 205 1 2   ; #constrained slave
# equalDOF 2 206 1 2
puts "Slave Nodes (3DOF Domain) at Soil-beam Interface generated"
#================= CREATE ZERO LENGTH SPRING MATERIAL ==============================
set E2 1e-05
uniaxialMaterial Elastic 401 $E2
#================= ZERO LENGTH SPRING Connect to slave nodes ==============================
#                     i(m) j(s)      
# element zeroLength 106 205 203 -mat 401 401 -dir 1 2
# element zeroLength 107 206 204 -mat 401 401 -dir 1 2
#================= Applt eleLoad(Line load) to the beam element ========================================
# set wya 10
# set wxa 0
# set aOverL 0
# set bOverL 1
# set wyb 0
# set wxb 0.1

set filePath u1.txt
timeSeries Path 705 -dt 1e-4 -filePath $filePath;  
pattern Plain 706 705 {
    # load 1 0 1 
    # load 2 0 1
    # for {set g 0} {$g < $L} {incr g} {
    #     eleLoad -ele [expr 105+$g] -type -beamUniform 20 0 0
    # }
    eleLoad -ele 105 -type -beamUniform 20 0  0
    # eleLoad -ele 106 -type -beamUniform 20 0  0
    # eleLoad -ele 107 -type -beamUniform 20 0  0
    # eleLoad -ele 108 -type -beamUniform 20 0  0
    # eleLoad -ele 109 -type -beamUniform 20 0  0
    # eleLoad -ele 105 -type -beamUniform $wya $wxa $aOverL $bOverL $wyb $wxb ;# Trapezoidal Beam Loads
}
puts "eleLoad had been add"
#====================== Recorder ========================
recorder Node -file "surfaceload/output/disp1.out" -time -node 1 -dof 1 2 3 disp;    #
recorder Node -file "surfaceload/output/disp101.out" -time -node 101 -dof 1 2 3 disp; 
recorder Node -file "surfaceload/output/disp201.out" -time -node 201 -dof 1 2 3 disp; 
recorder Node -file "surfaceload/output/disp203.out" -time -node 203 -dof 1 2 3 disp;    

recorder Node -file "surfaceload/output/vel1.out" -time -node 1 -dof 1 2 3 vel;
recorder Node -file "surfaceload/output/vel101.out" -time -node 101 -dof 1 2 3 vel;
recorder Node -file "surfaceload/output/vel201.out" -time -node 201 -dof 1 2 3 vel;
recorder Node -file "surfaceload/output/vel203.out" -time -node 203 -dof 1 2 3 vel;

recorder Element -file "surfaceload/output/ele1_stress.out" -time -ele 105 localForce;#globalForce
recorder Element -file "surfaceload/output/quad_stress1.out" -time -ele 1 material 1 stress
recorder Element -file "surfaceload/output/quad_stress50.out" -time -ele 50 material 1 stress
recorder Element -file "surfaceload/output/quad_stress100.out" -time -ele 100 material 1 stress
puts "Recorder ok"
#======== dynamic analysis ==================
constraints Transformation
numberer RCM
system UmfPack
test EnergyIncr 1.0e-6 200; #1.0e-6
algorithm Newton
integrator Newmark 0.5 0.25;  # LoadControl 0.01/Newmark 0.5 0.25
analysis Transient  ;  # Static/Transient
analyze 8000 0.0001; #total time: 0.8s
puts "finish analyze:0 ~ 0.8s"
