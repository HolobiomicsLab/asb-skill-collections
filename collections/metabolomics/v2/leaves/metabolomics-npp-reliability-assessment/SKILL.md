---
name: metabolomics-npp-reliability-assessment
description: Use when you have completed NPP runs from one or more metabolomics tools
  on a set of LC-HRMS mzML files AND you have reference information (target molecule
  list with molecular formula, main adduct, and RT boundaries) available for a subset
  of expected compounds in those files.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - mzRAPP
  - MZmine 2
  - R
  - XCMS
  - enviPat
  - Skyline
  - MSconvert (ProteoWizard)
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/btab231/6214530
  title: mzRAPP
evidence_spans:
- 'You can now start mzRAPP using: library(mzRAPP); callmzRAPP()'
- The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing
  (NPP)
- Below we provided one more example for MZmine2
- Download the XCMS- and MZmine 2-output files from [ucloud]
- library(mzRAPP)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzrapp_cq
    doi: 10.1093/bioinformatics/btab231/6214530
    title: mzRAPP
  dedup_kept_from: coll_mzrapp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab231/6214530
  all_source_dois:
  - 10.1093/bioinformatics/btab231/6214530
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-npp-reliability-assessment

## Summary

Assess the reliability of non-targeted data pre-processing (NPP) workflows in LC-HRMS metabolomics by comparing tool outputs (XCMS, MZmine 2, MS-DIAL, etc.) against a benchmark dataset with known molecules, retention times, and isotopologue patterns. This skill quantifies peak detection rates, isotopologue ratio degradation, and alignment errors to identify data quality deficits.

## When to use

Apply this skill when you have completed NPP runs from one or more metabolomics tools on a set of LC-HRMS mzML files AND you have reference information (target molecule list with molecular formula, main adduct, and RT boundaries) available for a subset of expected compounds in those files. Use it to validate NPP output quality, compare tool performance on the same dataset, or identify which pre-processing steps (alignment, peak picking) degrade isotopologue information.

## When NOT to use

- Input NPP output is already a manually curated, targeted feature table rather than an automated non-targeted output—benchmark comparison is designed for tool-generated peak lists.
- No reference molecule list (target file) with known retention times is available; the skill requires ground truth for validation.
- mzML files are profile-mode (not centroided); mzRAPP requires centroided input for accurate isotopologue boundary detection.

## Inputs

- centroided mzML files (≥5 files recommended, 30 typical)
- sample-group CSV file with columns: sample_name, sample_group
- target file CSV with columns: molecule, SumForm_c, main_adduct, user.rtmin, user.rtmax
- NPP output CSV files (unaligned peaks, aligned peaks) from XCMS, MZmine 2, or other tool
- instrument resolution specification (enviPat library or custom .csv with R and m/z columns)

## Outputs

- benchmark dataset (CSV with 47 molecules, 157 features, 2870 peaks for MTBLS267 scale)
- NPP assessment report with performance metrics (peak detection %, degenerated IR %, split peak count, alignment error count)
- interactive sunburst plot showing distribution of found vs. not-found peaks per molecule
- line plot showing quality of reported NPP peak abundances across isotopologues
- View NPP assessment tab with boxes: Post Alignment, Peak Picking, Alignment Step, Missing Peaks/Values Classification

## How to apply

First, generate a benchmark dataset by loading centroided mzML files, a sample-group CSV file (sample_name, sample_group columns), and a target file (molecule, SumForm_c, main_adduct, user.rtmin, user.rtmax columns) into mzRAPP. mzRAPP extracts ion chromatograms for all enviPat-predicted isotopologues, applies RT boundaries, and filters isotopologues with peak shape correlation <0.85 to most abundant isotopologue or abundance deviation >30% from theory. Next, export the NPP output (unaligned and aligned feature tables as CSV) from your tool of interest. Load both the benchmark and NPP outputs into mzRAPP's NPP assessment module, select the tool name (e.g., 'MZmine'), and execute the comparison. Extract three key metrics from the View NPP assessment tab: (1) post-alignment found peaks percentage and degenerated isotopologue ratio (IR) from the Post Alignment box, (2) split peak count from the Peak Picking box, and (3) alignment errors (BM divergence) from the Alignment Step box. Generate interactive sunburst and line plots showing peak found/not-found distributions and abundance quality. If post-alignment peak detection falls below 80%, degenerated IR >20%, or alignment error rate is high, investigate individual alignment or peak-picking parameters in the upstream tool.

