---
name: metabolite-taxonomy-database-lookup
description: Use when when you have MS/MS-annotated features from a natural extract
  (via SIRIUS, CANOPUS, or ISDB) and need to compute the Literature Component or Class
  Component of a priority rank—i.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - MZmine2
  - MZmine3
  - timaR
  - CANOPUS
  - MEMO
  - Lotus Database
  - GNPS
  - Open Tree of Life
  - SIRIUS
  - Inventa
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
derived_from:
- doi: 10.3389/fmolb.2022.1028334
  title: Inventa
- doi: 10.1038/s41467-021-23953-9
  title: ''
evidence_spans:
- MZmine output format using only the 'Peak area', 'row m/z' and 'row retention time'
  columns. -Inventa takes input directly from MZmine2
- Inventa takes input directly from MZmine2 or MZmine 3
- -Inventa takes input directly from MZmine2 or [MZmine 3](http://mzmine.github.io/),
  is possible to use other processing sofwares
- 'tima_results_filename: timaR reponderated output format. - for performing in silico
  annotations and taxonomically informed reponderation.'
- 'tima_results_filename: timaR reponderated output format'
- 'Class Component (CC): a score considering the presence of predicted known chemical
  classes new to the species'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_inventa_cq
    doi: 10.3389/fmolb.2022.1028334
    title: Inventa
  dedup_kept_from: coll_inventa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fmolb.2022.1028334
  all_source_dois:
  - 10.3389/fmolb.2022.1028334
  - 10.1038/s41467-021-23953-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Metabolite Taxonomy Database Lookup

## Summary

Cross-reference detected metabolite features and their chemical classes against taxon-specific literature records (species, genus, family levels) in curated natural product databases to assess the novelty and chemical diversity of an extract relative to known reported compounds.

## When to use

When you have MS/MS-annotated features from a natural extract (via SIRIUS, CANOPUS, or ISDB) and need to compute the Literature Component or Class Component of a priority rank—i.e., when your goal is to identify whether detected compounds or chemical classes are novel relative to what has been previously reported for a given organism's taxon. Apply this skill if you have curated taxonomy metadata (species, genus, family) linked to your samples and access to a compound literature frequency database such as Lotus Database or NPClassifyre.

## When NOT to use

- Your sample lacks reliable taxonomic classification or the organism is not represented in the target literature database (Lotus); the lookup will return zero or null frequencies, collapsing LC and CC scores to uninformative defaults.
- You have not yet performed MS/MS annotation or chemical class prediction; taxonomy lookup requires annotated features or predicted classes as input—use spectral dereplication or structure prediction tools first.
- Your goal is to assess novelty at the *feature* level based on spectral similarity alone (i.e., MS/MS fingerprinting), not literature frequency; use the Similarity Component (MEMO-based) instead.

## Inputs

- Sample metadata table with GNPS format and mandatory columns: ATTRIBUTE_Species, ATTRIBUTE_Genus (inferred or explicit), ATTRIBUTE_Family (inferred or explicit)
- Annotated feature table from MZmine2/MZmine3 with m/z, retention time, and peak area
- Annotation results from SIRIUS (compound_identification.tsv) or ISDB, filtered by ppm_error ≤ 5 ppm, shared_peaks ≥ 10, cosine ≥ 0.7
- CANOPUS chemical class predictions (npc_summary.tsv) with confidence scores
- Lotus Database or equivalent curated metabolite–taxon–literature frequency table

## Outputs

- Literature Component (LC) score per sample (range 0–1), reflecting novelty relative to species/genus/family literature
- Class Component (CC) score per sample (range 0–1), flagging unreported chemical classes
- Lookup table mapping each detected feature/class to database query results (reported count, taxonomic rank, reference literature frequency)
- Validation report confirming taxonomy name standardization and database query consistency

## How to apply

First, map each sample's taxonomic lineage (species, genus, family) to authoritative taxonomy records, using tools like Open Tree of Life to validate and standardize names. For each detected feature or CANOPUS-predicted chemical class, query the Lotus Database (or equivalent) to retrieve the count of structurally distinct compounds or classes previously reported at each taxonomic rank. For the Literature Component, subtract normalized fractions—computed as (reported_compounds / user_defined_max_threshold)—from a baseline score of 1.0 for each rank (e.g., max_comp_reported_sp=20, max_comp_reported_g=50, max_comp_reported_f=500), applying user-defined weighting (ws=1, wg=1, wf=1) to emphasize or de-emphasize rank-specific novelty. For the Class Component, flag any CANOPUS chemical class (confidence ≥ min_class_confidence=0.8, recurrence ≥ min_recurrence=5) that does not appear in the Lotus Database for the same species or genus, assigning a binary or graduated score. Validate that the database query returns consistent counts across replicate queries and that taxonomic name cleaning eliminates ambiguity (e.g., synonyms, deprecated nomenclature).

## Related tools

- **Lotus Database** (Query source for curated natural product compound–taxon frequency and chemical class occurrence across species, genus, and family levels)
- **Open Tree of Life** (Validates and standardizes taxonomic names (species, genus, family) to eliminate synonymy and deprecated nomenclature before database lookup) — https://opentree.readthedocs.io/en/latest/
- **SIRIUS** (Provides de novo structure prediction and candidate compound lists (compound_identification.tsv) that are cross-referenced against Lotus; output filtered by min_ZodiacScore ≥ 0.9, min_ConfidenceScore ≥ 0.0) — https://bio.informatik.uni-jena.de/software/sirius/
- **CANOPUS** (Predicts chemical taxonomy (NPClassifyre classes) for each feature; Class Component detects unreported classes by querying Lotus for species/genus-level class occurrence (min_class_confidence=0.8, min_recurrence=5))
- **Inventa** (Orchestrates Literature and Class Component calculation via parametrized taxonomy-aware database lookup and novelty scoring) — https://github.com/luigiquiros/inventa

## Examples

```
# After configuring Inventa with cleaned taxonomy and Lotus Database path:
# Set LC and CC parameters in notebook: LC_component = True, max_comp_reported_sp = 20, max_comp_reported_g = 50, max_comp_reported_f = 500, CC_component = True, min_class_confidence = 0.8
# Then run the notebook cell to compute Literature and Class Components via Lotus lookup
```

## Evaluation signals

- Verify that all samples have valid, standardized taxonomic names (species, genus, family) with no duplicates, synonyms, or deprecated names after Open Tree of Life cleaning.
- Confirm that Lotus Database lookup returns consistent (non-null) literature frequency counts for all input taxa; spot-check a subset of species–genus–family triplets against known literature records.
- Check that LC scores range 0–1 for all samples; an LC of 1.0 indicates zero previously reported compounds for the taxon, while LC < 1.0 reflects documented compounds; validate that LC decreases monotonically as reported compound counts increase.
- Validate that CC scores correctly flag unreported CANOPUS classes: a CC of 1.0 indicates a new class (novel to both species and genus), while CC < 1.0 reflects partial overlap; confirm that class predictions with confidence < 0.8 or recurrence < 5 are excluded.
- Audit the lookup output table for null, zero, or out-of-range (< 0 or > 1) component scores; investigate any row with missing database query result as a potential taxonomy mismatch or database connectivity issue.

## Limitations

- Lotus Database completeness and currency: literature frequency counts depend on the comprehensiveness of the curated database; rare or newly discovered organisms, particularly from understudied ecosystems, may have sparse or absent entries, inflating LC and CC scores artificially.
- Taxonomy ambiguity and nomenclatural drift: standardization via Open Tree of Life is a prerequisite but not always unambiguous; subspecies-level or strain-level variants are not resolved by genus/family lookup, potentially conflating distinct populations.
- Chemical class ontology mismatch: Lotus Database uses NPClassifyre while SIRIUS uses Classifyre; the article notes this incongruity must be resolved computationally, but class name reconciliation is imperfect and can cause false negatives (reported classes not matched due to naming differences).
- Feature-to-compound mapping ambiguity: a single MS/MS feature may correspond to multiple isomers or regioisomers, all of which may be grouped under one Lotus entry; this can underestimate novelty if different regioisomers have different literature frequencies.
- Dependency on annotation quality: LC and CC scores are only meaningful if upstream SIRIUS and CANOPUS predictions are reliable (ppm_error ≤ 5, cosine ≥ 0.7, confidence thresholds met); poor annotation propagates as uninformative taxonomy lookup results.

## Evidence

- [methods] The Literature Component (LC) is a score based on the number of compounds reported in the literature for the taxon of a given extract.: "The Literature Component (LC) is a score based on the number of compounds reported in the literature for the taxon of a given extract. It is independent of the spectral data."
- [other] Fractions of reported compounds at species/genus/family levels with thresholds: max_comp_reported_sp=20, max_comp_reported_g=50, max_comp_reported_f=500.: "fractions of reported compounds at species/genus/family levels (thresholds: max_comp_reported_sp=20, max_comp_reported_g=50, max_comp_reported_f=500) with weighting factors (ws=1, wg=1, wf=1)"
- [other] The Class Component (CC) by detecting unreported CANOPUS chemical classes compared to those in Lotus Database for the species and genus.: "Calculate Class Component (CC) by detecting unreported CANOPUS chemical classes in each extract compared to those in Lotus Database for the species and genus, using min_class_confidence=0.8 and"
- [other] The taxonomy should be cleaned to uptoday recognized names, you can use the Open Tree of Life.: "The taxonomy should be cleaned to uptoday recognized names, you can use the Open Tree of Life"
- [other] given that the Lotus Dabase uses the NPClassifyre ontology and Sirius uses the Classifyre ontology, performing this step is absolutley necesary.: "given that the Lotus Dabase uses the NPClassifyre ontology and Sirius uses the Classifyre ontology, performing this step is absolutley necesary"
- [readme] An LC value of 1 indicates no reported compounds for the considered taxon. From this initial value ('1'), fractions (ratio of reported compounds over the user-defined maximum value of reported compounds) are subtracted.: "An LC value of 1 indicates no reported compounds for the considered taxon. From this initial value ('1'), fractions (ratio of reported compounds over the user-defined maximum value of reported"
- [readme] A CC value of 1 implies that the chemical class is new to both the species (CCs 0.5) and the genus (CCg 0.5).: "A CC value of 1 implies that the chemical class is new to both the species (CCs 0.5) and the genus (CCg 0.5)."
