#!/usr/bin/python2

import sys
import subprocess
import thread
import time

import logging 
import redis_com

from  listener import hf_sancov_listener
from inputlisten import input_listener

#########CONFIGURATION#########

import config

###############################

logging.getLogger("tracer").setLevel(logging.DEBUG)
logging.getLogger("driller").setLevel(logging.DEBUG)

def usage():
    print "Usage " + sys.argv[0] + " <Honggfuzz directory> " + \
	" <binary> "+\
	"<instrumented binary>"+\
	" <input_files> "+\
	 " <output directory> \n"+\
	"Runs honggfuzz and the driller concolic execution engine"
    exit(1)

def main():
    logging.basicConfig(filename = 'temp.log', level = logging.DEBUG)
    if len(sys.argv) < 6:
        usage()
    #Assign arguments to variables
    honggfuzz_directory = sys.argv[1]
    binary_fuzzed = sys.argv[2]
    binary_fuzzed_instru = sys.argv[3]
    input_files_directory = sys.argv[4]
    output_directory = sys.argv[5]
    binary_name = binary_fuzzed_instru.rsplit('/',1)[-1]
    #open log file
    logFile = open(output_directory + "logFile","w+")
    logErr =open (output_directory + "logErr","w+")
    #open queue file
    #queueFile = open("queueFile","rw")
    # subprocess to run ./../honggfuzz/honggfuzz -f ../../honggfuzz/examples/inputfiles/ -C -- ../../honggfuzz/examples/targets/badcode1 ___FILE___
 #    p = subprocess.Popen([honggfuzz_directory + "/honggfuzz","-f",input_files_directory,"-W",output_directory,"-C","--",binary_fuzzed_instru,"___FILE___ "],stdout=logFile, stderr=logErr)
    p = subprocess.Popen([honggfuzz_directory + "/honggfuzz","-f",input_files_directory,"-W",output_directory,"-s","-C","--",binary_fuzzed_instru],stdout=logFile, stderr=logErr)
    #Create listener on HF_SANCOV FILE that creates a new sancov file for every raw file created
    red = redis_com.connect_redis(config.REDIS_DB1)
    driller_red = redis_com.connect_redis(config.REDIS_DB2)
    redis_com.clean_redis(red,binary_fuzzed_instru) 
    thread.start_new_thread(hf_sancov_listener,("Thread-1",binary_fuzzed,binary_fuzzed_instru, output_directory,input_files_directory, red))
    thread.start_new_thread(input_listener,("Thread-2",honggfuzz_directory,binary_fuzzed_instru,input_files_directory,output_directory,red))
    #Begin first symbolic/Concolic execution thread for every missed pc
    while(1):
   	pass
	
if __name__ == '__main__':
   main()
