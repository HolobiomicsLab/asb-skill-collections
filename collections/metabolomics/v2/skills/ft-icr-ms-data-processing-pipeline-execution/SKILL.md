---
name: ft-icr-ms-data-processing-pipeline-execution
description: Use when you have FT-ICR MS peak abundance data in Formularity .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - MetaboDirect
  - Python
  - R
  - NumPy
  - pandas
  - seaborn
  - matplotlib
  - Formularity
  - KEGGREST
  - vegan
  - SYNCSA
  - CoreMS
  - py4cytoscape
  - Cytoscape
  - UltraMassExplorer
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- Molecular transformation networks for each sample (mass difference network-based approach) are generated in this step
- The MetaboDirect pipeline consists of 6 major steps/categories (Fig. 1)
- The MetaboDirect pipeline was developed in Python 3.8 [38]
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- requires the Python dependencies NumPy [40], pandas [41, 42]
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39] and is available to install through the Python Package Index... It requires the Python dependencies NumPy
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect_cq
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-023-01476-3
  all_source_dois:
  - 10.1186/s40168-023-01476-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ft-icr-ms-data-processing-pipeline-execution

## Summary

Execute the MetaboDirect command-line pipeline to process direct-injection FT-ICR MS datasets through automated data pre-processing, diagnostics, exploration, chemodiversity analysis, statistical analysis, and optional transformation network generation. This skill transforms raw peak lists with assigned molecular formulas (in Formularity .csv format) into normalized, filtered, annotated datasets with Van Krevelen diagrams, elemental composition plots, diversity metrics, and biochemical transformation networks.

## When to use

You have FT-ICR MS peak abundance data in Formularity .csv format (with assigned molecular formulas, m/z values, and peak intensities) from one or more samples, and you need to perform end-to-end automated analysis including peak filtering (by m/z range, isotopic presence, formula assignment error ≤0.5 ppm, and sample prevalence threshold), molecular class assignment, thermodynamic index calculation, diversity metrics (via vegan/SYNCSA R packages), multivariate statistical analysis, and optional KEGG pathway annotation or mass-difference-based transformation networks.

## When NOT to use

- Input data is already processed, normalized, and filtered by another pipeline — MetaboDirect is designed for raw peak lists and would be redundant.
- FT-ICR MS data lacks pre-assigned molecular formulas or is in an unsupported format (not Formularity .csv); pre-processing tools like Formularity or CoreMS must be run first.
- Analysis goal is only chromatographic separation or isomer disambiguation — FT-ICR MS direct injection cannot resolve chemical isomers, and MetaboDirect does not perform compound-level separation.

## Inputs

- Formularity .csv file with assigned molecular formulas, m/z values, peak intensities, and sample identifiers
- Peak abundance list in MetaboDirect-compatible format
- User-defined parameter configuration (m/z range, formula error threshold, sample prevalence cutoff, normalization method)

## Outputs

- Filtered and normalized peak intensity matrix
- Molecular class and elemental composition assignments
- Van Krevelen diagrams
- Elemental and molecular class composition plots
- Chemodiversity metrics (alpha and beta diversity indices from vegan/SYNCSA)
- Multivariate statistical analysis results
- Biochemical transformation network (mass-difference-based, optional)
- KEGG pathway and module annotations (optional)
- Summary statistics and diagnostic plots
- Execution time benchmarks

## How to apply

Install MetaboDirect (v0.3.4 or later) from PyPI with all Python dependencies (numpy, pandas, seaborn, py4cytoscape, statsmodels, more-itertools) and R dependencies (tidyverse, vegan, SYNCSA, ggpubr, KEGGREST, factoextra, UpSetR, pmartR, ggvenn, ggrepel, RColorBrewer, ggnewscale) and Cytoscape (≥3.8) with FileTransfer plugin. Prepare input as Formularity .csv with columns for assigned formulas, m/z, intensities, and sample identifiers. Execute the pipeline via a single command specifying the input file, user-defined thresholds for peak m/z filtering, formula error tolerance (default 0.5 ppm), sample prevalence cutoff, and normalization method. The pipeline automatically executes all six steps (pre-processing, diagnostics, exploration, chemodiversity, statistics, optional transformation networks) in sequence. Optionally enable KEGG database querying via KEGGREST to annotate detected formulas with putative pathway and module assignments. Record wall-clock execution time for each configuration (main pipeline vs. with KEGG vs. with transformation networks) to establish computational benchmarks.

## Related tools

