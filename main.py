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
	p.add_option('--item', '-i', default=False, help="parses replays folder for item timings", action="store_true", dest="itemTimings")
	p.add_option('--csv', default=False, help="outputs results as csv", action="store_true", dest="csv")
	p.add_option('-o', '--output', default=False, help="output destination", action="store", dest="out")
	
	opts, args = p.parse_args()
	if (opts.itemTimings is True):
		getItemTimings(opts.csv)

def getItemTimings(csv):
	"""
	Parses and returns item timings
	@param  bool  csv          whether or not to print to csv or stdout 
	@return array itemTimings  the array of heroes, items bought, and time
	"""
	items = ItemTimings().parse('replays/1191255868.dem')
	print items
	# CsvUtil.write('test.csv', items)

if __name__ == '__main__':
	desc = "Dota2 stats parser"
	main(desc)