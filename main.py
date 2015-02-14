#!/usr/bin/env python
"""
Controller for command line parsing

@author     james@temboinc.com
@version    0.0.1
@since      2015-02-10
"""
import optparse
from parse.itemTimings import ItemTimings
from lib import csvUtil as CsvUtil

def main(desc):
	p = optparse.OptionParser(description=desc)
	p.add_option('--items', default=False, help="parses replay for item timings", action="store_true", dest="itemTimings")
	p.add_option('--csv', default=False, help="outputs results as csv", action="store_true", dest="csv")
	p.add_option('-o', '--output', default=False, help="output destination", action="store", dest="out")
	p.add_option('-i', '--input', default=False, help="input folder or direction", action="store", dest="inp")
	
	opts, args = p.parse_args()

	## check required params
	# if not options.inp:
	# 	p.error('Input path not given.')

    ## redirect to appropriate parse classes
	if (opts.itemTimings is True):
		getItemTimings(opts.csv)

def getItemTimings(csv):
	"""
	Parses and returns item timings
	@param  bool  csv          whether or not to print to csv or stdout 
	@return array itemTimings  the array of heroes, items bought, and time
	"""
	output = ItemTimings().parse('replays/1195864054_tongfu_rave.dem')
	print output
	# CsvUtil.write('test.csv', items)

if __name__ == '__main__':
	desc = "Dota2 stats parser"
	main(desc)