- **Formularity** (Signal processing and molecular formula assignment for raw FT-ICR MS data; produces .csv input files for MetaboDirect)
- **CoreMS** (Alternative open-source framework for signal processing and sample-agnostic molecular formula assignment prior to MetaboDirect analysis)
- **vegan** (R package for calculating diversity metrics (alpha and beta diversity indices) in the chemodiversity analysis step)
- **SYNCSA** (R package for computing diversity metrics used in MetaboDirect's chemodiversity analysis)
- **KEGGREST** (R package for querying KEGG database to annotate detected molecular formulas with putative pathway and module assignments)
- **py4cytoscape** (Python interface to Cytoscape for rendering and exporting biochemical transformation networks)
- **Cytoscape** (Network visualization platform (≥v3.8 with FileTransfer plugin) for displaying mass-difference-based transformation networks generated by MetaboDirect)
- **UltraMassExplorer** (Alternative web-based FT-ICR MS analysis platform; MetaboDirect offers greater automation and command-line flexibility)

## Examples

```
metabodirect -i bacterium_phage_dataset.csv -m 200 2000 -e 0.5 -p 0.5 --normalize intensity --enable-kegg --enable-transformations
```

## Evaluation signals

- Verify that all six pipeline steps (pre-processing, diagnostics, exploration, chemodiversity, statistical analysis, transformation network) completed without errors and generated expected output files (plots, tables, network files).
- Compare output execution times against published benchmarks: 40-sample dataset <1 minute (main), 120-sample dataset ~2 minutes (main); bacterium-phage dataset (36 samples, 495 avg peaks) ~36 seconds (main), ~10 minutes (with KEGG), ~21 minutes (full with transformation networks); S. fallax dataset (4 samples, 1793 avg formulas) ~30 seconds (main), ~32 minutes (full).
- Confirm that filtered peak count matches user-defined thresholds for m/z range, isotopic presence, formula error (≤0.5 ppm), and sample prevalence cutoff applied during pre-processing.
- Validate that Van Krevelen diagrams, elemental composition plots, and diversity metric tables are generated and contain non-zero entries consistent with input dataset complexity.
- When KEGG annotation is enabled, verify that returned pathway and module annotations are non-empty and correspond to detected molecular formulas; when transformation networks are generated, confirm that mass-difference network contains edges with defined transformation types and node attributes.

## Limitations

- FT-ICR MS cannot separate chemical isomers; MetaboDirect cannot distinguish between isomeric forms and will treat them as a single formula.
- Ion suppression and enhancement effects from direct injection MS can bias peak intensity estimates; MetaboDirect does not correct for these analytical artifacts and relies on input data quality.
- Existing FT-ICR MS software in general incurs a compromise between flexibility/customizability and user-friendliness; while MetaboDirect optimizes for ease of use via single-command execution, deep customization of individual pipeline steps requires code modification.
- KEGG database querying introduces external dependency and potential latency; KEGGREST queries may fail or return incomplete annotations for rare or novel formulas not in the KEGG database.

## Evidence

- [abstract] MetaboDirect requires only a single line of code to launch a fully automated framework for the generation and visualization of FT-ICR MS metabolomic data analysis: "MetaboDirect is superior in that it requires a single line of code to launch a fully automated framework for the generation and visualization"
- [methods] The six main steps of the MetaboDirect pipeline are data pre-processing, data diagnostics, data exploration, chemodiversity analysis, statistical analysis, and transformation network analysis: "The MetaboDirect pipeline consists of six main steps for the analysis of FT‑ICR MS data"
- [methods] Peaks are filtered by m/z values, isotopic presence (13C peaks), error in formula assignment (0.5 ppm), and number of samples present with user-determined thresholds: "detected peaks are filtered by their m/z values (based on the user's input) isotopic presence (13C peaks) error in formula assignment (0.5 ppm) based on the number of samples that they are present in"
- [methods] Diversity metrics are calculated using functions from the R packages vegan and SYNCSA in the chemodiversity analysis step: "calculate diversity metrics using functions from the R packages vegan and SYNCSA"
- [abstract] MetaboDirect uniquely generates biochemical transformation networks automatically based on mass differences using a mass-difference network-based approach: "MetaboDirect is also uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences (mass difference network‑based approach)"
- [other] Benchmarking results show MetaboDirect processed 40 samples in less than 1 minute and 120 samples in 2 minutes for main pipeline steps: "MetaboDirect processed 40 samples in <1 minute and 120 samples in 2 minutes for main pipeline steps"
- [methods] Input data must be in Formularity .csv format with assigned molecular formulas, peak intensities, and m/z values: "each in Formularity .csv format (assigned molecular formulas, peak intensities, m/z values)"
- [readme] MetaboDirect requires Python 3.5 and above, R 4 and above, Cytoscape 3.8 and above with specific Python and R library dependencies: "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above)"
- [other] KEGG database can be queried via KEGGREST to obtain putative pathway and module annotations for detected molecular formulas: "query the KEGG database via KEGGREST to obtain putative pathway and module annotations"
- [other] The complete MetaboDirect pipeline code is freely available in its GitHub repository, version 0.3.4 used for analyses: "The code of the MetaboDirect pipeline used for this analysis (v0.3.4) is available in its GitHub repository"
