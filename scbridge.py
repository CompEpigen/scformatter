import argparse
import os, sys
import time

import shlex
import subprocess


TYPES = ['S3toH5AD', 'S2toS3', 'H5toH5AD']
FORMATMAP = {'S2': 'seurat2','S3': 'seurat3', 'H5AD': 'h5ad', 'H5':'h5'}   

def getSyncLog(infoStr):
    os.system('echo "[%s] %s"' % (time.strftime('%H:%M:%S'), infoStr))


def scbridge(transtype, inf, cwd, outf):
    intype, outtype = transtype.split('to')
    inpath, outpath = ["{0}/rawdata/{1}".format(cwd, FORMATMAP[intype]),"{0}/procdata/{1}".format(cwd, FORMATMAP[outtype])]

    if not os.path.exists(inpath):
        os.makedirs(inpath)
    if os.path.exists(outpath):
        os.system("rm -r {0}".format(outpath))

    getSyncLog("Find files at {0}".format(inf))
    os.system("ls {0}/*".format(inf))
    os.system("cp {0}/* {1}".format(inf, inpath))

    #cpu = os.system("ls {0}/*.rds|wc -l".format(inf)) #multi-threads

    getSyncLog("Transformating {0} object to {1} object...".format(FORMATMAP[intype], FORMATMAP[outtype]))
    cmd = shlex.split("snakemake --use-singularity --cores 1 -s {0}/Snakefiles/Snakefile {1}".format(cwd, transtype))
    subprocess.Popen(cmd).wait()

    #clean files
    #os.system("rm {0}/*".format(inpath)) 
    if not os.path.abspath(outf) == cwd:
        getSyncLog("Move processed files to target directory: {0}".format(outf))
        os.system("mv {0}/* {1}".format(outpath, outf))
        os.system("rm -r {0}".format(outpath))
        getSyncLog("Please find the processed files at '{0}'".format(outf))
    else:
        getSyncLog("Please find the processed files at '{0}'".format(outpath))


def main():
    cwd = os.getcwd()
    
    try:
        parser = argparse.ArgumentParser(description="""Format transformation of single cell datasets""")
        parser.add_argument('-t', dest='transform_type', type=str, required = True, help="Please select from {0}".format(TYPES))
        parser.add_argument('-i', dest='input_folder', type=str, required = True, help='input_folder')
        parser.add_argument('-o', dest='output_folder', type=str, required = False, help='output_folder')
        
        args = parser.parse_args()
        inf, outf, trans = args.input_folder, args.output_folder, args.transform_type
        # check whether the transformation type is supported.
        if not trans in TYPES:
            getSyncLog("The function for {0} transformation is not supported for now. Please select from {1} or submit a git issue for requesting new function.".format(trans, TYPES))
            sys.exit(1)
        # check input folder
        if not inf:
            getSyncLog("Please specify the folder that stores the input files")
        # check output folder
        if not outf:
            getSyncLog("User did not specfify output folder. The output files will be generated at {0}/procdata".format(cwd))
            outf = cwd

        scbridge(trans, inf, cwd, outf) 
        
    except KeyboardInterrupt:
        sys.stderr.write("User interrupted me!\n")
        sys.exit(0)


if __name__ == '__main__':
    main()
