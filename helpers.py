# Global (python) modules

from subprocess import check_output 
from subprocess import CalledProcessError
import time
import glob
import sys
import math
import os

""" Small helper functions and utilities general to the ALC process. """

def readlines(infile):

	""" 
	
	A one-liner wrapper to open, readlines, and close a file
	
	Usage: readlines("my_file.txt")
	
	Notes: Outputs a list of lines corresponding to the contents of my_file.txt
	
	WARNING: Entire file is read into memory - do not use with large files
	
	"""
	
	ifstream = open(infile,'r')
	contents = ifstream.readlines()
	ifstream.close()
	
	return contents
	
def writelines(outfile, contents):

	""" 
	
	A one-liner wrapper to open, write all contents of a list, and close a file
	
	Usage: writelines("my_file.txt")
	
	Notes: Make sure lines contain '\n'

	"""	
	
	ofstream = open(outfile,'w')
	
	for line in contents:
		ofstream.write(line)
		
	ofstream.close()


def run_bash_cmnd(cmnd_str):

	""" 
	
	Runs a (bash) shell command - captures and returns any resulting output. 
	
	Usage: run_bash_cmnd("my command string")
	
	Notes: Linux wildcards will not work as expected. Use the glob if needed.
	
	"""

	msg = ""

	try:
		msg = check_output(cmnd_str.split())
	except CalledProcessError as err_msg:
		msg = err_msg.output

	return msg
	
def run_bash_cmnd_presplit(cmnd_str):

	""" 
	
	Runs a (bash) shell command - captures and returns any resulting output. 
	
	Usage: run_bash_cmnd(["my","pre-split", "string"])
	
	Notes: Linux wildcards will not work as expected. Use the glob if needed.
	
	"""

	msg = ""
	
	try:
		msg = check_output(cmnd_str)
	except CalledProcessError as err_msg:
		msg = err_msg.output

	return msg	
	
def run_bash_cmnd_to_file(outfile, cmnd_str):

	""" 
	
	Runs a bash shell command - captures and saves any returned output to file. 
	
	Usage: run_bash_cmnd_to_file("my_outfile_name.dat", "my command string")
	
	Notes: Linux wildcards will not work as expected. Use the glob if needed.
	
	"""
	
	#print cmnd_str
	#print run_bash_cmnd("pwd")
	#print run_bash_cmnd(cmnd_str)
	
	ofstream = open(outfile,'w+')
	ofstream .write(run_bash_cmnd(cmnd_str))
	ofstream .close()
	

	
def cat_to_var(*argv):

	""" 
	
	Concatenates a list of files and returns result. 
	
	Usage: cat_to_var(file1.dat, file2.dat, file3.dat)	
	
	Notes: Linux wildcards will not work as expected. Use the glob if needed.
	
	"""

	files_to_cat = argv # This is a pointer!
	
	contents = []
	
	for f in files_to_cat:
		
		ifstream = open(f,'r')
			
		contents += ifstream.readlines()	
			
		ifstream.close()
		
	return contents
	
	
def cat_specific(outfilename, *argv):

	""" 
	
	Concatenates a list of files and returns result. 
	
	Usage: cat_specific("my_outfile.dat", "file1.dat", "file2.dat", "file3.dat")	
	
	Notes: Linux wildcards will not work as expected. Use the glob if needed.
	
	"""
	
	# Assumes first file is large, so avoids reading contents

	files_to_cat = argv[0][0]

	run_bash_cmnd("cp " + files_to_cat + " " + outfilename)
	
	files_to_cat = argv[0][1:]

	with open(outfilename, "a") as ofstream:
		for f in files_to_cat:
		
			with open(f, "r") as ifstream:
		
				if os.path.getsize(f)/1E9 > 50:

					for line in ifstream:
						ofstream.write(line)
				else:
					ofstream.write(ifstream.read()) # Memory issues with large files

def cat_pattern(outfilename, pattern):

	""" 
	
	Concatenates files matching a linux pattern i.e. *, saves results to file. 
	
	Usage: cat_pattern("my_outfile.txt","*.dat")	
	
	Notes: Linux wildcards WILL work as expected. 
	
	"""

	files_to_cat = sorted(glob.glob(pattern))
	
	with open(outfilename, "wb") as ofstream:

		for f in files_to_cat:

			with open(f, "rb") as ifstream:
				ofstream.write(ifstream.read())
				
