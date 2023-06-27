wipe
#unit : m , kg
model BasicBuilder -ndm 2 -ndf 2

# build node
set b [expr 10.0/100.0]; #0.1
set n 100
for { set i 0} {$i <[expr $n+1]} {incr i} { ;#{$i <[expr $n+1]}
    #       id         x    y 
    node [expr 2*$i+1] 0  [expr $i*$b]; # 1.3.5.7-201
    node [expr 2*$i+2] $b [expr $i*$b]; # 2.4.6.8-202

    # equalDOF  [expr 2*$i+1] [expr 2*$i+2] 2; ####
    # puts "$i, [expr 2*$i+1], 0, [expr $i*$b]"
    # puts "$i, [expr 2*$i+2], $b, [expr $i*$b]"
}

#--------Control fix/free B.C----------------------#
# for { set i 1} {$i <[expr $n]} {incr i} {; #node 3~200
#     fix [expr 2*$i+1] 1 0;
#     fix [expr 2*$i+2] 1 0;
# }
for {set i 1} {$i <[expr $n+1]} {incr i} {      ;#node 3~202 same Disp
    equalDOF  [expr 2*$i+1] [expr 2*$i+2] 1 2;
}
fix 1   1 0 
fix 2   1 0
# fix 201 1 0
# fix 202 1 0  

#100:10%, 50:11%, 200:7%, 400:3%, 500:0.9%, 600:0.989%, 700:2%  
#                           $matTag   $E           $v    $rho
nDMaterial ElasticIsotropic  2000    15005714.286  0.3   2020    ;  #1600,vp =100, vs=53.452 ,E=11885714.286, G=4571428.571 n/m2, rho= 1600 kg/m3=1.6 ton/m3
for { set a 0} {$a < $n} {incr a} {
    #                eletag                i              j             k           l                         
    element quad [expr $a+1]     [expr 2*$a+1] [expr 2*$a+2] [expr 2*$a+4] [expr 2*$a+3] 1 "PlaneStrain" 2000   
}

# ----------given input force (node 1,2) and "Bottom Stress B.C"---------------------#
set filePath fp.txt
timeSeries Path 702 -dt 0.0001 -filePath $filePath;                                     #10(m)/100=0.1(s); 0.1/100 cell=0.001(s); 0.001/10 steps=0.0001(s)

pattern Plain 703 702 {
    load 1 0 1; # like "normal vector direction"
    load 2 0 1; # 2
}
puts "finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)" 

#----------Input stress boundary(node 201,202)------------# (if Stress B.C apply in Node 201,202(Top), we have to seperate the u1.txt file)
# set filePath2 u201.txt
# timeSeries Path 704 -dt 0.0001 -filePath $filePath2;
# pattern Plain 705 704 {
#     load 201 0 -1; 
#     load 202 0 -1; 
# }
# puts "finish Reaction Force File:0.1 ~ 0.2s "


# #----------Use velocity timeseries to make wave transport and Input velocity boundary(node 1,2)------------#
# # MultipleSupport SineWave ground motion (different velocity input at spec'd support nodes) -- two nodes here
# set iSupportNode "1 2";			# support nodes where ground motions are input, for multiple-support excitation
# set iGMdirection "2 2";			# ground-motion direction  -- for each support node
# #---------------------------------    perform Dynamic Ground-Motion Analysis------------#
# set filePath2 disp.txt;                                   #v1.txt
# set dt 1e-5;                                            #1e-4
# timeSeries Path 704 -dt $dt -filePath $filePath2; #1e-4

# # the following commands are unique to the Multiple-Support Earthquake excitation
# set IDloadTag 705;	
# set IDgmSeries 706;	    # for multipleSupport Excitation
# set DtGround $dt;	# time-step Dt for input grond motion 0.0001
# # multiple-support excitation: velocity input at individual nodes
# pattern MultipleSupport $IDloadTag  {
# 	foreach SupportNode $iSupportNode GMdirection $iGMdirection {
# 		set IDgmSeries [expr $IDgmSeries +1]

# 		groundMotion $IDgmSeries Plain -disp 704 -int Simpson; #Simpson/Trapezoidal
# 	     	imposedMotion $SupportNode  $GMdirection $IDgmSeries
# 	};	# end foreach	
# };	# end pattern
# puts "finish velocity File:0.0 ~ 0.1s; Velocity B.C:0.2s~0.3s"
#---------------------------------------------------------#

# set eigenvalues [eigen generalized 101]; #generalized
# puts $eigenvalues

#-------------zerolength to input reaction force(for stress boundary condition)--------------------#
# set filePath u1boundary.txt
# timeSeries Path 705 -dt 0.001 -filePath $filePath; #0.0001

# pattern Plain 704 705 {
#     load 203 0 1; # 1
#     load 204 0 1; # 2
# }
# puts "finish Input boundary File "

#-----------recorder---------------------
file mkdir output;
file mkdir output/velocity
file mkdir output/stress

recorder Node -file "output/node_disp1.out" -time -node 1 -dof 1 2 3 disp;
recorder Node -file "output/node_disp101.out" -time -node 101 -dof 1 2 3 disp;
recorder Node -file "output/node_disp201.out" -time -node 201 -dof 1 2 3 disp;

# ###########Display the model (show the video)################
# recorder display "Model" 10 10 1000 1000 -wipe
#     prp 0 0 50;  #horizon
#     vup 0 1 0;   #screen top
#     vpn -1 0 1;  #normal 
#     display 1 5 1; 

recorder Node -file "output/compare/velocity/node_vel1_Reactionforce.out" -time -node 1 -dof 1 2 3 vel;
# recorder Node -file "output/velocity/node_vel21.out" -time -node 21 -dof 1 2 3 vel;
recorder Node -file "output/compare/velocity/node_vel101_Reactionforce.out" -time -node 101 -dof 1 2 3 vel;
recorder Node -file "output/compare/velocity/node_vel201_Reactionforce.out" -time -node 201 -dof 1 2 3 vel;
#                                                                          Gauss points(for 4-node quads it can be 1 to 4)    
recorder Element -file "output/compare/stress/ele1_stress_Reactionforce.out" -time -ele 1 material 1 stress
# recorder Element -file "output/stress/ele10_stress.out" -time -ele 10 material 1 stress
recorder Element -file "output/compare/stress/ele50_stress_Reactionforce.out" -time -ele 50 material 1 stress
recorder Element -file "output/compare/stress/ele100_stress_Reactionforce.out" -time -ele 100 material 1 stress


# recorder Element -file "output/stress/ele1_stiff.out" -time -ele 1 stiffness
# recorder Node -file "output/eigen/nodeeigen_nomass.out" -time -dof 1 2 3 "eigen 101";#-node 101
# recorder Node -file "output/node_acc1.out" -time -node 1 -dof 1 2 3 accel;
# recorder Node -file "output/node_acc2.out" -time -node 2 -dof 1 2 3 accel;
#-----------recorder---------------------

#dynamic analysis
constraints Transformation
numberer RCM
system UmfPack
test EnergyIncr 1.0e-8 200; #1.0e-6
algorithm Newton
integrator Newmark 0.5 0.25
analysis Transient
analyze 8000 0.0001; #total time: 0.8s
puts "finish analyze:0 ~ 0.8s"



# puts [eigen -fullGenLapack 1]; #lambda = 100 , k=200 , wn =10 
# set lambda  [eigen 1]
# puts $lambda


