import driller
import logging
import os
import glob

l = logging.getLogger("driller.tests.test_driller")

def run_driller(binary_path,input_file_dir,redis):
	if os.path.isdir(input_file_dir):
		for input_file in os.listdir(input_file_dir):
			fd = open( input_file_dir + input_file ,'r')
			input_string = fd.read()
			fd.close()
			d = driller.Driller(binary_path,input_string,None)
			new_inputs = d.drill()
			return new_inputs
	else:
		fd = open(input_file_dir,'r')
		input_string = fd.read()
		fd.close()
		d = driller.Driller(binary_path,input_string,None)
		new_inputs = d.drill()
		return new_inputs

def test_drilling(threadName, binary_path,input_file_dir,test_case_dir,redis):
	newest_input = min(glob.iglob(test_case_dir+'*'), key=os.path.getctime)
	symbol_input = run_driller(binary_path,newest_input,redis)
	counter = 0
	if symbol_input:
	    #Retrieve last element of the set by converting it to a list. Set contains list so we then have a list of lists:
	    sub_list = list(symbol_input)
	    for my_list in sub_list:
	    	if my_list[-1]:
	    		counter += 1
			if not os.path.exists(input_file_dir+"/"+threadName):
		    		os.makedirs(input_file_dir+"/"+threadName)
	    		fd = open(input_file_dir+"/"+threadName+"/"+threadName+"-"+str(counter),'wb+')
	    		fd.write(my_list[-1])
	    		fd.close()
	return 0
	
