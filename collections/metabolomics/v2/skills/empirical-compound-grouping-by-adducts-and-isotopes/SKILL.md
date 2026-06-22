---
name: empirical-compound-grouping-by-adducts-and-isotopes
description: Use when after feature table normalization and imputation are complete, immediately before MS1 and MS2 annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - ThermoRawFileParser
  - Asari
  - khipu
  - PCPFM (pcpfm build_empCpds command)
  - mass2chem
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- Python-Centric Pipeline for Metabolomics
- The Python-Centric Pipeline for Metabolomics
- convert Thermo .raw to mzML (ThermoRawFileParser)
- process mzML data to feature tables (Asari)
- pre-annotation to group featues to empirical compounds (khipu)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm
schema_version: 0.2.0
---

# empirical-compound-grouping-by-adducts-and-isotopes

## Summary

Groups detected LC-MS features into putative empirical compounds by matching features that represent the same molecular entity under different ionization states (adducts) and isotopic variants (e.g., 13C). This pre-annotation step reduces feature table dimensionality and enables unified compound-level annotation before MS1/MS2 matching.

## When to use

Apply this skill after feature table normalization and imputation are complete, immediately before MS1 and MS2 annotation. Use it when you have a normalized feature table with m/z and retention time values and need to collapse related features into metabolite-level entities for more robust statistical and annotation workflows. This is particularly valuable in untargeted metabolomics where a single metabolite generates multiple detected peaks due to ionization chemistry.

## When NOT to use

- Input is already a metabolite-level table (not a feature table) — skip this step and proceed to annotation.
- m/z and retention time uncertainties are unknown or not well characterized — calibrate mass accuracy and retention time reproducibility first.
- Analysis goal is feature-level statistical discovery (e.g., differential abundance of individual m/z peaks across conditions) — empirical compound grouping may obscure feature-level signals.

## Inputs

- normalized feature table (TSV/CSV format with columns: feature ID, m/z, retention time, intensity across samples)
- adduct definition list (charge states and ionization modes)
- isotope pattern definition (carbon, nitrogen, sulfur isotope shifts)
- m/z tolerance threshold (ppm)
- retention time tolerance threshold (seconds)

## Outputs

- empirical compounds JSON file (hierarchical structure linking feature IDs to putative metabolites with adduct/isotope annotations)
- compound-level feature table (one row per empirical compound, intensities aggregated or representative)
- adduct/isotope assignment map (traceability of which features belong to which compound and why)

## How to apply

Run the khipu-based empirical compound builder on the final feature table by specifying (1) adduct definitions (e.g., [M+H]+, [M+Na]+, [M-H]−) with charge up to z=3; (2) isotope patterns (e.g., 13C1, 13C2, 13C3 for carbon isotopologues); (3) m/z tolerance matching (default 5 ppm, derived from instrument mass accuracy); and (4) retention time tolerance (default 2 sec, matching feature extraction RT tolerance). The algorithm groups features whose m/z and RT differences fall within these tolerances and whose mass differences correspond to known adduct or isotope shifts. Each group is output as an empirical compound JSON object with a representative m/z/RT, constituent feature IDs, and adduct/isotope assignments that can be carried forward to MS1 library matching and MS2 spectral annotation.

## Related tools

- **khipu** (Core algorithm for grouping features into empirical compounds via adduct and isotope pattern matching with configurable m/z and RT tolerances) — https://github.com/shuzhao-li-lab/khipu
- **PCPFM (pcpfm build_empCpds command)** (Orchestration wrapper that invokes khipu on the normalized feature table and outputs JSON empirical compound definitions) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **mass2chem** (Utility library for interpreting mass spectrometry data, adduct calculations, and isotope pattern generation) — https://github.com/shuzhao-li-lab/mass2chem

## Examples

```
pcpfm build_empCpds --feature_table normalized_feature_table.tsv --adducts '["[M+H]+", "[M+Na]+", "[M-H]-"]' --isotopes '["13C1", "13C2", "13C3"]' --mz_tolerance 5 --rt_tolerance 2 --output empCpd.json
```

## Evaluation signals

- Feature grouping coherence: each empirical compound contains features whose pairwise m/z differences match known adduct shifts (e.g., 1.008 Da for [M+H]+ vs [M]•+, 21.98 Da for [M+Na]+ vs [M+H]+) and RT values cluster within the specified tolerance (typically ±2 sec).
- Reduction in dimensionality: the number of empirical compounds is substantially lower than the number of input features; typical ratios range from 0.3–0.7× (e.g., 5,000 features → 1,500–3,500 compounds) depending on ionization complexity.
- Adduct assignment validity: adduct assignments in the output JSON are supported by the charge and ionization mode definitions provided; no features are assigned to chemically impossible adducts for the given polarity mode.
- Traceability: each empirical compound JSON entry contains a feature_id array allowing back-tracing to constituent raw features; feature counts per compound should be ≥1 with typical mode of 1–3 features per compound in high-resolution data.
- RT and m/z consistency: within each empirical compound, all constituent features have RT values within ±2 sec of the compound representative RT; all m/z values fall within ±5 ppm of the representative m/z.

## Limitations

- Grouping accuracy depends critically on mass accuracy (instrument calibration) and retention time reproducibility; uncalibrated or drifting instruments may falsely group unrelated features or fail to group true adducts.
- The algorithm assumes that adducts and isotopes produce predictable m/z shifts; unusual adducts (e.g., multiply charged species, in-source fragments) may not be recognized or may be misclassified.
- Overlapping RT windows (e.g., co-eluting isomers with identical adduct m/z values) cannot be resolved by m/z and RT alone; such features may be incorrectly merged into a single empirical compound.
- The method does not use intensity patterns or correlation across samples to validate grouping; features grouped by m/z/RT tolerance alone may not be biologically related.
- Configuration is required for each analysis (adduct list, isotope list, tolerances); inappropriate parameter choices (e.g., overly permissive RT tolerance or omitted adducts) degrade grouping quality without warning.

## Evidence

- [other] Build empirical compounds from final feature table using pcpfm build_empCpds with khipu, specifying adducts (charge up to z=3), isotope patterns (13C3), m/z tolerance (default 5 ppm), and retention-time tolerance (default 2 sec): "Build empirical compounds from final feature table using pcpfm build_empCpds with khipu, specifying adducts (charge up to z=3), isotope patterns (13C3), m/z tolerance (default 5 ppm), and"
- [readme] empirical compounds as a JSON file representing putative metabolites that can be annotated with MS1, MS2, or authentic standards: "empirical compounds as a JSON file representing putative metabolites that can be annotated with MS1, MS2, or authentic standards"
- [intro] pre-annotation to group featues to empirical compounds (khipu): "pre-annotation to group featues to empirical compounds (khipu)"
- [other] Asari feature extraction producing full and preferred feature tables; [...] empirical compound construction via khipu with configurable mz/rt tolerances and adduct/isotope definitions: "empirical compound construction via khipu with configurable mz/rt tolerances and adduct/isotope definitions"
- [readme] Generalized tree structure to annotate untargeted metabolomics and stable isotope tracing data: "Generalized tree structure to annotate untargeted metabolomics and stable isotope tracing data"