## Related tools

- **mzRAPP** (Primary tool for benchmark generation and NPP reliability assessment; executes performance metric extraction and visualization.) — https://github.com/YasinEl/mzRAPP
- **XCMS** (Example NPP tool whose output is assessed against the benchmark.)
- **MZmine 2** (Example NPP tool whose output is assessed against the benchmark; case study shows 82–92% peak detection.)
- **enviPat** (R package used by mzRAPP to predict isotopologue patterns and validate peak boundaries.)
- **R** (Programming environment for running mzRAPP; vignette() and library(mzRAPP) used for execution.)
- **Skyline** (Optional tool for manual peak curation to export RT boundaries for target file creation.)
- **MSconvert (ProteoWizard)** (Pre-processing step to convert vendor formats to centroided mzML files required by mzRAPP.)

## Examples

```
library(mzRAPP); callmzRAPP()  # Launch Shiny interface, or vignette("Vignette_mzRAPP_Example_workflow") for R-script workflow with benchmark generation and NPP assessment on MTBLS267 data.
```

## Evaluation signals

- Benchmark dataset contains expected count of molecules (47 for MTBLS267), features (157), and peaks (2870); schema validation confirms target file was correctly loaded.
- Post-alignment found peaks percentage for a baseline tool (e.g., XCMS run 3) is in the expected range (93–99%); degenerated IR is 3–20%; values outside literature ranges suggest input or parameter error.
- Peak detection and IR metrics are comparable or better than published benchmarks for the same tool on the same dataset; regression vs. published results indicates upstream tool parameter drift.
- Sunburst plot shows <5% of molecules with 0% peak detection; >80% detection across molecules is a practical quality threshold.
- Split peak count from Peak Picking box is <10% of total peaks; high split rates indicate alignment or noise filtering issues in the NPP tool.

## Limitations

- Benchmark quality depends on target file accuracy; incorrect RT boundaries or molecular formulas will cause false performance degradation.
- Isotopologue filtering (peak shape correlation >0.85, abundance bias <30%) may reject low-abundance isotopologues present in real data, leading to artificially high degenerated IR rates.
- Benchmark is molecule-specific; performance metrics do not generalize to features absent from the target file. Larger, more diverse target lists improve generalizability.
- Alignment error metrics (BM divergence) are relative; absolute interpretation requires domain expertise and comparison to multiple tools on the same data.
- mzRAPP requires centroided mzML input; profile-mode data must be pre-processed with MSconvert, adding conversion artifacts.

## Evidence

- [readme] The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing (NPP; XCMS, XCMS3, MetaboanalystR 3.0, SLAW, XCMS-online, MZmine 2, MZmine 3, MS-DIAL, OpenMS, El-MAVEN,..) in the realm of liquid chromatography high-resolution mass spectrometry (LC-HRMS).: "The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing (NPP; XCMS, XCMS3, MetaboanalystR 3.0, SLAW, XCMS-online, MZmine 2, MZmine 3, MS-DIAL, OpenMS, El-MAVEN,..)"
- [readme] mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues of those target molecules directly from mzML files.: "mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues of those target molecules directly from mzML files."
- [readme] Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed.: "Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed."
- [methods] In the <i>Post Alignment</i> box, we see that now about 82-92% of peaks have been detected, Which is, in our opinion, not bad but improvable. The proportion of degenerated IR is 1-9%: "In the Post Alignment box, we see that now about 82-92% of peaks have been detected, Which is, in our opinion, not bad but improvable. The proportion of degenerated IR is 1-9%"
- [other] Extract and validate the three key performance metrics from the View NPP assessment tab: (a) Post Alignment box for found peaks percentage and degenerated isotopologue ratio (IR), (b) Peak Picking box for total peaks detected and split peak count, (c) Alignment Step box for BM divergence and alignment errors.: "Extract and validate the three key performance metrics from the View NPP assessment tab: (a) Post Alignment box for found peaks percentage and degenerated isotopologue ratio (IR), (b) Peak Picking"
- [methods] Sufficient quality of low peaks was ensured by removing isotopologues that do not satisfy criteria in peak shape (peak shape correlation with most abundant isotopologue) and abundance (Isotopologue ratio bias < 30%): "Sufficient quality of low peaks was ensured by removing isotopologues that do not satisfy criteria in peak shape (peak shape correlation with most abundant isotopologue) and abundance (Isotopologue"
