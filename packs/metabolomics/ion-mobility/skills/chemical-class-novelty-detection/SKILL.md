---
name: chemical-class-novelty-detection
description: Use when when you have CANOPUS chemical class predictions for your samples and need to identify which extracts contain chemical classes absent from the literature for their species or genus.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0121
  tools:
  - MZmine2
  - MZmine3
  - timaR
  - CANOPUS
  - MEMO
  - GNPS
  - SIRIUS
  - Lotus Database
  - canopus_treemap
  - Open Tree of Life
  - INVENTA
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.3389/fmolb.2022.1028334
  title: Inventa
- doi: 10.1038/s41467-021-23953-9
  title: ''
evidence_spans:
- MZmine output format using only the 'Peak area', 'row m/z' and 'row retention time' columns. -Inventa takes input directly from MZmine2
- Inventa takes input directly from MZmine2 or MZmine 3
- -Inventa takes input directly from MZmine2 or [MZmine 3](http://mzmine.github.io/), is possible to use other processing sofwares
- 'tima_results_filename: timaR reponderated output format. - for performing in silico annotations and taxonomically informed reponderation.'
- 'tima_results_filename: timaR reponderated output format'
- 'Class Component (CC): a score considering the presence of predicted known chemical classes new to the species'
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

# Chemical Class Novelty Detection

## Summary

Detects unreported CANOPUS chemical classes in metabolomic extracts by comparing detected classes against known compounds in the Lotus Database at species and genus taxonomic levels. This identifies extracts with potentially novel chemical scaffolds, enabling prioritization of samples for natural product discovery.

## When to use

When you have CANOPUS chemical class predictions for your samples and need to identify which extracts contain chemical classes absent from the literature for their species or genus. This is particularly valuable when you want to prioritize samples for structure elucidation based on chemical novelty rather than feature abundance or spectral similarity alone.

## When NOT to use

- CANOPUS predictions are not available or confidence scores fall below your domain-specific threshold (< 0.8 by default).
- Taxonomy is not cleaned to currently recognized species/genus names (use Open Tree of Life first).
- You are prioritizing based on spectral diversity rather than chemical structure novelty; use Similarity Component (MEMO-based) instead.

## Inputs

- CANOPUS npc_summary.tsv file with chemical class predictions and confidence scores per feature/sample
- Lotus Database compound records indexed by species and genus taxonomy
- Sample metadata table with ATTRIBUTE_Species and ATTRIBUTE_Genus columns (GNPS format)
- Optionally: SIRIUS project space if re-computing class predictions with updated chemical ontology

## Outputs

- Class Component (CC) scores per sample (ranging from 0 to 1)
- Binary or continuous novelty flag per chemical class per sample
- Intermediate table mapping detected classes to literature reference status (species/genus/family level)

## How to apply

Load CANOPUS npc_summary.tsv chemical class predictions for each extract and cross-reference them against Lotus Database compound records filtered by species and genus taxonomy. For each detected CANOPUS class in an extract, check whether that class appears in any literature-reported compounds for the same species (scored as 0.5) or genus (scored as 0.5). Assign a Class Component (CC) score of 1 when a chemical class is unreported at both levels, 0.5 when novel to the species but known in the genus, or 0 when the class is already documented in the literature. Apply a minimum class confidence threshold (default 0.8) to filter low-confidence predictions, and optionally a minimum recurrence threshold (default 5) to ensure the class appears consistently across the dataset. The rationale is that chemically novel classes at the species level represent higher discovery priority than those merely novel to the genus.

## Related tools

- **CANOPUS** (Generates chemical class predictions and assigns confidence scores to features; output (npc_summary.tsv) is mined to detect unreported classes.) — https://bio.informatik.uni-jena.de/software/sirius/
- **SIRIUS** (Computes molecular formula and structure hypotheses; CANOPUS runs on SIRIUS project space; may be recomputed if ontology is updated.) — https://bio.informatik.uni-jena.de/software/sirius/
- **Lotus Database** (Reference database of natural product compounds indexed by species/genus/family; used to identify whether a detected CANOPUS class is already documented in the literature for the sample's taxon.)
- **canopus_treemap** (Visualization and post-processing tool for CANOPUS predictions; can generate npc_summary.csv if not already present in SIRIUS output.) — https://github.com/kaibioinfo/canopus_treemap
- **Open Tree of Life** (Reference taxonomy for cleaning and standardizing species/genus names before matching against Lotus Database.) — https://opentree.readthedocs.io/en/latest/readme.html
- **INVENTA** (End-to-end framework implementing Class Component calculation; orchestrates CANOPUS class detection, Lotus Database lookup, and novelty scoring.) — https://github.com/luigiquiros/inventa

## Examples

```
from inventa import Inventa; inventa = Inventa(canopus_npc_summary_filename='npc_summary.tsv', metadata_filename='metadata.tsv', lotus_db_path='lotus.db', min_class_confidence=0.8, min_recurrence=5); cc_scores = inventa.calculate_class_component()
```

## Evaluation signals

- All samples in the dataset have a Class Component (CC) score assigned (no null values).
- CC scores lie in the expected range [0, 1]; spot-check a few samples to verify that species-level novelty is scored 0.5 and genus-level novelty is scored 0.5 or 1 according to the article's logic.
- Chemical classes detected in the extract are verifiable in the CANOPUS npc_summary.tsv with confidence ≥ min_class_confidence threshold (0.8).
- Lotus Database lookup successfully matched detected classes against literature-reported compounds; verify by querying a sample's species/genus and confirming the absence (or presence) of the flagged classes.
- Samples flagged as having novel classes (CC = 1.0) show no overlap of their CANOPUS classes with the genus-level compound classes in Lotus Database.

## Limitations

- Novelty detection is limited by the completeness and currency of the Lotus Database; underreporting in the literature may incorrectly inflate novelty scores.
- CANOPUS ontology mismatch with Lotus Database (the article notes Lotus uses NPClassifyre while SIRIUS uses Classifyre); ontology alignment is necessary and may reduce precision of class matching.
- Confidence threshold (min_class_confidence = 0.8) is user-defined and may filter out lower-confidence but valid predictions; sensitivity depends on instrument accuracy and spectral quality.
- Genus-level matching is coarse; within-genus diversity may render genus-level literature data less predictive than intended for species-rich or morphologically similar genera.

## Evidence

- [methods] The Class Component (CC) indicates if an unreported CANOPUS chemical class is detected in a given extract compared to those reported in the species and the genus.: "The Class Component (CC) indicates if an unreported CANOPUS chemical class is detected in a given extract compared to those reported in the species and the genus."
- [other] Calculate Class Component (CC) by detecting unreported CANOPUS chemical classes in each extract compared to those in Lotus Database for the species and genus, using min_class_confidence=0.8 and min_recurrence=5.: "Calculate Class Component (CC) by detecting unreported CANOPUS chemical classes in each extract compared to those in Lotus Database for the species and genus, using min_class_confidence=0.8 and"
- [readme] A CC value of 1 implies that the chemical class is new to both the species (CCs 0.5) and the genus (CCg 0.5).: "A CC value of 1 implies that the chemical class is new to both the species (CCs 0.5) and the genus (CCg 0.5)."
- [other] given that the Lotus Dabase uses the NPClassifyre ontology and Sirius uses the Classifyre ontology, performing this step is absolutley necesary: "given that the Lotus Dabase uses the NPClassifyre ontology and Sirius uses the Classifyre ontology, performing this step is absolutley necesary"
- [readme] clone the following repository https://github.com/kaibioinfo/canopus_treemap. Recompute your project space from Sirius using the following code: from canopus import Canopus; C = Canopus(sirius="sirius_projectspace"); C.npcSummary().to_csv("npc_summary.csv"): "clone the following repository https://github.com/kaibioinfo/canopus_treemap. Recompute your project space from Sirius"
