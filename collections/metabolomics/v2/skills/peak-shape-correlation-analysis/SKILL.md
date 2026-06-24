---
name: peak-shape-correlation-analysis
description: Use when when extracting benchmark peaks from mzML files for multiple
  isotopologues of target molecules, after initial m/z and retention-time matching,
  to validate that detected isotopologue peaks exhibit consistent peak shape and expected
  abundance ratios before including them in a reliability.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - mzRAPP
  - R
  - enviPat
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/btab231/6214530
  title: mzRAPP
evidence_spans:
- 'You can now start mzRAPP using: library(mzRAPP); callmzRAPP()'
- The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing
  (NPP)
- library(mzRAPP)
- mzRAPP extracts and validates chromatographic peaks for which boundaries are provided
  for all (enviPat predicted) isotopologues
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

# peak-shape-correlation-analysis

## Summary

Filter isotopologue peaks by validating their chromatographic shape against the most abundant isotopologue in a cluster, removing peaks with Pearson correlation < 0.85 or intensity ratios deviating >30% from predicted values. This ensures only high-quality isotopologue clusters are retained for benchmark reliability assessment.

## When to use

When extracting benchmark peaks from mzML files for multiple isotopologues of target molecules, after initial m/z and retention-time matching, to validate that detected isotopologue peaks exhibit consistent peak shape and expected abundance ratios before including them in a reliability assessment dataset.

## When NOT to use

- When working with singly-charged or monoisotopic features only (no isotopologue clusters present).
- When isotopologue predictions are unavailable or unreliable for the target molecular formula.
- When the input intensity profiles lack sufficient chromatographic resolution (< 6 scans per peak) to compute meaningful correlation coefficients.

## Inputs

- matched isotopologue peak clusters with m/z, retention time boundaries, and intensity profiles from extracted ion chromatograms
- enviPat-predicted isotopologue abundance ratios for target molecular formulas
- reference (most abundant) isotopologue intensity profile per cluster

## Outputs

- validated isotopologue cluster records retained for benchmark dataset
- filtering flags indicating which isotopologues were removed (low correlation or degenerated ratio)
- benchmark peak table with quality-controlled isotopologue composition

## How to apply

For each isotopologue cluster within a matched benchmark peak: (1) identify the theoretically most abundant isotopologue as the reference; (2) compute Pearson correlation coefficient between the intensity profile (across retention time scans) of each secondary isotopologue and the reference isotopologue; (3) remove any isotopologue with correlation < 0.85; (4) calculate the observed/predicted abundance ratio for each remaining isotopologue using enviPat predictions; (5) remove isotopologues where this ratio deviates by >30% from the predicted value. Retain only isotopologue clusters where at least the reference and one additional isotopologue pass both thresholds. This filtering ensures that abundance distortions caused by co-eluting features or detector artifacts do not corrupt the benchmark.

## Related tools

- **mzRAPP** (Performs peak extraction, isotopologue matching, and applies peak-shape and ratio filters to generate benchmark datasets from mzML files) — https://github.com/YasinEl/mzRAPP
- **enviPat** (Predicts isotopologue m/z values and theoretical abundance ratios for target molecular formulas, enabling validation thresholds)
- **R** (Statistical computation environment for Pearson correlation coefficient calculation and filtering logic)

## Examples

```
library(mzRAPP); callmzRAPP()  # Then in UI: load benchmark peaks → Configure isotopologue validation with peak_shape_correlation >= 0.85 and isotopologue_ratio_bias < 30% → Execute filtering
```

## Evaluation signals

- Pearson correlation coefficient ≥ 0.85 between secondary and reference isotopologue intensity profiles across all retained isotopologues.
- Observed/predicted isotopologue ratio deviation ≤ 30% for all retained isotopologues.
- At least two isotopologues (reference + one secondary) pass both filters for each retained cluster.
- Benchmark dataset reports count and percentage of isotopologues removed due to low correlation vs. degenerated ratio.
- Comparison with NPP tool outputs shows improved degenerated IR metrics (3–20% range vs. baseline 28–53%).

## Limitations

- Pearson correlation threshold (0.85) and ratio bias threshold (30%) are fixed; may not be optimal for all instrument types or sample matrices.
- Filtering assumes that peak shape is predominantly determined by chromatographic behavior; co-eluting peaks or in-source fragmentation can violate this assumption.
- Requires at least the reference isotopologue and one additional isotopologue to be detected; molecules lacking multiple detectable isotopologues are excluded entirely.
- Very low-abundance isotopologues (< 0.05 relative abundance) may fail filtering due to poor signal-to-noise ratio rather than true peak shape mismatch.

## Evidence

- [methods] Peak shape correlation with most abundant isotopologue validation: "Sufficient quality of low peaks was ensured by removing isotopologues that do not satisfy criteria in peak shape (peak shape correlation with most abundant isotopologue)"
- [methods] Isotopologue ratio bias filtering threshold: "removing isotopologues that do not satisfy criteria in peak shape and abundance (Isotopologue ratio bias < 30%)"
- [readme] Correlation coefficient and dual-isotopologue requirement: "Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed."
- [readme] Minimum isotopologue detection for benchmark inclusion: "Only isotopologues for which the theoretically most abundant and at least one additional isotopologue are found are considered for the final benchmark."
- [methods] Performance improvement from filtering: "In the <i>Post Alignment</i> box, we see that now about 93-99% of peaks have been detected, which is quite some improvement. Also, the proportion of degenerated IR decreased to 3-20%."
