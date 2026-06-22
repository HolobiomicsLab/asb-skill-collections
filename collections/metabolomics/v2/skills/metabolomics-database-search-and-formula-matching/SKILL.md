---
name: metabolomics-database-search-and-formula-matching
description: Use when after you have detected LC-MS features, grouped them into empirical compounds via isotope and adduct clustering (using khipu), and have accurate m/z and retention time values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - pymzml
  - khipu
  - JMS
  - HMDB 4
  - asari
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- The default method uses `pymzml` to parse mzML files.
- The preannotaion is done via another package khipu (https://github.com/shuzhao-li-lab/khipu)
- The empirical compounds are searched against known compound database (default HMDB 4) via another package JMS (https://github.com/shuzhao-li/JMS).
- known compound database (default HMDB 4)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asari
    doi: 10.1038/s41467-023-39889-1
    title: asari
  dedup_kept_from: coll_asari
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-39889-1
  all_source_dois:
  - 10.1038/s41467-023-39889-1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-database-search-and-formula-matching

## Summary

Search empirical compounds (grouped isotopes and adducts) against a reference metabolite database (HMDB 4) using mass-based queries to retrieve matched molecular formulas, isomers, and chemical annotations. This skill bridges untargeted feature detection to compound identification by leveraging high-resolution m/z values and pre-annotation groupings.

## When to use

After you have detected LC-MS features, grouped them into empirical compounds via isotope and adduct clustering (using khipu), and have accurate m/z and retention time values. Use this skill when you need to assign chemical identities to detected features rather than report m/z values alone, particularly in discovery metabolomics where a high-resolution mass spectrometer and access to HMDB or similar database are available.

## When NOT to use

- Input is already a curated feature table with chemical identities assigned by targeted methods or standards library matching; re-searching would be redundant.
- Mass accuracy is <5 ppm or instrument resolution insufficient to distinguish isobars; formula assignment becomes statistically unreliable.
- Empirical compounds have not been pre-annotated with isotope and adduct grouping; submitting individual ion peaks instead of neutral masses will inflate false positive matches.

## Inputs

- empirical_compounds (list of grouped isotope and adduct clusters with inferred neutral mass)
- high_resolution_mz_values (accurate m/z per empirical compound, typically ±0.005 amu)
- retention_time_values (RT for each detected peak, calibrated across sample cohort)
- indexed_metabolite_database (HMDB 4 or equivalent, pre-formatted for JMS search)

## Outputs

- matched_formula_table (empirical_compound_id → matched molecular formula, isomers, HMDB_identifier)
- Annotated_empiricalCompounds.json (JSON-serialized matched annotations with mass error and confidence)
- Feature_annotation.tsv (feature-level annotations including database reference and formula assignment)

## How to apply

First, use khipu to group detected features into empirical compounds by clustering isotopes (13C/12C patterns) and common adducts (Na/H differences). Next, extract the neutral mass for each empirical compound by inferring the original compound mass from the observed ion peaks. Submit these neutral masses to JMS (Json's Metabolite Services) configured against HMDB 4 (or another indexed compound database) using mass-based search with a tolerance window (typically 5 ppm default in asari context). JMS returns candidate formulas and known compounds ranked by mass match quality. Record matched formulas, database identifiers, isomer information, and match confidence metrics in the output annotation table. Validate matches by cross-checking retention time expectations against literature or reference standards where available.

## Related tools

- **khipu** (Pre-annotation: groups detected ions into empirical compounds by identifying isotope and adduct relationships, infers neutral mass before database search) — https://github.com/shuzhao-li-lab/khipu
- **JMS** (Database search engine: performs mass-based lookup of empirical compound neutral masses against HMDB 4 or other indexed metabolite databases, returns matched formulas and compound records) — https://github.com/shuzhao-li/JMS
- **HMDB 4** (Reference metabolite database: indexed collection of known compounds, formulas, and structures queried via JMS by neutral mass)
- **asari** (Orchestrates the full workflow: detects features, constructs empirical compounds via khipu pre-annotation, then invokes database search and outputs annotated results) — https://github.com/shuzhao-li/asari

## Examples

```
asari annotate -i /path/to/preferred_Feature_table.tsv -o /path/to/output_dir -j annotation_job --workflow LC --mode pos
```

## Evaluation signals

- Annotated_empiricalCompounds.json is valid JSON with all empirical compounds assigned at least one matched formula; check for valid database record identifiers (HMDB accession codes).
- Mass error (observed m/z minus theoretical m/z from matched formula) is within expected tolerance (typically ≤5 ppm for high-resolution LC-MS); plot observed vs. theoretical to check for systematic bias.
- Matched formulas match chemical plausibility: inferred neutral masses fall within expected range for detected adducts (e.g., [M+H]+ → M = observed_mz − 1.0078, [M+Na]+ → M = observed_mz − 22.9892); validate adduct arithmetic.
- Feature annotation table has consistent non-null entries for matched formulas across detected samples; verify that low-abundance or singleton features still receive annotation (asari reports all features meeting SNR >2 and peakshape >0.5).
- Cross-validation: compare matched formulas to retention time libraries or orthogonal analytical data (e.g., MS/MS spectra from parallel LCMSMS run, or NMR) to confirm chemical identity beyond mass match alone.

## Limitations

- Database search depends on reference database completeness; unknown or recently discovered metabolites will not be matched even if detected with high mass accuracy.
- Mass accuracy alone (5 ppm tolerance) can match multiple candidate formulas, especially for complex ions or contaminated samples; isotope pattern and adduct inference via khipu reduces but does not eliminate ambiguity.
- Retention time prediction is not part of JMS/HMDB search; RT validation requires orthogonal reference data (e.g., retention time library, standards, or in silico prediction model) and is not automatic.
- Isobaric compounds (same m/z, different structures) cannot be distinguished by mass alone; MS/MS fragmentation or other orthogonal analysis is required for structural isomer resolution.
- Pre-annotation grouping quality (isotope and adduct detection via khipu) is critical; errors in empirical compound construction upstream will propagate false or missing formula matches.

## Evidence

- [methods] Perform pre-annotation using khipu to group isotopes and adducts into empirical compounds, then search against HMDB 4 via JMS to obtain matched formulas and isomers.: "Perform pre-annotation using khipu to group isotopes and adducts into empirical compounds, then search against HMDB 4 via JMS to obtain matched formulas and isomers."
- [methods] The preannotaion is done via another package khipu. The empirical compounds are searched against known compound database (default HMDB 4) via another package JMS.: "The preannotaion is done via another package khipu. The empirical compounds are searched against known compound database (default HMDB 4) via another package JMS."
- [readme] khipu: generalized tree structure to annotate untargeted metabolomics and stable isotope tracing data. Pre-annotation tool to annotate degenerate ions in relationships to the original compound and infer neutral mass.: "Pre-annotation tool to annotate degenerate ions in relationships to the original compound and infer neutral mass."
- [readme] A Python library for mapping identifiers between genome scale metabolic models and metabolite databases, reusable data structures for peaks, compounds and indexed data stores, efficient mass and empirical compound search functions.: "efficient mass and empirical compound search functions"
- [methods] Export results to preferred_Feature_table.tsv, full_Feature_table.tsv, _mass_grid_mapping.csv, cmap.pickle, epd.pickle, and Annotated_empiricalCompounds.json.: "Export results to preferred_Feature_table.tsv, full_Feature_table.tsv, _mass_grid_mapping.csv, cmap.pickle, epd.pickle, and Annotated_empiricalCompounds.json."
