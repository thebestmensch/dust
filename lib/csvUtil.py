"""
CSV Utility methods

@author     james@temboinc.com
@version    0.0.1
@since      2015-02-12
"""
import csv

def write(dest, data):
	"""
	Writes data array to csv
	@param string dest  the destination file
	@param dict   data  the data to write
	"""
	with open(dest, 'ab') as fp:
	    a = csv.writer(fp, delimiter='|')
	    a.writerows(data)

