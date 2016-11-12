#!/usr/bin/python2

import sys
import os
import glob
import sancov_script
import subprocess
import re

def usage():
    print "Usage " + sys.argv[0] + " <Honggfuzz directory> " + \
	" <input files> "+\
	" <binary> "+\
	 " <output directory> \n"+\
	"Runs honggfuzz and concolic execution"
    exit(1)

def main():
    if len(sys.argv) < 4:
        usage()
    print sys.argv
    #Assign arguments to variables
    honggfuzz_directory = sys.argv[1]
    input_files_directory = sys.argv[2]
    binary_fuzzed = sys.argv[3]
    binary_name = binary_fuzzed.rsplit('/',1)[-1]
    #output_directory = sys.argv[4]
    #open log file
    logFile = open("logFile","w")
    #.run ./../honggfuzz/honggfuzz -f ../../honggfuzz/examples/inputfiles/ -C -- ../../honggfuzz/examples/targets/badcode1 ___FILE___
    #p = subprocess.Popen([sys.argv[1]+"/honggfuzz","-f",sys.argv[1]+"/examples/inputfiles","-C","--",sys.argv[1]+"/examples/targets/badcode1","___FILE___ "],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = subprocess.Popen([honggfuzz_directory + "/honggfuzz","-f",input_files_directory,"-C","--",binary_fuzzed,"___FILE___ "],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = p.communicate()
    logFile.write(out)
    #Create listener on HF_SANCOV FILE that creates a new sancov file for every raw file created
    while(1):
	file_list_sancov = []
    	file_list_raw = []
        #Get newest sancov.raw
	newest_raw = min(glob.iglob('HF_SANCOV/*.raw'), key=os.path.getctime)
	#create a sancov file
	file_list_raw.append(newest_raw)
	file_list_sancov = (sancov_script.RawUnpack(file_list_raw))
	#Print covered PCS
	#print file_list_sancov[0]
	file_list_sancov = re.findall(r'\b(\w+.\w+.sancov)\b',str(file_list_sancov[0]))
	#print file_list_sancov
	covered_pc = sancov_script.PrintFiles(file_list_sancov)	
	#print missing PC
	missed_pc = sancov_script.PrintMissing(binary_fuzzed,covered_pc)
	#Begin symbolic/Concolic execution thread for every missed pc
	

if __name__ == '__main__':
   main() 
