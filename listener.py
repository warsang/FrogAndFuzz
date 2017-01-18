import glob
import os
import re
import redis_com
import thread

import sancov_script

from driller_call import test_drilling

def hf_sancov_listener(threadName,binary_fuzzed,binary_fuzzed_instru ,directory,input_dir, red):
    queueFile = open(directory+"queueFile","w+")
    counter = 3
    old_set = set()
    new_set = set()
    while(1):
	if(len(glob.glob(directory+'HF_SANCOV/*.raw'))):
	    file_list_sancov = []
            file_list_raw = []
            #Get newest sancov.raw
	    try:
		newest_raw = min(glob.iglob(directory+'HF_SANCOV/*.raw'), key=os.path.getctime)
	    except:
		continue
	    #create a sancov file
            file_list_raw.append(newest_raw)
            try:
	        file_list_sancov = (sancov_script.RawUnpack(file_list_raw))
	    except:
	        continue
            #Print covered PCS
            try:
	   	 file_list_sancov = re.findall(r'\b(\S+.sancov)\b',str(file_list_sancov[0]))
	    except:	
	        continue
            try:
		covered_pc = sancov_script.PrintFiles(file_list_sancov)
	    except:
		continue
	    new_set.update(covered_pc)
            # printing the missing PC
            missed_pc = sancov_script.PrintMissing(binary_fuzzed_instru,covered_pc)
            #Save to queue file
            queueFile.write('-----------------------------\n')
            fullsancov=sancov_script.GetInstrumentedPCsFormated(binary_fuzzed_instru)
            redis_com.add_Sancov(binary_fuzzed,red,str(fullsancov).strip('[]'))
            redis_com.add_Missed(binary_fuzzed,red,str(missed_pc).strip('[]'))
            for pc in missed_pc:
                queueFile.write(pc + '\n')
	    if old_set != new_set:
		#A new pc has been found, we launch a driller instance and replace the old set by a new one.
		old_set = new_set
		thread.start_new_thread(test_drilling,("Thread-"+ str(counter),binary_fuzzed,input_dir,directory,red))
		counter += 1
        else:
            pass