def head(*argv):
	
	""" 
	
	Mimics functionality of Linux head command. 
	
	Usage: head("my_file.txt") or head("my_file.txt",2)
	
	Notes: Linux wildcards will not work as expected. Use the glob if needed.
	
	"""	
	
	nlines = 10
	
	if len(argv) == 2:
		nlines = int(argv[1])
	elif len(argv) > 2:
		print "ERROR: Unrecognized head command: ", argv
		exit()
		
	possible = wc_l(argv[0])
	
	if possible < nlines:
		nlines = possible
		
	ifstream = open(argv[0],'r')
	
	contents = []
	
	for i in xrange(nlines):
			contents.append(ifstream.readline())
	
	ifstream.close()
	
	return contents
	
def tail(*argv):
	
	""" 
	
	Mimics functionality of Linux tail command. 
	
	Usage: tail("my_file.txt") or tail("my_file.txt",2)
	
	Notes: Linux wildcards will not work as expected. Use the glob if needed.
	
	"""	
	
	nlines = 10
	
	if len(argv) == 2:
		nlines = int(argv[1])
	elif len(argv) > 2:
		print "ERROR: Unrecognized head command: ", argv
		exit()
	
	total_lines = wc_l(argv[0])
		
	ifstream = open(argv[0],'r')
	
	contents = []
	
	for i in xrange(total_lines):
	
		line = ifstream.readline()
		
		if i >= (total_lines - nlines):
			
			contents.append(line)
	
	ifstream.close()
	
	return contents	
	
def wc_l(infile):

	""" 
	
	Mimics functionality of Linux wc -l command. 
	
	Usage: wc_l("my_file.txt")
	
	Notes: Linux wildcards will not work as expected. Use the glob if needed.
	
	"""	

	nlines = 0
	
	with open(infile, "r") as ifstream:
		for line in ifstream:
			nlines += 1
	return nlines		
	
def count_xyzframes_general(infile):

	""" 
	
	Counts the number of frames in a .xyz(f) file 
	
	Usage: count_xyzframes_general("my_file.txt")
	
	Notes: Linux wildcards will not work as expected. Use the glob if needed.
	
	"""	

	nframes = 0
	
	with open(infile, "r") as ifstream:
		for line in ifstream:
			if len(line.split()) == 1:
				nframes += 1
	return nframes	
	
def list_natoms(infile):

	""" 
	
	Generates a list of the number of atoms in each frames of a .xyz(f) file 
	
	Usage: list_natoms("my_file.txt")
	
	Notes: Linux wildcards will not work as expected. Use the glob if needed.
	
	"""	

	natoms = []
	
	with open(infile, "r") as ifstream:
		for line in ifstream:
			if len(line.split()) == 1:
				natoms.append(int(line[0]))
	return natoms		
	
	
def email_user(base, address, status):

	""" 
	
	Sends a message (status) to the specified email address (address)
	
	Usage: email_user("me@my_domain.com","email message text")
	
	Notes: This uses (requires) linux mailx. Nothing will be sent if
	       address is an empty string. Calls send_email.sh in utilities.

	"""

	if address:

		cmnd = base + "/utilities/send_email.sh " + address + " " + status + " "

		return run_bash_cmnd(cmnd)
		
	
