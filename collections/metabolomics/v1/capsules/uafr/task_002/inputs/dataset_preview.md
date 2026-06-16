### `figures/GraphicalAbstract.jpg`
_binary file, 121256 bytes_

### `paper.md`
```
# castratton__uafR

## Introduction


# uafR - A new standard for mass spectrometry data processing

<!-- badges: start -->
<!-- badges: end -->


## Methods

---
title: "uafR"
output: rmarkdown::html_vignette
vignette: >
  %\VignetteIndexEntry{uafR}
  %\VignetteEngine{knitr::rmarkdown}
  %\VignetteEncoding{UTF-8}
resource_files: man/figures/GraphicalAbstract.jpg
---
# <span style="color: rgba(80, 0, 96, 1); font-size:120%; background-color: rgba(0, 0, 0, 0)">Automated GC/LC-MS data processing</span>

***
<span style="color: rgba(80, 0, 96, 1); font-size:215%; background:none">Nothing in life is to be feared; it is only to be understood.</span>   
<span style="color: black; font-size:200%; background:none">--Marie Curie</span>


***

<center>
![Graphical Abstract](GraphicalAbstract.jpg)
</center>

```{css, echo = F}
pre code {
  white-space: pre-wrap;
}
```

```{r, include = FALSE}
knitr::opts_chunk$set(
  collapse = TRUE,
  comment = "#>"
)
```

```{r setup, include = FALSE}
# library(uafR)
standard_input = read.csv("standard_data.csv", stringsAsFactors = F)
standard_spread = readRDS("standard_spread.rds")
type_lib = read.csv("type_library.csv")
query_categ = readRDS("query_categorated.rds")
standard_categ = readRDS("standard_categorated.rds")
```

## <span style="color: rgba(80, 0, 96, 1); font-size:120%; background-color: rgba(0, 0, 0, 0.01)">Hello [Chemical] World!</span>

|        <span style="color: black; font-size:115%; background:inherit">Chemistry plays an active role in every aspect of human existence. Whether it be the digested molecules of our food, the solid matrices of plastic and metal that comprise our technology, or the macromolecules that build and run our cells, the compositions are all chemical. To understand this aspect of our existence, there are advanced instruments and techniques that identify chemicals of any system to name. These precise instruments also allow the number of molecules for each individual chemical to be quantified across ana
…[truncated]
```
