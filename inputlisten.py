import glob
import os
import subprocess
from driller_call import test_drilling

def input_listener(threadName,honggfuzz_directory,binary_fuzzed, directory,output_directory, red):
    old_input_files_set = set()
    new_input_files_set = set()
    while(1):
	for root,dirnames,filenames in os.walk(directory):
	    for dirname in dirnames:
		if(len(glob.glob(directory+'/'+ dirname+'*'))):
		 newest_input = min(glob.iglob(directory + '/' + dirname+'*'), key=os.path.getctime)
    	         new_input_files_set.add(newest_input)
	        if new_input_files_set != old_input_files_set:
		    old_input_files_set = new_input_files_set
		    logFile = open(output_directory + "threadlog","w+")
		    errFile = open(output_directory + "threaderrlog","w+")
		    p = subprocess.Popen([honggfuzz_directory + "/honggfuzz","-f",directory + '/' + dirname,"-W",output_directory,"-s","-C","--",binary_fuzzed],stdout=logFile, stderr=errFile)
		    logFile.close()
		    errFile.close()
 
