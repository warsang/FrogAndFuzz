#!/usr/bin/python2

import sys
import subprocess
import thread
import redis
import hashlib 

REDIS_HOST = '149.202.100.64'
REDIS_PORT = '6379'
REDIS_DB = '0'

from  listener import hf_sancov_listener
#from symbol import tracing_func
def usage():
    print "Usage " + sys.argv[0] + " <Honggfuzz directory> " + \
	" <input files> "+\
	" <binary> "+\
	 " <output directory> \n"+\
	"Runs honggfuzz and concolic execution"
    exit(1)

def connect_redis():
	pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
	r = redis.Redis(connection_pool=pool)
	print "connection redis called"
	return r
	#return redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
def add_Sancov(binary, red, sancov_data):
	sancov_hash = hashlib.sha256(sancov_data).hexdigest()
	new=red.hset(binary+ '-sancov', sancov_hash, sancov_data)
	if (new == 1): # means it's a new entry
		red.lpush(binary + '-sancovhashes', sancov_hash) 
def get_Sancov(binary, red, sancov_hash):
	return red.hget(binary + '-sancov', sancov_hash)
def get_SancovHashe(binary, red): # FIFO
	hash=red.rpop(binary + '-sancovhashes')
	red.lpush(binary + '-sancovhashesCalled', hash)
	return hash
def get_SancovData(binary, red):
	return get_Sancov(binary, red, get_SancovHashe(binary,red))
def clean_redis(red, binary):
    #red = redis.Redis(connection_pool=redis_pool)
    # delete all the traced entries
	red.delete("%s-traced" % binary)    
    # delete the finished entry
	red.delete("%s-finished" % binary)
	# delete all the sancovhashes entries
	red.delete("%s-sancovhashes" % binary)	
	# delete all the sancovhashesCalled entries
	red.delete("%s-sancovhashesCalled" % binary)
    # delete the sancov 
	red.delete("%s-sancov" % binary)

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
    print "i am finally here"
    #Create listener on HF_SANCOV FILE that creates a new sancov file for every raw file created
    red = connect_redis()
    thread.start_new_thread(hf_sancov_listener,("Thread-1",binary_fuzzed))
    #Begin symbolic/Concolic execution thread for every missed pc
    while(1):
	#tracing_func(binary_fuzzed,input_files_directory)
	pass	 

if __name__ == '__main__':
   main() 

