#!/usr/bin/env Rscript
library(Seurat)
library(SeuratDisk)
library(dplyr)
library(data.table)

args <- commandArgs(trailingOnly = TRUE)
#args = c("rawdata/seurat3", "procdata/h5ad")
dir.create(args[2], showWarnings = FALSE)
dir.create('tmp', showWarnings = FALSE)

move <- function(from, to) {
  todir <- dirname(to)
  if (!isTRUE(file.info(todir)$isdir)) dir.create(todir, recursive=TRUE)
  file.rename(from = from,  to = to)
}

in.files <- list.files(args[1], pattern = ".rds")

i=1
for (i in 1:length(x = in.files)) {
  fname <- in.files[i]
  print(fname)
  dir(args[1])
  ob <- readRDS(file = file.path(args[1],fname))
  fname = gsub(".rds","", fname)
  SaveH5Seurat(object = ob, file = file.path('tmp',paste0(fname,".h5seurat")), overwrite = TRUE)
  Convert(file.path('tmp',paste0(fname,".h5seurat")), dest = "h5ad", overwrite = TRUE)
  move(file.path('tmp',paste0(fname,".h5ad")), file.path(args[2], paste0(fname,".h5ad")))
}
unlink('tmp', recursive = T)
