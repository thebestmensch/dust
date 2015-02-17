#!/usr/bin/env python
"""
Controller for command line parsing

@author     james@temboinc.com
@version    0.0.1
@since      2015-02-10
"""
import optparse
import pandas as pd
import numpy as np
import os

from parse.itemTimings import ItemTimings
from parse.overview import Overview
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

	## get game metadata
	overview = getOverview()

    ## redirect to appropriate parse classes
	if (opts.itemTimings is True):
		item_timings = getItemTimings()
	output = item_timings.merge(overview, how="left", on=["match_id","hero_name"])
	output.to_csv('test.csv')
def getItemTimings():
	"""
	Parses and returns item timings
	@param  string     replay       replay or replay directory
	@return dataframe  itemTimings  the array of heroes, items bought, and time
	"""
	replay_dir = 'replays/'
	replays = os.listdir('replays')
	output = None
	for replay in replays: 
		if replay.index('.') == 0:
			continue

		replay = replay_dir + replay
		if output is None:
			output = ItemTimings().parse(replay)
		else:
			output = output.append(ItemTimings().parse(replay), ignore_index=True)
	return output
def getOverview():
	"""
	Parses and returns game and hero overview data
	@param  string    replay   replay or replay directory
	@return dataframe the over data 
	"""
	replay_dir = 'replays/'
	replays = os.listdir('replays')
	output = None
	for replay in replays:
		## make sure we're not trying to parse system files
		if replay.index('.') == 0:
			continue

		replay = replay_dir + replay
		if output is None:
			output = Overview().parse(replay)
		else:
			output = output.append(Overview().parse(replay), ignore_index=True)
	return output

if __name__ == '__main__':
	desc = "Dota2 stats parser"
	main(desc)