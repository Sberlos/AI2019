import sys
import run
import src.meta_heuristics
import src.utils
import src.local_search
import src.io_tsp
import src.constructive_algorithms
import src.genetic
import src.TSP_solver
#import src.__init__

run.run(str(sys.argv[1]), show_plots=False, verbose=True)
