---
name: mass-spectral-relationship-matching
description: Use when after peak detection and feature table generation when you have a collection of m/z, retention time, and intensity values and need to identify which features are related variants (isotopes, adducts, or fragments) of the same parent compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3648
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - masscube
  - Python
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-025-60640-5
  title: MassCube
evidence_spans:
- masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing.
- masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing
- masscube is an integrated Python package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_masscube_cq
    doi: 10.1038/s41467-025-60640-5
    title: MassCube
  dedup_kept_from: coll_masscube_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-60640-5
  all_source_dois:
  - 10.1038/s41467-025-60640-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectral-relationship-matching

## Summary

Annotate and group LC-MS features as isotopes, adducts, or in-source fragments by matching mass shifts and neutral loss patterns within retention time windows. This skill enables confident assignment of feature relationships that reflect the same underlying molecular entity.

## When to use

Apply this skill after peak detection and feature table generation when you have a collection of m/z, retention time, and intensity values and need to identify which features are related variants (isotopes, adducts, or fragments) of the same parent compound. Use it as a prerequisite for downstream annotation and compound identification workflows where grouping related features improves molecular hypothesis confidence.

## When NOT to use

- Input is already a grouped or curated metabolite list rather than raw detected features.
- Data from instruments or workflows where isotope envelopes or adduct formation are suppressed by design (e.g., some targeted methods with deliberate desalting).
- Feature table lacks reliable retention time information needed to enforce co-elution constraints.

## Inputs

- Feature table with m/z, retention time (RT), and intensity columns
- Detection parameters: isotope mass tolerance, adduct mass shifts, neutral loss patterns
- Retention time window threshold for co-elution

## Outputs

- Annotated feature table with group ID column
- Annotation label column (isotope, adduct, in-source fragment, or unrelated)
- Feature relationship network (implied by group membership)

## How to apply

Load the detected feature table containing m/z, retention time, and intensity columns. Sequentially apply three relationship detection engines: (1) Isotope detection: identify features differing by ~1.003 Da (carbon-13 shift) within a retention time window to group isotope envelopes. (2) Adduct detection: match features related by known adduct mass shifts (+H, +Na, +NH4, +K, –H) to identify multiply-charged or adducted ions. (3) In-source fragment detection: match features related by characteristic neutral loss patterns (–H2O, –NH3) to capture in-source fragmentation relationships. Assign each feature a group ID and an annotation label (isotope, adduct, or fragment) based on the detected relationships, then output the annotated feature table with group membership preserved. The retention time co-elution constraint ensures only chemically plausible relationships are confirmed.

## Related tools

- **masscube** (Integrated Python package that implements isotope, adduct, and in-source fragment detection and grouping for LC-MS feature tables.) — https://github.com/huaxuyu/masscube/

## Evaluation signals

- Every feature in the output table has been assigned a group ID and an annotation label (no missing or null values).
- Features assigned to the same group share a plausible mass relationship (isotope ±1.003 Da, adduct ±expected shift, fragment via known neutral loss) and co-elute within the specified retention time window.
- Isotope groups show monotonic intensity decrease from lighter to heavier isotopologues, consistent with natural abundance ratios.
- Adduct groups link the same molecular mass (M) under different ionization forms; verify by recalculating [M+adduct] for each member.
- In-source fragment groups show lower m/z and/or intensity compared to their parent feature, consistent with neutral loss mechanism.

## Limitations

- Accuracy depends on reliable m/z calibration and retention time alignment; poor peak detection or significant RT drift will confound relationship matching.
- Overlapping retention time windows and similar mass shifts (e.g., adduct +Na vs. in-source loss of water on a heavier ion) can cause misassignment; manual review of high-confidence matches is recommended for downstream use.
- The skill is designed for nontargeted LC-MS data; targeted or data-independent acquisition (DIA) workflows may require adapted parameters or thresholds.

## Evidence

- [other] masscube implements a feature group annotation mechanism that confidently labels features as isotopes, adducts, and in-source fragments.: "masscube implements a feature group annotation mechanism that confidently labels features as isotopes, adducts, and in-source fragments."
- [other] Apply isotope detection logic to identify features differing by 1.003 Da (carbon-13 isotope shift) within a retention time window. Apply adduct detection to identify features related by common adduct mass shifts (e.g., +H, +Na, +NH4, +K, –H). Apply in-source fragment detection to identify features related by characteristic neutral loss patterns (e.g., –H2O, –NH3).: "Apply isotope detection logic to identify features differing by 1.003 Da (carbon-13 isotope shift) within a retention time window. Apply adduct detection to identify features related by common adduct"
- [readme] Confident annotation of feature groups including isotopes, adducts and in-source fragments.: "Confident annotation of feature groups including isotopes, adducts and in-source fragments."
- [other] Load the feature table (containing m/z, retention time, and intensity values for detected features).: "Load the feature table (containing m/z, retention time, and intensity values for detected features)."
- [other] Assign each feature a group ID and annotation label (isotope, adduct, or fragment) based on detected relationships.: "Assign each feature a group ID and annotation label (isotope, adduct, or fragment) based on detected relationships."
