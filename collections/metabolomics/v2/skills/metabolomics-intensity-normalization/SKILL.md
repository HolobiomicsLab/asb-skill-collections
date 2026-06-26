---
name: metabolomics-intensity-normalization
description: Use when your input is a raw metabolomics intensity matrix (compounds
  × samples) with known batch assignment and QC sample labels, and you observe signal
  drift across the analytical sequence or batch-to-batch variation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Metanorm
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2025.09.30.679445v1
  title: Metanorm
- doi: 10.1021/acs.analchem.5c06841
  title: ''
evidence_spans:
- The R package implements three (new) robust normalization methods
- Metanorm supports robust metabolomics data normalization across scales and experimental
  designs
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metanorm_cq
    doi: 10.1101/2025.09.30.679445v1
    title: Metanorm
  dedup_kept_from: coll_metanorm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.09.30.679445v1
  all_source_dois:
  - 10.1101/2025.09.30.679445v1
  - 10.1021/acs.analchem.5c06841
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-intensity-normalization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply robust normalization methods (tGAM, rGAM, rLOESS, QC-RLSC, QC-RSC) to correct for signal drift and batch effects in untargeted metabolomics intensity matrices. This skill removes systematic variation across analytical runs while preserving biological signal, essential for cross-batch and multi-scale metabolomics studies.

## When to use

Your input is a raw metabolomics intensity matrix (compounds × samples) with known batch assignment and QC sample labels, and you observe signal drift across the analytical sequence or batch-to-batch variation. Apply this skill before statistical testing or multivariate analysis to enable fair comparison of biological samples.

## When NOT to use

- Input is already normalized or has had batch effects removed by other methods.
- You have no QC samples or batch labels in your experimental design.
- Your data are already feature-level (e.g., peak areas with retention time alignment complete); normalization requires raw intensity values prior to feature extraction.

## Inputs

- Unnormalized metabolomics intensity matrix (numerical matrix: rows = compounds, columns = samples)
- Batch assignment vector (character or factor, one entry per sample)
- QC sample type vector (character or factor, entries: 'QC' or other sample type labels)

## Outputs

- Normalized metabolomics intensity matrix (same dimensions as input)
- Diagnostic plots: intensity vs. run order pre- and post-normalization (per compound)
- PCA score plots before and after normalization (labeled by batch)

## How to apply

Load the raw intensity matrix (rows = compounds, columns = samples), batch vector, and QC sample type labels into R. Install Metanorm from GitHub and call the metanorm() function with your chosen model (tGAM recommended for superior robustness; rGAM or rLOESS for faster computation). Set QCcheck=TRUE to verify QC samples are representative of the batch. Optionally set QConly=TRUE if using legacy methods (QC-RLSC, QC-RSC) that require QC samples only; for tGAM, rGAM, and rLOESS, include both QC and biological samples for normalization. Generate diagnostic plots (intensity vs. run order, pre/post PCA) to visually confirm drift correction and assess whether batch effects have diminished. Export the normalized intensity matrix for downstream analysis.

## Related tools

- **Metanorm** (R package implementing five robust normalization methods (tGAM, rGAM, rLOESS, QC-RLSC, QC-RSC) and diagnostic plotting functions for metabolomics intensity data) — https://github.com/UGent-LIMET/Metanorm
- **R** (Runtime environment for executing Metanorm and data manipulation workflows (≥4.4.0 required)) — https://cloud.r-project.org/index.html

## Examples

```
library(metanorm); load(system.file('extdata', 'example.RData', package = 'metanorm')); normdat <- metanorm(rawdata[1:5,], model = 'tGAM', type = metanorm.qc, QCcheck = TRUE, batch = batch, plotdir = '~/metanormExample/')
```

## Evaluation signals

- PCA score plots show reduced or eliminated clustering by batch after normalization (visual confirmation of drift correction).
- Individual compound intensity vs. run order plots exhibit flattened trend lines post-normalization, with stable mean intensity across the analytical sequence.
- QC sample intensities remain consistent pre- and post-normalization (QC samples should not be artificially altered by the normalization).
- Biological sample relative abundances are preserved: fold-change ratios between sample groups remain stable or improve in signal-to-noise ratio.
- Metanorm QCcheck diagnostic output confirms QC samples are representative (no flagged discrepancies between QC and biological sample distributions).

## Limitations

- tGAM offers superior robustness but may be slower than rGAM or rLOESS; runtimes scale with number of compounds and samples.
- Normalization assumes systematic drift is smooth and monotonic or quasi-periodic; sharp instrumental failures or abrupt baseline shifts may not be fully corrected.
- Results depend on the representativeness of QC samples; if QC samples do not span the chemical space of biological samples, normalization may be suboptimal.
- The method is designed for untargeted metabolomics; applicability to targeted assays or non-LC-MS platforms has not been evaluated in the cited work.

## Evidence

- [readme] Metanorm supports robust metabolomics data normalization across scales and experimental designs. The R package implements three (new) robust normalization methods (tGAM, rGAM and rLOESS), alongside formerly proposed ones (QC-RLSC, QC-RSC).: "Metanorm supports robust metabolomics data normalization across scales and experimental designs. The R package implements three (new) robust normalization methods (tGAM, rGAM and rLOESS), alongside"
- [readme] tGAM is recommended due to its superior robustness, but rGAM and rLOESS are faster.: "tGAM is recommended due to its superior robustness, but rGAM and rLOESS are faster."
- [readme] We further recommend using both QC as well as biological samples for normalization, and to have metanorm check for discrepancies between QC and biological samples.: "We further recommend using both QC as well as biological samples for normalization, and to have metanorm check for discrepancies between QC and biological samples."
- [readme] Normalizing the data is achieved by calling the metanorm function. normalize the first 5 compounds in the example dataset using the (default) tGAM method normdat <- metanorm(rawdata[1:5,], model = 'tGAM', type = metanorm.qc, QCcheck = TRUE, batch = batch, plotdir = '~/Documents/metanormExample/'): "normalize the first 5 compounds in the example dataset using the (default) tGAM method normdat <- metanorm(rawdata[1:5,], model = 'tGAM', type = metanorm.qc, QCcheck = TRUE, batch = batch, plotdir ="
- [readme] Individual compound pre- vs. post-normalization intensity vs. order plots can be retrieved from the plotdir directory. These allow finegrained assessment of normalization performance.: "Individual compound pre- vs. post-normalization intensity vs. order plots can be retrieved from the plotdir directory. These allow finegrained assessment of normalization performance."
