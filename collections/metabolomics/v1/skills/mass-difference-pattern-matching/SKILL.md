---
name: mass-difference-pattern-matching
description: Use when after peak picking and sample alignment when you have an aligned feature table containing m/z and retention time coordinates. Use it when your untargeted LC-MS workflow needs to reduce feature redundancy caused by naturally occurring stable isotope patterns and common adduct formation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3557
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - Centwave
  - SLAW grouping module
derived_from:
- doi: 10.1021/acs.analchem.1c02687
  title: slaw
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_slaw
    doi: 10.1021/acs.analchem.1c02687
    title: slaw
  dedup_kept_from: coll_slaw
schema_version: 0.2.0
---

# mass-difference-pattern-matching

## Summary

Grouping of detected LC-MS features into isotopologue and adduct clusters by identifying features that share the same molecular ion but differ by characteristic mass shifts (e.g., C13, N15, D isotopes or [M+H]+, [M+Na]+, [M+NH4]+ adducts). This skill consolidates redundant ion representations into interpretable molecular entities for downstream analysis.

## When to use

Apply this skill after peak picking and sample alignment when you have an aligned feature table containing m/z and retention time coordinates. Use it when your untargeted LC-MS workflow needs to reduce feature redundancy caused by naturally occurring stable isotope patterns and common adduct formation. This is especially important for large-scale studies where thousands of features need to be grouped to improve feature interpretability and reduce false positives in annotation.

## When NOT to use

- Input is already a consolidated feature matrix with isotopologues and adducts pre-merged or manually curated.
- DIA (data-independent acquisition) experiments without DDA-MS2 data, which the SLAW workflow does not support.
- Profile-mode (non-centroided) mzML data, which must be centroided prior to peak picking and grouping.

## Inputs

- aligned feature table (m/z and retention time coordinates from sample alignment step)
- centroided mzML files (optional, for reference detection)

## Outputs

- grouped feature table with isotopologue/adduct cluster identifiers
- feature-to-cluster membership annotations

## How to apply

Load the aligned feature table (output from sample alignment) containing detected m/z and retention time coordinates. Apply the isotopologue and adduct grouping algorithm to cluster features that share the same molecular ion with mass differences corresponding to isotopic shifts (C13 ≈ +1.00335 Da, N15 ≈ +0.99703 Da, D ≈ +1.00628 Da) or common adduct transformations ([M+H]+ vs [M+Na]+ ≈ +21.98 Da, [M+H]+ vs [M+NH4]+ ≈ +18.03 Da). The algorithm uses retention time co-elution as a constraint to ensure grouped features originate from the same molecule. Assign cluster identifiers to each feature and output the grouped feature table with isotopologue/adduct group membership annotations, which can then be propagated to downstream gap-filling and annotation steps.

## Related tools

- **SLAW grouping module** (Performs isotopologue and adduct clustering on aligned features as part of the complete untargeted LC-MS workflow) — https://github.com/zamboni-lab/SLAW
- **Centwave** (Peak picking algorithm that precedes the grouping step; provides initial feature detection) — https://github.com/zamboni-lab/SLAW

## Evaluation signals

- All features within a cluster share retention time within the expected co-elution window (typically ±5–10 seconds in LC-MS).
- Mass differences between cluster members match known isotope shifts (C13, N15, D) or adduct mass differences within measurement tolerance (typically <5 ppm).
- No feature is assigned to multiple clusters; cluster membership is mutually exclusive.
- Cluster size distribution is reasonable (singletons acceptable, but spurious large clusters suggest incorrect grouping parameters).
- Downstream gap-filling and feature annotation steps show improved consistency when using grouped versus ungrouped feature tables (e.g., fewer conflicting annotations per molecular entity).

## Limitations

- Grouping accuracy depends on retention time alignment quality; poor sample alignment will propagate errors into isotopologue/adduct assignment.
- Mass tolerance parameters must be tuned based on instrument resolution; too loose tolerance may merge unrelated features, too tight may fail to group true isotopologues.
- Complex metabolite mixtures with high feature density may result in ambiguous assignments when multiple candidate clusters are equally plausible within tolerance windows.
- High-resolution instruments (e.g., Orbitrap) perform better than low-resolution instruments; algorithm assumes sufficient mass accuracy to distinguish isotope patterns from noise.

## Evidence

- [other] SLAW includes a processing step for grouping of isotopologues and adducts as part of its complete untargeted LC-MS workflow, which operates after peak picking and sample alignment.: "SLAW includes a processing step for grouping of isotopologues and adducts as part of its complete untargeted LC-MS workflow, which operates after peak picking and sample alignment."
- [other] Apply isotopologue and adduct grouping algorithm to cluster features sharing the same molecular ion with mass differences corresponding to isotopic shifts (e.g., C13, N15, D) or common adduct transformations (e.g., [M+H]+, [M+Na]+, [M+NH4]+).: "Apply isotopologue and adduct grouping algorithm to cluster features sharing the same molecular ion with mass differences corresponding to isotopic shifts (e.g., C13, N15, D) or common adduct"
- [readme] Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion: "Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion"
- [readme] All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard.: "All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard."