def create_and_launch_job(*argv, **kwargs):

	""" 
	
	Creates and submits a run file to the queuing system.
	
	Usage: create_and_launch_job(<arguments>)
	
	Notes: if "job_executable" is empty, uses the commands specified in *argv.
	       See function definition in helpers.py for a full list of options.
	       Currently, function only supports SLURM systems.
	
	"""	

	################################
	# 0. Set up an argument parser
	################################
	
	default_keys   = [""]*10
	default_values = [""]*10

	# Overall job controls
	
	default_keys[0 ] = "job_name"	       ; default_values[0 ] =	 "ALC-x-lsq-1"		# Name for ChIMES lsq job
	default_keys[1 ] = "job_nodes"         ; default_values[1 ] =	 "2"			# Number of nodes for ChIMES lsq job
	default_keys[2 ] = "job_ppn"	       ; default_values[2 ] =	 "36"			# Number of processors per node for ChIMES lsq job
	default_keys[3 ] = "job_walltime"      ; default_values[3 ] =	 "1"			# Walltime in hours for ChIMES lsq job
	default_keys[4 ] = "job_queue"         ; default_values[4 ] =	 "pdebug"		# Queue for ChIMES lsq job
	default_keys[5 ] = "job_account"       ; default_values[5 ] =	 "pbronze"		# Account for ChIMES lsq job
	default_keys[6 ] = "job_executable"    ; default_values[6 ] =	 ""			# Full path to executable for ChIMES lsq job
	default_keys[7 ] = "job_system"        ; default_values[7 ] =	 "slurm"		# slurm or torque	
	default_keys[8 ] = "job_file"          ; default_values[8 ] =	 "run.cmd"		# Name of the resulting submit script	
	default_keys[9 ] = "job_email"         ; default_values[9 ] =	 True			# Name of the resulting submit script	
	

	args = dict(zip(default_keys, default_values))
	args.update(kwargs)
	
	################################
	# 1. Create the job file
	################################	
	
	
	run_bash_cmnd("rm -f " + args["job_file"])
	
	JOB = []
	JOB.append(" -N " + args["job_name"])
	JOB.append(" -l " + "nodes=" + args["job_nodes"] + ":ppn=" + args["job_ppn"])
	JOB.append(" -l " + "walltime=" + args["job_walltime"])# + ":00:00")	  	   
	JOB.append(" -q " + args["job_queue"])
	if args["job_email"]:
		JOB.append(" -m abe")   
	JOB.append(" -A " + args["job_account"])  
	JOB.append(" -V " )
	JOB.append(" -o " + "stdoutmsg")
	
	ofstream = open(args["job_file"],'w')
	ofstream.write("#!/bin/bash\n")
	
	for i in xrange(len(JOB)):
	
		if args["job_system"] == "slurm":
			JOB[i] = "#MSUB" + JOB[i]
		elif args["job_system"] == "torque":
			JOB[i] = "#PBS"  + JOB[i]
		else:
			print "ERROR: Unknown job_system: ", args["job_system"]
			exit()
			
		ofstream.write(JOB[i] + '\n')
	
	if args["job_executable"]:
	
		ofstream.write(args["job_executable"] + '\n')
	else:
		job_list = argv[0]
		
		for i in xrange(len(job_list)):
			
			ofstream.write(job_list[i] + '\n')
	
	ofstream.close()
	
	################################
	# 2. Launch the job file
	################################

	jobid = None
	
	if args["job_system"] == "slurm":
		jobid = run_bash_cmnd("msub " + args["job_file"])
	else:	
		jobid = run_bash_cmnd("qsub " + args["job_file"])

	return jobid	
	

def wait_for_job(active_job, **kwargs):

	""" 
	
	Pauses the code until a single SLURM job completes.
	
	Usage: wait_for_job(2116091,<arguments>)
	
	Notes: Accepts a jobid and queries the queueing system to determine
	       whether the job is active. Doesn't return until job completes.
	       See function definition in helpers.py for a full list of options.
	
	"""	

	################################
	# 0. Set up an argument parser
	################################

	default_keys   = [""]*3
	default_values = [""]*3
	
	default_keys  [0] = "job_system" ; default_values[0] = "slurm"
	default_keys  [1] = "verbose"    ; default_values[1] = False 
	default_keys  [2] = "job_name"   ; default_values[2] = "unspecified" 
	
	args = dict(zip(default_keys, default_values))
	args.update(kwargs)
	
	active_job = str(active_job).split()[0]
	
	
	################################
	# 1. Determine job status, hold until complete
	################################

	while True:
		
		check_job = ""
		
		if args["job_system"] == "slurm":
			check_job = "squeue -j " + active_job
			
		elif args["job_system"] == "torque":
			print "ERROR: torque support not yet implemented in wait_for_job"
		else:
			print "ERROR: Unknown job_system: ", args["job_system"]
			exit()
			
		if active_job in  run_bash_cmnd(check_job):
		
			if args["verbose"]:
				print "Sleeping for 60 more seconds while waiting for job ", active_job, "...", args["job_name"]
		
			time.sleep(60) # sleep for 60 seconds
		else:		
			print "Breaking ... "
			break				
			
	return
	

