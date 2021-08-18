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
            getSyncLog("User did not specfify output folder. Please find the output files in {0}/procdata".format(cwd))
            outf = cwd

        if (trans == 'S4toH5AD'):
            cmd = shlex.split("cp {0}/*.rds {1}/rawdata/seurat4".format(inf, cwd))
            print(cmd)
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process
            getSyncLog("Find files")
                
    except KeyboardInterrupt:
        sys.stderr.write("User interrupted me!\n")
        sys.exit(0)

if __name__ == '__main__':
    main()
