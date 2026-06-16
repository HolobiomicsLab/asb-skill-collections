### `paper.md`
```
# shuzhao-li-lab__PythonCentricPipelineForMetabolomics

## Introduction

# Introduction 

[![Documentation Status](https://readthedocs.org/projects/pythoncentricpipelineformetabolomics/badge/?version=latest)](https://pythoncentricpipelineformetabolomics.readthedocs.io/en/latest/?badge=latest)

The Python-Centric Pipeline for Metabolomics is designed to take raw LC-MS metabolomics data and ready them for downstream statistical analysis. The pipeline can 
- convert Thermo .raw to mzML (ThermoRawFileParser)
- process mzML data to feature tables (Asari)
- perform quality control
- data normalization and batch correction
- pre-annotation to group featues to empirical compounds (khipu)
- perform MS1 annotation using an authentic compound library, a public database (e.g. HMDB, LIPID MAP), or custom database
- perform MS2 annotation (matchms) using a custom database (default MoNA)
- output data in standardized formats (.txt, JSON), ready for downstream analysis

Asari supports a visual dashboard to explore and inspect individual features.
We are working to add supports of GC and other data types.

Note that to replicate the presented results you will need to run the `download extras` command. See below.

# Citations

Please cite these publications if you use PCPFM and Asari:

- Mitchell, J.M., Chi, Y., Thapa, M., Pang, Z., Xia, J. and Li, S., 2024. Common data models to streamline metabolomics processing and annotation, and implementation in a Python pipeline. PLOS Computational Biology, 20(6), p.e1011912. (https://doi.org/10.1371/journal.pcbi.1011912)

-

## Methods

# Introduction 

[![Documentation Status](https://readthedocs.org/projects/pythoncentricpipelineformetabolomics/badge/?version=latest)](https://pythoncentricpipelineformetabolomics.readthedocs.io/en/latest/?badge=latest)

The Python-Centric Pipeline for Metabolomics is designed to take raw LC-MS metabolomics data and ready them for downstream statistical analysis. The pipeline can 
- convert Thermo .raw to mzM
…[truncated]
```
