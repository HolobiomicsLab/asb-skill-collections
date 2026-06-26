---
name: non-targeted-preprocessing-tool-comparison
description: Use when you have LC-HRMS mzML data processed by at least one non-targeted
  pre-processing tool (XCMS, MZmine 2, MZmine 3, MS-DIAL, OpenMS, El-MAVEN, or similar),
  you have access to curated retention time boundaries and molecular formulas for
  a set of known target compounds (ideally 30+ molecules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3635
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - mzRAPP
  - MZmine 2
  - R
  - XCMS
  - enviPat
  - Skyline
  - MSConvert
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# non-targeted-preprocessing-tool-comparison

## Summary

Quantitatively compare the performance of different non-targeted metabolomics data pre-processing tools (XCMS, MZmine 2, MS-DIAL, etc.) against a reference benchmark derived from known target molecules, measuring peak detection rate, isotopologue ratio degradation, and alignment error. This skill enables detection of systematic biases and failure modes in peak picking and alignment workflows before biological interpretation.

## When to use

You have LC-HRMS mzML data processed by at least one non-targeted pre-processing tool (XCMS, MZmine 2, MZmine 3, MS-DIAL, OpenMS, El-MAVEN, or similar), you have access to curated retention time boundaries and molecular formulas for a set of known target compounds (ideally 30+ molecules spanning a range of m/z and RT), and you want to assess whether the tool's reported peak abundances, alignment quality, and isotopologue detection meet acceptable thresholds (e.g., >80% peak recovery, <20% isotopologue ratio degradation) before proceeding to statistical analysis or publication.

## When NOT to use

- You do not have curated retention time boundaries or molecular formulas for target compounds; mzRAPP requires user-provided RT limits for benchmark generation.
- Your mzML files are profile-mode (not centroided); mzRAPP requires centroided input; use MSConvert to centroid first.
- You are comparing tools at the feature-detection stage only and do not care about alignment quality or isotopologue ratio degradation; simpler peak-counting metrics may suffice.
- Your non-targeted tool output cannot be exported as a CSV with m/z, RT, and per-sample abundances; mzRAPP's matching algorithm requires this format.

## Inputs

- Centroided mzML files from LC-HRMS analysis (30 files recommended, minimum 5)
- Non-targeted preprocessing tool output (unaligned peaks CSV with m/z, RT, abundance per sample; aligned peaks CSV with aligned m/z, RT, and abundances)
- Sample-group CSV file (sample_name, sample_group columns)
- Target file CSV (molecule, SumForm_c, main_adduct, user.rtmin, user.rtmax columns; optionally adduct_c, StartTime.EIC, EndTime.EIC, FileName)
- Instrument resolution parameters (selected from enviPat package or custom CSV with R and m/z columns)

## Outputs

- Benchmark dataset CSV (47+ molecules, 157+ features, 2870+ peaks for MTBLS267 scale; contains validated isotopologue peaks with intensity, m/z, RT for each sample and group)
- NPP assessment report (interactive Shiny app tabs: NPP assessment metrics, found/not-found peak sunburst visualization, split peak counts, alignment error distribution)
- Performance metric summaries: post-alignment peak detection percentage (e.g., 82–92%), degenerated isotopologue ratio percentage (e.g., 1–9%), peak abundance quality line plots, alignment error counts and BM divergence scores
- Diagnostic plots (sunburst of peak classification, line plots of reported vs. expected peak abundances, summary statistics table)

## How to apply

First, generate a reference benchmark dataset from the same mzML files using mzRAPP by providing centroided mzML files, a sample-group CSV (mapping file names to treatment groups), a target file with molecular composition (SumForm_c), main adduct (e.g. M+H), and user-curated retention time boundaries (user.rtmin, user.rtmax in seconds) for each target compound. mzRAPP will extract and validate isotopologue peaks meeting quality criteria: peak shape correlation ≥0.85 with the most abundant isotopologue and isotopologue ratio bias <30%. Next, export the non-targeted tool's output (unaligned peaks CSV and aligned peaks CSV) and load both the tool outputs and the benchmark into mzRAPP's assessment module. Select the tool name (e.g., 'MZmine') and run the NPP assessment to compare the tool's detected peaks against benchmark peaks via m/z and retention time matching. Extract the three key performance metrics from the NPP assessment results: (a) Post-Alignment box: percentage of peaks detected and degenerated isotopologue ratio; (b) Peak Picking box: total peaks detected and split peak count; (c) Alignment Step box: BM divergence and alignment error count. Visualize results using mzRAPP's sunburst plot (showing distribution of found/not-found/split peaks) and abundance line plots to assess peak abundance quality. Tools are judged acceptable if post-alignment peak detection is ≥80–90% and degenerated isotopologue ratio is <10–30%, depending on your tolerance.

## Related tools

- **mzRAPP** (Primary software for benchmark generation from known targets and assessment of non-targeted tool performance via peak matching, isotopologue validation, and metrics computation) — https://github.com/YasinEl/mzRAPP
- **XCMS** (Example non-targeted preprocessing tool whose outputs (unaligned and aligned peaks) are compared against mzRAPP benchmark)
- **MZmine 2** (Example non-targeted preprocessing tool whose outputs are imported and assessed for peak detection and alignment quality)
- **enviPat** (R package used by mzRAPP to predict isotopologue patterns and masses for target molecules; provides instrument resolution calibration data)
- **Skyline** (Recommended tool for manual curation of peak boundaries (start/end retention times) that are exported as the target file input for mzRAPP)
- **MSConvert** (ProteoWizard utility for converting vendor mass spectrometry files to centroided mzML format, required input for mzRAPP)

## Examples

```
library(mzRAPP); callmzRAPP()
```

## Evaluation signals

- Benchmark dataset contains expected molecule count (47), feature count (157 including adducts and isotopologues), and total peak count (2870) for MTBLS267-scale input; isotopologue peaks pass quality filters: Pearson correlation ≥0.85 and isotopologue ratio bias <30%.
- Post-alignment peak detection rate falls within tool-specific range (XCMS: 83–99%, MZmine 2: 82–92%); degenerated isotopologue ratio is <10–20% post-alignment; alignment error count and BM divergence are computed and reported.
- Sunburst visualization shows clear separation of found, not-found, and split peaks; majority of benchmark peaks are classified as 'found' (not missed or fragmented).
- Peak abundance line plots show reported peak intensity tracks expected benchmark intensity; slope near 1.0 and R² >0.7 for abundance correlation.
- Tool outputs match benchmark peaks via m/z tolerance (default: 5 ppm) and RT tolerance (narrow at RT boundaries); split peak events (single benchmark peak matched to multiple tool peaks) are counted and visualized separately.

## Limitations

- Benchmark quality depends critically on user-provided retention time boundaries; if RT limits are inaccurate or too broad, false matches and degraded isotopologue ratios may result.
- The benchmark only validates performance on known target compounds; it does not measure sensitivity for novel, untargeted metabolites outside the target list.
- Isotopologue ratio quality filtering (Pearson correlation ≥0.85, ratio bias <30%) removes low-abundance or poorly resolved isotopologues, potentially biasing benchmarks toward easy-to-detect peaks; extreme/edge-case peaks may be underrepresented.
- Peak matching between tool output and benchmark relies on m/z and RT tolerances (default 5 ppm); tools with systematic mass or RT calibration errors may show artificially low performance.
- Currently supports comparison of standard output formats (CSV with m/z, RT, abundance); tools with non-standard or binary output formats require manual export to CSV before assessment.

## Evidence

- [readme] mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues of those target molecules directly from mzML files.: "mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues"
- [readme] The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing (NPP; XCMS, XCMS3, MetaboanalystR 3.0, SLAW, XCMS-online, MZmine 2, MZmine 3, MS-DIAL, OpenMS, El-MAVEN,..) in the realm of liquid chromatography high-resolution mass spectrometry (LC-HRMS).: "reliability assessment of non-targeted data pre-processing (NPP; XCMS, XCMS3, MetaboanalystR 3.0, SLAW, XCMS-online, MZmine 2, MZmine 3, MS-DIAL, OpenMS, El-MAVEN..)"
- [readme] Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed.: "Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 are removed"
- [methods] In the Post Alignment box, we see that about 82-92% of peaks have been detected, Which is, in our opinion, not bad but improvable. The proportion of degenerated IR is 1-9%: "about 82-92% of peaks have been detected...The proportion of degenerated IR is 1-9%"
- [readme] Download all 30 mzML files (at least five if you do not want to process that many) ending on "_POS.mzML" from the repository MTBLS267: "Download all 30 mzML files (at least five if you do not want to process that many) ending on "_POS.mzML" from the repository MTBLS267"
- [readme] In order to generate a benchmark you need to provide your centroided mzML files. Conversion of files of different vendors to mzML as well as centroiding can be done by Proteowizards MSconvert.: "you need to provide your centroided mzML files...centroiding can be done by Proteowizards MSconvert"
- [readme] Maximum spread of mass peaks in the mz dimension to be still considered part of the same chromatogram. <b>mz accuracy [ppm]</b>: Maximum difference between the accurate mz of two: "Maximum spread of mass peaks in the mz dimension to be still considered part of the same chromatogram"
