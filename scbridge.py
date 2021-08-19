import argparse
import os
import time

import shlex
import subprocess


def getSyncLog(infoStr):
    os.system('echo "[%s] %s"' % (time.strftime('%H:%M:%S'), infoStr))

def main():
    cwd = os.getcwd()
    
    try:
        parser = argparse.ArgumentParser(description="""single cell dataset parser""")
        parser.add_argument('-t', dest='transform_type', type=str, required = True, help="Please select from S4toH5AD")
        parser.add_argument('-i', dest='input_folder', type=str, required = True, help='input_folder')
        parser.add_argument('-o', dest='output_folder', type=str, required = False, help='output_folder')
        
        
        args = parser.parse_args()
        
        inf, outf, trans = args.input_folder, args.output_folder, args.transform_type
        # check input folder
        if not inf:
            getSyncLog("Please specify the folder that stores the input files")
        
        # check output folder
        if not outf:
            getSyncLog("User did not specfify output folder. The output files will be generated at {0}/procdata".format(cwd))
            outf = cwd

        if trans == 'S4toH5AD':
            getSyncLog("Find files at {0}".format(inf))
            os.system("ls {0}/*.rds".format(inf))
            #cpu = os.system("ls {0}/*.rds|wc -l".format(inf))
            os.system("cp {0}/*.rds {1}/rawdata/seurat4".format(inf, cwd))

            getSyncLog("Transformating Seurat4 object to Scanpy H5AD object...")
            cmd = shlex.split("snakemake --use-singularity --cores 1 -s Snakefile.S4")
            #print(cmd)
            subprocess.Popen(cmd).wait()
            if not outf == cwd:
                os.system("mv {0}/procdata/h5ad/* {1}".format(cwd, outf))
                
    except KeyboardInterrupt:
        sys.stderr.write("User interrupted me!\n")
        sys.exit(0)

if __name__ == '__main__':
    main()
