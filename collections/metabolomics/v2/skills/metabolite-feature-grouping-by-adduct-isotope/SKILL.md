---
name: metabolite-feature-grouping-by-adduct-isotope
description: Use when immediately after generating a feature table (m/z, retention
  time, intensity) from centroided mzML data when you need to collapse multiple feature
  detections of the same compound (arising from different ionization states, charge
  states, or isotope patterns) into unified empirical compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - khipu
  - Python
  - Asari
  techniques:
  - LC-MS
  - direct-infusion-MS
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- pre-annotation to group featues to empirical compounds (khipu)
- Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm_cq
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1011912
  all_source_dois:
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-feature-grouping-by-adduct-isotope

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Group individual LC-MS features into empirical compounds by recognizing isotopologues and adducts using mass-to-charge and retention time tolerances. This pre-annotation step collapses redundant feature detections arising from the same chemical entity, enabling more accurate downstream metabolite annotation.

## When to use

Apply this skill immediately after generating a feature table (m/z, retention time, intensity) from centroided mzML data when you need to collapse multiple feature detections of the same compound (arising from different ionization states, charge states, or isotope patterns) into unified empirical compound groups before MS1 and MS2 annotation.

## When NOT to use

- Feature table has already been collapsed to a single m/z per compound (e.g., from targeted analysis); grouping would be redundant.
- Retention time alignment across samples is poor or absent; 2 sec tolerance will not reliably identify co-eluting isotopologues.
- Data were acquired in a chromatography mode (e.g., flow injection analysis or direct infusion) where retention time is not meaningful; use mass tolerance only.

## Inputs

- feature table (TSV or similar) with m/z, retention time, and intensity columns
- ionization mode (positive or negative)

## Outputs

- empirical compounds (EmpCpd) grouped as JSON object (empCpd.json)
- pre-annotation labels per group (adduct, isotope state, charge)

## How to apply

Initialize khipu with default parameters for the inferred ionization mode (positive or negative ion): charge states up to z=3, m+13C isotopologues up to 3 carbons, and common adducts appropriate to your chromatography mode. Group features by applying 5 ppm mass-to-charge tolerance and 2 second retention time tolerance to detect co-eluting isotopologues and adducts. Assign each group to an empirical compound with a pre-annotation label indicating the inferred adduct and isotope state. Serialize the grouped EmpCpd structure to JSON format and save to the experiment's annotations subdirectory. The 5 ppm and 2 sec thresholds are calibrated for Orbitrap LC-MS data; adjust downward for higher mass accuracy instruments or if co-elution is not expected.

## Related tools

- **khipu** (Core tool for isotope and adduct grouping; applies mz and retention time tolerances to assign features to empirical compounds) — https://github.com/shuzhao-li-lab/khipu
- **Asari** (Upstream feature detection tool that generates the input feature table from mzML data) — https://github.com/shuzhao-li/asari
- **Python** (Programming environment for orchestrating khipu and serializing output)

## Evaluation signals

- Check that each empirical compound has ≥1 feature (no empty groups); inspect JSON structure for valid adduct and isotope annotations.
- Verify that grouped features within each EmpCpd differ by ≤5 ppm in m/z and ≤2 sec in retention time; spot-check that co-eluting isotopologues (e.g., m, m+1, m+2 for 13C) are correctly assigned.
- Compare cardinality: feature count before grouping should exceed empirical compound count; a 1:1 ratio suggests features were not being grouped (possible mode mismatch or extreme m/z drift).
- Validate pre-annotations are sensible: check for common adducts ([M+H]+, [M+Na]+, [M-H]−, etc.) and isotope patterns consistent with the ionization mode and sample chemistry.
- Run downstream MS1 annotation on the EmpCpd JSON and verify that no obvious duplicates appear in the final annotation table (e.g., the same compound listed twice with different adduct labels).

## Limitations

- Default 5 ppm and 2 sec tolerances are optimized for Orbitrap LC-MS; users with lower-resolution instruments (e.g., quadrupole TOF) may need looser tolerances, and high-resolution FTICR may warrant tighter thresholds.
- Isotope pattern recognition up to m+13C3 assumes standard organic chemistry; samples with non-standard isotope abundances (e.g., 15N enrichment) or unusual elemental composition may be mis-grouped or split.
- Retention time tolerance assumes consistent peak shape and chromatographic stability across the run; poor retention time reproducibility or peak tailing can lead to false splits of the same compound into multiple EmpCpds.
- Pre-annotation is rule-based and assigns only adduct and isotope state; it does not validate chemical plausibility or perform cross-sample consensus checking.

## Evidence

- [other] Khipu constructs empirical compounds by grouping features as isotopes and adducts with default parameters: charges up to z=3, m+13C3 isotopologues, common adducts by chromatography mode, 5 ppm mz tolerance, and 2 sec rt tolerance for Orbitrap LC data.: "charges up to z=3, m+13C3 isotopologues, common adducts by chromatography mode, 5 ppm mz tolerance, and 2 sec rt tolerance for Orbitrap LC data"
- [other] Group features by applying m/z tolerance (5 ppm) and retention time tolerance (2 seconds) to identify co-eluting isotopologues and adducts.: "Group features by applying m/z tolerance (5 ppm) and retention time tolerance (2 seconds) to identify co-eluting isotopologues and adducts"
- [other] Assign each group to an empirical compound with a pre-annotation label indicating the inferred adduct and isotope state.: "Assign each group to an empirical compound with a pre-annotation label indicating the inferred adduct and isotope state"
- [intro] pre-annotation to group featues to empirical compounds (khipu): "pre-annotation to group featues to empirical compounds (khipu)"
- [readme] This includes feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM and empirical compounds as a JSON file representing putative metabolites that can be annotated with MS1, MS2, or authentic standards.: "empirical compounds as a JSON file representing putative metabolites that can be annotated with MS1, MS2, or authentic standards"
