# Configred for seamless run on UM-ARC (Great Lakes)

################################
##### General options
################################

ATOM_TYPES     = ["C"]
NO_CASES       = 1
USE_AL_STRS    = -1 # Do not fit stresses

DRIVER_DIR     = "/home/rklinds/codes/al_driver-myLLfork"
WORKING_DIR    = DRIVER_DIR + "/examples/simple_iter_single_statepoint-lmpwlmp/"
CHIMES_SRCDIR  = "/home/rklinds/codes/chimes_lsq-myLLfork/src/"

################################
#### HPC Settings
################################

HPC_ACCOUNT = "rklinds1"
HPC_PYTHON  = "/sw/pkgs/arc/python3.9-anaconda/2021.11/bin/python"

################################
##### ChIMES LSQ
################################

ALC0_FILES    = WORKING_DIR + "ALL_BASE_FILES/ALC-0_BASEFILES/"
CHIMES_LSQ    = CHIMES_SRCDIR + "../build/chimes_lsq"
CHIMES_SOLVER = CHIMES_SRCDIR + "../build/chimes_lsq.py"
CHIMES_POSTPRC= CHIMES_SRCDIR + "../build/post_proc_chimes_lsq.py"
CHIMES_MODULES= "intel/2022.1.2 impi/2021.5.1 mkl/2022.0.2 python3.9-anaconda/2021.11"

N_HYPER_SETS  = 1 # Number of unique fm_setup.in files; allows fitting, e.g., multiple overlapping models to the same data

WEIGHTS_FORCE =   [["A","B"],[[1.0],[1.0,-1.0]]] 

REGRESS_ALG   = "dlasso"
REGRESS_VAR   = "1.0E-5"
REGRESS_NRM   = True

# Job submitting settings (avoid defaults because they will lead to long queue times)

CHIMES_BUILD_NODES = 1
CHIMES_BUILD_QUEUE = "standard"
CHIMES_BUILD_TIME  = "01:00:00"

CHIMES_SOLVE_NODES = 1
CHIMES_SOLVE_QUEUE = "standard"
CHIMES_SOLVE_TIME  = "01:00:00"
CHIMES_LSQ_MODULES = CHIMES_MODULES

################################
##### Molecular Dynamics
################################

MD_STYLE          = "LMP"
MD_QUEUE          = ["standard"]*NO_CASES
MD_TIME           = ["00:03:00"]*NO_CASES
MD_NODES          = ["1"]      * NO_CASES
MD_FILES          = WORKING_DIR + "/ALL_BASE_FILES/LMPMD_BASEFILES/"
MD_MPI            = "/home/rklinds/codes/chimes_calculator-myLLfork/etc/lmp/exe/lmp_mpi_chimes"
MD_SER            = None # Part of ChIMES cluster entropy active learning - not used with LAMMPS as a driver or reference method
MD_MODULES        = "cmake/3.22.2  intel/18.0.5 impi/2018.4.274"
MOLANAL           = CHIMES_SRCDIR + "../contrib/molanal/src/"
MOLANAL_SPECIES   = ["C"]

################################
##### Single-Point QM (or other reference method)
################################

BULK_QM_METHOD = "LMP"
IGAS_QM_METHOD = "LMP" # Must be defined, even if unused
QM_FILES       = WORKING_DIR + "ALL_BASE_FILES/LMP_BASEFILES"

LMP_EXE      = "/home/rklinds/codes/chimes_calculator-myLLfork/etc/lmp/build/lammps_stable_29Oct2020/src/lmp_mpi_chimes" # Has class2 compiled in it
LMP_UNITS    = "REAL"
LMP_TIME     = "00:10:00"
LMP_NODES    = 1
LMP_PPN      = 1
LMP_MEM      = 128 
LMP_QUEUE    = "standard"
LMP_MODULES  = "intel/2022.1.2 impi/2021.5.1 mkl/2022.0.2"

