# overview_only.py
import io

from smoke.io.wrap import demo as io_wrp_dm
from smoke.replay import demo as rply_dm
from smoke.replay.demo import Data

with io.open('replays/1191255868.dem', 'rb') as infile:
    demo_io = io_wrp_dm.Wrap(infile)
    overview_offset = demo_io.bootstrap() # returns offset to overview

    # we can seek on the raw underlying IO instead of parsing everything
    infile.seek(overview_offset)

    demo = rply_dm.Demo(demo_io)
    demo.finish()

    print demo.match.overview