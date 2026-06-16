### `figures/Lib2NIST_configuration.png`
_binary file, 59628 bytes_

### `figures/Lib2NIST_define_subset.png`
_binary file, 47284 bytes_

### `figures/check_number_of_spectra_nist.png`
_binary file, 10543 bytes_

### `paper.md`
```
# QizhiSu__mspcompiler

## Introduction


<!-- README.md is generated from README.Rmd. Please edit that file -->

# mspcompiler

<!-- badges: start -->
<!-- badges: end -->

The goal of mspcompiler is to offer ways to compile either EI or tandem
mass spectral libraries from various sources, such as NIST (if you have
it installed), MoNA, and GPNS, and organize them into a neat and
up-to-date msp file that can be used in MS-DIAL.


## Methods

---
title: "Compile EI and tandem mass spectral libraries"
description: Learn how to compile various EI or MS2 mass spectral libraries 
  into a single, up-to-date, and MS-DIAL friendly msp file.
output: rmarkdown::html_vignette
vignette: >
  %\VignetteIndexEntry{Compile EI and tandem mass spectral libraries}
  %\VignetteEngine{knitr::rmarkdown}
  %\VignetteEncoding{UTF-8}
---
```{r, include = FALSE}
knitr::opts_chunk$set(
  collapse = TRUE,
  comment = "#>",
  eval = FALSE
)
```

```{r setup, include = FALSE}
library(mspcompiler)
```

Here, we will show you in detail how to compile various mass spectral libraries 
into a single, up-to-date, and MS-DIAL friendly library in msp format. This tutorial 
will be divided into two sections explaining the pipeline to process EI and tandem
mass spectral libraries, respectively. To understand each function in detail, 
please use "help or ?", for example,
```{r}
?read_lib
```

## EI libraries
### NIST EI library
NIST is the most commonly used **commercial** EI library. Once you have the 
NIST library installed, you can transformed it into a msp file by *Lib2NIST*. 
Normally *Lib2NIST* will be installed along with the NIST library installation. 
If not, you can download it from https://chemdata.nist.gov/dokuwiki/doku.php?id=chemdata:nist17.
Please use the following settings in *Lib2NIST*:

1. *Add Input Libraries/Files*. For Agilent users, the input file can be found
in, for example, "C:/database/NIST14.L". 

2. Tick *Use Subset* and click *Define Subset* to set detail parameters:

    * En
…[truncated]
```
