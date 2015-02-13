import io

from smoke.io.wrap import demo as io_wrp_dm
from smoke.replay import demo as rply_dm
from smoke.replay.demo import Data

class Overview(object):
	"""
	Parses replay for match overview data

	@author		james@jamesmensch.com
	@version 	0.0.1
	@since 		2015-02-12
	"""
	def parse(replay):
		"""
		Parses the replay
		@param string replay  the path to the replay .dem
		"""
		with io.open(replay, 'rb') as infile:
		    demo_io = io_wrp_dm.Wrap(infile)
		    
		    ## returns offset to overview
		    overview_offset = demo_io.bootstrap() 
		    
		    ## we can seek on the raw underlying IO instead of parsing everything
		    infile.seek(overview_offset)

		    demo = rply_dm.Demo(demo_io)
		    demo.finish()
			return demo.match.overview
