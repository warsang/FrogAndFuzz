import redis
import hashlib

REDIS_HOST = '149.202.100.64'
REDIS_PORT = '6379'
REDIS_DB = '0'

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
