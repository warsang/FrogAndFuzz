#!/usr/bin/python2

import sys
import subprocess
import thread

import redis_com
from  listener import hf_sancov_listener

#from symbol import tracing_func
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
    #print sys.argv
    #Assign arguments to variables
    honggfuzz_directory = sys.argv[1]
    input_files_directory = sys.argv[2]
    binary_fuzzed = sys.argv[3]
    binary_name = binary_fuzzed.rsplit('/',1)[-1]
    #output_directory = sys.argv[4]
    #open log file
    logFile = open("logFile","w")
    errFile =open ("logErr","w")
    #open queue file
    #queueFile = open("queueFile","rw")
    #.run ./../honggfuzz/honggfuzz -f ../../honggfuzz/examples/inputfiles/ -C -- ../../honggfuzz/examples/targets/badcode1 ___FILE___
    p = subprocess.Popen([honggfuzz_directory + "/honggfuzz","-f",input_files_directory,"-C","--",binary_fuzzed,"___FILE___ "],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = p.communicate()
    logFile.write(out)
    errFile.write(err)
    #print "i am finally here"
    #Create listener on HF_SANCOV FILE that creates a new sancov file for every raw file created
    red = redis_com.connect_redis()
    thread.start_new_thread(hf_sancov_listener,("Thread-1",binary_fuzzed))
    #Begin symbolic/Concolic execution thread for every missed pc
    while(1):
	#tracing_func(binary_fuzzed,input_files_directory)
	pass	 

if __name__ == '__main__':
   main() 

