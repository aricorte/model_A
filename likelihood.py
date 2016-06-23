__all__ = ["plot_thing", "load_likelihood_error"]
import numpy as np
import glob
import os
import sys
import matplotlib.pyplot as plt
import traceback

def plot_thing(vmean, srmean, svmean, shmean, rhmean, vmean_err, srmean_err, svmean_err, shmean_err, title=None, descr=None):
    """Creates error bar figure."""
#    means = np.mean(matrix, 1)
#    stds = np.std(matrix, 1)
    # n = len(means)
    # x = range(n)
    plt.figure()
    plt.errorbar(rhmean, vmean, yerr=vmean_err, fmt='o', c='k')
    plt.errorbar(rhmean, srmean, yerr=srmean_err, fmt='o', c='r')
    plt.errorbar(rhmean, svmean, yerr=svmean_err, fmt='o', c='b')
    plt.errorbar(rhmean, shmean, yerr=shmean_err, fmt='o', c='g')
#    plt.errorbar(radii, err, yerr=serrmed, fmt='o', c='k')
    if title:
        plt.title(title)
    if descr:
        plt.text(400, 350, descr)
    plt.xlim(0, 600)
    plt.ylim(0, 400)
    plt.xlabel ("Radius")
    plt.ylabel ("kine")
    plt.grid()
    plt.tight_layout()













def load_likelihood_error(dirname, file_errors=None):
    """
    Loads all likelihood.dat and error.dat inside each directory matching catalog*.
    
    Returns (likelihood, error) (both are lists)
    
    """
    
    model_name = dirname[dirname.index("_")+1:]

    dirs = glob.glob("%s/catalog*" % dirname)
    dirs.sort()

    print "Directories to consider:"
    for dir_ in dirs:
        print "- ", dir_

    likelihood = []
    error = []

    for dir_ in dirs:
        path_likelihood = os.path.join(dir_, "likelihood.dat")
        if not os.path.isfile(path_likelihood):
            if file_errors:
                file_errors.write(dir_+"\n")
            print "WARNING: skipping %s" % dir_
        else:
            likelihood.append(np.loadtxt(path_likelihood))
            # print likelihood[-1]
            error.append(np.loadtxt(os.path.join(dir_, "error.dat")))
            # print counts[-1]
            
            ncat = len(likelihood)
           

    if len(likelihood) == 0:
        raise RuntimeError("Skipped all catalogues, cannot do anything")

        
        
    print ncat    
   # return likelihood, error
    
   



    #likelihood, error = load_likelihood_error(".")

    # Isolates 1st and 2nd columns of all files
    temp_v = []
    temp_sr = []
    temp_sv = []
    temp_sh = []
    temp_rh = []
    temp_npne = []

    vmean = []
    srmean = []
    svmean = []
    shmean = []
    rhmean = []
    npnemean = []
    npnetot= []
#    temp_ntot = []


    for like, err in zip(likelihood, error):
        temp_v.append(like[:, 1:2])
        # print temp_nw
        # sys.exit()
        temp_sr.append(like[:, 2:3])
        temp_sv.append(like[:, 3:4])
        temp_sh.append(like[:, 4:5])
        temp_rh.append(like[:, 7:8])
        temp_npne.append(like[:, 8:9])

    #temp_vmin.append(like[:, 0:1])
    #temp_vmax.append(like[:, 1:2])
    # print temp_nw
    # sys.exit()
    #temp_srmin.append(like[:, 2:3])
    #temp_srmax.append(like[:, 3:4])
    #temp_svmin.append(like[:, 4:5])
    #temp_svmax.append(like[:, 5:6])
    #temp_shmin.append(like[:, 6:7])
    #temp_shmax.append(like[:, 7:8])
    

# Now stacks into matrices
    v = np.hstack(temp_v)
    sr = np.hstack(temp_sr)
    sv = np.hstack(temp_sv)
    sh = np.hstack(temp_sh)
    rh = np.hstack(temp_rh)
    npne= np.hstack(temp_npne)
#vmin = np.hstack(temp_vmin)
#srmin = np.hstack(temp_srmin)
#svmin = np.hstack(temp_svmin)
#srmin = np.hstack(temp_shmin)
#rhmin = np.hstack(temp_rhmin)
#vmax = np.hstack(temp_vmax)
#srmax = np.hstack(temp_srmax)
#svmax = np.hstack(temp_svmax)
#srmax = np.hstack(temp_shmax)
#rhmax = np.hstack(temp_rhmax)

    vmean = np.mean(v, 1)
    vmean_err=np.std(v, 1)
    srmean = np.mean(sr, 1)
    srmean_err = np.std(sr, 1)
    svmean = np.mean(sv, 1)
    svmean_err = np.std(sv, 1)
    shmean = np.mean(sh, 1)
    shmean_err = np.std(sh, 1)
    rhmean = np.mean(rh, 1)
    npnemean = np.mean(npne, 1)
    npnetot = np.sum(npnemean)
    print npnetot, npnemean
    descr="%.i, %.i" % (npnetot, ncat)


#stds_nw = np.std(nw, 1)
#print "means nw", means_nw
#print "stds nw", stds_nw

#read nw1 1 read nlike1 2 read rgal1 3 read ntot1 4
#read nb1 1 read nbl 2 read nd 3 read ndl 4 read nbclip1 7 read nbclipno1 8 


    plot_thing(vmean, srmean, svmean, shmean, rhmean, vmean_err, srmean_err, svmean_err, shmean_err, model_name, descr) 
    plt.savefig("%s-like.png"  % model_name)
