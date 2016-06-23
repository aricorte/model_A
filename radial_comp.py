import numpy as np
import glob
import os
import sys
import matplotlib.pyplot as plt



###################################
# library
###################################

def plot_thing(radii, err, serrmed, title=None, descr=None):
#    means = np.mean(matrix, 1)
#    stds = np.std(matrix, 1)
    # n = len(means)
    # x = range(n)
    plt.figure()
    plt.errorbar(radii, err, yerr=serrmed, fmt='o', c='k')
    if title:
        plt.title(title)
    if descr:
        plt.text(400, .9, descr)
    plt.xlim(0, 600)
    plt.ylim(0, 1)


###################################
# program
###################################

title = None
if len(sys.argv) > 1:
    title = sys.argv[1]
# print "arguments:", sys.argv


def plot_model(dirname):

    model_name = dirname[dirname.index("_")+1:]

    dirs = glob.glob("catalog*")
    dirs.sort()

    print "Directories to consider:"
    for dir_ in dirs:
        print "- ", dir_

    rads = []
    counts = []

    for dir_ in dirs:
        rads.append(np.loadtxt(os.path.join(dir_, "radial.dat")))
        # print rads[-1]
        counts.append(np.loadtxt(os.path.join(dir_, "count.dat")))
        # print counts[-1]


    # Isolates 1st and 2nd columns of all files
    temp_nw = []
    temp_like = []
    temp_rgal = []
    temp_nb = []
    temp_nbl = []
    temp_ntot = []


    for rad, count in zip(rads, counts):
        temp_nw.append(rad[:, 0:1])
        # print temp_nw
        # sys.exit()
        temp_like.append(rad[:, 1:2])
        temp_rgal.append(rad[:, 2:3])
        
        temp_nb.append(count[0])
        temp_nbl.append(count[1])
        temp_ntot.append(count[5])
       
        
        
    # Now stacks into matrices
    nw = np.hstack(temp_nw)
    like = np.hstack(temp_like)
    rgal = np.hstack(temp_rgal)

    #nb = np.hstack(temp_nb)
    #nbl = np.hstack(temp_nbl)
    #ntot = np.hstack(temp_ntot)

    print nw
    print like
    print rgal


    nlikebin = np.mean(like, 1)
    serr = np.std(nw, 1)
    errmed = np.mean(nw, 1)
    err = errmed/nlikebin
    serrmed = serr/nlikebin

    radii = np.mean(rgal, 1)

    nb_med=np.mean(temp_nb)
    ntot_med=np.mean(temp_ntot)
    nbl_med=np.mean(temp_nbl)
    descr="%.0f, %.0f, %.0f" % (nb_med,nbl_med,ntot_med)


    #stds_nw = np.std(nw, 1)
    #print "means nw", means_nw
    #print "stds nw", stds_nw

    #read nw1 1 read nlike1 2 read rgal1 3 read ntot1 4
    #read nb1 1 read nbl 2 read nd 3 read ndl 4 read nbclip1 7 read nbclipno1 8 


    plot_thing(radii, err, serrmed, title, descr)
    plt.save_png("radial-%s.png" % model_name)
    plt.show()