def wait_for_jobs(*argv, **kwargs):

	""" 
	
	Pauses the code until SLURM job completes.
	
	Usage: wait_for_jobs([2116091, 2116092], <arguments>)
	
	Notes: Accepts list of jobid and queries the queueing system to determine
	       whether any jobs are active. Doesn't return until job completes.
	       See function definition in helpers.py for a full list of options.
	
	"""

	################################
	# 0. Set up an argument parser
	################################

	default_keys   = [""]*3
	default_values = [""]*3
	
	default_keys  [0] = "job_system" ; default_values[0] = "slurm"
	default_keys  [1] = "verbose"    ; default_values[1] = False 
	default_keys  [2] = "job_name"   ; default_values[2] = "unspecified" 
	
	args = dict(zip(default_keys, default_values))
	args.update(kwargs)
	
	active_jobs = argv[0] # Pointer!
	

	################################
	# 1. Determine job status, hold until complete
	################################

	njobs  = len(active_jobs)

	active = [True]*njobs
	
	while True:
	
		for i in xrange(njobs):
			check_job = ""
			
			if type(active_jobs[i]) == type(1):
				active_jobs[i] = str(active_jobs[i])
		
			if args["job_system"] == "slurm":

				check_job = "squeue -j " + active_jobs[i]
			
			elif args["job_system"] == "torque":
				print "ERROR: torque support not yet implemented in wait_for_job"
			else:
				print "ERROR: Unknown job_system: ", args["job_system"]
				exit()
			
			if active_jobs[i] in  run_bash_cmnd(check_job):
				active[i] = True
			else:
				active[i] = False
			
		
		if True in active:
		
			if args["verbose"]:
				print "Sleeping for 60 more seconds while waiting for jobs ", active_jobs, "...", args["job_name"]
		
			time.sleep(60) # sleep for 60 seconds
		else:		
			print "Breaking ... "
			break					
	return
	

def str2bool(v):

	""" 
	
	Converts "true" or "false" in any case to a corresponding boolean value.
	
	Usage: str2bool("FALSE")
	
	"""

	return v.lower() in ("true")

def break_apart_xyz(*argv):

	""" 
	
	Breaks a .xyz(f) file into individual frames.
	
	Usage: break_apart_xyz(250, "my_file.xyz")
	
	Notes: Takes as input a number of frames and a .xyz or .xyzf file, and breaks it apart 
	       into frames. 
	       Optional: break into chunks of n frames (3rd arg).
	       Optional: Save only the first frame of each chunk (True or False; 4th arg)
	       	
	"""

	# Takes as input a number of frames and a .xyz or .xyzf file, and breaks it apart 
	# into frames. 

	# Optional: break into chunks of (3rd arg)


	print "Breaking apart file: ", argv[1]
	print "WARNING: Converting forces from Hartree/bohr to simulation units (kca/mol/Ang)"
	

	# How many frames are there? ... just do grep -F "Step" <file> | wc -l to find out
	FRAMES = int(argv[0])

	#########

	# What is the input .xyz file?
	XYZFILE = open(argv[1],"r")

	CHUNK_LEN = 1
	if len(argv) >= 3:
	    CHUNK_LEN = int(argv[2])
	    
	FIRST_ONLY = False
	if len(argv) >= 4:
	    FIRST_ONLY = argv[3]

	#########

	ZEROES = len(str(FRAMES))+1


	for f in xrange(FRAMES):

	    if f%CHUNK_LEN == 0:
	    
	        if f > 1:
	            OFSTREAM.close()
	            FRSTREAM.close()

	        # Generate the output filename

	        TAG = ""
	        for i in xrange(ZEROES):
	            if f == 0:
	                if f+1 < pow(10.0,i):
	                    for j in xrange(ZEROES-i):
	                        TAG += "0"
	                    TAG += `f`
	                    break
	                
	            elif f < pow(10.0,i):
	                for j in xrange(ZEROES-i):
	                    TAG += "0"
	                TAG += `f`
	                break

	        OUTFILE  = argv[1]
	        FORCES   = argv[1]
	        TESTER   = OUTFILE [0:-4]
	        TESTER   = TESTER  [-1]

	        if TESTER == ".":
	            FORCES   = OUTFILE[0:-5] + "_FORCES_#" + TAG + ".xyzf" 
	            OUTFILE  = OUTFILE[0:-5] + "_#"        + TAG + ".xyzf" 
	            
	        else:
	            FORCES   = OUTFILE[0:-4] + "_FORCES_#" + TAG + ".xyz" 
	            OUTFILE  = OUTFILE[0:-4] + "_#"        + TAG + ".xyz" 
	            

	        OFSTREAM = open(OUTFILE,"w")
	        FRSTREAM = open(FORCES,"w")
	        
	    if FIRST_ONLY and f%CHUNK_LEN > 0: # We still need to filter through ignored frames
	    
	        # Read the first line to get the number of atoms in the frame,
	        # print back out to the xyzf file
	    
	        ATOMS = XYZFILE.readline()
	    
	        ATOMS = ATOMS.split()
		
	        ATOMS = int(ATOMS[0])
	    
	        # Read/print the comment line

	        XYZFILE.readline()

	        # Now, read/print each atom line
	    
	        for j in xrange(ATOMS):
	            XYZFILE.readline()
	            
	    else:
	    
	        # Read the first line to get the number of atoms in the frame,
	        # print back out to the xyzf file
	    
	        ATOMS = XYZFILE.readline()
	        
	        OFSTREAM.write(ATOMS)
	    
	        ATOMS = ATOMS.split()
	        
	        ATOMS = int(ATOMS[0])
	    
	        # Read/print the comment line

	        OFSTREAM.write( XYZFILE.readline())

	        # Now, read/print each atom line
	    
	        for j in xrange(ATOMS):
	    
	            LINE = XYZFILE.readline()

	            OFSTREAM.write(LINE)
	        
	            LINE = LINE.split()

	            if len(LINE)>4:
	                FRSTREAM.write(`float(LINE[4])*(627.50960803*1.889725989)` + '\n')
	                FRSTREAM.write(`float(LINE[5])*(627.50960803*1.889725989)` + '\n')
	                FRSTREAM.write(`float(LINE[6])*(627.50960803*1.889725989)` + '\n')    
	return


	
