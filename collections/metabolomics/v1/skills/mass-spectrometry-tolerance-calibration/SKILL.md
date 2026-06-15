---
name: mass-spectrometry-tolerance-calibration
description: Use when after generating a feature table from mzML data (via Asari) and before performing MS1 or MS2 annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - ThermoRawFileParser
  - khipu
  - Python
  - Asari
  - mass2chem
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- convert Thermo .raw to mzML (ThermoRawFileParser)
- pre-annotation to group featues to empirical compounds (khipu)
- Python-Centric Pipeline for Metabolomics
- The Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm
schema_version: 0.2.0
---

# mass-spectrometry-tolerance-calibration

## Summary

Configures m/z and retention time tolerances in khipu's build_empCpds command to group features into empirical compounds by matching isotopes and adducts. Tolerance selection directly affects the specificity and sensitivity of feature clustering and downstream metabolite annotation.

## When to use

After generating a feature table from mzML data (via Asari) and before performing MS1 or MS2 annotation. Use this skill when you need to cluster individual features into putative metabolite groups (empirical compounds) and must decide appropriate tolerance windows based on your instrument's mass accuracy and chromatographic resolution. Critical when working with high-resolution instruments where default tolerances may be too stringent, or with lower-resolution data where they may be too permissive.

## When NOT to use

- Input is already an annotated compound list (e.g., from authentic standards or prior MS2 matching); re-clustering may fragment or merge known metabolites incorrectly.
- Tolerance windows are unknown and instrument specifications are unavailable; using defaults without validation risks systematic false positives or false negatives in empirical compound construction.
- Data contains significant systematic mass or retention time drift uncorrected by the feature detection step; tolerance calibration alone cannot compensate for instrumental artifacts that should be addressed upstream.

## Inputs

- Feature table in TSV format (from asari_results/preferred_Feature_table.tsv)
- Ionization mode specification (positive or negative)
- Adduct definitions for the detected polarity (e.g., [M+H]+, [M+Na]+)

## Outputs

- empCpd.json file containing grouped empirical compounds with list_of_features, median m/z, median rt, and pre-annotation fields
- Feature groupings organized by isotopologue and adduct relationships

## How to apply

Invoke khipu's build_empCpds command with configurable m/z tolerance (default 5 ppm) and retention time tolerance (default 2 seconds), specifying ionization mode and adduct definitions for the detected polarity. The m/z tolerance should reflect your instrument's mass measurement accuracy—5 ppm is suitable for Orbitrap and time-of-flight instruments, but may need adjustment for lower-resolution platforms. Retention time tolerance (default 2 seconds) accounts for chromatographic peak width and coelution; adjust downward if peaks are well-resolved or upward if broad peaks or overlapping retention times are common. The command clusters features by matching observed mass differences against known isotope patterns (e.g., 13C, 34S, 2H shifts) and adduct masses (e.g., [M+H]+, [M+Na]+, [M+NH4]+) within these windows, then serializes the grouped empirical compounds to JSON format. Validate the output by inspecting the JSON schema (list_of_features, median m/z, median rt, and pre-annotation fields) and spot-checking a subset of feature groups to ensure isotopes and adducts are clustered appropriately.

## Related tools

- **khipu** (Groups features into empirical compounds using build_empCpds command with configurable m/z and retention time tolerances, and assigns isotopologue and adduct annotations) — https://github.com/shuzhao-li-lab/khipu
- **Asari** (Generates the input feature table (TSV format) from mzML data prior to tolerance calibration and empirical compound construction) — https://github.com/shuzhao-li/asari
- **mass2chem** (Provides utilities for interpreting mass spectrometry data and isotope/adduct pattern definitions used by khipu during feature grouping) — https://github.com/shuzhao-li-lab/mass2chem

## Examples

```
khipu build_empCpds preferred_Feature_table.tsv --mz_tolerance 5 --rt_tolerance 2 --ionization_mode positive --adduct_list '[M+H]+,[M+Na]+,[M+NH4]+' --output_json empCpd.json
```

## Evaluation signals

- JSON output schema validation: all empirical compound objects contain required fields (list_of_features, median m/z, median rt, pre-annotation) with correct data types and no missing entries.
- Feature clustering specificity: inspect a sample of grouped features to confirm that isotope mass differences match expected shifts (e.g., ~1.003 Da for 13C, ~0.997 Da for 34S) and are within the configured m/z tolerance in parts per million.
- Adduct annotation consistency: verify that adduct assignments in pre-annotation fields reflect the specified ionization mode and configured adduct list, and that intra-group mass offsets align with known adduct mass differences (e.g., ~22.99 Da for Na+ vs. H+).
- Carryover from tolerance tuning: compare empirical compound counts and feature groupings across tolerance scenarios (e.g., 5 ppm vs. 10 ppm m/z, 2 s vs. 5 s rt) to confirm that tolerance changes produce expected shifts in clustering density without introducing obvious over-grouping or fragmentation.
- Retention time coherence: confirm that grouped features share retention times within the configured tolerance window; large rt deviations within a single empirical compound suggest tolerance is too permissive or that systematic rt drift was not adequately corrected upstream.

## Limitations

- Default tolerances (5 ppm m/z, 2 seconds rt) are tuned for Orbitrap and similar high-resolution instruments; lower-resolution platforms (e.g., quadrupole, sector) may require broader m/z windows to avoid fragmenting true isotope/adduct families.
- Retention time tolerance does not account for systematic chromatographic drift across a sample batch; if significant drift is present, batch correction should be applied before tolerance calibration, or rt tolerance should be set empirically per batch.
- Tolerance calibration relies on accurate adduct and isotope definitions; if ionization mode is misspecified or adduct list is incomplete or incorrect, feature grouping will be incorrect regardless of tolerance window.
- No automatic tolerance optimization is provided; practitioners must either use defaults or empirically tune based on their instrument and sample matrix, which may require iterative testing or external mass calibration standards.
- Very narrow tolerances (e.g., <2 ppm m/z) may fail to group legitimate isotope families if the feature table contains unresolved or noisy m/z measurements; inspection of raw peak positions and calibration quality is recommended before narrowing tolerances below instrument specification.

## Evidence

- [other] The build_empCpds command constructs empirical compounds by matching isotopes and adducts with configurable m/z tolerance (default 5 ppm) and rt tolerance (default 2 seconds): "Invoke khipu via the build_empCpds command with configurable m/z tolerance (default 5 ppm) and retention time tolerance (default 2 seconds), specifying ionization mode and adduct definitions"
- [other] Empirical compounds are serialized to JSON with grouped features, m/z and rt values, and pre-annotation fields: "Serialize the empirical compound collection to JSON format, including list_of_features, median m/z, median rt, and pre-annotation fields for each group."
- [other] Features are clustered within m/z and rt windows and assigned isotopologue and adduct annotations based on mass differences and charge state patterns: "Construct feature groups by clustering features within the specified m/z and rt windows, assigning isotopologue and adduct annotations based on observed mass differences and charge state patterns."
- [other] JSON structure must be validated to ensure all required fields are present: "Validate JSON structure and confirm all required fields are present."
- [readme] Pre-annotation groups features to empirical compounds in the metabolomics pipeline workflow: "pre-annotation to group featues to empirical compounds (khipu)"
