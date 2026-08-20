---
name: gradient-performance-encoding
description: Use when when you have extracted retention times from the top detected
  MS1 features in a LC-MS run and need to evaluate whether the gradient spreads those
  compounds efficiently across the available chromatographic time window—particularly
  during iterative gradient optimization where you need a.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Jupyter Notebook
  - bago
  - pyopenms
  - scikit-learn
  techniques:
  - LC-MS
  - direct-infusion-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2023.09.08.556930
  title: BAGO
- doi: 10.1002/9780470508183
  title: ''
evidence_spans:
- Download and install Python 3.8 or later from `python.org`
- model.computeNextGradient()
- A Jupyter Notebook is provided to help you get started with the LC gradient optimization
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bago_cq
    doi: 10.1101/2023.09.08.556930
    title: BAGO
  dedup_kept_from: coll_bago_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2023.09.08.556930
  all_source_dois:
  - 10.1101/2023.09.08.556930
  - 10.1002/9780470508183
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# gradient-performance-encoding

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Encodes LC gradient separation performance as a single normalized metric (0–1) by computing the distribution and spacing of MS1 feature retention times across the chromatographic window. This omics-scale quantification enables rapid evaluation of gradient quality without full compound identification.

## When to use

When you have extracted retention times from the top detected MS1 features in a LC-MS run and need to evaluate whether the gradient spreads those compounds efficiently across the available chromatographic time window—particularly during iterative gradient optimization where you need a fast, single-value performance score for each trial run.

## When NOT to use

- Input already contains a pre-computed separation efficiency or quality score from another tool—avoid redundant re-encoding.
- Retention times are not available or cannot be reliably extracted from raw MS data (e.g., data is already feature-aggregated or m/z-only).
- The chromatographic method is not gradient-based (e.g., isocratic or flow-injection analysis), making gradient time range meaningless.

## Inputs

- rtSeq: list of float (retention times in minutes from top MS1 features)
- rtRange: tuple of float (gradient start time, gradient end time in minutes)
- MS1 feature list or extracted m/z and intensity pairs

## Outputs

- sepEfficiency score: float in range [0.0, 1.0] (normalized separation efficiency metric)
- optionally: distribution statistics (e.g., mean, std dev of retention times across gradient window)

## How to apply

Extract a series of retention times (rtSeq) from the top detected MS1 features and define the gradient time range (rtRange, in minutes) between gradient start and end. Pass both rtSeq and rtRange to the sepEfficiency function, which calculates the distribution and spacing of retention times across the usable gradient window. The function returns a normalized float between 0 (no separation, all compounds elute in a narrow window) and 1 (complete separation, compounds are evenly spread). Validate that the output falls within [0, 1] and that the value reflects realistic separation performance relative to the input feature set—e.g., a score near 1 should correspond to features distributed across most of the gradient duration, while a score near 0 should indicate clustering near the void volume or column dead volume.

## Related tools

- **bago** (Python package providing the sepEfficiency function for calculating separation efficiency from retention times and gradient time range) — https://github.com/huaxuyu/bago
- **pyopenms** (Provides MSExperiment and ms1Spectrum objects for reading and structuring raw LC-MS data prior to retention time extraction)
- **scikit-learn** (Optional utility for preprocessing and standardization of retention time data if normalization is needed before encoding)

## Examples

```
from bago import sepEfficiency; score = sepEfficiency(rtSeq=[2.5, 5.1, 8.3, 12.7, 15.2, 18.9], rtRange=(1.0, 20.0))
```

## Evaluation signals

- Output is a float strictly within [0.0, 1.0]; values outside this range indicate implementation error.
- A separation efficiency score of ~1.0 correlates with retention times spanning >80% of the gradient time window (rtRange); a score of ~0.0 correlates with retention times confined to <10% of the window.
- Increasing the number of well-distributed features (longer rtSeq) with wide spacing should increase or maintain the sepEfficiency score; clustering features in a narrow time band should decrease it.
- Repeating the calculation on the same rtSeq and rtRange produces identical results (deterministic).
- The score reflects the empirical distribution of rtSeq relative to rtRange, not external reference standards—validation should compare gradient trials where manually observed separation quality (e.g., by visual inspection of BPC or extracted ion chromatograms) correlates with the encoded score.

## Limitations

- Encodes only the temporal distribution of detected features; does not account for peak width, tailing, resolution between adjacent peaks, or chemical diversity of separated compounds.
- Depends critically on accurate retention time extraction from MS1 scans; errors or artifacts in feature detection will propagate to the efficiency score.
- Assumes the gradient time range (rtRange) is correctly specified; if rtRange does not correspond to the actual gradient employed, the score becomes uninterpretable.
- At omics scale, the score averages performance across hundreds or thousands of features; localized separation failures in one region of the gradient may be masked by strong separation elsewhere.
- No changelog available for version tracking or changes to the sepEfficiency algorithm implementation.

## Evidence

- [other] Extract or receive a series of retention times (rtSeq) from the top detected MS1 features and the gradient time range (rtRange, in minutes): "Extract or receive a series of retention times (rtSeq) from the top detected MS1 features and the gradient time range (rtRange, in minutes) defining when the gradient begins and ends."
- [other] sepEfficiency function calculates separation efficiency using a series of retention times extracted from LC-MS data: "The sepEfficiency function calculates separation efficiency using a series of retention times extracted from LC-MS data, producing a singular metric that encodes compound-separation performance for"
- [other] Return a normalized float value between 0 (no separation) and 1 (complete separation): "Return a normalized float value between 0 (no separation) and 1 (complete separation) that quantifies how effectively the gradient spreads compounds across the chromatographic window."
- [readme] Separation efficiency was defined to evaluate the performance of a gradient: "Separation efficiency was defined to evaluate the performance of a gradient."
- [methods] Calculate the separation efficiency using a series of retention times: "sepEfficiency - calculate separation efficiency from retention times: Calculate the separation efficiency using a series of retention times"
