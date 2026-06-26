---
name: batch-effect-correction-chromatography
description: Use when when analyzing untargeted LC/HRMS data from population-scale
  projects (n > 500) spanning multiple sample batches or instrument runs, peaks with
  identical or near-identical m/z values appear at systematically shifted retention
  times across batches due to instrument drift, column aging, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - IDSL.IPA
  - R
  - xcms
  - MZmine 2
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.2c00120
  title: IDSL.IPA
evidence_spans:
- '**Intrinsic Peak Analysis (IPA)** by the [**Integrated Data Science Laboratory
  for Metabolomics and Exposomics (IDSL.ME)**](https://www.idsl.me) is a light-weight
  R package'
- light-weight R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idsl_ipa_cq
    doi: 10.1021/acs.jproteome.2c00120
    title: IDSL.IPA
  dedup_kept_from: coll_idsl_ipa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00120
  all_source_dois:
  - 10.1021/acs.jproteome.2c00120
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# batch-effect-correction-chromatography

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Retention time correction across multiple LC/HRMS batches aligns peaks with similar m/z and RT profiles, harmonizing retention times to enable reliable downstream peak annotation and quantification in population-scale untargeted studies. This corrects instrumental drift and batch-to-batch chromatographic variation that would otherwise confound peak identity across samples.

## When to use

When analyzing untargeted LC/HRMS data from population-scale projects (n > 500) spanning multiple sample batches or instrument runs, peaks with identical or near-identical m/z values appear at systematically shifted retention times across batches due to instrument drift, column aging, or environmental factors. Apply this skill before peak annotation and alignment to ensure that the same compound is not reported as multiple distinct features.

## When NOT to use

- Input data is from a single batch or single instrument run (no batch-to-batch drift to correct).
- Endogenous reference markers or anchor compounds are not reliably detected or are absent across all batches.
- Retention time variation is caused by real biological or chemical differences (e.g., derivatization, column selectivity) rather than instrumental drift — correcting this would conflate distinct species.

## Inputs

- Multi-batch LC/HRMS raw data files (mzXML, mzML, netCDF formats)
- Extracted ion chromatogram (EIC) candidate peak lists with uncorrected retention time and m/z for each batch
- IPA parameter spreadsheet with retention time correction settings and endogenous reference marker specifications
- List of known endogenous reference compounds or internal standards expected in all batches

## Outputs

- Batch-corrected peak table with harmonized retention times across all samples
- Retention time correction offset model (per-batch RT shift parameters)
- Aligned peak table indexed by corrected m/z and RT coordinates
- Batch-level RT correction diagnostics (e.g., offset magnitude, alignment statistics)

## How to apply

Load extracted ion chromatogram (EIC) candidate peaks from all batches into IDSL.IPA, preserving their retention time and m/z values. The retention time correction algorithm identifies endogenous reference markers (or user-specified anchor compounds) that appear consistently across batches and uses their RT shifts to model a batch-specific correction curve. Apply this RT offset model to all peaks within each batch, then re-align peaks across batches using the corrected retention times. Generate a corrected peak table with harmonized retention times for each batch, enabling reliable peak matching by m/z ± tolerance and corrected RT ± tolerance. Validate correction by checking that peak clusters expected to be identical across batches now show reduced RT spread (e.g., within 10–30 seconds).

## Related tools

- **IDSL.IPA** (Primary tool implementing retention time correction, EIC candidate generation, peak detection, and peak property evaluation for batch alignment in LC/HRMS) — https://github.com/idslme/IDSL.IPA
- **R** (Runtime environment for IDSL.IPA package and user-defined correction workflows)
- **xcms** (Alternative peak picking and alignment tool for comparison; does not natively implement IDSL.IPA's retention time correction method)
- **MZmine 2** (Comparative peak picking tool; IDSL.IPA outperforms it in sensitivity and specificity)

## Examples

```
library(IDSL.IPA); IPA_workflow("path/to/IPA_parameters.xlsx")
```

## Evaluation signals

- Corrected retention times for the same compound cluster within each batch show reduced spread (< 15–30 sec) compared to uncorrected data.
- Peak alignment table shows increased number of matched peaks across batches at the same corrected m/z and RT coordinates, with fewer singleton or duplicate features.
- Endogenous reference markers used for correction align to within ± 5–10 seconds across all batches after correction.
- Pairwise correlations list shows increased peak height correlations for expected adducts and isotopologues after RT correction.
- Batch correction offset parameters remain stable and within expected instrumental drift ranges (typically < 1–3 min over multi-batch runs).

## Limitations

- Correction quality depends on availability and consistency of endogenous reference markers across all batches; sparse or missing markers reduce model robustness.
- Algorithm assumes RT drift is systematic and can be modeled by a smooth function; non-linear or highly variable instrumental behavior may not be corrected accurately.
- Correction does not account for m/z drift; separate recursive mass correction is required for accurate mass alignment.
- Population-scale studies (n >> 100) may require parameter tuning for different instrument types, columns, or LC gradients; default parameters may not be optimal.
- Changelog is not provided in the repository, limiting visibility into algorithmic changes or corrections across versions.

## Evidence

- [intro] retention time correction across multiple batches: "recursive mass correction, retention time correction across multiple batches and peak annotation"
- [intro] Algorithm design for multi-batch alignment: "IDSL.IPA is a suite of new algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation, recursive mass correction, retention time correction"
- [readme] Use of endogenous reference markers: "Retention time correction using endogenous reference markers for multi-batch large scale studies"
- [readme] Population-scale scope and output formats: "Individual peaklists for each HRMS file in *.Rdata* and *.csv* formats in the "peaklists" directory. 5.2. Peak alignment tables in the "peak_alignment" directory"
- [readme] Application domain and input types: "To process your mass spectrometry data (**mzXML**, **mzML**, **netCDF**), download the [IPA parameter spreadsheet]"