import sys


def dftbgen_to_xyz(*argv):

	""" 
	
	Converts a .gen file to .xyz and prints box lengths.
	
	Usage: dftbgen_to_xyz(250, "my_file.xyz")
	
	Notes: Assumes an orthorhombic box.
	       Prints box lengths to a separate file (*.box).
	       	
	"""

	#NOTE: Assumes an orthorhombic box

	# How many frames are there? ... just do grep -F "Step" <file> | wc -l to find out
	FRAMES = int(argv[0])

	# What is the input file?
	IFSTREAM = open(argv[1],"r")

	SKIP = 1
	if len(argv) == 3:
		SKIP = int(argv[2])

	# What is the outputfile
	OUTFILE  = argv[1]
	OUTFILE  = OUTFILE[0:-4] + ".xyz" # replace ".gen" with ".xyz"
	OFSTREAM = open(OUTFILE,"w")

	BOXFILE  = argv[1]
	BOXFILE  = BOXFILE[0:-4] + ".box" # replace ".gen" with ".xyz"
	BOXSTREAM = open(BOXFILE,"w")


	for i in xrange(FRAMES):
		
		# Read the first line to get the number of atoms in the frame
		
		ATOMS = IFSTREAM.readline()
		ATOMS = ATOMS.split()
		ATOMS = int(ATOMS[0])
		
		# Read the next line to get the atom types
		
		SYMBOLS = IFSTREAM.readline()
		SYMBOLS = SYMBOLS.split()
		
		# Print the header bits of the xyz file
		
		if (i+1)%SKIP == 0:
		
			OFSTREAM.write(`ATOMS` + '\n')
			OFSTREAM.write("Frame " + `i+1` + '\n')
		
		# Now read/print all the atom lines in the present frame
		
		for j in xrange(ATOMS):
		
			LINE = IFSTREAM.readline()
			LINE = LINE.split()
			
			# Replace the atom type index with a chemical symbol
		
			for k in xrange(len(SYMBOLS)):
				if k+1 == int(LINE[1]):
					LINE[1] = SYMBOLS[k]
					break
					
			# Print out the line
			
			if (i+1)%SKIP == 0:
			
				OFSTREAM.write(' '.join(LINE[1:len(LINE)]) + '\n')
			
		# Finally, read the box lengths... assume cubic
		
		LINE = IFSTREAM.readline()	# Cell angles?
		
		LINE = IFSTREAM.readline().split()	
		X = LINE[0]
		
		LINE = IFSTREAM.readline().split()	
		Y = LINE[1]
		
		LINE = IFSTREAM.readline().split()	
		Z = LINE[2]	
		
		if (i+1)%SKIP == 0:
		
			BOXSTREAM.write(X + " " + Y + " " + Z + '\n')
			
	return

