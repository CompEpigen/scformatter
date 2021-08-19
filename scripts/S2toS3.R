#!/usr/bin/env Rscript
library(Seurat)
library(SeuratDisk)
library(dplyr)
library(data.table)

getwd()
args <- commandArgs(trailingOnly = TRUE)
#args = c("rawdata/seurat3", "procdata/seurat4")
dir.create(args[2], showWarnings = FALSE)

move <- function(from, to) {
  todir <- dirname(to)
  if (!isTRUE(file.info(todir)$isdir)) dir.create(todir, recursive=TRUE)
  file.rename(from = from,  to = to)
}

in.files <- list.files(args[1])

i=1
for (i in 1:length(x = in.files)) {
  fname <- in.files[i]
  print(fname)
  dir(args[1])
  if (grep(".Robj", fname)){
    x=load(file.path(args[1],fname))
    y=get(x)
    rm(x)
    ob = SeuratObject::UpdateSeuratObject(y)
  }else if (grep(".rds", fname)){
    ob <- readRDS(file = file.path(args[1],fname))
    ob = SeuratObject::UpdateSeuratObject(y)
  }
  fname = gsub(".rds|.Robj","", fname)
  SeuratObject::DefaultAssay(ob) <- "RNA"
  saveRDS(object = ob, file = file.path(args[2], paste0(fname, ".rds")))
}

