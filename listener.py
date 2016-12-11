import glob
import os
import re
import redis_com

import sancov_script

def hf_sancov_listener(threadName,binary_fuzzed, directory, red):
    queueFile = open(directory+"queueFile","w")
    while(1):
        if(len(glob.glob(directory+'/HF_SANCOV/*.raw'))):
            file_list_sancov = []
            file_list_raw = []
            #Get newest sancov.raw
            newest_raw = min(glob.iglob(directory+'/HF_SANCOV/*.raw'), key=os.path.getctime)
            #create a sancov file
            file_list_raw.append(newest_raw)
            file_list_sancov = (sancov_script.RawUnpack(file_list_raw))
            #Print covered PCS
            #print file_list_sancov[0]
            file_list_sancov = re.findall(r'\b(\S+.sancov)\b',str(file_list_sancov[0]))
            #print file_list_sancov
            covered_pc = sancov_script.PrintFiles(file_list_sancov)
            # printing the missing PC
            missed_pc = sancov_script.PrintMissing(binary_fuzzed,covered_pc)
            #print missed_pc
            #Save to queue file
            queueFile.write('-----------------------------\n')
            fullsancov=sancov_script.GetInstrumentedPCsFormated(binary_fuzzed)
            redis_com.add_Sancov(binary_fuzzed,red,str(fullsancov).strip('[]'))
            redis_com.add_Missed(binary_fuzzed,red,str(missed_pc).strip('[]'))

            for pc in missed_pc:
                queueFile.write(pc + '\n')
        else:
            pass
                	# TODO SAVE TO REDIS DB
                #	for pc in missed_pc:
                #		print queueFile
                #		queueFile.write(pc)
