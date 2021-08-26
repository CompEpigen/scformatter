import argparse
import os, sys
import time

import shlex
import subprocess

import numpy as np
import pandas as pd
import scanpy as sc
import glob
import re


def getSyncLog(infoStr):
    os.system('echo "[%s] %s"' % (time.strftime('%H:%M:%S'), infoStr))

def load_data(sample):
    adata = sc.read_10x_h5(sample)
    adata.var_names_make_unique()
    sc.pp.filter_cells(adata, min_genes=200)
    sc.pp.filter_genes(adata, min_cells=3)
    adata.var['mt'] = adata.var_names.str.startswith('MT-')  # annotate the group of mitochondrial genes as 'mt'
    sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)
    
    adata = adata[adata.obs.n_genes_by_counts < 2500, :]
    adata = adata[adata.obs.pct_counts_mt < 5, :]
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)
    
    adata.raw = adata
    adata = adata[:, adata.var.highly_variable]
    sc.pp.regress_out(adata, ['total_counts', 'pct_counts_mt'])
    sc.pp.scale(adata, max_value=10)
    
    sc.tl.pca(adata, svd_solver='arpack')
    sc.pp.neighbors(adata, n_neighbors=10, n_pcs=40)
    sc.tl.umap(adata)
    sc.tl.leiden(adata)
    return adata

def main():
    cwd = os.getcwd()
    
    try:
        parser = argparse.ArgumentParser(description="""10XH5 parser""")
        parser.add_argument('-i', dest='input_folder', type=str, required = True, help='input_folder')
        parser.add_argument('-o', dest='output_folder', type=str, required = False, help='output_folder')
        parser.add_argument('-n', dest='name', type=str, required=True, help='prefix of the output file name')
        parser.add_argument('-e', dest='each_file', action="store_true", default=False, help='This option should be given or not. Add this option means to parse the files one by one, not integrate them into a single output file.')
        
        args = parser.parse_args()
        inf, outf, name, each = args.input_folder, args.output_folder, args.name, args.each_file
        # check input folder
        if not inf:
            getSyncLog("Please specify the folder that stores the input files")
            sys.exit(1)
        # check output folder
        if not outf:
            getSyncLog("User did not specfify output folder. The output files will be generated at {0}/procdata".format(cwd))
            outf = cwd

        if not os.path.exists(outf):
            os.makedirs(outf)
        
        getSyncLog('Collect file list under the input folder: {0}'.format(inf))
        infiles = list()
        for f in os.listdir(inf):
            if f.endswith(".h5") or f.endswith(".H5"):
                infiles.append(os.path.join(inf, f))
                if each:
                    getSyncLog('Transforming data format for each file...')
                    print(os.path.join(inf, f))
                    eachadata = load_data(os.path.join(inf, f))
                    f = re.sub(r'\.[hH]5', '', f)
                    eachadata.write(os.path.join(outf, ''.join([name, '_', f, '.h5ad'])))
        if not each:
            getSyncLog('Integrating all files and transforming data format...')
            adatas = [load_data(filename) for filename in infiles]
            adata = adatas[0].concatenate(adatas[1:])
            adata.write(os.path.join(outf, ''.join([name, '.h5ad'])))
            getSyncLog('Finished. Please find the output at {0}'.format(os.path.join(outf, ''.join([name, '.h5ad']))))
                
                
    except KeyboardInterrupt:
        sys.stderr.write("User interrupted me!\n")
        sys.exit(0)

if __name__ == '__main__':
    main()
