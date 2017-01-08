import driller
import logging
import os

l = logging.getLogger("driller.tests.test_driller")

def test_drilling(binary_path,input_file,redis):

	binary = "../honggfuzz/examples/targets/badcode_nocov"

	d = driller.Driller(binary,"123456789012345678901234567890123456789012345678901234567890\n123456789012345678901234567890123456789012345678901234567890")
	
	new_inputs = d.drill()
	
	print new_inputs
