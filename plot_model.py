"""
Plot single model given by command-line argument.
to run it 
cd outputs
python ../plot_model.py model_A01
"""

import matplotlib.pyplot as plt
import sys 
from lib_plot_radial import *
from likelihood import *

###################################
# program
###################################

title = None
if len(sys.argv) < 2:
    print "Usage: plot_model.py dirname"

plot_model(sys.argv[1])
load_likelihood_error(sys.argv[1])
plt.show()
