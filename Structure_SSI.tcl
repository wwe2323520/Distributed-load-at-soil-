wipe
model BasicBuilder -ndm 2 -ndf 3
# ---------- set unit : m ; MPa ---------------------------- 
# file mkdir extend_soil;
# file mkdir extend_soil/Structure/Stress
# file mkdir extend_soil/Structure/velocity 
# ======================= Build Portal Frame(2D) ==================================== #
# 1 ft = 0.3048 m 
set g    9.81 ;# m/s2
set LCol 0.3
set LBeam 0.2
set Weight 196.2 ;# MPa
set HCol 0.1
set BCol 0.1
set HBeam 0.1
set BBeam 0.1
#---------------------- calculated parameters ------------------------------------------
set PCol [expr $Weight/2]; 		# nodal dead-load weight per column
set Mass [expr $PCol/$g];		# nodal mass = 20 
set MCol [expr 1./12.*($Weight/$LBeam)*pow($LBeam,2)];	# beam-end moment due to distributed load.
# calculated geometry parameters
set ACol [expr $BCol*$HCol];					# cross-sectional area
set ABeam [expr $BBeam*$HBeam];
set IzCol [expr 1./12.*$BCol*pow($HCol,3)]; 			# Column moment of inertia
set IzBeam [expr 1./12.*$BBeam*pow($HBeam,3)]; 		# Beam moment of inertia
#---------- Node Coordinates----------------
node 1 0 0
node 2 $LBeam 0
node 3 0 $LCol
node 4 $LBeam $LCol
#----------- B.C --------------
fix 1 1 1 0
fix 2 1 1 0
fix 3 0 0 0
fix 4 0 0 0

mass 3 $Mass 0.0  0.0
mass 4 $Mass 0.0  0.0
# define geometric transformation: performs a linear geometric transformation of beam stiffness and resisting force from the basic system to the global-coordinate system
set ColTransfTag 1; 			# associate a tag to column transformation
set BeamTransfTag 2; 			# associate a tag to beam transformation (good practice to keep col and beam separate)
set ColTransfType Linear ;			# options, Linear PDelta Corotational 
geomTransf $ColTransfType $ColTransfTag ; 	# only columns can have PDelta effects (gravity effects)
geomTransf Linear $BeamTransfTag  ; 	
# Define ELEMENTS -------------------------------------------------------------
# Material parameters (1 ksi = 6.89 MPa)/ 
set ksi 1
set psi [expr $ksi/1000.]; # 1 ksi = 1000 psi

set fc [expr -4.*$ksi]; 		# CONCRETE Compressive Strength (+Tension, -Compression)
set Ec [expr 57*$ksi*sqrt(-$fc/$psi)]; 	# Concrete Elastic Modulus

element elasticBeamColumn 1 1 3 $ACol $Ec $IzCol  $ColTransfTag
element elasticBeamColumn 2 2 4 $ACol $Ec $IzCol  $ColTransfTag
element elasticBeamColumn 3 3 4 $ABeam $Ec $IzBeam  $BeamTransfTag

# Define RECORDERS -------------------------------------------------------------
recorder Node -file "extend_soil/Structure/DFree.out" -time -node 3 4 -dof 1 2 3 disp;		# displacements of free nodes
recorder Node -file "extend_soil/Structure/DBase.out" -time -node 1 2 -dof 1 2 3 disp;		# displacements of support nodes
recorder Node -file "extend_soil/Structure/RBase.out" -time -node 1 2 -dof 1 2 3 reaction;		# support reaction
recorder Drift -file "extend_soil/Structure/Drift.out" -time -iNode 1 2 -jNode 3 4 -dof 1   -perpDirn 2 ;	# lateral drift
recorder Element -file "extend_soil/Structure/FCol.out" -time -ele 1 2 globalForce;			# element forces -- column
recorder Element -file "extend_soil/Structure/FBeam.out" -time -ele 3 globalForce;	

# define GRAVITY -------------------------------------------------------------
# set WzBeam [expr $Weight/$LBeam];
# pattern Plain 1 Linear {
#    eleLoad -ele 3 -type -beamUniform -$WzBeam ; # distributed superstructure-weight on beam
# }
# # ------------------------------------------------- apply gravity load
# set Tol 1.0e-8;			# convergence tolerance for test
# constraints Plain;     		# how it handles boundary conditions
# numberer Plain;			# renumber dof's to minimize band-width (optimization), if you want to
# system BandGeneral;		# how to store and solve the system of equations in the analysis
# test NormDispIncr $Tol 6 ; 		# determine if convergence has been achieved at the end of an iteration step
# algorithm Newton;			# use Newton's solution algorithm: updates tangent stiffness at every iteration
# set NstepGravity 10;  		# apply gravity in 10 steps
# set DGravity [expr 1./$NstepGravity]; 	# first load increment;
# integrator LoadControl $DGravity;	# determine the next time step for an analysis
# analysis Static;			# define type of analysis static or transient
# analyze $NstepGravity;		# apply gravity
# ------------------------------------------------- maintain constant gravity loads and reset time to zero
loadConst -time 0.0

puts "Model Built"

#============ Dynamic.sine.wave Input ================================
# set filePath fp.txt   ;#fp.txt
# timeSeries Path 702 -dt 0.0001 -filePath $filePath;                                     #10(m)/100=0.1(s); 0.1/100 cell=0.001(s); 0.001/10 steps=0.0001(s)
# pattern Plain 703 702 {
#    load  3  0 -1 0
# }

# #dynamic analysis
# constraints Transformation
# numberer RCM
# system UmfPack
# test EnergyIncr 1.0e-8 200; #1.0e-6 200
# algorithm Newton
# integrator Newmark 0.5 0.25
# analysis Transient
# analyze 8000 0.0001; #total time: 0.8s
# puts "finish analyze:0 ~ 0.8s"
